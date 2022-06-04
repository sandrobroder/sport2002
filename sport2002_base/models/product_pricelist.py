# -*- coding: utf-8 -*-
from odoo import fields, models
import json


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    see_with_tax = fields.Boolean(string="Tax in website")
