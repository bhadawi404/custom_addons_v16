# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models,api,_
from odoo.tools.safe_eval import safe_eval
import re
from odoo.exceptions import UserError, ValidationError

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

class PaymentBeneficiaries(models.Model):
    _name = 'payment.beneficaries'

    date_payment = fields.Date('Payment Date')
    case_id = fields.Many2one('probate.case', string='case')
    beneficiaries_id = fields.Many2one('probate.case.beneficiaries', string='Beneficiaries Details')
    property_id = fields.Many2one('probate.case.property', string='Case Inventory')
    amount = fields.Float('Amount')
    remarks = fields.Text('Remarks')
    beneficaries_name = fields.Char('beneficaries_name', related='beneficiaries_id.name')
    property_name = fields.Char('property_name', related='property_id.name')

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
    case_property_ids = fields.One2many('probate.case.property', 'case_id', string='Properties', ondelete='cascade')
    administrator_name = fields.Many2one('res.users', string='User Clerk', default=lambda self: self.env.user,)
    email_clerk = fields.Char('Clerk email', related='administrator_name.email')
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
        ('case_to_close', 'Case to Close'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', group_expand='_group_expand_states', tracking=True, track_visibility='always')
    supervisor_id = fields.Many2one('res.users', string='Supervisor')
    email_supervisor = fields.Char(string='Supervisor Email', related='supervisor_id.email')
    show_button_confirm_for_supervisor = fields.Boolean('show_button_confirm_for_supervisor', compute='_show_button_confirm_suppervisor')
    show_button_upload_document = fields.Boolean('show_button_upload_document', compute='_show_button_upload_document')
    document_ids = fields.One2many('probate.case.document', 'case_id', string='document',ondelete='cascade')
    form_ids = fields.One2many('probate.case.form', 'case_id', string='form',ondelete='cascade')
    show_button_confirm_for_administrator = fields.Boolean('show_button_confirm_for_administrator', compute='_show_button_confirm_administrator')
    show_button_upload_document_administrator = fields.Boolean('show_button_upload_document', compute='_show_button_upload_document_administrator')
    hro_approval = fields.Many2one('res.users', string='HRO Approval')
    email_hro = fields.Char(string='HRO Email', related='hro_approval.email')
    show_button_confirm_for_hro = fields.Boolean('show_button_confirm_for_hro', compute='_show_button_confirm_hro')
    show_button_confirm_for_payment = fields.Boolean('show_button_confirm_for_payment', compute='_show_button_confirm_payment')
    accounting_id = fields.Many2one('res.users', string='Accounting')
    email_accounting = fields.Char(string='Accounting Email', related='accounting_id.email')
    payment_beneficaries_ids = fields.One2many('payment.beneficaries', 'case_id', string='Payment Of Beneficaries',ondelete='cascade')
    property_value_ids = fields.One2many('probate.case.property.value', 'case_id', string='Property Value',ondelete='cascade')
    show_button_closed_for_payment = fields.Boolean('show_button_closed_for_payment', compute='_show_button_closed_for_payment')

    #Presiding Judge
    form_closssure_ids = fields.One2many('probate.case.form.closssure', 'case_id', string='form',ondelete='cascade')
    show_button_closed = fields.Boolean('show_button_closed', compute='_show_button_closed')
    show_button_upload_document_clossure_presiding = fields.Boolean('show_button_upload_document_clossure_presiding', compute='_show_button_upload_document_clossure_presiding')


    #APPROVAL DATE
    approve_date_creator = fields.Date('Approved Created by')
    approve_date_supervisor = fields.Date('Approved Supervisor')
    approve_date_administrator = fields.Date('Approved Administrator')
    approve_date_hro = fields.Date('Approved HRO')
    approve_date_accounting = fields.Date('Approved Accounting')
    approve_date_closed = fields.Date('Closed Case')

    administrator_of_state = fields.Char('Name of the Administrator of the estate')

    def get_state_count(self):
        """get the activity count details"""
        activity = self.env['probate.case']
        value_property = self.env['probate.case.property.value']
        payment_beneficaries = self.env['payment.beneficaries']
        domain = []
        # if self.env.user._is_admin():
        #     domain = domain
        # else:
        #     domain.append(('user_id', '=', self.env.user.id), )
        all = activity.with_context(active_test=False).search(domain)
        draft = all.filtered(lambda x: x.state == 'draft')
        waiting_tiss = all.filtered(lambda x: x.state == 'waiting_tiss')
        completion_form = all.filtered(lambda x: x.state == 'completion_form')
        pending_hro_approval = all.filtered(lambda x: x.state == 'pending_hro_approval')
        pending_payment = all.filtered(lambda x: x.state == 'pending_payment')
        closed = all.filtered(lambda x: x.state == 'closed')
        case_to_closed = all.filtered(lambda x: x.state == 'case_to_close')
        case = activity.sudo().search(domain)
        total = 0
        for total_inventory in case:
            total += total_inventory.total_value

        paid_value = payment_beneficaries.sudo().search(domain)
        total_paid = 0
        for paid in paid_value:
            total_paid += paid.amount
        
        partially_value = value_property.sudo().search(([('state','=', 'partial')]))
        total_partially = 0
        for partially in partially_value:
            total_partially += partially.paid

        not_paid_value = value_property.sudo().search(([('state','=', 'pending_payment')]))
        total_not_paid = 0
        for not_paid in not_paid_value:
            total_not_paid += not_paid.balance
        res = {
            'len_all': len(all),
            'len_waiting_tiss': len(waiting_tiss),
            'len_draft': len(draft),
            'len_completion_form': len(completion_form),
            'len_pending_hro_approval': len(pending_hro_approval),
            'len_pending_payment': len(pending_payment),
            'len_closed': len(closed),
            'len_case_to_close': len(case_to_closed),
            'total_inventory':f'{total:,.2f}',
            'paid_inventory':f'{total_paid:,.2f}',
            'partially_inventory': f'{total_partially:,.2f}',
            'not_paid': f'{total_not_paid:,.2f}'
        }
        return res
    
    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        for ml in self:
            if ml.state!='draft':
                raise UserError(_("Sorry, You can't delete Case(s) that has already been processed"))

    def send_email_notification(self, stage=None):
        if stage == 'waiting_tiss':
            to = self.supervisor_id.name
            email_to = self.supervisor_id.email
            message = f"You have been assigned to complete the Tiss Attachment Stage to the Case Number : {self.name}"
        if stage == 'completion_form':
            to = self.administrator_name.name
            email_to = self.administrator_name.email
            message = f"You have been assigned to complete the Form Attachment Stage to the Case Number : {self.name}"
        if stage == 'pending_hro_approval':
            to = self.hro_approval.name
            email_to = self.hro_approval.email
            message = f"You have been assigned to complete the approval for Case Number: {self.name}"
        if stage == 'pending_payment':
            to = self.accounting_id.name
            email_to = self.accounting_id.email
            message = f"You have been assigned to complete the payment management of Case: {self.name}"
        if stage == 'case_to_close':
            to = self.presiding_magistrate.name
            email_to = self.presiding_magistrate.email
            message = f"You have been assigned to closed of Case: {self.name}"
        if stage == 'closed':
            to = 'All'
            email_to = [self.supervisor_id.partner_id.id,self.administrator_name.partner_id.id,self.accounting_id.partner_id.id]
            message = f"All tasks have been completed and the case: This {self.name} has been closed "
        for rec in self:
            #Send Email
            action_url = '%s/web#id=%s&menu_id=%s&action=%s&model=probate.case&view_type=form' % (
                self.get_base_url(),
                rec.id,
                self.env.ref('porbate_case_management.menu_case_root').id,
                self.env.ref('porbate_case_management.case_action').id,
            )
            template_approval = self.env.ref('porbate_case_management.email_assign_task', raise_if_not_found=False)
            template_context = {
                'to': to,
                'message': message,
                'company_id': self.env.company.name,
                'action_url': action_url,
            }
            if rec.state == 'closed':
                template_approval.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={'recipient_ids': email_to}, email_layout_xmlid='mail.mail_notification_light')
            else:
                template_approval.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={'email_to': email_to}, email_layout_xmlid='mail.mail_notification_light')
    #STAGE SUBMIT
    def action_submit(self):
        now = fields.date.today()
        self.write({'state': 'waiting_tiss','approve_date_creator': now})
        self.send_email_notification(stage='waiting_tiss')
        

    def action_back_to_draft(self):
        self.write({'state': 'draft'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    #STAGE AWAITING TISS
    def _show_button_confirm_suppervisor(self):
        for record in self:
            if record.state == 'waiting_tiss':
                if record.document_ids:
                    if record.env.user.id == record.supervisor_id.id:
                        record.show_button_confirm_for_supervisor = True
                    else:
                        record.show_button_confirm_for_supervisor = False
                else:
                    record.show_button_confirm_for_supervisor = False
            else:
                record.show_button_confirm_for_supervisor = False
    
    def _show_button_upload_document(self):
        for record in self:
            if record.state == 'waiting_tiss':
                if record.env.user.id == record.supervisor_id.id:
                    record.show_button_upload_document = True
                else:
                    record.show_button_upload_document = False
            else:
                record.show_button_upload_document = False

    def action_upload_document(self):
        form_view_id = self.env.ref('porbate_case_management.upload_document_view_form').id
        list_property = []
        property = self.env['probate.case.property'].search([('case_id','=', self.id)])
        for record in property:
            validation_in_document = self.env['probate.case.document'].search([('property_id','=', record.id)])
            if validation_in_document:
                continue
            else:
                list_property.append(record.id)
        action =  {
            'name': _('Upload Document'),
            'view_mode': 'form',
            'res_model': 'document.upload',
            'view_id': form_view_id,
            'views': [(form_view_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
            'default_name': self.name,
            'default_detail_property_id': list_property
        }
        }
        return action
    
    def action_confirm(self):
        now = fields.date.today()
        self.write({'state': 'completion_form','approve_date_supervisor': now})
        self.send_email_notification(stage='completion_form')
        
    

    
    #STAGE COMPLETION FORM
    def _show_button_confirm_administrator(self):
        for record in self:
            if record.state == 'completion_form':
                if record.form_ids:
                    if record.env.user.id == record.administrator_name.id:
                        record.show_button_confirm_for_administrator = True
                    else:
                        record.show_button_confirm_for_administrator = False
                else:
                    record.show_button_confirm_for_administrator = False
            else:
                record.show_button_confirm_for_administrator = False
    
    def _show_button_upload_document_administrator(self):
        for record in self:
            if record.state == 'completion_form':
                if record.env.user.id == record.administrator_name.id:
                    record.show_button_upload_document_administrator = True
                else:
                    record.show_button_upload_document_administrator = False
            else:
                record.show_button_upload_document_administrator = False

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
    
    def complete_form_attachment(self):
        now = fields.date.today()
        self.write({'state': 'pending_hro_approval','approve_date_administrator': now})
        self.send_email_notification(stage='pending_hro_approval')

    def action_upload_form(self):
        form_view_id = self.env.ref('porbate_case_management.upload_form_view_form').id
        action =  {
            'name': _('Upload Form'),
            'view_mode': 'form',
            'res_model': 'form.upload',
            'view_id': form_view_id,
            'views': [(form_view_id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
            'default_name': self.name,
        }
        }
        return action
    

    #STAGE APPROVAL HRO
    def _show_button_confirm_hro(self):
        for record in self:
            if record.state == 'pending_hro_approval':
                if record.env.user.id == record.hro_approval.id:
                    record.show_button_confirm_for_hro = True
                else:
                    record.show_button_confirm_for_hro = False
            else:
                record.show_button_confirm_for_hro = False

    def action_approve_hro(self):
        now = fields.date.today()
        self.write({'state': 'pending_payment','approve_date_hro': now})
        for rec in self.case_property_ids:
            property_value = self.env['probate.case.property.value'].sudo().search([('property_id','=',rec.id)])
            if not property_value:
                vals = {
                    'property_id': rec.id,
                    'case_id': rec.case_id.id
                }
                create_property_value = self.env['probate.case.property.value'].sudo().create(vals)
            else:
                for value in property_value:
                    value.sudo().write({
                        'case_id': rec.case_id.id,
                        'property_id': rec.id
                    })
        self.send_email_notification(stage='pending_payment') 
                
    def action_reject_hro(self):
        form_view_hro = self.env.ref('porbate_case_management.reject_approval_hro').id
        action =  {
            'name': _('Reason Reject'),
            'view_mode': 'form',
            'res_model': 'reason.reject.hro',
            'view_id': form_view_hro,
            'views': [(form_view_hro, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action

    
    #STAGE PAYMENT
    def _show_button_confirm_payment(self):
        for record in self:
            if record.state == 'pending_payment':
                if record.env.user.id == record.accounting_id.id:
                    record.show_button_confirm_for_payment = True
                else:
                    record.show_button_confirm_for_payment = False
            else:
                record.show_button_confirm_for_payment = False

    def _show_button_closed_for_payment(self):
        for record in self:
            if record.state == 'pending_payment':
                total_value = 0
                for paid in record.property_value_ids:
                    total_value += paid.balance
                if total_value != 0:
                    record.show_button_closed_for_payment = False
                else:
                    if record.env.user.id == record.accounting_id.id:
                        record.show_button_closed_for_payment = True
                    else:
                        record.show_button_closed_for_payment = False
            else:
                record.show_button_closed_for_payment = False
    
    def action_pay(self):
        form_view_create_payment = self.env.ref('porbate_case_management.payment_view_form').id
        action =  {
            'name': _('Create Payment'),
            'view_mode': 'form',
            'res_model': 'payment.beneficaries.wizard',
            'view_id': form_view_create_payment,
            'views': [(form_view_create_payment, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_case_id': self.id,
            }
            
        }
        return action

    def action_reject_payment(self):
        form_view_payment = self.env.ref('porbate_case_management.reject_approval_payment').id
        action =  {
            'name': _('Reason Reject'),
            'view_mode': 'form',
            'res_model': 'reason.reject.payment',
            'view_id': form_view_payment,
            'views': [(form_view_payment, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action
    
    def closed_to_payment(self):
        now = fields.date.today()
        self.write({'state': 'case_to_close','approve_date_accounting': now})
        self.send_email_notification(stage='case_to_close')
        
    #STAGE CLOSED CASE
    def _show_button_closed(self):
        for record in self:
            if record.state == 'case_to_close':
                if record.form_closssure_ids:
                    if record.env.user.id == record.presiding_magistrate.id:
                        record.show_button_closed = True
                    else:
                        record.show_button_closed = False
                else:
                    record.show_button_closed = False
            else:
                record.show_button_closed = False

    def _show_button_upload_document_clossure_presiding(self):
        for record in self:
            if record.state == 'case_to_close':
                if record.env.user.id == record.presiding_magistrate.id:
                    record.show_button_upload_document_clossure_presiding = True
                else:
                    record.show_button_upload_document_clossure_presiding = False
            else:
                record.show_button_upload_document_clossure_presiding = False

    def action_approve_presiding(self):
        now = fields.date.today()
        self.write({'state': 'closed','approve_date_closed': now})
        self.send_email_notification(stage='closed')

    def action_reject_predising(self):
        form_view_presiding = self.env.ref('porbate_case_management.reject_approval_presiding').id
        action =  {
            'name': _('Reason Reject'),
            'view_mode': 'form',
            'res_model': 'reason.reject.presiding',
            'view_id': form_view_presiding,
            'views': [(form_view_presiding, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return action

    def action_upload_closser(self):
        form_view_closer = self.env.ref('porbate_case_management.upload_form_closser_view_form').id
        action =  {
            'name': _('Upload Form'),
            'view_mode': 'form',
            'res_model': 'form.upload.closser',
            'view_id': form_view_closer,
            'views': [(form_view_closer, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
            'default_name': self.name,
        }
        }
        return action


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

class ProbateCaseProperty(models.Model):
    _name = 'probate.case.property'

    case_id = fields.Many2one('probate.case', string='case')
    type_properties = fields.Selection([
        ('land', 'Land'),
        ('cash', 'Cash'),
    ], string='Type Properties', required="1")
    name = fields.Char('Detail')
    value = fields.Float('Value')
    paid = fields.Float('Paid')
    balance = fields.Float('Balance')

class ProbateCasePropertyValue(models.Model):
    _name = 'probate.case.property.value'

    case_id = fields.Many2one('probate.case', string='case')
    property_id = fields.Many2one('probate.case.property', string='Property')
    type_properties = fields.Selection([
        ('land', 'Land'),
        ('cash', 'Cash'),
    ], string='Type Properties', related='property_id.type_properties')
    name = fields.Char('Detail', related='property_id.name')
    value = fields.Float('Value', related='property_id.value')
    paid = fields.Float('Paid')
    balance = fields.Float('Balance', compute='_get_balance')
    state = fields.Selection([
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partial Payment'),
        
    ], string='Payment State', compute='_compute_state', store=True)
    
    @api.depends('value','balance','paid')
    def _compute_state(self):
        for rec in self:
            if rec.paid == 0:
                rec.update({'state': 'pending_payment'})
                rec.state = 'pending_payment'
            elif rec.paid != rec.value:
                rec.update({'state': 'partial'})
                rec.state = 'partial'
            elif rec.balance == 0:
                rec.update({'state': 'paid'})

    def _get_balance(self):
        for rec in self:
            rec.balance = rec.value - rec.paid