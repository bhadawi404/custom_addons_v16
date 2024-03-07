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
    presiding_magistrate = fields.Many2one('res.partner', string='Presiding Magistrate')
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
    ], string='state', default='draft')

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
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('name', 'New Case') == 'New Case':
    #             date = fields.Date.today()
    #             code_district = self.env['probate.case.district'].search([('id','=', int(vals.get('district_id')))]).district_code
    #             code_branch_district = self.env['probate.case.branch.district'].search([('id','=', int(vals.get('branch_district_id')))]).branch_district_code
    #             date_today = date.strftime('%d/%m/%Y')
                
    #             pattern = code_district + '/' + code_branch_district + ' ' + '%' + '/' + date_today
    #             last_seq_number_rec = self.env['probate.case'].sudo().search([
    #                     ('name', 'like', pattern)
    #                 ], order='id desc', limit=1)

    #             if last_seq_number_rec and last_seq_number_rec.name:
    #                 last_seq_number_match = re.search(r'\s(\d{2})/', last_seq_number_rec.name)
    #                 if last_seq_number_match:
    #                     last_seq_number = int(last_seq_number_match.group(1))
    #                     sequence_number = last_seq_number + 1
    #                 else:
    #                     sequence_number = 1
    #             else:
    #                 sequence_number = 1

    #             vals['name'] = code_district + '/' + code_branch_district + ' ' + str(sequence_number).zfill(2) + '/' + date_today
    #         return super().create(vals)


    def action_submit(self):
        self.write({'state': 'waiting_tiss'})

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