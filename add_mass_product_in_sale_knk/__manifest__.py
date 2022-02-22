# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Add/import  Mass/multiple product in order line',
    'version': '1.1',
    'summary': 'This module is allow to add multiple product in purchase order line or import order line from xls file | add multiple products | add mass products | import xlsx for sale line | xlsx import',
    'description': """
        1.You can select multiple product from 'Add mass product' button
        2.You can able to import order lines by xls file
        3.You can Sample file download from sample.xls
        Add multiple products in order lines| Import order lines from xls file|Download sample file| select multiple product
    """,
    'category': 'Sales/Sales',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'depends': ['sale_management'],
    'data': [
        'wizard/add_mass_product_wizard_view.xml',
        'wizard/import_from_file_wizard_view.xml',
        'views/knk_sale_order_view.xml',
        'security/ir.model.access.csv'
    ],
    'images': ['static/description/banner.png'],
    'sequence': 1,
    'installable': True,
    'price': 20,
    'currency': 'EUR',
}
