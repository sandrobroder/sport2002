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