# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    ref_unique_code = fields.Char("Ref. Unique Code")

    @api.model
    def create(self, vals):
        vals['ref_unique_code'] = self.env['ir.sequence'].next_by_code('res.partner.code')
        result = super(ResPartner, self).create(vals)
        return result


class CustomerCodeSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def generate_code(self):
        res = self.env['res.partner'].sudo().search([('ref_unique_code', '=', False)])

        for rec in res:
            if not rec.ref_unique_code:
                sequence_obj = self.env['ir.sequence']
                code = sequence_obj.next_by_code('res.partner.code')
                rec.write({'ref_unique_code': code})
        return True
