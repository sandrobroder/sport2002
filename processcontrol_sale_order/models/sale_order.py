import time

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class import_product_var_wizard(models.TransientModel):
    _inherit = "import.product.var.wizard"
