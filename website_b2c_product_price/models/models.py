# -*- coding: utf-8 -*-

from itertools import chain

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import inspect


class ProductTemplate(models.Model):
    _inherit = "product.template"

    customer_list_price = fields.Float(string="Customer Sales Price(Tax Inc.)", digits='Product Price')
    product_price_to_show = fields.Selection(
        [("sales_price", "Sales Price"), ("price_with_tax", "Sales Price(Tax Inc.)")],
        compute="compute_which_price_to_show")
    description_product = fields.Text()

    def compute_which_price_to_show(self):
        for rec in self:
            if self.env.user.product_price_to_show == "sales_price":
                rec.product_price_to_show = "sales_price"
            elif self.env.user.product_price_to_show == "price_with_tax":
                rec.product_price_to_show = "price_with_tax"
            else:
                rec.product_price_to_show = False

    def open_pricelist_rules(self):
        self.ensure_one()
        domain = ['|',
                  ('product_tmpl_id', '=', self.id),
                  ('product_id', 'in', self.product_variant_ids.ids)]
        return {
            'name': _('Price Rules'),
            'view_mode': 'tree,form',
            # 'views': [(self.env.ref('product.product_pricelist_item_tree_view_from_product').id, 'tree'), (False, 'form')],
            'res_model': 'product.pricelist.item',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'context': {
                'default_product_tmpl_id': self.id,
                'default_applied_on': '1_product',
                'product_without_variants': self.product_variant_count == 1,
            },
        }

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)
        if pricelist and pricelist.use_b2c_price and self.customer_list_price:
            combination_info["list_price"] = self.customer_list_price
            has_discounted_price = pricelist.currency_id.compare_amounts(self.customer_list_price,
                                                                         combination_info["price"]) == 1
            combination_info['has_discounted_price'] = has_discounted_price
        return combination_info


class PriductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _compute_base_price(self, product, quantity, uom, date, target_currency):
        """ Compute the base price for a given rule

        :param product: recordset of product (product.product/product.template)
        :param float qty: quantity of products requested (in given uom)
        :param uom: unit of measure (uom.uom record)
        :param datetime date: date to use for price computation and currency conversions
        :param target_currency: pricelist currency

        :returns: base price, expressed in provided pricelist currency
        :rtype: float
        """
        target_currency.ensure_one()
        if self.pricelist_id.use_b2c_price:
            rule_base = "customer_list_price"
        else:
            rule_base = self.base or 'list_price'
        if rule_base == 'pricelist' and self.base_pricelist_id:
            price = self.base_pricelist_id._get_product_price(product, quantity, uom, date)
            src_currency = self.base_pricelist_id.currency_id
        elif rule_base == "standard_price":
            src_currency = product.cost_currency_id
            price = product.price_compute(rule_base, uom=uom, date=date)[product.id]
        else:  # list_price
            src_currency = product.currency_id
            price = product.price_compute(rule_base, uom=uom, date=date)[product.id]

        if src_currency != target_currency:
            price = src_currency._convert(price, target_currency, self.env.company, date, round=False)

        return price


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    use_b2c_price = fields.Boolean()

    # def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
    #     """ Low-level method - Mono pricelist, multi products
    #     Returns: dict{product_id: (price, suitable_rule) for the given pricelist}
    #
    #     Date in context can be a date, datetime, ...
    #
    #         :param products_qty_partner: list of typles products, quantity, partner
    #         :param datetime date: validity date
    #         :param ID uom_id: intermediate unit of measure
    #     """
    #     self.ensure_one()
    #     if not date:
    #         date = self._context.get('date') or fields.Datetime.now()
    #     if not uom_id and self._context.get('uom'):
    #         uom_id = self._context['uom']
    #     if uom_id:
    #         # rebrowse with uom if given
    #         products = [item[0].with_context(uom=uom_id) for item in products_qty_partner]
    #         products_qty_partner = [(products[index], data_struct[1], data_struct[2]) for index, data_struct in
    #                                 enumerate(products_qty_partner)]
    #     else:
    #         products = [item[0] for item in products_qty_partner]
    #
    #     if not products:
    #         return {}
    #
    #     categ_ids = {}
    #     for p in products:
    #         categ = p.categ_id
    #         while categ:
    #             categ_ids[categ.id] = True
    #             categ = categ.parent_id
    #     categ_ids = list(categ_ids)
    #
    #     is_product_template = products[0]._name == "product.template"
    #     if is_product_template:
    #         prod_tmpl_ids = [tmpl.id for tmpl in products]
    #         # all variants of all products
    #         prod_ids = [p.id for p in
    #                     list(chain.from_iterable([t.product_variant_ids for t in products]))]
    #     else:
    #         prod_ids = [product.id for product in products]
    #         prod_tmpl_ids = [product.product_tmpl_id.id for product in products]
    #
    #     items = self._compute_price_rule_get_items(products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids,
    #                                                categ_ids)
    #
    #     results = {}
    #     for product, qty, partner in products_qty_partner:
    #         results[product.id] = 0.0
    #         suitable_rule = False
    #
    #         # Final unit price is computed according to `qty` in the `qty_uom_id` UoM.
    #         # An intermediary unit price may be computed according to a different UoM, in
    #         # which case the price_uom_id contains that UoM.
    #         # The final price will be converted to match `qty_uom_id`.
    #         qty_uom_id = self._context.get('uom') or product.uom_id.id
    #         qty_in_product_uom = qty
    #         if qty_uom_id != product.uom_id.id:
    #             try:
    #                 qty_in_product_uom = self.env['uom.uom'].browse([self._context['uom']])._compute_quantity(qty,
    #                                                                                                           product.uom_id)
    #             except UserError:
    #                 # Ignored - incompatible UoM in context, use default product UoM
    #                 pass
    #
    #         # if Public user try to access standard price from website sale, need to call price_compute.
    #         # TDE SURPRISE: product can actually be a template
    #         if self.use_b2c_price:
    #             price = product.price_compute('customer_list_price')[product.id]
    #         else:
    #             price = product.price_compute('list_price')[product.id]
    #
    #         price_uom = self.env['uom.uom'].browse([qty_uom_id])
    #         for rule in items:
    #             if rule.min_quantity and qty_in_product_uom < rule.min_quantity:
    #                 continue
    #             if is_product_template:
    #                 if rule.product_tmpl_id and product.id != rule.product_tmpl_id.id:
    #                     continue
    #                 if rule.product_id and not (
    #                         product.product_variant_count == 1 and product.product_variant_id.id == rule.product_id.id):
    #                     # product rule acceptable on template if has only one variant
    #                     continue
    #             else:
    #                 if rule.product_tmpl_id and product.product_tmpl_id.id != rule.product_tmpl_id.id:
    #                     continue
    #                 if rule.product_id and product.id != rule.product_id.id:
    #                     continue
    #
    #             if rule.categ_id:
    #                 cat = product.categ_id
    #                 while cat:
    #                     if cat.id == rule.categ_id.id:
    #                         break
    #                     cat = cat.parent_id
    #                 if not cat:
    #                     continue
    #
    #             if rule.base == 'pricelist' and rule.base_pricelist_id:
    #                 price_tmp = \
    #                     rule.base_pricelist_id._compute_price_rule([(product, qty, partner)], date, uom_id)[product.id][
    #                         0]  # TDE: 0 = price, 1 = rule
    #                 price = rule.base_pricelist_id.currency_id._convert(price_tmp, self.currency_id, self.env.company,
    #                                                                     date, round=False)
    #             else:
    #                 # if base option is public price take sale price else cost price of product
    #                 # price_compute returns the price in the context UoM, i.e. qty_uom_id
    #                 if self.use_b2c_price:
    #                     price = product.price_compute('customer_list_price')[product.id]
    #                 else:
    #                     price = product.price_compute(rule.base)[product.id]
    #
    #             if price is not False:
    #                 # pass the date through the context for further currency conversions
    #                 rule_with_date_context = rule.with_context(date=date)
    #                 price = rule_with_date_context._compute_price(price, price_uom, product, quantity=qty,
    #                                                               partner=partner)
    #                 suitable_rule = rule
    #             break
    #         # Final price conversion into pricelist currency
    #         if suitable_rule and suitable_rule.compute_price != 'fixed' and suitable_rule.base != 'pricelist':
    #             if suitable_rule.base == 'standard_price':
    #                 cur = product.cost_currency_id
    #             else:
    #                 cur = product.currency_id
    #             price = cur._convert(price, self.currency_id, self.env.company, date, round=False)
    #
    #         if not suitable_rule:
    #             cur = product.currency_id
    #             price = cur._convert(price, self.currency_id, self.env.company, date, round=False)
    #
    #         results[product.id] = (price, suitable_rule and suitable_rule.id or False)
    #     return results


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'company_id')
    def _compute_tax_id(self):
        super(SaleOrderLine, self)._compute_tax_id()
        for line in self:
            if line.tax_id and line.order_id.pricelist_id.use_b2c_price:
                tax_id = self.env["account.tax"].search([("is_b2c_tax", "=", True), ("type_tax_use", "=", "sale")])
                if tax_id:
                    line.tax_id = tax_id[0].ids
    #

    # @api.depends('product_id', 'company_id')
    # def _compute_tax_id(self):
    #     taxes_by_product_company = defaultdict(lambda: self.env['account.tax'])
    #     lines_by_company = defaultdict(lambda: self.env['sale.order.line'])
    #     cached_taxes = {}
    #     for line in self:
    #         lines_by_company[line.company_id] += line
    #     for product in self.product_id:
    #         for tax in product.taxes_id:
    #             taxes_by_product_company[(product, tax.company_id)] += tax
    #     for company, lines in lines_by_company.items():
    #         for line in lines.with_company(company):
    #             taxes = taxes_by_product_company[(line.product_id, company)]
    #             if not line.product_id or not taxes:
    #                 # Nothing to map
    #                 line.tax_id = False
    #                 continue
    #             fiscal_position = line.order_id.fiscal_position_id
    #             cache_key = (fiscal_position.id, company.id, tuple(taxes.ids))
    #             if cache_key in cached_taxes:
    #                 result = cached_taxes[cache_key]
    #             else:
    #                 result = fiscal_position.map_tax(taxes)
    #                 cached_taxes[cache_key] = result
    #             # If company_id is set, always filter taxes by the company
    #             line.tax_id = result


class AccountTax(models.Model):
    _inherit = "account.tax"

    is_b2c_tax = fields.Boolean()


class ResUsers(models.Model):
    _inherit = "res.users"

    product_price_to_show = fields.Selection(
        [("sales_price", "Sales Price"), ("price_with_tax", "Sales Price(Tax Inc.)")])


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('customer_list_price')
        return result

    def _loader_params_product_pricelist(self):
        result = super()._loader_params_product_pricelist()
        result['search_params']['fields'].append('use_b2c_price')
        return result


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        print("vals_list", vals_list)
        lines = super().create(vals_list)

        for line in lines:
            if line.tax_ids and line.order_id.pricelist_id.use_b2c_price:
                tax_id = self.env["account.tax"].search([("is_b2c_tax", "=", True), ("type_tax_use", "=", "sale")])
                if tax_id:
                    line.tax_ids = tax_id[0].ids
                # line.tax_ids = False
            # if "order_id" in vals and "tax_ids" in vals:
        lines._onchange_amount_line_all()
        return lines
