# -*- coding: utf-8 -*-
"""This file is used for create and inherit the core controllers"""
import datetime
import logging
import json
import ast
from collections import defaultdict
from odoo import http, fields, _
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as Home
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.sale.controllers.variant import VariantController
from odoo.addons.sale.controllers.portal import CustomerPortal
from itertools import product as cartesian_product
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):
    @http.route()
    def account(self, redirect=None, **post):
        """ display only allowed countries in user address page from website portal """
        res = super(CustomerPortal, self).account(redirect=redirect, **post)
        countries = res.qcontext.get('countries', False)
        if countries and request.website.allow_countries == 'selected':
            updated_countries = request.website.country_group_id.country_ids + request.website.default_country_id + request.env.user.partner_id.country_id
            res.qcontext['countries'] = updated_countries
        return res


class WebsiteSaleExt(WebsiteSale):

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        # No limit because attributes are obtained from complete product list
        product_count, details, fuzzy_search_term = website._search_with_fuzzy("products_only",
                                                                               search,
                                                                               limit=None,
                                                                               order=self._get_search_order(
                                                                                   post),
                                                                               options=options)
        search_result = details[0].get('results', request.env['product.template']).with_context(
            bin_size=True)
        if attrib_set:
            # Attributes value per attribute
            attribute_values = request.env['product.attribute.value'].browse(attrib_set)
            values_per_attribute = defaultdict(lambda: request.env['product.attribute.value'])
            # In case we have only one value per attribute we can check for a combination using those attributes directly
            multi_value_attribute = False
            if attribute_values.pav_attribute_line_ids:
                for value in attribute_values:
                    if value.pav_attribute_line_ids:
                        values_per_attribute[value.attribute_id] |= value
                        if len(values_per_attribute[value.attribute_id]) > 1:
                            multi_value_attribute = True

            is_brand_filter_applied = False
            brand_attrib_values = [[int(x) for x in v.split("-")] for v in post.get('attrib') if v]
            for value in brand_attrib_values:
                ids = []
                if value[0] == 0:
                    is_brand_filter_applied = True
                    ids.append(value[1])
                if ids:
                    ctx = request.env.context.copy()
                    ctx.update({'is_brands_attr': ids})
                    request.env.context = ctx

            def filter_template(template, attribute_values_list):
                # Transform product.attribute.value to product.template.attribute.value
                attribute_value_to_ptav = dict()
                for ptav in template.attribute_line_ids.product_template_value_ids:
                    attribute_value_to_ptav[ptav.product_attribute_value_id] = ptav.id
                possible_combinations = False
                for attribute_values in attribute_values_list:
                    ptavs = request.env['product.template.attribute.value'].browse(
                        [attribute_value_to_ptav[val] for val in attribute_values if
                         val in attribute_value_to_ptav])
                    if len(ptavs) < len(attribute_values) and not is_brand_filter_applied:
                        # In this case the template is not compatible with this specific combination
                        continue
                    if len(ptavs) == len(
                            template.attribute_line_ids) and not is_brand_filter_applied:
                        if template._is_combination_possible(ptavs):
                            return True
                    elif len(ptavs) < len(template.attribute_line_ids):
                        if len(attribute_values_list) == 1:
                            if any(template._get_possible_combinations(necessary_values=ptavs)):
                                return True
                        if not possible_combinations:
                            possible_combinations = template._get_possible_combinations()
                        if any(len(ptavs & combination) == len(ptavs) for combination in
                               possible_combinations):
                            return True
                    elif is_brand_filter_applied:
                        return True
                return False

            # If multi_value_attribute is False we know that we have our final combination (or at least a subset of it)
            if not multi_value_attribute:
                possible_attrib_values_list = [attribute_values]
            else:
                # Cartesian product from dict keys and values
                possible_attrib_values_list = [
                    request.env['product.attribute.value'].browse([v.id for v in values]) for values
                    in cartesian_product(*values_per_attribute.values())]
            # if not is_brand_filter_applied:
            search_result = search_result.filtered(
                lambda tmpl: filter_template(tmpl, possible_attrib_values_list))

        brand = int(post.get('brand', False))
        if brand and search_result:
            search_result = search_result.filtered(lambda l: l.product_brand_id.id == brand)

        return fuzzy_search_term, product_count, search_result

    @http.route(['/shop',
                 '/shop/page/<int:page>',
                 '/shop/category/<model("product.public.category"):category>',
                 '/shop/category/<model("product.public.category"):category>/page/<int:page>',
                 '/shop/brands/<model("product.brand"):brand>',
                 '/shop/brands/<model("product.brand"):brand>/page/<int:page>', ], type='http',
                auth="public",
                website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False,
             **post):

        website = request.env['website'].get_current_website()
        ppr = http.request.env['website'].get_current_website().shop_ppr or 4
        ppg = http.request.env['website'].get_current_website().shop_ppg or 20

        attrib_list = request.httprequest.args.getlist('attrib')
        if not attrib_list:
            attrib_list += request.httprequest.args.getlist('attrib[]')
            new_args = request.httprequest.args.copy()
            new_args.update({'attrib': attrib_list})
            request.httprequest.args = new_args

        res = super(WebsiteSaleExt, self).shop(page=page, category=category, search=search,
                                               min_price=min_price,
                                               max_price=max_price, ppg=ppg, **post)

        bins = TableCompute().process(res.qcontext.get('products'), ppg, ppr)

        if post.get('brand', False):
            url = "/shop/brands/%s" % slug(post.get('brand', False))
            product_count = len(request.env['product.template'].search(
                [('sale_ok', '=', True), ('website_id', 'in', (False, request.website.id)),
                 ('product_brand_id', '=', post.get('brand', False).id), ]))

            pager = website.pager(url=url, total=product_count, page=page, step=ppg, scope=7,
                                  url_args=None)
            res.qcontext.update(
                {'pager': pager, 'products': res.qcontext.get('products'), 'bins': bins,
                 'search_count': product_count})

        if post.get('brand', False):
            res.qcontext.update({'brand_val': post.get('brand', False)})

        # Create Report for the search keyword
        curr_website = request.website.get_current_website()
        if search and curr_website.enable_smart_search:
            search_term = ' '.join(search.split()).strip().lower()
            attrib = res.qcontext.get('attrib_values', False)
            if search_term and not category and not attrib and page == 0:
                request.env['search.keyword.report'].sudo().create({
                    'search_term': search_term,
                    'no_of_products_in_result': res.qcontext.get('search_count', 0),
                    'user_id': request.env.user.id
                })

        return res

    def _get_search_options(
            self, category=None, attrib_values=None, pricelist=None, min_price=0.0, max_price=0.0,
            conversion_rate=1, **post
    ):
        options = super(WebsiteSaleExt, self)._get_search_options(category=category,
                                                                  attrib_values=attrib_values,
                                                                  pricelist=pricelist,
                                                                  min_price=min_price,
                                                                  max_price=max_price,
                                                                  conversion_rate=conversion_rate,
                                                                  **post)
        if post.get('out_of_stock', False):
            options.update({'out_of_stock': post.get('out_of_stock')})
        return options

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, access_token=None, revive='', **post):
        """
        inherited to check for b2b option for public user
        @return: super object
        """
        if request.website.b2b_hide_add_to_cart and request.website.is_public_user():
            return request.redirect('/', code=301)
        return super(WebsiteSaleExt, self).cart(access_token=access_token, revive=revive, **post)

    @http.route(['/shop/clear_cart'], type='json', auth="public", website=True)
    def clear_cart(self):
        """
        Clear the cart in e-commerce website
        @return: -
        """
        order = request.website.sale_get_order()
        order and order.website_order_line.unlink()

    def _get_country_related_render_values(self, kw, render_values):
        res = super(WebsiteSaleExt, self)._get_country_related_render_values(kw=kw, render_values=render_values)
        partner_id = int(kw.get('partner_id', -1))
        if request.website.allow_countries == 'selected':
            res[
                'countries'] = request.website.country_group_id.country_ids + request.website.default_country_id if request.website.default_country_id not in request.website.country_group_id.country_ids else request.website.country_group_id.country_ids
        if partner_id == -1:
            mode = render_values['mode']
            default_country = request.website.default_country_id and request.website.default_country_id.exists() or res[
                'country']
            res['country'] = default_country
            res['country_states'] = default_country.get_website_sale_states(mode=mode[1])
        if res['country'] not in res['countries']:
            res['countries'] += res['country']
        if not res['country']:
            res['country'] = request.website.default_country_id
        return res


