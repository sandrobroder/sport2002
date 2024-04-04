# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers import main


class WebsiteSale(main.WebsiteSale):

    def _prepare_shop_payment_confirmation_values(self, order):
        tx = order.get_portal_last_transaction()
        if tx and order.get_portal_last_transaction().provider_id.auto_confirm_sale_order and order.website_id.auto_confirm_quotation:
            order.with_context(send_email=True).action_confirm()
        return super()._prepare_shop_payment_confirmation_values(order)
