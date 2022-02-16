{
    'name': 'ProcessControl | Comisiones de agentes por zonas',
    'version': '1.0.0',
    'category': 'Website',
    'author': "ProcessControl",
    'website': "https://www.processcontrol.es",
    'description': """""",
    'depends': ['sale_commission','base_location','account','product'],
    'installable': True,
    'auto_install': False,
    'data': [
        'views/res_country_state_view.xml',
        'views/product_category_view.xml',
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/stock_picking_view.xml'
    ]
}
