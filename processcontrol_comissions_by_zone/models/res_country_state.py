
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    agent_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="partner_agent_rel2",
        column1="partner_id",
        column2="agent_id",
        domain=[("agent", "=", True)],
        readonly=False,
        string="Agentes",
    )