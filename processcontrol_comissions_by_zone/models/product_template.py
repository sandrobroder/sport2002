from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_id = fields.Many2one(comodel_name='website',string='Sitio Web')

