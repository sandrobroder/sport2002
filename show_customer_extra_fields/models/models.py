# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    credito_y_caucion = fields.Boolean()
    cesce_credito = fields.Boolean()
    solunion_credito = fields.Boolean()


class AccountMove(models.Model):
    _inherit = "account.move"

    credito_y_caucion = fields.Boolean(compute="compute_extra_fields", store=True, precompute=True, readonly=False)
    cesce_credito = fields.Boolean(compute="compute_extra_fields", store=True, precompute=True, readonly=False)
    solunion_credito = fields.Boolean(compute="compute_extra_fields", store=True, precompute=True, readonly=False)

    @api.depends("partner_id")
    def compute_extra_fields(self):
        for rec in self:
            if rec.partner_id:
                rec.credito_y_caucion = rec.partner_id.credito_y_caucion
                rec.cesce_credito = rec.partner_id.cesce_credito
                rec.solunion_credito = rec.partner_id.solunion_credito
            else:
                rec.credito_y_caucion = False
                rec.cesce_credito = False
                rec.solunion_credito = False
