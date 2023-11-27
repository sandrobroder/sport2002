# -*- coding: utf-8 -*-
{
    'name': "Product Custom Label Print",

    'summary': """Product Custom Label Print""",

    'description': """Product Custom Label Print""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Product',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'application': True,
}
