# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.tools.mail import is_html_empty
from odoo.exceptions import UserError, ValidationError

class PaymentBeneficaries(models.TransientModel):
    _name = 'payment.beneficaries.wizard'
    _description = 'Payment to Beneficaries'


    date_payment = fields.Date('Payment Date')
    case_id = fields.Many2one('probate.case', string='case')
    beneficiaries_id = fields.Many2one('probate.case.beneficiaries', string='Beneficiaries Details')
    property_id = fields.Many2one('probate.case.property', string='Case Inventory')
    amount = fields.Float('Amount')
    remarks = fields.Text('Remarks')
    paid = fields.Float('Paid')
    balance = fields.Float('Balance')

    def action_pay(self):
        case = self.env['probate.case'].browse(self.env.context.get('active_ids'))
        vals = {
            'date_payment': self.date_payment,
            'case_id': case.id,
            'beneficiaries_id': self.beneficiaries_id.id,
            'property_id': self.property_id.id,
            'amount': self.amount,
            'remarks': self.remarks,
        }
        create_payment_beneficaries = self.env['payment.beneficaries'].sudo().create(vals)
        find_property_value = self.env['probate.case.property.value'].search([('case_id','=', case.id),('property_id','=', self.property_id.id)],limit=1)
        
        find_property_value.sudo().write({
            'paid': find_property_value.paid + self.amount
        })
    
    @api.onchange('property_id')
    def _onchange_property_id(self):
        for record in self:
            find_property_value = self.env['probate.case.property.value'].search([('property_id','=', record.property_id.id)],limit=1)
            record.balance = find_property_value.balance

    @api.constrains('amount','balance')
    def _constrains_amount(self):
        if self.amount > self.balance:
            raise ValidationError(_("Sorry !! The amount to be paid must not exceed the amount outstanding."))
        if self.amount == 0:
            raise ValidationError(_("Sorry !! the amount to be paid cannot be zero"))
