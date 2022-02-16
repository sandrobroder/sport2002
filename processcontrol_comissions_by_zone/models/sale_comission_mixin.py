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


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("order_id.partner_id","product_template_id")
    def _compute_agent_ids(self):
        agent_ids = []
        self.agent_ids = False  # for resetting previous agents
        for record in self.filtered(lambda x: x.order_id.partner_id):
            partner = record.order_id.partner_id
            if not record.commission_free:
                #chequeo si el producto seleccionado, tiene en la categoria configurado el agente y si tiene configurado agente en la provicia del cliente
                if record.product_template_id.categ_id.agent_ids and partner.state_id and partner.state_id.agent_ids:
                    for agent in record.product_template_id.categ_id.agent_ids:
                        if agent.id in partner.state_id.agent_ids.ids and agent not in agent_ids:
                            agent_ids.append(agent)
                    if agent_ids:
                        record.agent_ids = [(0, 0, agent) for agent in agent_ids]
                    else:
                        record.agent_ids= [(0, 0, self._prepare_agent_vals(agent)) for agent in partner.agent_ids]
                else:
                    record.agent_ids = record._prepare_agents_vals_partner(
                        record.order_id.partner_id
                    )