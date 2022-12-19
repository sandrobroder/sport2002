# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LabelQtyWizard(models.TransientModel):
    _name = "label.qty.wizard"

    qty = fields.Integer(default=1)
    order_id = fields.Many2one("sale.order")

    def print_label(self):
        self.ensure_one()
        if self.qty and self.order_id:
            return self.env.ref('sale_order_label.action_report_sale_order_label').report_action(self)