class WebsiteExt(Website):
    """ Class for Website Inherit """

    @http.route(website=True, auth="public", sitemap=False, csrf=False)
    def web_login(self, *args, **kw):
        """
            Login - overwrite of the web login so that regular users are redirected to the backend
            while portal users are redirected to the same page from popup
            Returns formatted data required by login popup in a JSON compatible format
        """
        login_form_ept = kw.get('login_form_ept', False)
        if 'login_form_ept' in kw.keys():
            kw.pop('login_form_ept')
        response = super(WebsiteExt, self).web_login(*args, **kw)
        if login_form_ept:
            if response.is_qweb and response.qcontext.get('error', False):
                return json.dumps(
                    {'error': response.qcontext.get('error', False), 'login_success': False,
                     'hide_msg': False})
            else:
                if request.params.get('login_success', False):
                    uid = request.session.authenticate(request.session.db, request.params['login'],
                                                       request.params['password'])
                    user = request.env['res.users'].browse(uid)
                    redirect = '1'
                    if user.totp_enabled:
                        redirect = request.env(user=uid)['res.users'].browse(uid)._mfa_url()
                        return json.dumps(
                            {'redirect': redirect, 'login_success': True, 'hide_msg': True})
                    if user.has_group('base.group_user'):
                        redirect = b'/web?' + request.httprequest.query_string
                        redirect = redirect.decode('utf-8')
                    return json.dumps(
                        {'redirect': redirect, 'login_success': True, 'hide_msg': False})
        return response

    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999,
                     options=None):
        """ to explicitly render products and categories in result,
         and provide quick navigation of searched brand or attribute value """
        res = super(WebsiteExt, self).autocomplete(search_type=search_type, term=term,
                                                   order=order, limit=limit,
                                                   max_nb_chars=max_nb_chars, options=options)
        website = request.website.get_current_website()
        categories = request.env['product.public.category'].sudo().search(
            [('website_id', 'in', (False, website.id))]) \
            .filtered(lambda catg: term.strip().lower() in catg.name.strip().lower())
        search_categories = []
        for categ in categories:
            search_categories.append({'_fa': 'fa-folder-o', 'name': categ.name,
                                      'website_url': '/shop/category/%s' % categ.id})
        res['categories'] = search_categories[:10]
        if term and website and website.enable_smart_search:
            is_quick_link = {'status': False}
            brand = request.env['product.brand'].sudo().search([('website_id', 'in', (False, website.id))]).filtered(
                lambda b: term.strip().lower() in b.name.strip().lower())

            if brand:
                is_quick_link.update({'status': True,
                                      'navigate_type': 'brand',
                                      'name': brand[0].name,
                                      'url': '/shop/brands/%s' % brand[0].id})
            else:
                prod_att_value = request.env['product.attribute.value'].sudo().search([]).filtered(
                    lambda value: term.strip().lower() in value.name.strip().lower())
                if prod_att_value:
                    is_quick_link.update({'status': True,
                                          'navigate_type': 'attr_value',
                                          'name': prod_att_value[0].name,
                                          'attribute_name': prod_att_value[0].attribute_id.name,
                                          'url': '/shop?search=&attrib=%s-%s' % (
                                              prod_att_value[0].attribute_id.id,
                                              prod_att_value[0].id)})
            res['is_quick_link'] = is_quick_link
        return res


