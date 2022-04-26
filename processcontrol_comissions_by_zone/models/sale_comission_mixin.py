# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from logging import getLogger
_logger=getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("order_id.partner_id", "product_template_id")
    def _compute_agent_ids(self):
        agent_ids = []
        domain_agent_ids = []
        # for resetting previous agents
        for record in self.filtered(lambda x: x.order_id.partner_id):
            record.agent_ids = False
            if not record.commission_free:
                domain_agent_ids = record._prepare_agents_vals_partner(
                    record.order_id.partner_id
                )
                _logger.info('CATEGORIAS AGENTES %s', record.product_template_id.categ_id.agent_ids)
                _logger.info('DOMAIN AGENTES %s', domain_agent_ids)
                # chequeo que los agentes en la ficha del cliente, esten dentro de la marca:
                if record.product_template_id.categ_id.agent_ids:
                    for agent in record.product_template_id.categ_id.agent_ids:
                        if agent.id in domain_agent_ids:
                            agent_ids.append(agent)
                if agent_ids:
                    record.agent_ids = agent_ids



