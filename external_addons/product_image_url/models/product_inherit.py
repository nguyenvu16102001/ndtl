# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Nilmar Shereef(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
import base64
import requests
from PIL import Image
# from StringIO import StringIO
from io import BytesIO, StringIO
from odoo import models, fields, api
from odoo.exceptions import Warning


import logging
_logger = logging.getLogger(__name__)


class ProductTemplateImageUrl(models.Model):
    _inherit = 'product.template'

    web_url = fields.Char(string='Web URL', help='Automatically sanitized HTML contents', copy=False)

    def write(self, vals):
        if vals.get('web_url'):
            image_url = vals['web_url']
            try:
                resp = requests.get(image_url)
                image = base64.b64encode(resp.content).decode("ascii")
                vals['image'] = image
            except Exception:
                _logger.debug('Incorrect image url')
        res = super(ProductTemplateImageUrl, self).write(vals)
        return res


class ProductProductImageUrl(models.Model):
    _inherit = 'product.product'

    variant_web_url = fields.Char(string='Variant Image URL', copy=False,
                                  help='Automatically sanitized HTML contents')

    image_url = fields.Char('Image URL', compute='_compute_image_url')

    def _compute_image_url(self):
        for record in self:
            image_url = record.get_image_public_url()
            record.image_url = image_url

    def _get_medium_image_public_url(self, size='image_medium'):
        root_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        image_url = '/web/image?model=product.product&field=%s&id=%s' % (size, self.id)
        return root_url + image_url

    def get_image_public_url(self):
        """ Get product variant public url, always use variant image if available.

        :param self: product.product recordset
        :return res: dictionary with key is product id, and value is variant image url
        """
        if self.web_url and not self.variant_web_url:
            url = self.web_url
        elif not self.web_url and self.variant_web_url:
            url = self.variant_web_url
        else:
            url = self._get_medium_image_public_url()
        return url

    def write(self, vals):
        if vals.get('variant_web_url'):
            image_url = vals['variant_web_url']
            try:
                resp = requests.get(image_url)
                image = base64.b64encode(resp.content).decode("ascii")
                vals['image_variant'] = image
            except Exception:
                _logger.debug('Incorrect image url')
        res = super(ProductProductImageUrl, self).write(vals)
        return res
