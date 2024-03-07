# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models,_
from odoo.tools.safe_eval import safe_eval


class CaseStage(models.Model):
    _name = 'probate.case.stage'
    _description = 'Probate Case Stage'
    _rec_name = 'name'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Stage Name')

