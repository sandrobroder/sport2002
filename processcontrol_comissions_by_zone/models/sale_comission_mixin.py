# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("order_id.partner_id", "product_id")
    def _compute_agent_ids(self):
        agent_ids = []
        domain_agent_ids = []
        # for resetting previous agents
        for record in self.filtered(lambda x: x.order_id.partner_id):
            record.agent_ids = False
            partner = record.order_id.partner_id
            if not record.commission_free:
                domain_agent_ids = record._prepare_agents_vals_partner(
                    record.order_id.partner_id
                )
                # chequeo que los agentes en la ficha del cliente, esten dentro de la marca:
                if record.product_id.product_tmpl_id.categ_id.agent_ids:
                    if domain_agent_ids:
                        for agent in record.product_id.product_tmpl_id.categ_id.agent_ids:
                            if agent.id in domain_agent_ids:
                                agent_ids.append(agent)
                if not agent_ids:
                    record.agent_ids = domain_agent_ids
                else:
                    record.agent_ids = agent_ids

    @api.onchange('product_id')
    def product_id_change(self):
        for rec in self:
            super(SaleOrderLine, self).product_id_change()
            rec._compute_agent_ids()


