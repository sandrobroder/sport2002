# -*- coding: utf-8 -*-
{
    'name': "Generate Orders by Excel",

    'summary': """Generate Orders by Excel""",

    'description': """Generate Orders by Excel zip file""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly

    'depends': ['sale_management', 'customer_ref_unique_code'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True
}
