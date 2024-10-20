# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from odoo.exceptions import UserError
import base64
from zipfile import ZipFile
import io
from odoo.tools import ustr
import os
import codecs
from urllib import parse


class ShImportImgZipShop(models.TransientModel):
    _name = "sh.import.img.zip.shop.wizard"
    _description = "Import Images from zip file eCommerce"

    zip_file = fields.Binary(string="Zip File", required=True)

    product_by = fields.Selection([
        ('name', 'Name'),
        ('default_code', 'Internal Reference'),
        ('barcode', 'Barcode'),
        ('id', 'ID'),
    ], default="name", string="Product By")

    product_model = fields.Selection([
        ('pro_tmpl', 'Product Template'),
        ('pro_var', 'Product Variants'),
    ], default="pro_tmpl", string="Product Model")

    is_import_extra_product_media = fields.Boolean(
        string="Import Extra Product Media?")

    import_extra_images_with_underscore_naming_format = fields.Boolean(
        string="Import Extra Images With _ Naming Format?")

    def show_success_msg(self, counter, skipped_images_dic):
        # open the new success message box
        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        dic_msg = str(counter) + " Images imported successfully"
        if skipped_images_dic:
            dic_msg = dic_msg + "\nNote:"
        for k, v in skipped_images_dic.items():
            dic_msg = dic_msg + "\nImage name " + k + " " + v + " "
        context['message'] = dic_msg
        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def button_import(self):
        if self and self.zip_file:

            # choose specific model and field name  based on selection.
            model_obj = ""
            field_name = ""
            skipped_images_dic = {}

            field_name = self.product_by

            if self.product_model == 'pro_var':
                model_obj = self.env['product.product']
            elif self.product_model == 'pro_tmpl':
                model_obj = self.env['product.template']

            base64_data_file = base64.b64decode(self.zip_file)
            try:
                with ZipFile(io.BytesIO(base64_data_file), 'r') as archive:
                    folder_inside_zip_name = ""
                    counter = 0
                    for file_name in archive.namelist():
                        print("\n 1  file_name ==>", file_name)
                        try:
                            img_data = archive.read(file_name)
                            if len(img_data) == 0:
                                folder_inside_zip_name = file_name
                                continue
                            if img_data:
                                img_name_with_ext = ""
                                if folder_inside_zip_name != "":
                                    img_name_with_ext = file_name.replace(
                                        folder_inside_zip_name, "")
                                    just_img_name = ""
                                    if img_name_with_ext != "":
                                        just_img_name = os.path.splitext(
                                            img_name_with_ext)[0]
                                        if just_img_name != "" and model_obj != "" and field_name != "":

                                            query_dict = {}
                                            has_integer = False
                                            if self.is_import_extra_product_media:
                                                if self.import_extra_images_with_underscore_naming_format:
                                                    first = self.spli_function(
                                                        just_img_name, just_img_name.count('_'))
                                                    print(
                                                        "\n\n 1 first ===>", first)
                                                    try:
                                                        has_integer = int(
                                                            first[1])
                                                        #query_dict['name'] = just_img_name
                                                        just_img_name = first[0]
                                                        query_dict['name'] = just_img_name
                                                        query_dict['mname'] = just_img_name
                                                    except Exception as e:
                                                        has_integer = False
                                                else:
                                                    try:
                                                        query_dict = dict(
                                                            parse.parse_qsl(just_img_name))
                                                    except Exception as e:
                                                        query_dict = {}

                                                    if query_dict.get('mname', False):
                                                        just_img_name = query_dict.get(
                                                            'mname')
                                            search_record = model_obj.sudo().search([
                                                (field_name, '=', just_img_name)
                                            ], limit=1)
                                            print(
                                                "\n\n search_record===>", search_record)
                                            print(
                                                "\n\n just_img_name===>", just_img_name)
                                            print(
                                                "\n\n query_dict===>", query_dict)
                                            if search_record:
                                                image_base64 = codecs.encode(
                                                    img_data, 'base64')
                                                if query_dict:
                                                    extra_image_vals = {
                                                        'name': query_dict.get('name'),
                                                        'image_1920': image_base64,
                                                    }

                                                    if query_dict.get('seq', False):
                                                        extra_image_vals.update({
                                                            'sequence': query_dict.get('seq', 0)
                                                        })

                                                    print(
                                                        "\n extra_image_vals ==>", extra_image_vals.get("name", False))
                                                    if self.product_model == 'pro_var':
                                                        search_record.product_variant_image_ids = [
                                                            (0, 0, extra_image_vals)]
                                                    elif self.product_model == 'pro_tmpl':
                                                        search_record.product_template_image_ids = [
                                                            (0, 0, extra_image_vals)]
                                                else:
                                                    record_vals = {
                                                        'image_1920': image_base64
                                                    }
                                                    if self.product_model == 'pro_var':
                                                        record_vals.update({
                                                            'image_variant_1920': image_base64,
                                                        })
                                                    search_record.sudo().write(record_vals)

                                                counter += 1

                                            else:
                                                skipped_images_dic[img_name_with_ext] = " - Record not found for this image " + \
                                                    img_name_with_ext
                                        else:
                                            skipped_images_dic[img_name_with_ext] = " - Record not found for this image " + \
                                                img_name_with_ext
                                    else:
                                        skipped_images_dic[img_name_with_ext] = " - Image name not resolve for this image " + file_name
                                else:
                                    skipped_images_dic[img_name_with_ext] = " - Zip file have no any folder inside it "
                            else:
                                skipped_images_dic[img_name_with_ext] = " - Image data not found for this image " + file_name

                        except Exception as e:
                            skipped_images_dic[file_name] = " - Value is not valid. " + ustr(
                                e)
                            continue

                    # show success message here.
                    res = self.show_success_msg(counter, skipped_images_dic)
                    return res

            except Exception as e:
                msg = "Something went wrong - " + ustr(e)
                raise UserError(_(msg))

    def spli_function(self, name, n):
        a = name.split("_")
        b = "_".join(a[:n])
        c = "_".join(a[n:])
        return [b, c]
