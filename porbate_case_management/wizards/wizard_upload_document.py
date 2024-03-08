# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.tools.mail import is_html_empty


class UploadDocument(models.TransientModel):
    _name = 'document.upload'
    _description = 'Upload Document'

    name = fields.Char('Case')
    detail_property_id = fields.Many2one('probate.case.property', string='Detail Property')
    description = fields.Text('Description')
    attachment = fields.Binary('Attachment')

    def action_upload(self):
        self.ensure_one()
        probate_case = self.env['probate.case'].browse(self.env.context.get('active_ids'))
        document = {
            'name': self.name,
            'description': self.description,
            'attachment': self.attachment,
            'case_id': probate_case.id,
            'property_id': self.detail_property_id.id,
        }
        create_doc = self.env['probate.case.document'].sudo().create(document)

class UploadForm(models.TransientModel):
    _name = 'form.upload'
    _description = 'Upload Form'

    name = fields.Char('Form Name')
    form_type = fields.Selection([
        ('vendor_form', 'Vendor Form'),
        ('bank_statement', 'Bank Statement'),
        ('mom', 'Minutes of Meetings to Distribute'),
        ('distribution_form', 'Distribution form'),
        ('voucher_payment', 'Voucher for payment'),
    ], string='Form Type')
    description = fields.Text('Description')
    attachment = fields.Binary('Attachment')

    
    def action_upload_form(self):
        self.ensure_one()
        probate_case = self.env['probate.case'].browse(self.env.context.get('active_ids'))
        document = {
            'name': self.name,
            'description': self.description,
            'attachment': self.attachment,
            'case_id': probate_case.id,
            'form_type': self.form_type
        }
        create_form = self.env['probate.case.form'].sudo().create(document)