class EmiproThemeBaseExtended(WebsiteSaleWishlist):

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        """
        Inherit method for implement Price Filter and Brand Filter
        :param search:
        :param category:
        :param attrib_values:
        :return: search domain
        """
        domain = super(EmiproThemeBaseExtended, self)._get_search_domain(search=search,
                                                                         category=category,
                                                                         attrib_values=attrib_values,
                                                                         search_in_description=search_in_description)
        min_price = request.httprequest.values.get('min_price', 0.0)
        max_price = request.httprequest.values.get('max_price', 0.0)
        if max_price and min_price:
            try:
                max_price = float(max_price)
                min_price = float(min_price)
            except ValueError:
                raise NotFound()
            products = request.env['product.template'].sudo().search(domain)
            # return the product ids as per option selected (sale price or discounted price)
            if products:
                pricelist = request.website.pricelist_id
                if request.website.price_filter_on == 'website_price':
                    context = dict(request.context, quantity=1, pricelist=pricelist.id if pricelist else False)
                    products = products.with_context(context)
                    new_prod_ids = products.filtered(
                        lambda r: r.list_price >= float(min_price) and r.list_price <= float(max_price)).ids
                else:
                    new_prod_ids = products.filtered(lambda r: r.currency_id._convert(
                        r.list_price, pricelist.currency_id, request.website.company_id,
                        date=fields.Date.today()) >= float(min_price) and r.currency_id._convert(
                        r.list_price, pricelist.currency_id, request.website.company_id,
                        date=fields.Date.today()) <= float(max_price)).ids
                domain.append(('id', 'in', new_prod_ids or []))
            else:
                domain = [('id', '=', False)]

        # brand Filter
        if attrib_values:
            ids = []
            for value in attrib_values:
                if value[0] == 0:
                    ids.append(value[1])
            if ids:
                domain.append(('product_brand_id.id', 'in', ids))

        if request.params.get('brand', False):
            domain.append(('product_brand_id', '=', request.params.get('brand').id))

        if request.params.get('out_of_stock', False):
            domain.extend(['|', ('allow_out_of_stock_order', '=', True), '&',
                           ('free_qty', '>', 0), ('allow_out_of_stock_order', '=', False)])
        return domain

    @http.route('/hover/color', type='json', auth="public", methods=['POST'], website=True)
    def on_color_hover(self, color_id='', product_id='', hover=False):
        """
        veriant color hover
        @param color_id: attrubute of color type
        @param product_id: product_id
        @param hover: Boolean
        @return: product image src path
        """
        product = request.env['product.template'].browse(int(product_id))
        if hover:
            variant = product.product_variant_ids.filtered(
                lambda p: int(
                    color_id) in p.product_template_variant_value_ids.product_attribute_value_id.ids)[
                0]
            return f'/web/image/product.product/{str(variant.id)}/image_512'
        return f'/web/image/product.template/{product_id}/image_512'


