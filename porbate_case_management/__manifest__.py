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
        'views/dashboard.xml',
        'views/reporting.xml',
        'data/report_probate_case.xml',
        'wizards/wizard_payment_view.xml',
        'wizards/wizard_upload_document_view.xml',
        'data/email_reject.xml',
        'wizards/wizard_approval_view.xml',
        'views/case_view.xml',
        'views/user_court.xml',
        'data/position_user.xml',
        'views/district_view.xml',
        'views/court_view.xml',
        'views/menu_items.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'porbate_case_management/static/src/css/dashboard.css',
            'porbate_case_management/static/src/css/style.scss',
            'porbate_case_management/static/src/css/material-gauge.css',
            'porbate_case_management/static/src/xml/activity_dashboard_view.xml',
            'porbate_case_management/static/src/js/activity_dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}