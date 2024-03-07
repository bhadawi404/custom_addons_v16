# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models,_
from odoo.tools.safe_eval import safe_eval


class Court(models.Model):
    _name = 'probate.case.court'
    _description = 'Probate Case Court'

    court_code = fields.Char('Court Code')
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=', country_id)]")
    name = fields.Char('Court Name')
    status = fields.Boolean('Status')


class Disctrict(models.Model):
    _name = 'probate.case.district'
    _description = 'Probate Case District'

    court_id = fields.Many2one('probate.case.court', string='High Court')
    district_code = fields.Char('District Code')
    branch_distric_ids = fields.One2many('probate.case.branch.district', 'district_id', string='Branch District')
    status = fields.Boolean('Status')
    name = fields.Char('District Name')

class BranchDisctrict(models.Model):
    _name = 'probate.case.branch.district'
    _description = 'Probate Case Branch District'

    district_id = fields.Many2one('probate.case.district', string='District')
    branch_district_code = fields.Char('Branch District Code')
    name = fields.Char('Branch District Name')

class PositionCourt(models.Model):
    _name = 'probate.case.position'
    _description = 'Probate Case Poition'
    _rec_name = 'position_name'

    position_name = fields.Char('Position Name')

class CourtUser(models.Model):
    _inherit = 'res.partner'

    court_ids = fields.Many2many('probate.case.court', string='Court')
    position_id = fields.Many2one('probate.case.position', string='Position')