class EmiproThemeBase(http.Controller):

    def template_render(self, template, is_theme=False, **kw):
        module = 'theme_clarico_vega' if is_theme else 'emipro_theme_base'
        response = http.Response(template=f"{module}.{template}", qcontext=kw)
        return response

    @http.route(['/quick_view_item_data'], type='json', auth="public", website=True)
    def get_quick_view_item(self, product_id=None):
        """
        This controller return the template for QuickView with product details
        :param product_id: get product id
        :return: quick_view template html
        """
        if product_id:
            product = request.env['product.template'].search([['id', '=', product_id]])
            response = self.template_render('quick_view_container', is_theme=False,
                                            **{'product': product})
            return response.render()

    @http.route(['/get_toast_token_details'], type='json', auth="public", website=True)
    def get_toast_token_details(self, product_variant_id=None):
        if product_variant_id:
            product = request.env['product.product'].sudo().search([['id', '=', product_variant_id]])
            return {
                'name': product.display_name,
                'image': f"/web/image/product.product/{product.id}/image_128"
            }

    @http.route(['/get_confirmation_popup_details'], type='json', auth="public", website=True)
    def get_confirmation_popup_details(self, product_variant_id=None):
        if product_variant_id:
            product = request.env['product.product'].sudo().search([['id', '=', product_variant_id]])
            product_tmpl_id = product.product_tmpl_id
            order = request.website.sale_get_order()
            response = self.template_render('confirmation_popup_details', is_theme=True,
                                            **{'added_product': product, 'product': product_tmpl_id, 'order': order})
            return response.render()


