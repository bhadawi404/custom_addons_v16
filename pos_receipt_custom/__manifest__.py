{
    "name": "Customized POS Receipt",
    "version": "16.0.0.1",
    'sequence': 1,
    'category':"Point of Sale",
    'summary':"RePrint POS Receipt From Pos Order Add Company Logo and Customer Detail in Pos Receipt.",
    "depends": [
        "base",
        "point_of_sale",
    ],
    "data": [
        'views/res_company.xml',
        'report/report_paperformat.xml', 
        'report/pos_report_template.xml',
        'report/pos_order.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_custom/static/src/xml/pos_receipt.xml',
            'pos_receipt_custom/static/src/js/pos_custom.js',
            'pos_receipt_custom/static/src/js/product_screen.js',
            'pos_receipt_custom/static/src/js/pos_receipt.js',
            'pos_receipt_custom/static/src/xml/pos_items_count.xml',
        ],
    },    
    
}

