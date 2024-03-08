# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.tools.mail import is_html_empty


class UploadDocument(models.TransientModel):
    _name = 'document.upload'
    _description = 'Upload Document'

    name = fields.Char('Case')
    description = fields.Text('Description')
    attachment = fields.Binary('Attachment')

    def action_upload(self):
        self.ensure_one()
        probate_case = self.env['probate.case'].browse(self.env.context.get('active_ids'))
        document = {
            'name': self.name,
            'description': self.description,
            'attachment': self.attachment,
            'case_id': probate_case.id
        }
        create_doc = self.env['probate.case.document'].sudo().create(document)
        