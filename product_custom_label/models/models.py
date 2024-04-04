# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[("3x7", "3 x 7"), ("3x7xprice", "3 x 7 with price")],
                                    ondelete={'3x7': 'set default', '3x7xprice': 'set default'})
