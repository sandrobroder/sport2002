# -*- coding: utf-8 -*-
import ast
import base64
import csv
from datetime import datetime

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    google_category_id = fields.Many2one("product.google.category", string="Google Category for Product")
    brand_id = fields.Many2one('product.brand', string='Brand Name')
    gtin = fields.Char(string='GTIN')
    mpn = fields.Char(string='MPN')


class ProductBrand(models.Model):
    _name = "product.brand"

    name = fields.Char('Brand Name')


class FacebookField(models.Model):
    _name = "fb.catalogue.product.field"

    name = fields.Char("Field Name")
    is_required = fields.Boolean("Is Required")


class FieldMappingLine(models.Model):
    _name = "field.mapping.line"

    fb_product_field_id = fields.Many2one("fb.catalogue.product.field", string="Facebook Field",
                                          help='Facebook field for product')
    odoo_model_field_id = fields.Many2one("ir.model.fields", string="Odoo Model Field",
                                          domain=[('model', '=', 'product.template')], help='Odoo field for product')
    default_value = fields.Char("Default Value", help='Use when Odoo field has no value')
    mapping_id = fields.Many2one("fb.odoo.field.mapping")


class FieldMapping(models.Model):
    _name = "fb.odoo.field.mapping"

    name = fields.Char("Mapping Name")
    created_by_data = fields.Boolean()
    field_mapping_ids = fields.One2many("field.mapping.line", "mapping_id",
                                        string="Facebook Odoo Field Mapping for Product")

    def create(self, vals):
        for rec in vals:
            if 'created_by_data' in rec:
                if rec['created_by_data']:
                    fb_fields = self.env['fb.catalogue.product.field'].search([('is_required', '=', True)])
                    mapping_line = []
                    for fb_field in fb_fields:
                        model_field = None
                        default_value = ""
                        if fb_field.name in ['id', 'link', 'image_link']:
                            model_field = self.env['ir.model.fields'].search(
                                [('model', '=', 'product.template'), ('name', '=', 'id')])
                        elif fb_field.name == 'title':
                            model_field = self.env['ir.model.fields'].search(
                                [('model', '=', 'product.template'), ('name', '=', 'display_name')])
                        elif fb_field.name == 'description':
                            model_field = self.env['ir.model.fields'].search(
                                [('model', '=', 'product.template'), ('name', '=', 'description')])
                        elif fb_field.name == 'availability':
                            default_value = 'in stock'
                        elif fb_field.name == 'condition':
                            default_value = 'new'
                        elif fb_field.name == 'price':
                            model_field = self.env['ir.model.fields'].search(
                                [('model', '=', 'product.template'), ('name', '=', 'list_price')])
                        elif fb_field.name == 'brand':
                            model_field = self.env['ir.model.fields'].search(
                                [('model', '=', 'product.template'), ('name', '=', 'brand_id')])

                        if model_field:
                            mapping_line.append([0, 0, {'fb_product_field_id': fb_field.id,
                                                        'odoo_model_field_id': model_field.id}])
                        else:
                            mapping_line.append([0, 0, {'fb_product_field_id': fb_field.id,
                                                        'default_value': default_value}])
                    rec['field_mapping_ids'] = mapping_line
        result = super(FieldMapping, self).create(vals)
        return result


class FbAttachmentMapping(models.Model):
    _name = "fb.catalogue.attachment.map"
    _rec_name = 'fb_catalogue_id'
    _order = 'id desc'

    fb_catalogue_id = fields.Many2one("facebook.catalogue", string='Facebook Catalogue')
    is_latest = fields.Boolean(string='Is Latest Feed', default=True)
    attachment_id = fields.Many2one('ir.attachment')

    @api.model
    def create(self, vals):
        attachment_ids = self.env['fb.catalogue.attachment.map'].search([('is_latest', '=', True)])
        for attachment in attachment_ids:
            if attachment.is_latest:
                attachment.is_latest = False
        return super(FbAttachmentMapping, self).create(vals)


