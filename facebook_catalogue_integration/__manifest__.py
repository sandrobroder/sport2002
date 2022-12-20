# -*- coding: utf-8 -*-
{
    'name': "Facebook Catalog Integration",

    'summary': """
       Facebook Marketing: Create and Upload Product Feeds to Facebook Catalogue Manager""",

    'description': """Create Product feeds and upload products to the Facebook Catalogue Manager, This will put the 
    products to the social platform and attract customers to your online shop. This will increase the revenue""",

    'author': 'ErpMstar Solutions',
    'category': 'Management System',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 40,
    'currency': 'EUR',
}
