# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import base64
import binascii
import tempfile
import xlrd
import xlwt
from io import BytesIO

from odoo import models, fields


class AddXls(models.TransientModel):
    _name = 'import.from.file.sale'
    _description = "Import xls File"

    def _get_sample_file(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.add_sheet("Sample File")
        sheet.write(0, 0, 'Internal Reference')
        sheet.write(0, 1, 'Product')
        sheet.write(0, 2, 'Description')
        sheet.write(0, 3, 'Quantity')
        sheet.write(0, 4, 'Unit Price')
        sheet.write(0, 5, 'Subtotal')
        stream = BytesIO()
        workbook.save(stream)
        return base64.encodebytes(stream.getvalue())

    file = fields.Binary(string="Import File")
    filename = fields.Char(size=256, default="Sample.xls")
    download_sample_file = fields.Binary(string="Download Sample File", default=_get_sample_file, readonly=True)

    def import_file(self):
        order = self.env['sale.order'].browse(self.env.context.get('active_ids'))

        if self.file:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            values = []
            for row_no in range(sheet.nrows):
                if row_no > 0:
                    line = list(map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    product_id = self.env['product.product'].search(['|', ('default_code', '=', line[0]), ('name', 'in', line)], limit=1)
                    if product_id:
                        values.append((0, 0, {'product_id': product_id.id, 'product_uom_qty': line[3], 'price_unit': line[4]}))
            order.order_line = values
