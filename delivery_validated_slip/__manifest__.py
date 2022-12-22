# -*- coding: utf-8 -*-
{
    'name': "Validated Delivery Slip",

    'summary': """Validated Delivery Slip""",

    'description': """Validated Delivery Slip""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'report/report_deliveryslip.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
}
