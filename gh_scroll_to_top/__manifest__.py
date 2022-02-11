# -*- coding: utf-8 -*-
{
    'name': "Website Scroll to Top",

    'summary': """
        automatic scroll to top in website""",

    'description': """
        automatic scroll to top in website
    """,

    'author': "Gabriel Hernandez",
    'website': "https://www.linkedin.com/in/gabrielhernandez3333",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'templates/assets.xml',
        'templates/button_to_top.xml'
    ],

    'images': [
        'static/description/thubmnail.png'
    ]
}
