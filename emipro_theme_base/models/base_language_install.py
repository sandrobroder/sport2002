# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class BaseLanguageInstall(models.TransientModel):
    _inherit = "base.language.install"

    def lang_install(self):
        action = super(BaseLanguageInstall, self).lang_install()
        menu = self.env['website.menu'].search([('is_mega_menu', '=', True), ('dynamic_mega_menu', '=', True)])
        for m in menu:
            m._set_field_is_mega_menu_overrided()
        return action
