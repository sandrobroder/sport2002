from odoo.exceptions import ValidationError
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('image_1920')
    def get_image_field(self):
        for rec in self:
            if not rec.image_1920:
                image = False
                for var in rec.product_variant_ids:
                    if var.image_variant_1920:
                        image = var.image_variant_1920
                    else:
                        pass
                rec.image_1920 = image
