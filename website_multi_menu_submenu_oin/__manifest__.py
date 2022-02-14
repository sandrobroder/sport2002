# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2021 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'Website Multiple Menus/Submenus',
    'category': 'Website',
    'summary': 'Website Multiple Menus/Submenus',

    'version': '14.0.1',
    'description': """
Website Multiple Menus/Submenus
===============================
This module allows to list multiple menus/submenus in website.
        """,

    'author': 'Odoo IT now',
    'website': 'http://www.odooitnow.com/',
    'license': 'Other proprietary',

    'depends': [
        'website'
    ],

    'data': [
        'views/assets.xml',
        'views/website_templates.xml',
    ],
    'images': ['images/OdooITnow_screenshot.png'],

    'price': 10.0,
    'currency': 'EUR',

    'installable': True,
    'application': True
}
