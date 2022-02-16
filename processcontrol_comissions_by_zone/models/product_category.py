from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductCategory(models.Model):
    _inherit = 'product.category'

    agent_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="partner_agent_rel3",
        column1="partner_id",
        column2="agent_id",
        domain=[("agent", "=", True)],
        readonly=False,
        string="Agentes",
    )