# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


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
            record.price=Float()
            product_pricelist_item_obj=self.env['product.pricelist.item']
            if record.product_id:
                user_id = self.env['res.users'].browse(record._uid.id)
                if user_id.login == 'info@skaterootsbcn.com':
                    pricelist_id = product_pricelist_item_obj.search([('product_id','=',record.product_id.id),('pricelist_id','=',21870)],limit=1)
                    if pricelist_id:
                        rec.price = pricelist_id.fixed_price
                else:
                    rec.price = rec.product_id.list_price




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
