# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    block_automation = fields.Boolean('Block Automation')
