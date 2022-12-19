# -*- coding: utf-8 -*-
{
    'name': "Website Hide Public Price",

    'summary': """Website Hide Public Price""",

    'description': """Website Hide Public Price""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale', 'theme_clarico_vega'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True
}
