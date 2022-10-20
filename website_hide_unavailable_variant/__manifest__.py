# -*- coding: utf-8 -*-
{
    'name': "Hide Unavailable Variants",

    'summary': """
           Hide Unavailable Variants on the website""",
    'description': """ This module gives option to hide the variants form the website by simply enabling a
       boolean field. Here no need to set the exclusions. So customer can only see the valid and available attribute 
       values for the product.
       Hide Variants,
       Hide Attribute Values,
       Odoo Hide Variants,
       Hide Product Variants """,

    'author': "ErpMstar Solutions",
    'category': 'eCommerce',
    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': ['website_sale', 'emipro_theme_base', 'theme_clarico_vega'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode

    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
}
