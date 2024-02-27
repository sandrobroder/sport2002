# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    auto_confirm_sale_order = fields.Boolean()


class Website(models.Model):
    _inherit = "website"

    auto_confirm_quotation = fields.Boolean()