class AuthSignupHome(Home):

    @http.route(website=True, auth="public", sitemap=False, csrf=False)
    def web_auth_signup(self, *args, **kw):
        """
            Signup from popup and redirect to the same page
            Returns formatted data required by login popup in a JSON compatible format
        """
        qcontext = self.get_auth_signup_qcontext()

        if 'signup_form_ept' in kw.keys():
            kw.pop('signup_form_ept')

        login_email = kw.get('login', False)

        def recaptcha_token_verification(token=None):
            ip_addr = request.httprequest.remote_addr
            recaptcha_result = request.env['ir.http']._verify_recaptcha_token(ip_addr, token)
            if recaptcha_result in ['is_human', 'no_secret', 'is_bot']:
                return [True, 'Validation Successful']
            if recaptcha_result == 'wrong_secret':
                return [False, 'The reCaptcha private key is invalid.']
            elif recaptcha_result == 'wrong_token':
                return [False, 'The reCaptcha token is invalid.']
            elif recaptcha_result == 'timeout':
                return [False, 'Your request has timed out, please retry.']
            elif recaptcha_result == 'bad_request':
                return [False, 'The request is invalid or malformed.']
            else:
                return [False, "Form didn't submitted, Try again"]

        # Check google recaptcha if available
        if login_email and 'error' not in qcontext and request.httprequest.method == 'POST':
            if request.website.signup_captcha_option:
                token = ''
                if 'recaptcha_token_response' in kw.keys():
                    token = kw.pop('recaptcha_token_response')
                if 'recaptcha_token_response' in request.params:
                    request.params.pop('recaptcha_token_response')
                verification = recaptcha_token_verification(token)
                if not verification[0]:
                    qcontext['captcha_error'] = _(verification[1])

        if 'captcha_error' in qcontext:
            return json.dumps(
                {'error': qcontext.get('captcha_error', False), 'login_success': False})

        response = super(AuthSignupHome, self).web_auth_signup(*args, **kw)
        if request.httprequest.method == 'POST':
            if response.is_qweb and response.qcontext.get('error', False):
                return json.dumps(
                    {'error': response.qcontext.get('error', False), 'login_success': False})
            else:
                return json.dumps({'redirect': '1', 'login_success': True})

        return response

    @http.route(auth='public', website=True, sitemap=False, csrf=False)
    def web_auth_reset_password(self, *args, **kw):
        """
            Reset password from popup and redirect to the same page
            Returns formatted data required by login popup in a JSON compatible format
        """
        reset_form_ept = kw.get('reset_form_ept', False)
        if 'reset_form_ept' in kw.keys():
            kw.pop('reset_form_ept')
        response = super(AuthSignupHome, self).web_auth_reset_password(*args, **kw)
        if reset_form_ept:
            if response.is_qweb and response.qcontext.get('error', False):
                return json.dumps({'error': response.qcontext.get('error', False)})
            elif response.is_qweb and response.qcontext.get('message', False):
                return json.dumps({'message': response.qcontext.get('message', False)})
        return response


class VariantControllerExt(VariantController):

    @http.route(['/sale/get_combination_info_website'], type='json', auth="public",
                methods=['POST'], website=True)
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty,
                                     **kw):
        res = super(VariantControllerExt, self).get_combination_info_website(
            product_template_id=product_template_id,
            product_id=product_id,
            combination=combination,
            add_qty=add_qty, **kw)
        product = request.env['product.product'].sudo().search([('id', '=', res.get('product_id'))])
        product_tempate = request.env['product.template'].sudo().search([('id', '=', product_template_id)])
        res.update({
            'sku_details': product.default_code if product_tempate.product_variant_count > 1 else product_tempate.default_code})
        pricelist = request.website.get_current_pricelist()
        if request.website._display_product_price():
            res['price_table_details'] = pricelist.enable_price_table and self.get_price_table(pricelist, product, product_tempate)
        res.update({'is_offer': False})
        try:
            if pricelist and product:
                partner = request.env['res.users'].sudo().search([('id', '=', request.uid)]).partner_id
                vals = pricelist._compute_price_rule(product, add_qty)
                if vals.get(int(product)) and vals.get(int(product))[1]:
                    suitable_rule = vals.get(int(product))[1]
                    suitable_rule = request.env['product.pricelist.item'].sudo().search(
                        [('id', '=', suitable_rule), ('is_display_timer', '=', True)])
                    if suitable_rule.date_end and (
                            suitable_rule.applied_on == '3_global' or
                            suitable_rule.product_id or suitable_rule.product_tmpl_id or suitable_rule.categ_id):
                        start_date = int(round(datetime.datetime.timestamp(suitable_rule.date_start) * 1000))
                        end_date = int(round(datetime.datetime.timestamp(suitable_rule.date_end) * 1000))
                        current_date = int(round(datetime.datetime.timestamp(datetime.datetime.now()) * 1000))
                        res.update({'is_offer': True,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'current_date': current_date,
                                    'suitable_rule': suitable_rule,
                                    'offer_msg': suitable_rule.offer_msg,
                                    })
        except Exception as e:
            return res
        return res

    def get_price_table(self, pricelist, product, product_tempate):
        current_date = datetime.datetime.now()
        items = pricelist._get_applicable_rules(product, current_date)
        # Get the rules based on the priority based on condition
        updated_rules = (items.filtered(
            lambda rule: rule.applied_on == '0_product_variant' and rule.product_id.id == product.id)
                         or items.filtered(
                    lambda rule: rule.applied_on == '1_product' and rule.product_tmpl_id.id == product_tempate.id)
                         or items.filtered(lambda
                                               rule: rule.applied_on == '2_product_category' and rule.categ_id.id in product_tempate.categ_id.search(
                    [('id', 'parent_of', product_tempate.categ_id.ids)]).ids)
                         or items.filtered(lambda rule: rule.applied_on == '3_global'))
        price_list_items = []
        minimum_qtys = set(updated_rules.mapped('min_quantity'))
        minimum_qtys.add(1)
        minimum_qtys.discard(0)
        minimum_qtys = list(minimum_qtys)
        minimum_qtys.sort()
        for qty in minimum_qtys:
            price = pricelist._get_product_price(product=product, quantity=qty, target_currency=pricelist.currency_id)
            data = {'qty': int(qty), 'price': price}
            price_list_items.append(data)
        price_list_vals = {
            'pricelist_items': price_list_items,
            'currency_id': pricelist.currency_id,
        }
        price_table_details = http.Response(template="emipro_theme_base.product_price_table",
                                            qcontext=price_list_vals).render()
        return price_table_details


