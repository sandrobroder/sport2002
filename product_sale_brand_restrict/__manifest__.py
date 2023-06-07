# -*- coding: utf-8 -*-
{
    'name': "Product Sale Brand Restrict",

    'summary': """Product Sale Brand Restrict""",

    'description': """Product Sale Brand Restrict""",

    'author': "ErpMstar Solutions",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['emipro_theme_base', 'website_sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
}
