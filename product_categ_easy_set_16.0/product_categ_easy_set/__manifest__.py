# -*- coding: utf-8 -*-
{
    'name': "Product Category Easy Set",

    'summary': """Product Category Easy Set""",

    'description': """Product Category Easy Set""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'website_sale', 'theme_clarico_vega'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True
}
