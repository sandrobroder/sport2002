# -*- coding: utf-8 -*-
import logging

from odoo import fields, models
import json
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    without_automatism = fields.Boolean(string="Without Automatism")
    
    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        """Override for website, where we want to:
            - take the website pricelist if no pricelist is set
            - apply the b2b/b2c setting to the result

        This will work when adding website_id to the context, which is done
        automatically when called from routes with website=True.
        """
        self.ensure_one()

        current_website = False

        if self.env.context.get('website_id'):
            current_website = self.env['website'].get_current_website()
            if not pricelist:
                pricelist = current_website.get_current_pricelist()

        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if self.env.context.get('website_id'):
            partner = self.env.user.partner_id
            company_id = current_website.company_id
            product = self.env['product.product'].browse(combination_info['product_id']) or self

            tax_display = self.user_has_groups(
                'account.group_show_line_subtotals_tax_excluded') and 'total_excluded' or 'total_included'

            if pricelist.see_with_tax:
                tax_display = "total_included"
            fpos = self.env['account.fiscal.position'].sudo().get_fiscal_position(partner.id)
            taxes = fpos.map_tax(product.sudo().taxes_id.filtered(lambda x: x.company_id == company_id), product,
                                 partner)
            _logger.error("***********************************************")
            _logger.error("****************** CALCULO TARIFA *****************************")
            _logger.error("***********************************************")
            _logger.error("Tax display:")
            _logger.error(tax_display)
            _logger.error("Tarifa:")
            _logger.error(pricelist)
            _logger.error(pricelist.name)
            # Añado esta linea para que obtenga de nuevo el precio bi del producto ya que sin esta linea, duplica
            # los impuestos por que pasa por la funcion 2 veces.Meter el precio de nuevo nos ayuda a restaurar el
            # funcionamiento correcto
#             list_price = product.price_compute('list_price')[product.id]
#             _logger.error("List Price")
#             _logger.error(list_price)
# #             price = product.price if pricelist else list_price
#             _logger.error("Precio")
#             _logger.error(price)

            # The list_price is always the price of one.
            quantity_1 = 1
#             combination_info['price'] = self.env['account.tax']._fix_tax_included_price_company(
#                 price,
#                 product.sudo().taxes_id,
#                 taxes, company_id)
            price = taxes.compute_all(combination_info['price'], pricelist.currency_id, quantity_1, product, partner)[
                tax_display]
            if pricelist.discount_policy == 'without_discount':
                combination_info['list_price'] = self.env['account.tax']._fix_tax_included_price_company(
                    combination_info['list_price'], product.sudo().taxes_id, taxes, company_id)
                list_price = \
                    taxes.compute_all(combination_info['list_price'], pricelist.currency_id, quantity_1, product,
                                      partner)[
                        tax_display]
            else:
                list_price = price
            has_discounted_price = pricelist.currency_id.compare_amounts(list_price, price) == 1

            combination_info.update(
                price=price,
                list_price=list_price,
                has_discounted_price=has_discounted_price,
            )
            
            _logger.error("///////// COMBINACION ///////////")
            _logger.error(combination_info)

        return combination_info
