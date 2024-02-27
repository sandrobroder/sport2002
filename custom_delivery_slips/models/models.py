# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    shipping_carrier_id = fields.Selection([("1", "TXT"), ("2", "Mailboxes"), ("3", "Cliente"), ("4", "Correos"), ("5", "Mathias"), ("6", "Otros")])
    no_of_packages = fields.Integer()

