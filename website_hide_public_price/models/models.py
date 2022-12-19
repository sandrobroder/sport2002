# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.onchange('b2b_hide_details')
    def _onchange_b2b_hide_details(self):
        if self.b2b_hide_details:
            self.b2b_hide_add_to_cart = True
        else:
            self.b2b_hide_add_to_cart = False
            self.b2b_hide_price = False
            self.is_b2b_message = False
