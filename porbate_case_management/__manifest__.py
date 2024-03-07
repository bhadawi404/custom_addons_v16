# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Porbate Case Management',
    'version': '1.0',
    'category': 'Porbate/Website',
    'author': "Ahmad Badawi",
    'summary': 'Porbate Case Management - v1.0',
    'depends': ['base','contacts'],
    'data': [
        'views/stage_view.xml',
        'views/user_court.xml',
        'data/position_user.xml',
        'views/district_view.xml',
        'views/court_view.xml',
        'views/menu_items.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}