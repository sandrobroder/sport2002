from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_cyc = fields.Boolean(string='CyC')
    x_cesce = fields.Boolean(string='CESCE')

    @api.onchange('partner_id')
    def onchange_invoice_partner_information(self):
        for rec in self:
            if rec.partner_id:
                rec.x_cyc = rec.partner_id.x_cyc
                rec.x_cesce= rec.partner_id.x_cesce

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends("move_id.partner_id",'commission_free')
    def _compute_agent_ids(self):
        agent_ids = []
        domain_agent_ids = []
        # for resetting previous agents
        for record in self.filtered(lambda x: x.move_id.partner_id):
            record.agent_ids = False
            partner = record.move_id.partner_id
            if not record.commission_free:
                domain_agent_ids = record._prepare_agents_vals_partner(
                    record.move_id.partner_id
                )
                product_template_id = record.product_id.product_tmpl_id
                # chequeo que los agentes en la ficha del cliente, esten dentro de la marca:
                if product_template_id.categ_id.agent_ids:
                    if domain_agent_ids:
                        for agent in product_template_id.categ_id.agent_ids:
                            if (agent.id in domain_agent_ids):
                                agent_ids.append(agent)
                if not agent_ids:
                    record.agent_ids = domain_agent_ids
                else:
                    record.agent_ids = agent_ids

    def recompute_agents(self):
        self._compute_agent_ids()
