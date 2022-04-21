{
    'name': 'ProcessControl | Sale Order',
    'version': '1.0.0',
    'category': 'Sales',
    'author': "ProcessControl",
    'website': "https://www.processcontrol.es",
    'description': """""",
    'depends': ['sale', 'delivery_package_number'],
    'installable': True,
    'auto_install': False,
    'data': [
        'views/sale_order.xml',
    ]
}
