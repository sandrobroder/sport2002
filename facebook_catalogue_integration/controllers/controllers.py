# -*- coding: utf-8 -*-
import base64

from odoo import http
from odoo.http import content_disposition


class FacebookCatalogueIntegration(http.Controller):
    @http.route('/shop/<int:catalogue_id>/feeds', auth='public')
    def index(self, catalogue_id, **kw):
        catalogue_obj = http.request.env['facebook.catalogue'].sudo().browse(catalogue_id)
        latest_attachment = catalogue_obj.catalogue_attachment_ids.filtered(lambda l: l.is_latest)
        if latest_attachment:
            file_name = latest_attachment.attachment_id.name
            encoded_file = latest_attachment.attachment_id.datas
            decoded_file = base64.b64decode(encoded_file)
            return http.request.make_response(decoded_file, [('Content-Type', 'text/csv'),
                                                             ('Content-Disposition', content_disposition(file_name))])
