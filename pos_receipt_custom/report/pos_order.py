from odoo import fields,models,api,_

class pos_order(models.Model):
	_inherit = "pos.order"
	
	def print_mai_pos_receipt_custom(self):
		return self.env.ref('pos_receipt_custom.action_print_mai_pos_receipt_custom').report_action(self)