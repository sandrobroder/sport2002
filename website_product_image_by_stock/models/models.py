# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def set_product_template_image(self, offset=0, limit=100):
        product_tmpl_ids = self.env["product.template"].sudo().search(
            [("is_published", "=", True), ("type", "=", "product")], order="id", limit=limit, offset=offset)
        for product_template_id in product_tmpl_ids:
            available_variant = None
            for variant in product_template_id.product_variant_ids:
                qty_available = variant.qty_available
                if qty_available > 0 and variant.image_variant_128:
                    available_variant = variant
                    break
            if available_variant:
                product_template_id.image_1920 = available_variant.image_1920

    # def _get_image_holder(self):
    #     """Returns the holder of the image to use as default representation.
    #     If the product template has an image it is the product template,
    #     otherwise if the product has variants it is the first variant
    #
    #     :return: this product template or the first product variant
    #     :rtype: recordset of 'product.template' or recordset of 'product.product'
    #     """
    #     self.ensure_one()
    #     variant = self.env['product.product'].browse(self._get_first_possible_variant_id())
    #     website = self.env['website'].get_current_website()
    #
    #     if variant:
    #         qty_available = variant.with_context(warehouse=website._get_warehouse_available()).qty_available
    #         if qty_available > 0 and variant.image_variant_128:
    #             return variant
    #         else:
    #             for variant in self.product_variant_ids:
    #                 qty_available = variant.with_context(warehouse=website._get_warehouse_available()).qty_available
    #                 if qty_available > 0 and variant.image_variant_128:
    #                     return variant
    #     # if the variant has no image anyway, spare some queries by using template
    #     return self
