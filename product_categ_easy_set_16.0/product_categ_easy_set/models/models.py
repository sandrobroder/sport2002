# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = "product.category"

    public_categ_ids = fields.Many2many("product.public.category")
    pos_categ_id = fields.Many2one("pos.category")
    brand_id = fields.Many2one("product.brand")

    def action_update_category(self):
        updated_categ = []
        for categ in self:
            if categ.id in updated_categ:
                continue
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]):
                updated_categ.append(sub_categ_id.id)
                # print("sub_categ_id", sub_categ_id, sub_categ_id.name)
                product_ids = self.env['product.template'].search([('categ_id', 'child_of', sub_categ_id.ids)])
                # print("product_ids", len(product_ids))
                if product_ids:
                    vals_to_update = {}
                    if sub_categ_id.public_categ_ids:
                        vals_to_update.update({
                            "public_categ_ids": [(6, 0, sub_categ_id.public_categ_ids.ids)]
                        })
                    if sub_categ_id.pos_categ_id:
                        vals_to_update.update({
                            "pos_categ_id": sub_categ_id.pos_categ_id.id
                        })

                    if sub_categ_id.brand_id:
                        vals_to_update.update({
                            "product_brand_id": sub_categ_id.brand_id.id
                        })
                    if vals_to_update:
                        # print("vals_to_update", vals_to_update)
                        for product in product_ids:
                            product.write(vals_to_update)
            # print("\n")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        def get_public_categ(category_id):
            if category_id.public_categ_ids:
                return category_id.public_categ_ids
            elif category_id.parent_id:
                return get_public_categ(category_id.parent_id)
            else:
                return None

        def get_pos_categ(category_id):
            if category_id.pos_categ_id:
                return category_id.pos_categ_id
            elif category_id.parent_id:
                return get_pos_categ(category_id.parent_id)
            else:
                return None

        def get_brand(category_id):
            if category_id.brand_id:
                return category_id.brand_id
            elif category_id.parent_id:
                return get_brand(category_id.parent_id)
            else:
                return None

        for vals in vals_list:
            if "categ_id" in vals:
                categ_id = vals.get("categ_id")
                categ_id = self.env["product.category"].browse(categ_id)
                vals_to_update = {}
                public_categ_ids = get_public_categ(categ_id)
                if public_categ_ids:
                    vals_to_update.update({
                        "public_categ_ids": [(6, 0, public_categ_ids.ids)]
                    })

                pos_categ_id = get_pos_categ(categ_id)
                if pos_categ_id:
                    vals_to_update.update({
                        "pos_categ_id": pos_categ_id.id
                    })
                brand_id = get_brand(categ_id)
                if brand_id:
                    vals_to_update.update({
                        "product_brand_id": brand_id.id
                    })
                if vals_to_update:
                    vals.update(vals_to_update)
        return super().create(vals_list)

    def write(self, vals):
        if "categ_id" in vals:
            categ_id = vals.get("categ_id")
            categ_id = self.env["product.category"].browse(categ_id)
            vals_to_update = {}

            def get_public_categ(category_id):
                if category_id.public_categ_ids:
                    return category_id.public_categ_ids
                elif category_id.parent_id:
                    return get_public_categ(category_id.parent_id)
                else:
                    return None

            def get_pos_categ(category_id):
                if category_id.pos_categ_id:
                    return category_id.pos_categ_id
                elif category_id.parent_id:
                    return get_pos_categ(category_id.parent_id)
                else:
                    return None

            def get_brand(category_id):
                if category_id.brand_id:
                    return category_id.brand_id
                elif category_id.parent_id:
                    return get_brand(category_id.parent_id)
                else:
                    return None

            public_categ_ids = get_public_categ(categ_id)
            if public_categ_ids:
                vals_to_update.update({
                    "public_categ_ids": [(6, 0, public_categ_ids.ids)]
                })
            pos_categ_id = get_pos_categ(categ_id)
            if pos_categ_id:
                vals_to_update.update({
                    "pos_categ_id": pos_categ_id.id
                })
            brand_id = get_brand(categ_id)
            if brand_id:
                vals_to_update.update({
                    "product_brand_id": brand_id.id
                })
            if vals_to_update:
                vals.update(vals_to_update)
        return super().write(vals)
