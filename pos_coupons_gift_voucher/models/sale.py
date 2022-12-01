# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, tools
import logging
_logger = logging.getLogger(__name__)


class pos_order(models.Model):
	_inherit = 'pos.order'

	coupon_id = fields.Many2one('pos.gift.coupon')

	@api.model
	def create_from_ui(self, orders, draft=False):
		order_ids = super(pos_order, self).create_from_ui(orders, draft=False)
		for order_id in order_ids:
			try:
				pos_order_id = self.browse(order_id.get('id'))
				if pos_order_id:
					ref_order = [o['data'] for o in orders if o['data'].get('name') == pos_order_id.pos_reference]
					for order in ref_order:
						coupon_id = order.get('coupon_id', False)
						if coupon_id:
							coup_max_amount = order.get('coup_maxamount',False)
							pos_order_id.write({'coupon_id':  coupon_id})
							pos_order_id.coupon_id.update({
								'coupon_count': pos_order_id.coupon_id.coupon_count + 1,
								'max_amount': coup_max_amount
							})

			except Exception as e:
				_logger.error('Error in point of sale validation: %s', tools.ustr(e))
		return order_ids


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
