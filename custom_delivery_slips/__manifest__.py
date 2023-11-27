# -*- coding: utf-8 -*-
{
    'name': "Custom Delivery Slips",

    'summary': """Custom Delivery Slips""",

    'description': """Custom Delivery Slips (With Price & Without Price""",

    'author': "ErpMstar Solutions",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
        'report/report_delivery_slip_price.xml',
        'report/report_delivery_slip_without_price.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True
}
