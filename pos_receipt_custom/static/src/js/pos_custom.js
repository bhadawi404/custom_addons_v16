odoo.define('pos_receipt_custom.pos_custom', function(require){
    'use strict';
    console.log('Before Widget.................................................................!');
    const {PosGlobalState} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosGlobalState1 = (PosGlobalState) => class PosGlobalState1 extends PosGlobalState {
        async gettax(order_id, tax_id) {
            const tax = await this.env.services.rpc({
                model: 'pos.order',
                method: 'get_group_tax',
                args: [order_id, tax_id],
            });
            const taxValueId = 'taxValue_' + tax_id;
            const taxNetId = 'taxNet_' + tax_id;
            const taxVatId = 'taxVat_' + tax_id;
            const taxValueElement = document.getElementById(taxValueId);
            const taxNetElement = document.getElementById(taxNetId);
            const taxVatElement = document.getElementById(taxVatId);
            if (taxValueElement) {
                taxValueElement.innerText = tax.total;
            }
            if (taxNetElement) {
                taxNetElement.innerText = tax.net;
            }
            if (taxVatElement) {
                taxVatElement.innerText = tax.vat;
            }
            return tax;
        }
        async get_tax_label(product_name) {
            console.log("Product Name:", product_name);
            const tax_label = await this.env.services.rpc({
                model: 'pos.order.line',
                method: 'get_label_tax',
                args: [product_name],
            });
            console.log(tax_label,"=== TAX LABEL ====")
            const taxLabelId = 'taxLabel_' + product_name;
            const taxLabelElement = document.getElementById(taxLabelId);
            if (taxLabelElement) {
                taxLabelElement.innerText = tax_label;
            }
            return tax_label;
        }
    }

    
    Registries.Model.extend(PosGlobalState, PosGlobalState1);

});