class ProductHotspot(WebsiteSale):
    """
    Class for product hotspot handling
    """

    # Render the Hotspot Product popover template
    @http.route('/get-pop-up-product-details', type='http', auth='public', website=True)
    def get_popup_product_details(self, **kw):
        """
        Render the Hotspot Product popover template
        @param kw: dict for product details
        @return: response for template
        """
        product = int(kw.get('product'))
        if kw.get('product', False):
            product = request.env['product.template'].sudo().browse(product)
            values = {
                'product': product,
            }
            return request.render("emipro_theme_base.product_add_to_cart_popover", values,
                                  headers={'Cache-Control': 'no-cache'})


class WebsiteSaleExtended(WebsiteSale):

    @http.route('/see_all', type='json', auth="public", methods=['POST'], website=True)
    def get_see_all(self, attr_id='', is_mobile='', search='', category='', brand_val='', domain_qs=''):
        if domain_qs:
            domain_qs = ast.literal_eval(domain_qs)

        if brand_val:
            ctx = request.env.context.copy()
            ctx.update({'is_brands': brand_val})
            request.env.context = ctx
        else:
            brand_attrib_values = [[int(x) for x in v.split("-")] for v in domain_qs if v]
            for value in brand_attrib_values:
                if value[0] == 0:
                    brand_id = [sublist[1] for sublist in brand_attrib_values]
                    ctx = request.env.context.copy()
                    ctx.update({'is_brands_attr': brand_id})
                    request.env.context = ctx

        if attr_id:
            attributes = request.env['product.attribute'].search([('id', '=', attr_id), ('visibility', '=', 'visible')])
            if is_mobile:
                response = http.Response(template="theme_clarico_vega.see_all_attr_mobile",
                                         qcontext={'attributes': attributes,
                                                   'search': search,
                                                   'category': category,
                                                   'domain_qs': domain_qs})
            else:
                response = http.Response(template="theme_clarico_vega.see_all_attr", qcontext={'attributes': attributes,
                                                                                               'search': search,
                                                                                               'category': category,
                                                                                               'domain_qs': domain_qs})
        else:
            attributes = request.env['product.brand'].search([('is_published', '=', True)])
            if is_mobile:
                response = http.Response(template="theme_clarico_vega.see_all_brand_mobile",
                                         qcontext={'brand_list': attributes, 'search': search, 'category': category,
                                                   'domain_qs': domain_qs})
            else:
                response = http.Response(template="theme_clarico_vega.see_all_brand",
                                         qcontext={'brand_list': attributes, 'search': search, 'category': category,
                                                   'domain_qs': domain_qs})

        return response.render()


class WebsiteSnippetFilterEpt(Website):

    @http.route('/website/snippet/filters', type='json', auth='public', website=True)
    def get_dynamic_filter(self, filter_id, template_key, limit=None, search_domain=None, with_sample=False, **post):
        dynamic_filter = request.env['website.snippet.filter'].sudo().search(
            [('id', '=', filter_id)] + request.website.website_domain()
        )
        add2cart = post.get('product_context', {}).get('add2cart') == 'true'
        wishlist = post.get('product_context', {}).get('wishlist') == 'true'
        rating = post.get('product_context', {}).get('rating') == 'true'
        quickview = post.get('product_context', {}).get('quickview') == 'true'
        product_label = post.get('product_context', {}).get('product_label') == 'true'
        count = post.get('brand_context', {}).get('count') or post.get('category_context', {}).get('count') == 'true'
        return dynamic_filter and dynamic_filter.with_context(add2cart=add2cart, wishlist=wishlist, rating=rating, quickview=quickview, product_label=product_label, count=count)._render(template_key, limit, search_domain, with_sample) or []

