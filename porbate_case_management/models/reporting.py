# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models,api,tools,_
from odoo.tools.safe_eval import safe_eval
import re
from odoo.exceptions import UserError, ValidationError


class PaymentBeneficiaries(models.Model):
    _name = 'report.payment.beneficaries'
    _auto = False

    date_payment = fields.Date('Payment Date')
    case_id = fields.Many2one('probate.case', string='Case')
    beneficiaries_id = fields.Many2one('probate.case.beneficiaries', string='Beneficiaries Details')
    property_id = fields.Many2one('probate.case.property', string='Case Inventory')
    amount = fields.Float('Amount')
    beneficaries_name = fields.Char('beneficaries_name', related='beneficiaries_id.name')
    property_name = fields.Char('property_name', related='property_id.name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_tiss', 'Awaiting for tiss'),
        ('completion_form', 'Completion of forms'),
        ('pending_hro_approval', 'Pending HRO approval'),
        ('pending_payment', 'Pending payment'),
        ('closed', 'Closed'),
    ], string='State',group_expand='_group_expand_states', tracking=True, track_visibility='always')

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_payment_beneficaries')
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW report_payment_beneficaries AS (
                SELECT 
                    ROW_NUMBER() OVER () AS id,
                    pb.case_id,
                    pb.date_payment,
                    pb.beneficiaries_id,
                    pb.property_id,
                    pb.amount,
                    pc.state
                FROM 
                    payment_beneficaries pb
                JOIN 
                    probate_case pc ON pb.case_id = pc.id
                JOIN 
                    probate_case_beneficiaries pcb ON pb.beneficiaries_id = pcb.id
                JOIN 
                    probate_case_property pcp ON pb.property_id = pcp.id
            )
        ''')