class FacebookCatalogue(models.Model):
    _name = "facebook.catalogue"

    name = fields.Char()
    price_list_id = fields.Many2one("product.pricelist")
    currency_id = fields.Many2one(related="price_list_id.currency_id")
    field_mapping_id = fields.Many2one('fb.odoo.field.mapping', help='Used in Facebook Odoo field mapping')
    catalogue_attachment_ids = fields.One2many('fb.catalogue.attachment.map', 'fb_catalogue_id')
    attachment_count = fields.Integer(string='#Feeds', compute='compute_att_count', help='Total created feeds')
    shop_url = fields.Char('Shop URL', help='Base URL of the shop website')
    feed_url = fields.Char('Feed URL', compute='get_feed_url', help='Use this URL to get the feeds')
    cron_id = fields.Many2one('ir.cron', help='Feeds Auto Create Activated')

    # product selection
    product_select_by = fields.Selection(
        [('category', 'By Category'), ('brand', 'By Brand'), ('top_sell', 'Most Sold'), ('domain', 'By Domain'),
         ('manual', 'Manually')],
        string='Product Selection',
        default='category')

    public_categ_ids = fields.Many2many(
        'product.public.category', relation='product_public_category_facebook_catalogue_rel',
        string='Website Product Category',
        help="The product will be available in each mentioned eCommerce category. Go to Shop > "
             "Customize and enable 'eCommerce categories' to view all eCommerce categories.")
    brand_ids = fields.Many2many('product.brand', string='Product Brand')
    date_duration_start = fields.Date()
    date_duration_end = fields.Date()
    manual_select_product_ids = fields.Many2many('product.template', relation='product_template_facebook_catalogue_rel')
    rule_products_domain = fields.Char(string="Based on Products", default=[('is_published', '=', True)])
    limit = fields.Integer(default=10)

    def get_feed_url(self):
        for rec in self:
            if rec.shop_url:
                if rec.shop_url[-1] == '/':
                    rec.feed_url = rec.shop_url + 'shop/' + str(rec.id) + '/feeds'
                else:
                    rec.feed_url = rec.shop_url + '/shop/' + str(rec.id) + '/feeds'
            else:
                rec.feed_url = ""

    def action_create_csv(self):
        product_ids = []
        if self.product_select_by == 'category':
            domain = [('is_published', '=', True)]
            if self.public_categ_ids:
                domain.append(('public_categ_ids', 'in', self.public_categ_ids.ids))
            product_ids = self.env['product.template'].search(domain)

        elif self.product_select_by == 'brand':
            domain = [('is_published', '=', True)]
            if self.brand_ids:
                domain.append(('brand_id', 'in', self.brand_ids.ids))
            product_ids = self.env['product.template'].search(domain)

        elif self.product_select_by == 'top_sell':
            domain = [('is_published', '=', True)]
            if self.date_duration_start and self.date_duration_end and self.limit:
                datetime_start = datetime.combine(self.date_duration_start, datetime.min.time())
                datetime_end = datetime.combine(self.date_duration_end, datetime.min.time())

                order_ids = self.env['sale.order'].sudo().search(
                    [('date_order', '>=', datetime_start), ('date_order', '<=', datetime_end), ('state', '=', 'sale')])
                products = set()
                for order_id in order_ids:
                    for line in order_id.order_line:
                        products.add(line.product_id.id)
                        if len(products) == self.limit:
                            break
                    if len(products) == self.limit:
                        break
                domain.append(('id', 'in', list(products)))
            product_ids = self.env['product.template'].search(domain)
        elif self.product_select_by == 'domain':
            domain = self.rule_products_domain
            domain_list = ast.literal_eval(domain)
            product_ids = self.env['product.template'].search(domain_list, limit=self.limit)
        elif self.product_select_by == 'manual':
            domain = [('is_published', '=', True)]
            if self.manual_select_product_ids:
                domain.append(('id', 'in', self.manual_select_product_ids.ids))
            product_ids = self.env['product.template'].sudo().search(domain)

        top_row = []
        csv_header = []
        with open('fb_feeds.csv', 'w') as my_file:
            wr = csv.writer(my_file)
            field_mapping_ids = self.field_mapping_id.field_mapping_ids
            for mapping_id in field_mapping_ids:
                if mapping_id.fb_product_field_id:
                    if mapping_id.fb_product_field_id.is_required:
                        top_row.append("#Required")
                    else:
                        top_row.append("#Optional")
                    csv_header.append(mapping_id.fb_product_field_id.name)
            wr.writerow(top_row)
            wr.writerow(csv_header)

            for product_id in product_ids:
                row = []
                for mapping_id in field_mapping_ids:

                    if mapping_id.odoo_model_field_id:
                        result = product_id.read([mapping_id.odoo_model_field_id.name])
                        if not result[0][mapping_id.odoo_model_field_id.name] or \
                                result[0][mapping_id.odoo_model_field_id.name] == '':
                            row.append(mapping_id.default_value)
                        else:
                            if self.shop_url[-1] == '/':
                                url = self.shop_url[:-1]
                            else:
                                url = self.shop_url
                            if 'list_price' in result[0]:
                                obj = self.env['product.template'].browse(result[0]['id'])
                                price_list_app = obj._get_combination_info(pricelist=self.price_list_id,
                                                                           only_template=True)
                                price = str(price_list_app['list_price']) + ' ' + self.currency_id.name
                                row.append(price)
                            elif mapping_id.fb_product_field_id.name == 'image_link':
                                product__id = result[0][mapping_id.odoo_model_field_id.name]
                                image_link = url + '/web/image/product.template/' + str(product__id) + '/image_1920/'
                                row.append(image_link)

                            elif mapping_id.fb_product_field_id.name == 'link':
                                product__id = result[0][mapping_id.odoo_model_field_id.name]
                                link = url + '/shop/product/' + str(product__id)
                                row.append(link)

                            elif mapping_id.fb_product_field_id.name == 'brand':
                                row.append(result[0][mapping_id.odoo_model_field_id.name][1])
                            else:
                                row.append(result[0][mapping_id.odoo_model_field_id.name])

                    else:
                        if mapping_id.default_value:
                            row.append(mapping_id.default_value)
                wr.writerow(row)
        data = open("fb_feeds.csv", "rb").read()
        encoded = base64.b64encode(data)
        Attachment = self.env['ir.attachment']
        name = datetime.now().strftime("%m/%d/%Y_%H:%M:%S")
        attachment_data = {
            'name': 'catalogue_' + name + '.csv',
            'datas': encoded,
        }
        attachment_id = Attachment.create(attachment_data).id
        self.env['fb.catalogue.attachment.map'].create({
            'fb_catalogue_id': self.id,
            'attachment_id': attachment_id
        })

    def compute_att_count(self):
        for rec in self:
            rec.attachment_count = len(
                self.env['fb.catalogue.attachment.map'].search([('fb_catalogue_id', '=', rec.id)]))

    def view_attachments(self):
        return {
            'name': 'Catalogue Attachments',
            'type': 'ir.actions.act_window',
            'res_model': 'fb.catalogue.attachment.map',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'target': 'current',
            '_order': 'id desc',
            'domain': [('fb_catalogue_id', '=', self.id)]
        }

    def create_cron(self):
        model_id = self.env['ir.model'].search([('name', '=', 'facebook.catalogue')], limit=1).id
        self.cron_id = self.env['ir.cron'].create({'name': self.name + " Feed Creator, Click to Configure",
                                                   'model_id': model_id,
                                                   'user_id': self.env.user.id,
                                                   'state': 'code',
                                                   'interval_type': 'weeks',
                                                   'active': True,
                                                   'code': "env['facebook.catalogue'].browse(" + str(
                                                       self.id) + ").action_create_csv()"
                                                   }).id

    def remove_cron(self):
        self.cron_id.unlink()


class GoogleCategory(models.Model):
    _name = "product.google.category"

    name = fields.Char('Category Name')
    code = fields.Integer('Category Code')
