# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models,api,_
from odoo.tools.safe_eval import safe_eval
import re

class CaseStage(models.Model):
    _name = 'probate.case.stage'
    _description = 'Probate Case Stage'
    _rec_name = 'name'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Stage Name')

class Parties(models.Model):
    _name = 'probate.case.parties'

    case_id = fields.Many2one('probate.case', string='case')
    name = fields.Char('Name')
    email = fields.Char('Email')
    phone = fields.Char('Phone')

class Parties(models.Model):
    _name = 'probate.case.beneficiaries'

    case_id = fields.Many2one('probate.case', string='case')
    name = fields.Char('Name')
    email = fields.Char('Email')
    phone = fields.Char('Phone')

class ProbateCase(models.Model):
    _name = 'probate.case'
    _description = 'Probate Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    case_number = fields.Char('Case Number')
    name = fields.Char(string='System Case Number', compute='_get_system_number')
    court_id = fields.Many2one('probate.case.court', string='Court Name')
    district_id = fields.Many2one('probate.case.district', string='District')
    branch_district_id = fields.Many2one('probate.case.branch.district', string='Branch District')
    presiding_magistrate = fields.Many2one('res.users', string='Presiding Magistrate')
    phone = fields.Char('Phone', related='presiding_magistrate.phone')
    email = fields.Char('Email', related='presiding_magistrate.email')
    parties_involved = fields.One2many('probate.case.parties', 'case_id', string='Parties Involved', ondelete='cascade')
    beneficiaries = fields.One2many('probate.case.beneficiaries', 'case_id', string='Beneficiaries', ondelete='cascade')
    case_property_ids = fields.One2many('probate.case.property', 'case_id', string='Properties', ondelete="cascade")
    administrator_name = fields.Many2one('res.users', string='Name of the Administrator of the estate', default=lambda self: self.env.user,)
    deceased_name = fields.Char(string='Deceased Name')
    completion_date = fields.Date(string='Completion Date')
    administrator_phone = fields.Char(string='Administrators phone number')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')
    total_value = fields.Float('Total', store=True, readonly=True, compute='_amount_all')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_tiss', 'Awaiting for tiss'),
        ('completion_form', 'Completion of forms'),
        ('pending_hro_approval', 'Pending HRO approval'),
        ('pending_payment', 'Pending payment'),
        ('closed', 'Closed'),
    ], string='state', default='draft', tracking=True)
    supervisor_id = fields.Many2one('res.users', string='Supervisor')
    email_supervisor = fields.Char(string='Supervisor Email', related='supervisor_id.email')
    show_button_confirm_for_supervisor = fields.Boolean('show_button_confirm_for_supervisor', compute='_show_button_confirm_suppervisor')
    
    def action_approved_completion_form(self):
        self.write({'state': 'pending_hro_approval'})
    
    def action_reject_not_completion_form(self):
        form_view_id = self.env.ref('porbate_case_management.reject_approval').id
        action =  {
            'name': _('Reason Reject'),
            'view_mode': 'form',
            'res_model': 'reason.reject',
            'view_id': form_view_id,
            'views': [(form_view_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action

    def _show_button_confirm_suppervisor(self):
        for record in self:
            if record.state == 'waiting_tiss':
                if record.env.user.id == record.supervisor_id.id:
                    record.show_button_confirm_for_supervisor = True
                else:
                    record.show_button_confirm_for_supervisor = False
            else:
                record.show_button_confirm_for_supervisor = False

    def action_confirm(self):
        self.write({'state': 'completion_form'})
        now = fields.date.today()
        date_string = now.strftime('%d-%m-%Y')
        message = f"{self.administrator_name.name} has been assigned by {self.env.user.name} on {date_string} "
        self.message_post(body=message)
        

    @api.depends('case_number', 'district_id', 'branch_district_id')
    def _get_system_number(self):
        for record in self:
            record.name = ''
            if record.case_number and not record.district_id and not record.branch_district_id:
                sequence = record.case_number
                record.update({
                    'name': sequence,
                })
            if record.case_number and record.district_id and not record.branch_district_id:
                sequence = record.district_id.district_code + ' ' +record.case_number 
                record.update({
                    'name': sequence,
                })
            if record.case_number and record.district_id and record.branch_district_id:
                sequence = record.district_id.district_code + '/' + record.branch_district_id.branch_district_code +  ' ' + record.case_number 
                record.update({
                    'name': sequence,
                })
    
    @api.onchange('court_id')
    def _onchange_get_presiding_magistrate(self): 
        res = {}
        if self.court_id:
            presiding_magistrate_ids = self.env['res.users'].sudo().search([('court_ids','in', self.court_id.ids)])
            list_presiding = [(pr.id) for pr in presiding_magistrate_ids]
            res = {'domain': {'presiding_magistrate': [('id', 'in', list_presiding)]}}
        else:
            res = {'domain': {'presiding_magistrate': [('id', '=', False)]},
               'value': {'presiding_magistrate': False}}
        return res
    
    def action_submit(self):
        self.write({'state': 'waiting_tiss'})
        now = fields.date.today()
        date_string = now.strftime('%d-%m-%Y')
        message = f"{self.supervisor_id.name} has been assigned by {self.env.user.name} on {date_string} "
        self.message_post(body=message)

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id
    
    @api.depends('case_property_ids.value')
    def _amount_all(self):
        for order in self:
            total_value = 0
            for line in order.case_property_ids:
                total_value += line.value
                currency_name = order.currency_id
                currency = order.currency_id or self.env.company.currency_id
                order.update({
                    'total_value': currency.round(total_value),
                })

class ProbateCase(models.Model):
    _name = 'probate.case.property'

    case_id = fields.Many2one('probate.case', string='case')
    type_properties = fields.Selection([
        ('land', 'Land'),
        ('cash', 'Cash'),
    ], string='Type Properties', required="1")
    name = fields.Char('Detail')
    value = fields.Float('Value')