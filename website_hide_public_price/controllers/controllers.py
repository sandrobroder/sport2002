# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteHidePublicPrice(http.Controller):
#     @http.route('/website_hide_public_price/website_hide_public_price/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_hide_public_price/website_hide_public_price/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_hide_public_price.listing', {
#             'root': '/website_hide_public_price/website_hide_public_price',
#             'objects': http.request.env['website_hide_public_price.website_hide_public_price'].search([]),
#         })

#     @http.route('/website_hide_public_price/website_hide_public_price/objects/<model("website_hide_public_price.website_hide_public_price"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_hide_public_price.object', {
#             'object': obj
#         })
