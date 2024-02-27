# -*- coding: utf-8 -*-
{
    'name': "Stock Show Customer Warning",

    'summary': """Stock Show Customer Warning""",

    'description': """Stock Show Customer Warning""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['stock_barcode'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_show_customer_warning/static/src/**/*.js',
            'stock_show_customer_warning/static/src/**/*.xml',
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
