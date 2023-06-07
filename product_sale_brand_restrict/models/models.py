# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    enable_brand_restriction = fields.Boolean()


class ResPartner(models.Model):
    _inherit = "res.partner"

    restricted_brand_ids = fields.Many2many("product.brand.ept")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        if request.website and request.website.enable_brand_restriction:
            if product_id:
                product = self.env["product.product"].sudo().browse(product_id)
                partner_id = self.env.user.partner_id
                if product.product_brand_ept_id and partner_id.restricted_brand_ids:
                    if product.product_brand_ept_id.id in partner_id.restricted_brand_ids.ids:
                        raise UserError(
                            "Sorry, You are not allowed to buy the products of %s brand!" % product.product_brand_ept_id.name)
        return super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
