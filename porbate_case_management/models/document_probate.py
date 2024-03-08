# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models,api,_
from odoo.tools.safe_eval import safe_eval
import re

class DocumentProbate(models.Model):
    _name = 'probate.case.document'
    _description = 'Probate Case Document'
    _rec_name = 'name'

    case_id = fields.Many2one('probate.case', string='Probate')
    name = fields.Char('Case')
    description = fields.Text('Description')
    attachment = fields.Binary('Attachment')
    property_id = fields.Many2one('probate.case.property', string='Property Detail')


class FormProbate(models.Model):
    _name = 'probate.case.form'
    _description = 'Probate Case Form'
    _rec_name = 'name'

    case_id = fields.Many2one('probate.case', string='Probate')
    name = fields.Char('Form Name')
    form_type = fields.Selection([
        ('vendor_form', 'Vendor Form'),
        ('bank_statement', 'Bank Statement'),
        ('mom', 'Minutes of Meetings to Distribute'),
        ('distribution_form', 'Distribution form'),
        ('voucher_payment', 'Voucher for payment'),
    ], string='Form Type')
    description = fields.Text('Details')
    attachment = fields.Binary('Attachment')