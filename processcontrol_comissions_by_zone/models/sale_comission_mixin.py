# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class SaleCommissionMixin(models.AbstractModel):
    _inherit = "sale.commission.mixin"

    def _prepare_agents_vals_partner(self, partner):
        if partner.state_id:
            if partner.state_id.agent_ids:
                return [(0, 0, self._prepare_agent_vals(agent)) for agent in partner.state_id.agent_ids]
        return [(0, 0, self._prepare_agent_vals(agent)) for agent in partner.agent_ids]