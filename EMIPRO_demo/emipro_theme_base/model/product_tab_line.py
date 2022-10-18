from odoo import api, fields, models, tools, _
from odoo.tools.translate import html_translate


class ProductTabLine(models.Model):
    _name = "product.tab.line"
    _inherit = ['website.published.multi.mixin']
    _description = 'Product Tab Line'
    _order = "sequence, id"
    _rec_name = "tab_name"

    product_id = fields.Many2one('product.template', string='Product Template')
    tab_name = fields.Char("Tab Name", required=True, translate=True)
    tab_content = fields.Html("Tab Content", sanitize_attributes=False, translate=html_translate, sanitize_form=False)
    icon_content = fields.Html("Icon Content", translate=html_translate,
                               default='<span class="fa fa-info-circle mr-2"/>')
    website_ids = fields.Many2many('website', help="You can set the description in particular website.")
    sequence = fields.Integer('Sequence', default=1, help="Gives the sequence order when displaying.")
    tab_type = fields.Selection([('specific product', 'Specific Product'), ('global', 'Global')], string='Tab Type')

    def checkTab(self, currentWebsite, tabWebsiteArray):
        result = False
        if currentWebsite in tabWebsiteArray or len(tabWebsiteArray) == 0:
            result = True
        return result

    @api.onchange('tab_type')
    def onchange_tab_type(self):
        if self.tab_type == 'global':
            self.product_id = None
