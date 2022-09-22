# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo.http import request


class WebsiteSales(WebsiteSale):

    def _get_products_recently_viewed(self):
        res = super(WebsiteSales, self)._get_products_recently_viewed()
        if res and res.get("products"):
            to_filter_with_index = []
            product_ids = []
            index = 0
            for recent_product in res.get("products"):
                to_filter_with_index.append((index, recent_product.get("id")))
                product_ids.append(recent_product.get("id"))
                index += 1
            product_ids = request.env['product.product'].browse(product_ids)
            print("product_ids", product_ids)
            product_to_remove = product_ids.filtered(lambda product_id: not product_id.with_context(special_call=True)._is_variant_possible())
            print("product_to_remove", product_to_remove)
            index_to_remove = [index for index, product_id in to_filter_with_index if product_id in product_to_remove.ids]

            for index in sorted(index_to_remove, reverse=True):
                del res.get("products")[index]
        return res
