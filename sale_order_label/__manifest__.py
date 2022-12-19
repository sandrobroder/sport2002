# -*- coding: utf-8 -*-
{
    'name': "Sale Order Label Print",

    'summary': """Sale Order Label Print""",

    'description': """Sale Order Label Print""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'delivery'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/so_label_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
}
