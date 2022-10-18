from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSale
from datetime import timedelta
import datetime
from odoo.http import request
from odoo import http, _
from odoo.tools.safe_eval import safe_eval


class SliderBuilder(WebsiteSale):

    # Render the product list
    @http.route(['/get-product-list'], type='json', auth="public", website=True)
    def get_product_listing(self, name=False, **kwargs):
        products = filters = error = error_msg = False
        limit = int(kwargs.get('limit'))

        if name:
            if name == 'new-arrival':
                products = self.new_arrival_products(20)
            elif name == 'best-seller':
                products = self.best_seller_products(20)
            elif name == 'product-discount':
                products = self.discounted_products('product', 20)
            elif name == 'product-category-discount':
                products = self.discounted_products('category', request.website.category_check().ids,
                                                    discount_policy='product', limit=20)
            elif name == 'custom-domain':
                filters = request.env['slider.filter'].sudo().search([('website_published', '=', True),
                                                                      ('filter_domain', '!=', False)])
            elif name == 'manual-configuration':
                products = request.env['product.template'].sudo().search([], limit=2)

            if (name == 'custom-domain' and not filters) or (name != 'custom-domain' and not products):
                error = True

        if error:
            error_msg = _("ERROR MESSAGE WILL BE DISPLAYED HERE")

        context = {'name': name, 'limit': limit, 'products': products, 'filters': filters, 'error': error,
                   'error_msg': error_msg}
        response = http.Response(template='emipro_theme_base.product_display_prod_template', qcontext=context)
        return {'template_data': response.render(), 'error': error, 'error_msg': error_msg}

    # Render the the selected products while edit the manual configuration slider
    @http.route('/get-products-of-slider', type='json', auth='public', website=True)
    def get_products_of_slider(self, **kw):
        product_ids = kw.get('item_ids')
        if product_ids:
            products = request.env['product.template'].browse(product_ids).filtered(lambda r: r.exists() and r.sale_ok and r.website_published and r.website_id.id in (False, request.website.id) and r.type in ['product', 'consu'])
            response = http.Response(template='emipro_theme_base.edit_product_template',
                                     qcontext={'products': products})
            return response.render()

    @http.route('/load-more-category-brand', type='json', auth='public', website=True)
    def load_more_category_brand(self, **kw):
        name = kw.get('name', False)
        loaded_items = int(kw.get('loaded_items', False))
        item_ids = self.get_item_ids(kw.get('item_ids', []), 'int')
        response = False
        items, items_count = self.get_category_brand(name=name) if loaded_items and name else False
        items = (items - items.filtered(lambda r: r.id not in item_ids)) + items.filtered(
            lambda r: r.id not in item_ids) if item_ids else items
        items = items[loaded_items:loaded_items + 20]
        if items:
            tmplt = request.env['ir.ui.view'].sudo().search(
                [('key', '=', 'emipro_theme_base.brand_category_configure_template')])
            if tmplt:
                response = http.Response(template='emipro_theme_base.list_items',
                                         qcontext={'items': items, 'name': name})
        return {'response': response.render() if response else False, 'items_count': items_count,
                'loaded_items': loaded_items + len(items) if items else loaded_items if loaded_items else 20}

    # Render Category or Brand and it's count
    def get_category_brand(self, name, item_ids=None):
        if name == 'category-slider':
            domain = [('website_id', 'in', [False, request.website.id]), ('image_1920', '!=', False)]
            if item_ids:
                domain.append(('id', 'in', item_ids))
            pub_categ_obj = request.env['product.public.category']
            items = pub_categ_obj.sudo().search(domain, order='id desc')
            items_count = pub_categ_obj.sudo().search_count([('website_id', 'in', [False, request.website.id]),
                                                             ('image_1920', '!=', False)])
        else:
            domain = [('website_id', 'in', [False, request.website.id]), ('logo', '!=', False),
                      ('website_published', '=', True)]
            if item_ids:
                domain.append(('id', 'in', item_ids))
            brand_obj = request.env['product.brand.ept']
            items = brand_obj.sudo().search(domain, order='id desc')
            items_count = brand_obj.sudo().search_count([('website_published', '=', True), ('logo', '!=', False),
                                                         ('website_id', 'in', [False, request.website.id])])
        return items, items_count

    # Render Slider Popup
    @http.route('/get-slider-builder-popup', type='json', auth='public', website=True)
    def get_brand_category_template(self, **kw):
        name = kw.get('name')
        exclude = kw.get('exclude', False)
        if name in ['category-slider', 'brand-slider']:
            tmplt = request.env['ir.ui.view'].sudo().search([('key', '=', 'emipro_theme_base.brand_category_configure_template')])
            if tmplt:
                item_ids = self.get_item_ids(kw.get('item_ids', []), 'int')
                items, items_count = self.get_category_brand(name, item_ids=item_ids)
                loaded_items = len(item_ids) if item_ids else 20
                slider_type = 'category' if name == 'category-slider' else 'brand'
                styles = request.env['slider.styles'].search([('slider_type', '=', slider_type),
                                                              ('style_template_key', '!=', False)])
                limit = int(kw.get('limit'))
                context = {'name': name, 'items': items[:20], 'items_count': items_count, 'limit': limit,
                           'styles': styles, 'exclude': exclude, 'loaded_items': loaded_items,
                           'available_slider_style': list(set(styles.mapped('slider_style')))}
                response = http.Response(template='emipro_theme_base.brand_category_configure_template',qcontext=context)
                return response.render()
        else:
            tmplt = request.env['ir.ui.view'].sudo().search([('key', '=', 'emipro_theme_base.product_configure_template')])
            if tmplt:
                filters = request.env['slider.filter'].sudo().search([('website_published', '=', True),
                                                                      ('filter_domain', '!=', False)])
                styles = request.env['slider.styles'].search([('slider_type', '=', 'product'),
                                                              ('style_template_key', '!=', False)])
                context = {'name': name, 'filters': filters, 'styles': styles, 'exclude': exclude,
                           'available_slider_style': list(set(styles.mapped('slider_style')))}
                response = http.Response(template='emipro_theme_base.product_configure_template', qcontext=context)
                return response.render()

    # Render Suggested Product
    @http.route('/get-suggested-products', type='json', auth='public', website=True)
    def get_suggested_products(self, **kw):
        tmplt = request.env['ir.ui.view'].sudo().search([('key', '=', 'emipro_theme_base.suggested_products')])
        if tmplt:
            key = kw.get('key')
            exclude_products = kw.get('exclude_products')
            website_domain = request.website.website_domain()
            website_domain += [('id', 'not in', exclude_products), ('sale_ok', '=', True), ('name', 'ilike', key),
                               ('type', 'in', ['product', 'consu']), ('website_published', '=', True)]
            products = request.env['product.template'].search(website_domain, limit=10)
            response = http.Response(template='emipro_theme_base.suggested_products', qcontext={'products': products})
            return response.render()

    # Render the category And brand slider
    @http.route(['/slider/category-brand-render'], type='json', auth="public", website=True)
    def category_brand_render(self, **kwargs):
        item_ids = self.get_item_ids(kwargs.get('item_ids', []), 'int')
        name = kwargs.get('name', False)
        if item_ids and name:
            limit = int(kwargs.get('limit', 10))
            sort_by = kwargs.get('sort_by', 'name asc')
            style = int(kwargs.get('style', False))

            if name == 'brand-slider':
                items = request.env['product.brand.ept'].search([('id', 'in', item_ids)], limit=limit, order=sort_by).filtered(lambda r: r.exists() and r.website_id.id in [False, request.website.id] and r.website_published and r.logo)
            else:
                items = request.env['product.public.category'].search([('id', 'in', item_ids)], limit=limit, order=sort_by).filtered(lambda r: r.exists() and r.image_1920 and r.website_id.id in [False, request.website.id])

            slider_style = request.env['slider.styles'].sudo().browse(style)
            if items and slider_style:
                display_product_count = kwargs.get('product_count', False) == '1'
                vals = {"items": items, 'display_product_count': display_product_count}
                template = request.website.sudo().theme_id.name + '.' + slider_style.style_template_key
                if request.env['ir.ui.view'].sudo().search([('key', '=', template)]):
                    response = http.Response(template=template, qcontext=vals)
                    return response.render()

        if request.env['ir.ui.view'].sudo().search([('key', '=', request.website.sudo().theme_id.name + '.' + 'slider_error_message')]):
            response = http.Response(template=request.website.sudo().theme_id.name + '.' + 'slider_error_message')
            return response.render()

    # Render The Product Slider
    @http.route(['/slider/render'], type='json', auth="public", website=True)
    def slider_data(self, **kwargs):
        name = kwargs.get('name', False)
        slider_style_template = int(kwargs.get('style', 0))
        theme_name = request.website.sudo().theme_id.name

        if name and slider_style_template:
            slider_style = request.env['slider.styles'].sudo().browse(slider_style_template)
            item_ids = self.get_item_ids(kwargs.get('item_ids', []), 'int')
            limit = int(kwargs.get('limit', 10))

            products = []
            if name == 'manual-configuration' and item_ids:
                domain = [('id', 'in', item_ids), ('sale_ok', '=', True), ('website_published', '=', True),
                          ('website_id', 'in', [False, request.website.id]), ('type', 'in', ['product', 'consu'])]
                products = request.env['product.template'].sudo().search(domain, limit=limit)
            elif name == 'new-arrival':
                products = self.new_arrival_products(limit)
            elif name == 'custom-domain':
                sort_by = kwargs.get('sort_by', 'name asc')
                products = self.custom_domain_products(item_ids, limit, sort_by)
            elif name == 'best-seller':
                products = self.best_seller_products(limit)
            elif name == 'product-discount':
                products = self.discounted_products('product', limit=limit)
            elif name == 'product-category-discount' and item_ids:
                discount_policy = kwargs.get('discount_policy', False)
                products = self.discounted_products('category', item_ids, discount_policy, limit)

            if products and slider_style:
                selected_ui_options = self.get_item_ids(kwargs.get('ui_options', []))
                q_context = {'option': selected_ui_options or [], 'filter_data': products[:limit]}
                template = f"{theme_name}.{slider_style.style_template_key}"
                if request.env['ir.ui.view'].sudo().search([('key', '=', template)]):
                    response = http.Response(template=template, qcontext=q_context)
                    return response.render()

        if request.env['ir.ui.view'].sudo().search([('key', '=', theme_name + '.' + 'slider_error_message')]):
            response = http.Response(template=theme_name + '.' + 'slider_error_message')
            return response.render()

    # Render the custom domain products
    def custom_domain_products(self, filter_id, limit=20, sort_by='name asc'):
        if filter_id:
            filter = request.env['slider.filter'].sudo().browse(filter_id[0])
            if filter and filter.website_published:
                domain = safe_eval(filter.filter_domain)
                domain += ['|', ('website_id', '=', None), ('website_id', '=', request.website.id),
                           ('website_published', '=', True), ('type', 'in', ['product', 'consu']), ('sale_ok', '=', True)]
                return request.env['product.template'].sudo().search(domain, limit=limit, order=sort_by)
        return False

    # Render the new arrival products
    def new_arrival_products(self, limit=10):
        domain = request.website.sale_product_domain()
        domain += ['|', ('website_id', '=', None), ('website_id', '=', request.website.id),
                   ('website_published', '=', True), ('type', 'in', ['product', 'consu'])]
        return request.env['product.template'].sudo().search(domain, limit=limit, order='id desc')

    # Render the best seller products
    def best_seller_products(self, limit=10):
        website_id = request.website.id
        query = f"""SELECT * FROM sale_report WHERE website_id={website_id} AND state in ('sale','done') AND 
        date BETWEEN '{datetime.datetime.today() - timedelta(30)}' and '{datetime.datetime.today()}'"""
        request.env.cr.execute(query)
        sale_report_ids = [x[0] for x in request.env.cr.fetchall()]
        products = request.env['sale.report'].sudo().browse(sale_report_ids).mapped('product_tmpl_id')
        products = products.search([('sale_ok', '=', True), ('website_published', '=', True),
                                    ('website_id', 'in', [False, website_id]), ('type', '!=', 'service')], limit=limit)
        return products

    # Return Category product or category discount product
    def discounted_products(self, applied_on=None, category_ids=None, discount_policy=None, limit=10):
        price_list = request.website.get_current_pricelist()
        today = datetime.datetime.today()
        pl_items = price_list.item_ids.filtered(lambda r: r.applied_on == '1_product' and
        ((not r.date_start or r.date_start <= today) and (not r.date_end or r.date_end > today)))
        domain = ['|', ('website_id', '=', False), ('website_id', '=', request.website.id),
                  ('website_published', '=', True), ('type', 'in', ['product', 'consu']), ('sale_ok', '=', True)]
        if applied_on == 'product':
            return pl_items.mapped('product_tmpl_id').search(domain, limit=limit)
        elif category_ids and applied_on == 'category' and discount_policy == 'discounts':
            domain.append(('public_categ_ids', 'in', category_ids))
            return pl_items.mapped('product_tmpl_id').search(domain, limit=limit)
        else:
            domain = request.website.sale_product_domain()
            domain += ['|', ('website_id', '=', False), ('website_id', '=', request.website.id),
                       ('website_published', '=', True), ('public_categ_ids', 'in', category_ids),
                       ('type', 'in', ['product', 'consu'])]
            return request.env['product.template'].sudo().search(domain, limit=limit)

    def get_item_ids(self, ids, type=None):
        item_ids = []
        if ids and isinstance(ids, str):
            item_ids = [int(i) if type and type == 'int' else i for i in ids.split(',')]
        elif ids:
            item_ids = [int(i) if type and type == 'int' else i for i in ids]
        return item_ids
