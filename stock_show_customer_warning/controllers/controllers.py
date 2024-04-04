# -*- coding: utf-8 -*-
# from odoo import http


# class StockShowCustomerWarning(http.Controller):
#     @http.route('/stock_show_customer_warning/stock_show_customer_warning', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_show_customer_warning/stock_show_customer_warning/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_show_customer_warning.listing', {
#             'root': '/stock_show_customer_warning/stock_show_customer_warning',
#             'objects': http.request.env['stock_show_customer_warning.stock_show_customer_warning'].search([]),
#         })

#     @http.route('/stock_show_customer_warning/stock_show_customer_warning/objects/<model("stock_show_customer_warning.stock_show_customer_warning"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_show_customer_warning.object', {
#             'object': obj
#         })
