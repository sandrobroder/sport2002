# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('image_variant_1920')
    def get_image_field(self):
        for rec in self:
            image = ''
            for var in rec.product_tmpl_id.product_variant_ids:
                if var.image_variant_1920:
                    image = var.image_variant_1920
            if not rec.product_tmpl_id.image_1920:
                rec.product_tmpl_id.image_1920 = image
