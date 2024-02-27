# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    commission_free = fields.Boolean(string="Free of commission", default=False)


class ProductCategory(models.Model):
    _inherit = "product.category"

    agent_ids = fields.Many2many("res.partner", domain="[('agent', '=', True)]")
    commission_percent = fields.Float()

    def get_categ_agent(self, agents):
        if self.agent_ids and self.agent_ids & agents:
            return self.agent_ids & agents
        elif self.parent_id:
            return self.parent_id.get_categ_agent(agents)
        else:
            return self.env["res.partner"]

    def get_categ_commission(self):
        if self.commission_percent:
            return self.commission_percent
        elif self.parent_id:
            return self.parent_id.get_categ_commission()
        else:
            return 0
