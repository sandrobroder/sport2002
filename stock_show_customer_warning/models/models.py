# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    customer_warning_message = fields.Text(compute="compute_customer_warming")

    def compute_customer_warming(self):
        for rec in self:
            if rec.partner_id and rec.partner_id.sale_warn == "warning" and rec.partner_id.sale_warn_msg:
                rec.customer_warning_message = rec.partner_id.sale_warn_msg
            else:
                rec.customer_warning_message = False

    def _get_fields_stock_barcode(self):
        field = super()._get_fields_stock_barcode()
        return field.append("customer_warning_message")
