# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	"name" : "POS Gift Coupons & POS Vouchers Discount in Odoo",
	"version" : "14.0.1.4",
	"category" : "Point of Sale",
	"depends" : ['base','sale','point_of_sale'],
	"author": "BrowseInfo",
	"price": 39.00,
	"currency": 'EUR',
	'summary': 'Point Of Sales discount Coupons POS Discount pos voucher POS Promocode Discount pos bonus Coupons POS offers Discount pos Coupons discount POS promo Discount pos offer discount pos bonus pos sale discount POS Promotional',
	"description": """
	
	Purpose :- 
	odoo gift coupons POS gift coupons Point of sales gift coupons POS offer discount POS
	odoo points of sales gift voucher pos discount vouchers point of sales Gift Coupons pos Gift Coupons pos Gift Vouchers
odoo Create Gift Vouchers/Coupons for discount on special occasions for grabbing more customers.
odoo pos discount vouchers gift discount pos promotion pos promo coupon point of sales promo code
odoo point of sales promo coupon odoo pos promotional discount Gift Coupons Discount in pos pos Gift Coupons Discount pos vouchers discount pos gift vouchers discount
odoo pos discount coupon pos gift discount pos discount vouhcer pos coupon discount pos voucher coupon 
odoo POS discount Point of Sale Discount POS Gift Vouchers Point of Sale Gift Voucher Point of sale Coupons
odoo pos gift coupon pos discount coupon pos discount vouchers pos coupon voucher pos coupon discount
odoo point of sale gift coupon point of sale discount coupon point of sale discount vouchers
odoo point of sale coupon voucher point of sale coupon discount POS coupon code point of sales coupon code
odoo POS promo-code Point of sale promocode POS promocode Point of sale promo-code 
odoo Point of sales Discount odoo Discount on POS Disount on point of sales Deducation on POS 
odoo POS deducation Point of sale deduction Gift Voucher on POS Gift Voucher on Point of sales.

odoo pos coupons discoun pos voucher discount pos gift vouchers pos gift vouchers
odoo pos gift vouchers card pos giftcard pos gift card odoo giftcards in pos
odoo gift cards in point of sales odoo pos gifts cards pos gift cards pos gift promotion
odoo pos giftcards POS Gift Card point of sales gift cards point of sales giftcards
odoo giftcards in pos odoo pos offer giftcards odoo point of sales giftcards in pos odoo point of sale offer giftcards odoo

	""",
	"website" : "https://www.browseinfo.in",
	"data": [
		'security/ir.model.access.csv',
		'views/custom_pos_view.xml',
		'views/pos_gift_coupon.xml',
		'views/pos_order_view.xml',
		'views/report_pos_gift_coupon.xml',
	],
	'qweb': [
		'static/src/xml/pos_coupons_gift_voucher.xml',
	],
	"auto_install": False,
	"installable": True,
	"live_test_url":'https://youtu.be/6gI4E2B4YZ8',
	"images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
