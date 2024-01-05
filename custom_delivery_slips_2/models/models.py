# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    shipping_carrier_id = fields.Selection([("1", "One"), ("2", "Two")])
    no_of_packages = fields.Integer()

