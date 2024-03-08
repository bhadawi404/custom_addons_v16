# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.tools.mail import is_html_empty


class ReasonReject(models.TransientModel):
    _name = 'reason.reject'
    _description = 'Get Mention Reason'

    remarks = fields.Html(
        'Reason Reject', sanitize=True
    )

    def action_reject(self):
        self.ensure_one()
        case = self.env['probate.case'].browse(self.env.context.get('active_ids'))
        if not is_html_empty(self.remarks):
            case._track_set_log_message(
                '<div style="margin-bottom: 4px;"><p>%s:</p>%s<br /></div>' % (
                    _('Reason Reject'),
                    self.remarks
                )
            )
        case.sudo().write({'state': 'waiting_tiss'})
        for rec in case:
            #Send Email
            action_url = '%s/web#id=%s&menu_id=%s&action=%s&model=probate.case&view_type=form' % (
                self.get_base_url(),
                rec.id,
                self.env.ref('porbate_case_management.menu_case_root').id,
                self.env.ref('porbate_case_management.case_action').id,
            )
            template_approval = self.env.ref('porbate_case_management.email_reject', raise_if_not_found=False)
            template_context = {
                'suppervisor': rec.supervisor_id.name,
                'message': self.remarks,
                'user_id': self.env.user.name,
                'company_id': self.env.company.name,
                'action_url': action_url,
            }
            template_approval.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={'email_to': rec.supervisor_id.email}, email_layout_xmlid='mail.mail_notification_light')

class ReasonRejectHRO(models.TransientModel):
    _name = 'reason.reject.hro'
    _description = 'Get Mention Reason HRO'

    remarks = fields.Html(
        'Reason Reject', sanitize=True
    )

    def action_reject(self):
        self.ensure_one()
        case = self.env['probate.case'].browse(self.env.context.get('active_ids'))
        if not is_html_empty(self.remarks):
            case._track_set_log_message(
                '<div style="margin-bottom: 4px;"><p>%s:</p>%s<br /></div>' % (
                    _('Reason Reject'),
                    self.remarks
                )
            )
        case.sudo().write({'state': 'completion_form'})
        for rec in case:
            #Send Email
            action_url = '%s/web#id=%s&menu_id=%s&action=%s&model=probate.case&view_type=form' % (
                self.get_base_url(),
                rec.id,
                self.env.ref('porbate_case_management.menu_case_root').id,
                self.env.ref('porbate_case_management.case_action').id,
            )
            template_approval = self.env.ref('porbate_case_management.email_reject_hro', raise_if_not_found=False)
            template_context = {
                'administration': rec.administrator_name.name,
                'message': self.remarks,
                'user_id': self.env.user.name,
                'company_id': self.env.company.name,
                'action_url': action_url,
            }
            template_approval.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={'email_to': rec.administrator_name.email}, email_layout_xmlid='mail.mail_notification_light')

class ReasonRejectAdmini(models.TransientModel):
    _name = 'reason.reject.payment'
    _description = 'Get Mention Reason Payment'

    remarks = fields.Html(
        'Reason Reject', sanitize=True
    )

    def action_reject(self):
        self.ensure_one()
        case = self.env['probate.case'].browse(self.env.context.get('active_ids'))
        if not is_html_empty(self.remarks):
            case._track_set_log_message(
                '<div style="margin-bottom: 4px;"><p>%s:</p>%s<br /></div>' % (
                    _('Reason Reject'),
                    self.remarks
                )
            )
        case.sudo().write({'state': 'pending_hro_approval'})
        for rec in case:
            #Send Email
            action_url = '%s/web#id=%s&menu_id=%s&action=%s&model=probate.case&view_type=form' % (
                self.get_base_url(),
                rec.id,
                self.env.ref('porbate_case_management.menu_case_root').id,
                self.env.ref('porbate_case_management.case_action').id,
            )
            template_approval = self.env.ref('porbate_case_management.email_reject_payment', raise_if_not_found=False)
            template_context = {
                'hro': rec.hro_approval.name,
                'message': self.remarks,
                'user_id': self.env.user.name,
                'company_id': self.env.company.name,
                'action_url': action_url,
            }
            template_approval.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={'email_to': rec.hro_approval.email}, email_layout_xmlid='mail.mail_notification_light')