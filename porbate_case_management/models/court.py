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
    status = fields.Boolean('Status',default=True)

    def name_get(self):
        res = []
        for rec in self:
            name = f"[{rec.court_code}] - {rec.name}"
            res.append((rec.id, name))
        return res


class Disctrict(models.Model):
    _name = 'probate.case.district'
    _description = 'Probate Case District'

    court_id = fields.Many2one('probate.case.court', string='High Court')
    district_code = fields.Char('District Code')
    branch_distric_ids = fields.One2many('probate.case.district.line', 'district_id', string='Branch District')
    status = fields.Boolean('Status', default=True)
    name = fields.Char('District Name')

class DisctrictLine(models.Model):
    _name = 'probate.case.district.line'
    _description = 'Probate Case District'

    district_id = fields.Many2one('probate.case.district', string='High Court')
    branch_district_id = fields.Many2one('probate.case.branch.district', string='District')
    branch_district_code = fields.Char('Branch District Code', related='branch_district_id.branch_district_code')
    branch_district_name = fields.Char('Branch District Name', related='branch_district_id.name')

class BranchDisctrict(models.Model):
    _name = 'probate.case.branch.district'
    _description = 'Probate Case Branch District'

    branch_district_code = fields.Char('Branch District Code')
    name = fields.Char('Branch District Name')

    def name_get(self):
        res = []
        for rec in self:
            name = f"[{rec.branch_district_code}] - {rec.name}"
            res.append((rec.id, name))
        return res
    
class PositionCourt(models.Model):
    _name = 'probate.case.position'
    _description = 'Probate Case Poition'
    _rec_name = 'position_name'

    position_name = fields.Char('Position Name')

class CourtUser(models.Model):
    _inherit = 'res.users'

    
    court_ids = fields.Many2many('probate.case.court', string='Court')