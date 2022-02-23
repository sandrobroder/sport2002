# Copyright 2020 David Cantador - david.cantador@processcontrol.es
# License AGPL-3.0 or later
{
    "name": "Product B2B Sport2002",
    "summary":
        "Module to control the basic actions of the website catalog B2B.",
    "version": "14.0.1.0.0",
    "category": "undefined",
    "website": "",
    "author": "ProcessControl",
    "license": "AGPL-3",
    "depends": [
        "base",
        "emipro_theme_base",
        "theme_clarico_vega",
        "website_sale",
    ],
    'data': [
        'templates/product.xml',
        #'templates/product.xml',
        # 'views/product_template.xml'
    ],
    "application": True,
    "installable=": True
}
