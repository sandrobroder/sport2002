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
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

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
