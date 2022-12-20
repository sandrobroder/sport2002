# -*- coding: utf-8 -*-
import base64

from odoo import http
from odoo.http import content_disposition


class FacebookCatalogueIntegration(http.Controller):
    @http.route('/shop/<int:catalogue_id>/feeds', auth='public')
    def index(self, catalogue_id, **kw):
        catalogue_obj = http.request.env['facebook.catalogue'].sudo().browse(catalogue_id)
        file_name = catalogue_obj.file_name
        encoded_file = catalogue_obj.attachment
        decoded_file = base64.b64decode(encoded_file)
        return http.request.make_response(decoded_file, [('Content-Type', 'text/csv'),
                                                         ('Content-Disposition', content_disposition(file_name))])
