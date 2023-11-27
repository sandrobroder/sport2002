# -*- coding: utf-8 -*-
{
    'name': "Customer Unique Code",

    'summary': """Assign Unique Code to Customer for Reference""",

    'description': """Assign a Unique Reference Code to each Customer and use this code to identify each costumer 
    uniquely""",

    'author': 'ErpMstar Solutions',
    'category': 'Contacts',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        'data/sequence.xml',
        'views/views.xml',

    ],
    # 'qweb': [
    #     'static/src/xml/pos.xml',
    # ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.jpg'],
    'website': '',
    'auto_install': False,
    'price': 9,
    'currency': 'EUR',

}
