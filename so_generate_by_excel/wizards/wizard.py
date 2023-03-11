# -*- coding: utf-8 -*-
import base64
import mimetypes
import os
import tempfile
import zipfile
from io import BytesIO
from os.path import join as opj

import xlrd

from odoo import models, fields, _
from odoo.exceptions import ValidationError, UserError, _logger
from odoo.loglevels import exception_to_unicode

CUSTOMER_NAME_ROW = 7
CUSTOMER_NAME_COL = 1
ROW_START = 9
PRODUCT_IDENTIFIER_COL = 0
ATTR_START = 5
ATTR_END = 11


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class ImportExcel(models.TransientModel):
    _name = "import.excel.wizard"

    file_data = fields.Binary()
    file_name = fields.Char()
    activity_dead_line = fields.Date()
    results = fields.Text()

    def read_excel(self, file_path, file_name):
        workbook = xlrd.open_workbook(file_path)
        sheet = workbook.sheet_by_index(0)
        order_line_items = []
        customer_identifier = sheet.cell_value(CUSTOMER_NAME_ROW, CUSTOMER_NAME_COL)
        if not customer_identifier:
            raise ValidationError("Unable to get customer code from the uploaded excel!\nFile Name: %s" % file_name)

        for row_no in range(ROW_START, sheet.nrows):
            product_identifier = sheet.cell_value(row_no, PRODUCT_IDENTIFIER_COL)
            if not product_identifier:
                continue
            split_ls = product_identifier.rsplit('-', 1)
            if len(split_ls) != 2:
                continue
            identifier_prefix = split_ls[0]
            identifier_main = int(split_ls[1])

            for col in range(ATTR_START, ATTR_END + 1):
                value = sheet.cell_value(row_no, col)
                if value:
                    # check for invalid cell
                    if str(value).lower() == "x":
                        continue
                    qty = int(value)
                    if qty > 0:
                        product_identifier_actual = "%s-%s" % (identifier_prefix, identifier_main)
                        order_line_items.append((product_identifier_actual, qty))
                identifier_main += 1

        if order_line_items:
            return customer_identifier, order_line_items

    def import_excel_zip(self):
        zip_data = base64.decodebytes(self.file_data)
        fp = BytesIO()
        fp.write(zip_data)
        zip_file = fp
        if not zip_file:
            raise Exception(_("No file set."))
        if not zipfile.is_zipfile(zip_file):
            raise UserError(_('Only zip files are supported.'))
        mime_type, x = mimetypes.guess_type(self.file_name)
        if mime_type != "application/zip":
            raise UserError(_('Only zip files are supported.'))
        errors = dict()
        all_orders = []
        r = []
        with zipfile.ZipFile(zip_file, "r") as z:
            total_files = len(z.filelist)
            r.append("Total %s excel files imported." % total_files)
            # for zf in z.filelist:
            #     print("zf.filename", zf.filename)
            #     if zf.file_size > MAX_FILE_SIZE:
            #         raise UserError(_("File '%s' exceed maximum allowed file size", zf.filename))
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    z.extractall(temp_dir)
                    excel_files = [file for file in os.listdir(temp_dir)]
                    for excel_file_name in excel_files:
                        try:
                            path = opj(temp_dir, excel_file_name)
                            order_data = self.read_excel(path, excel_file_name)
                            if order_data:
                                all_orders.append(order_data)
                        except Exception as e:
                            _logger.exception('Error while importing module')
                            errors[excel_file_name] = exception_to_unicode(e)
                except Exception as e:
                    _logger.exception('Error while importing module')
        if all_orders:
            orders = []
            for order in all_orders:
                customer_identifier, order_items = order
                customer_id = self.env["res.partner"].search([("ref_unique_code", "=", customer_identifier)])
                order_line = []
                for default_code, qty in order_items:
                    product_id = self.env["product.product"].search([("default_code", "=", default_code)])
                    if product_id:
                        order_line.append((0, 0, {
                            "product_id": product_id.id,
                            "product_uom_qty": qty,
                        }))

                orders.append({
                    "partner_id": customer_id.id,
                    "order_line": order_line
                })
            order_batches = chunks(orders, 100)
            created_orders = []
            for order_batch in order_batches:
                order_ids = self.env["sale.order"].sudo().create(order_batch)
                order_ids.activity_schedule("so_generate_by_excel.mail_act_sale_imported", self.activity_dead_line)
                order_ids.action_confirm()
                created_orders.extend(order_ids.ids)
            r.append("Total %s orders created" % len(created_orders))
        for excel_file_name, error in errors.items():
            r.append("Error while importing excel '%s'.\n\n %s \n Make sure layout is correct and try again." % (
                excel_file_name, error))
        if r:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'import.excel.wizard',
                'name': "Import Result",
                'view_mode': 'form',
                "context": {"default_results": '\n'.join(r)},
                "target": "new"
            }

    # def load_excel(self):
    #
    #     # self._read_xls()
    #     # print("_read_xls", data)
    #     fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    #     if self.file_data:
    #         fp.write(binascii.a2b_base64(self.file_data))
    #         fp.seek(0)
    #         values = {}
    #         res = {}
    #         workbook = xlrd.open_workbook(fp.name)
    #         sheet = workbook.sheet_by_index(0)
    #         order_line_items = []
    #         customer_identifier = sheet.cell_value(CUSTOMER_NAME_ROW, CUSTOMER_NAME_COL)
    #         print("customer_identifier, ", customer_identifier)
    #         if not customer_identifier:
    #             raise ValidationError("Unable to get customer code from the uploaded excel!")
    #         customer_id = self.env["res.partner"].search([("ref_unique_code", "=", customer_identifier)])
    #         print("customer_id", customer_id)
    #         for row_no in range(ROW_START, sheet.nrows):
    #             product_identifier = sheet.cell_value(row_no, PRODUCT_IDENTIFIER_COL)
    #             print("product_identifier", product_identifier)
    #             if not product_identifier:
    #                 continue
    #             split_ls = product_identifier.rsplit('-', 1)
    #             print("")
    #             if len(split_ls) != 2:
    #                 continue
    #             identifier_prefix = split_ls[0]
    #             identifier_main = int(split_ls[1])
    #             print("product_identifier", identifier_prefix, identifier_main)
    #
    #             for col in range(ATTR_START, ATTR_END + 1):
    #                 value = sheet.cell_value(row_no, col)
    #                 print("value", value)
    #                 if value:
    #                     # check for invalid cell
    #                     if str(value).lower() == "x":
    #                         continue
    #                     qty = int(value)
    #                     if qty > 0:
    #                         product_identifier_actual = "%s-%s" % (identifier_prefix, identifier_main)
    #                         order_line_items.append((product_identifier_actual, qty))
    #
    #                 identifier_main += 1
    #         order_line = []
    #         if order_line_items:
    #             for default_code, qty in order_line_items:
    #                 product_id = self.env["product.product"].search([("default_code", "=", default_code)])
    #                 if product_id:
    #                     order_line.append((0, 0, {
    #                         "product_id": product_id.id,
    #                         "product_uom_qty": qty,
    #                     }))
    #
    #         order_id = self.env["sale.order"].sudo().create({
    #             "partner_id": customer_id.id,
    #             "order_line": order_line
    #
    #         })
    #         print("order_line_items", order_line_items, order_id)
