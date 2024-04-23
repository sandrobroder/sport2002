# -*- coding: utf-8 -*-
{
    'name': "Website Show Product Barcode",

    'summary': """Show the product Barcode in website""",

    'description': """By using this application you can show the product's Barcode in the
                product's website page. It gives better experience with the products that have multiple variants.""",

    'author': 'ErpMstar Solutions',
    'category': 'Website/Website',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
        'views/settings.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
        'web.assets_frontend': ['/website_show_product_internal_reference/static/src/js/show_product_ref.js']},
    'images': ['static/description/banner.jpg'],
    'application': True,
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 30,
    'currency': 'EUR',
    'live_test_url': 'https://www.youtube.com/watch?v=4vfZHEB4L_Q'
}
