# -*- coding: utf-8 -*-
{
    'name': "Odoo Image Preview Widget",

    'summary': """Image full screen preview""",

    'description': """Click on the preview button and view the image in full size.""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tool',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [

    ],
    'assets': {
        'web.assets_backend': [
            '/image_preview_widget/static/src/js/widget.js',
            '/image_preview_widget/static/src/css/widget.css',
            '/image_preview_widget/static/src/xml/widget.xml',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
}
