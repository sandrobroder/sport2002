# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)


class PrintProductLabelLine(models.TransientModel):
    _name = "print.product.label.line"
    _description = 'Line with Product Label Data'

    selected = fields.Boolean(
        string='Print',
        compute='_compute_selected',
        readonly=True,
    )
    wizard_id = fields.Many2one('print.product.label', 'Print Wizard')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    barcode = fields.Char('Barcode', related='product_id.barcode')
    qty_initial = fields.Integer('Initial Qty', default=1)
    qty = fields.Integer('Label Qty', default=1)
    price = fields.Float('Precio',compute='_compute_price',store=True)

    @api.depends('product_id')
    def _compute_price(self):
        for record in self:
            record.price= float()
            product_pricelist_item_obj=self.env['product.pricelist.item']
            if record.product_id:
                user_id = self.env['res.users'].browse(record._uid)
                combination_info = record.with_context(website_id=2).product_id.product_tmpl_id._get_combination_info()

                if user_id.login == 'info@skaterootsbcn.com':
                    combination_info = record.with_context(website_id=2).product_id.product_tmpl_id._get_combination_info()

                record.price = combination_info['price']





    @api.depends('qty')
    def _compute_selected(self):
        for record in self:
            if record.qty > 0:
                record.update({'selected': True})
            else:
                record.update({'selected': False})

    def action_plus_qty(self):
        for record in self:
            record.update({'qty': record.qty + 1})

    def action_minus_qty(self):
        for record in self:
            if record.qty > 0:
                record.update({'qty': record.qty - 1})
