# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   If not, see <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import http, tools,api, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute
from odoo.addons.http_routing.models.ir_http import slug

from odoo.addons.website.controllers.main import QueryURL
from odoo import http
import logging

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(['/lazy/load'], type='json', auth="public", methods=['POST'], website=True)
    def lazy_load(self, **post):
        category = None
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        category= int(post.get("category_selected"))
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category
        page = post.get('page') or 1
        search = post.get("search") or ''
        ppg = 8
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        if post.get('attributes'):
            attrib_list = ["-".join(map(str, x)) for x in eval(post.get('attributes'))]
        else:
            attrib_list = request.httprequest.args.getlist('attrib')

        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template']

        search_categories = False
        if search:
            categories = Product.search(domain).mapped('public_categ_ids')
            search_categories = Category.search([('id', 'parent_of', categories.ids)] + request.website.website_domain())
            categs = search_categories.filtered(lambda c: not c.parent_id)
        else:
            categs = Category.search([('parent_id', '=', False)] + request.website.website_domain())

        parent_category_ids = []
        if category:
            url = "/shop/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        offset = post.get('offset') or pager['offset']
        products = Product.search(domain, limit=ppg, offset=offset, order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.value_ids', '!=', False), ('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'search_categories_ids': search_categories and search_categories.ids,
        }
        if category:
            values['main_object'] = category
        if post.get('view') == 'list':
            data_grid = request.env['ir.ui.view']._render_template("website_lazy_loading.wk_lazy_list_product_item", values)
        else:
            data_grid = request.env['ir.ui.view']._render_template("website_lazy_loading.wk_lazy_product_item", values)
        return {'count': len(products), 'data_grid': data_grid}
