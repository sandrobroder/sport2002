# -*- coding: utf-8 -*-
{
    'name': "Website Product Image By Stock",

    'summary': """Website Product Image By Stock""",

    'description': """Website Product Image By Stock""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'data/ir_cron.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True
}
