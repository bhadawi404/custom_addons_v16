from odoo import api, fields, models, tools, _



class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def get_group_tax(self, receive_name, tax_id):
        amount_tax = self.env['account.tax'].search([('id','=', tax_id)],limit=1).amount
        order_lines = self.env['pos.order'].search([('pos_reference','=', receive_name.get('name'))]).lines
        tax_totals = []
        for line in order_lines:
            product_template = line.product_id.product_tmpl_id
            taxs = self.env['product.template'].search([('id','=', product_template.id),('taxes_id','in', [tax_id])])
            if taxs:
                total_tax = line.price_subtotal_incl
                tax_totals.append(total_tax)
        total = sum(tax_totals)
        net = total /(amount_tax+100)*100
        vat = total - net
        net_round = round(net, 2)
        vat_round = round(vat, 2)
        vals = {
            'total': "{:.2f}".format(total),
            'net': "{:.2f}".format(net_round),
            'vat': "{:.2f}".format(vat_round)
        }
        return vals

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.model
    def get_label_tax(self, product_name):
        products = self.env['product.product'].search([('name','=', product_name)],limit=1)
        tax_labels = []
        for product in products:
            product_taxs = product.product_tmpl_id.taxes_id
            for taxes in product_taxs:
                tax_labels.append(taxes.name)
        print(tax_labels)
        if len(tax_labels) > 1:
            label = ', '.join(tax_labels)
        elif len(tax_labels) == 1:
            label = tax_labels[0]
        else:
            label = '-'
        print(label)
        return label

        