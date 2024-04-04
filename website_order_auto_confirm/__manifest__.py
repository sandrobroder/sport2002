# -*- coding: utf-8 -*-
{
    'name': "Website Order Auto Confirm",

    'summary': """Website Order Auto Confirm without payment""",

    'description': """This module will help you to auto confirm the orders from selected website for a selected payment provide""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/Website',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
    'price': 15,
    'currency': 'EUR',
}
