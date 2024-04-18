# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import _, api, exceptions, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('image_1920')
    def get_image_field(self):
        for rec in self:
            if not rec.image_1920:
                for var in rec.product_variant_ids:
                    if var.image_variant_1920:
                        rec.image_1920 = var.image_variant_1920
                if rec.image_1920 == '':
                    raise exceptions.Warning(
                        _('No se pudo obtener una imagen de las variantes.'))
