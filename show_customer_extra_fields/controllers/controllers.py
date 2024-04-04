# -*- coding: utf-8 -*-
# from odoo import http


# class ShowCustomerExtraFields(http.Controller):
#     @http.route('/show_customer_extra_fields/show_customer_extra_fields', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/show_customer_extra_fields/show_customer_extra_fields/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('show_customer_extra_fields.listing', {
#             'root': '/show_customer_extra_fields/show_customer_extra_fields',
#             'objects': http.request.env['show_customer_extra_fields.show_customer_extra_fields'].search([]),
#         })

#     @http.route('/show_customer_extra_fields/show_customer_extra_fields/objects/<model("show_customer_extra_fields.show_customer_extra_fields"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('show_customer_extra_fields.object', {
#             'object': obj
#         })
