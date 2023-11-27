# -*- coding: utf-8 -*-
import json

from lxml import etree

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = "res.users"

    warehouse_id = fields.Many2one("stock.warehouse")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    on_hand_qty_wh_one = fields.Float()
    on_hand_qty_wh_two = fields.Float()
    allowed_warehouse_one_id = fields.Many2one("stock.warehouse", compute='_compute_quantities_on_hand')
    allowed_warehouse_two_id = fields.Many2one("stock.warehouse", compute='_compute_quantities_on_hand')

    @api.depends(
        'product_variant_ids',
        'product_variant_ids.stock_move_ids.product_qty',
        'product_variant_ids.stock_move_ids.state',
    )
    @api.depends_context('company', 'location', 'warehouse')
    def _compute_quantities_on_hand(self):
        # TDE FIXME: why not using directly the function fields ?
        if self.env.user.warehouse_id:
            variants_available = self.mapped('product_variant_ids').with_context(
                warehouse=self.env.user.warehouse_id.id)._compute_quantities_dict(self._context.get('lot_id'),
                                                                                  self._context.get('owner_id'),
                                                                                  self._context.get('package_id'),
                                                                                  self._context.get('from_date'),
                                                                                  self._context.get('to_date'))
            for template in self:
                qty_available = 0
                for p in template.product_variant_ids:
                    qty_available += variants_available[p.id]["qty_available"]
                template.on_hand_qty_wh_one = qty_available
                template.on_hand_qty_wh_two = 0
                template.allowed_warehouse_one_id = self.env.user.warehouse_id.id
                template.allowed_warehouse_two_id = False
        else:
            all_warehouse_ids = self.env["stock.warehouse"].search([], limit=2)
            if len(all_warehouse_ids) == 2:
                variants_available = self.mapped('product_variant_ids').with_context(
                    warehouse=all_warehouse_ids[0].id)._compute_quantities_dict(self._context.get('lot_id'),
                                                                                self._context.get('owner_id'),
                                                                                self._context.get('package_id'),
                                                                                self._context.get('from_date'),
                                                                                self._context.get('to_date'))
                for template in self:
                    qty_available = 0
                    for p in template.product_variant_ids:
                        qty_available += variants_available[p.id]["qty_available"]
                    template.on_hand_qty_wh_one = qty_available
                    template.allowed_warehouse_one_id = all_warehouse_ids[0].id

                variants_available = self.mapped('product_variant_ids').with_context(
                    warehouse=all_warehouse_ids[1].id)._compute_quantities_dict(self._context.get('lot_id'),
                                                                                self._context.get('owner_id'),
                                                                                self._context.get('package_id'),
                                                                                self._context.get('from_date'),
                                                                                self._context.get('to_date'))

                for template in self:
                    qty_available = 0
                    for p in template.product_variant_ids:
                        qty_available += variants_available[p.id]["qty_available"]
                    template.on_hand_qty_wh_two = qty_available
                    template.allowed_warehouse_two_id = all_warehouse_ids[1].id
            else:
                for template in self:
                    template.on_hand_qty_wh_one = 0
                    template.on_hand_qty_wh_two = 0
                    template.allowed_warehouse_one_id = False
                    template.allowed_warehouse_two_id = False

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductTemplate, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                           submenu=submenu)
        if view_type == 'tree' and res.get('toolbar', False):
            # tree_view_id_1 = self.env['ir.model.data'].xmlid_to_res_id('product.product_product_tree_view')
            tree_view_id_2 = self.env['ir.model.data'].xmlid_to_res_id('product.product_template_tree_view')
            # print("res.get('view_id')", res.get('view_id'), [tree_view_id_1, tree_view_id_2])
            if res.get('view_id') in [tree_view_id_2]:
                tree = etree.XML(res['arch'])
                if self.env.user.warehouse_id:
                    for node in tree.xpath("//field[@name='on_hand_qty_wh_one']"):
                        node.set('string', str(self.env.user.warehouse_id.name) + " On-Hand Qty")
                    for node in tree.xpath("//field[@name='on_hand_qty_wh_two']"):
                        modifiers = json.loads(node.get("modifiers"))
                        modifiers['column_invisible'] = True
                        node.set("modifiers", json.dumps(modifiers))
                    res['arch'] = etree.tostring(tree, encoding='unicode')
                else:
                    all_warehouse_ids = self.env["stock.warehouse"].search([], limit=2)
                    if len(all_warehouse_ids) == 2:
                        for node in tree.xpath("//field[@name='on_hand_qty_wh_one']"):
                            node.set('string', str(all_warehouse_ids[0].name) + " On-Hand Qty")
                        for node in tree.xpath("//field[@name='on_hand_qty_wh_two']"):
                            node.set('string', str(all_warehouse_ids[1].name) + " On-Hand Qty")
                        res['arch'] = etree.tostring(tree, encoding='unicode')
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    on_hand_qty_wh_one = fields.Float(compute='_compute_quantities_on_hand')
    on_hand_qty_wh_two = fields.Float(compute='_compute_quantities_on_hand')
    allowed_warehouse_one_id = fields.Many2one("stock.warehouse", compute='_compute_quantities_on_hand')
    allowed_warehouse_two_id = fields.Many2one("stock.warehouse", compute='_compute_quantities_on_hand')

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    @api.depends_context(
        'lot_id', 'owner_id', 'package_id', 'from_date', 'to_date',
        'location', 'warehouse',
    )
    def _compute_quantities_on_hand(self):
        products = self.filtered(lambda p: p.type != 'service')
        if self.env.user.warehouse_id:
            res = products.with_context(warehouse=self.env.user.warehouse_id.id)._compute_quantities_dict(
                self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'),
                self._context.get('from_date'), self._context.get('to_date'))
            for product in products:
                product.on_hand_qty_wh_one = res[product.id]['qty_available']
                product.on_hand_qty_wh_two = 0
                product.allowed_warehouse_one_id = self.env.user.warehouse_id.id
                product.allowed_warehouse_two_id = False

            # Services need to be set with 0.0 for all quantities
            services = self - products
            services.on_hand_qty_wh_one = 0.0
            services.on_hand_qty_wh_two = 0.0
            services.allowed_warehouse_one_id = False
            services.allowed_warehouse_two_id = False
        else:
            all_warehouse_ids = self.env["stock.warehouse"].search([], limit=2)
            if all_warehouse_ids and len(all_warehouse_ids) == 2:
                res = products.with_context(warehouse=all_warehouse_ids[0].id)._compute_quantities_dict(
                    self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'),
                    self._context.get('from_date'), self._context.get('to_date'))
                for product in products:
                    product.on_hand_qty_wh_one = res[product.id]['qty_available']
                    product.allowed_warehouse_one_id = all_warehouse_ids[0].id

                res = products.with_context(warehouse=all_warehouse_ids[1].id)._compute_quantities_dict(
                    self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'),
                    self._context.get('from_date'), self._context.get('to_date'))
                for product in products:
                    product.on_hand_qty_wh_two = res[product.id]['qty_available']
                    product.allowed_warehouse_two_id = all_warehouse_ids[1].id

                # Services need to be set with 0.0 for all quantities
                services = self - products
                services.on_hand_qty_wh_one = 0.0
                services.on_hand_qty_wh_two = 0.0
                services.allowed_warehouse_one_id = False
                services.allowed_warehouse_two_id = False
            else:
                self.on_hand_qty_wh_one = 0.0
                self.on_hand_qty_wh_two = 0.0
                self.allowed_warehouse_one_id = False
                self.allowed_warehouse_two_id = False

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductProduct, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                          submenu=submenu)
        if view_type == 'tree' and res.get('toolbar', False):
            tree_view_id_1 = self.env['ir.model.data'].xmlid_to_res_id('product.product_product_tree_view')
            # tree_view_id_2 = self.env['ir.model.data'].xmlid_to_res_id('product.product_template_tree_view')
            # print("res.get('view_id')", res.get('view_id'), [tree_view_id_1, tree_view_id_2])
            if res.get('view_id') in [tree_view_id_1]:
                tree = etree.XML(res['arch'])
                if self.env.user.warehouse_id:
                    for node in tree.xpath("//field[@name='on_hand_qty_wh_one']"):
                        node.set('string', str(self.env.user.warehouse_id.name) + " On-Hand Qty")
                    for node in tree.xpath("//field[@name='on_hand_qty_wh_two']"):
                        modifiers = json.loads(node.get("modifiers"))
                        modifiers['column_invisible'] = True
                        node.set("modifiers", json.dumps(modifiers))
                    res['arch'] = etree.tostring(tree, encoding='unicode')
                else:
                    all_warehouse_ids = self.env["stock.warehouse"].search([], limit=2)
                    if len(all_warehouse_ids) == 2:
                        for node in tree.xpath("//field[@name='on_hand_qty_wh_one']"):
                            node.set('string', str(all_warehouse_ids[0].name) + " On-Hand Qty")
                        for node in tree.xpath("//field[@name='on_hand_qty_wh_two']"):
                            node.set('string', str(all_warehouse_ids[1].name) + " On-Hand Qty")
                        res['arch'] = etree.tostring(tree, encoding='unicode')
        return res
