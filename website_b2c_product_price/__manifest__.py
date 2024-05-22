# -*- coding: utf-8 -*-
{
    'name': "Website B2C Product Price",

    'summary': """Website B2C Product Price""",

    'description': """Website B2C Product Price""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'eCommerce',
    'version': '1.3',

    # any module necessary for this one to work correctly
    'depends': ['website_sale', 'theme_clarico_vega', 'point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'website_b2c_product_price/static/src/js/pos.js', ]
    },
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
    'installable': True,
}
