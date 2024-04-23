# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super()._get_combination_info(combination, product_id, add_qty,pricelist, parent_combination,
                                                         only_template)
        if self.env.context.get('website_id'):
            product = self.env['product.product'].browse(combination_info['product_id']) or self
            if product.default_code:
                combination_info.update(
                    internal_ref=product.barcode,
                )
        return combination_info


class Website(models.Model):
    _inherit = "website"

    show_product_barcode = fields.Boolean(string='Show Product Barcode in website')
