# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class InheritedProductProduct(models.Model):
    _name = 'product.product'
    _inherit = "product.product"

    product_code_ids = fields.One2many(
        comodel_name='product.product.code',
        inverse_name='product_id',
        string='Product Codes')
    contained_product_ids = fields.One2many(
        comodel_name='product.product.package',
        inverse_name='packaging_id',
        string='Material Products')
    unique_product_qty = fields.Float(
        string='Total Contained',
        compute='_compute_unique_product_qty',
        store=True,
        digits=dp.get_precision('Product Unit of Measure'))
    total_contained_qty = fields.Float(
        string='Total Contained Quantity',
        compute='_compute_total_contained_qty',
        digits=dp.get_precision('Product Unit of Measure'))
    like_product_ids = fields.Many2many(
        comodel_name='product.product',
        relation='like_products',
        column1='product_id',
        column2='like_product_id',
        string='Like Products')
    is_not_unbuild_suggest = fields.Boolean(string='Not Unbuild Suggest')

    @api.depends('contained_product_ids')
    def _compute_unique_product_qty(self):
        for record in self:
            record.unique_product_qty = len(record.contained_product_ids)

    @api.depends('contained_product_ids')
    def _compute_total_contained_qty(self):
        for record in self:
            record.total_contained_qty = sum(record.contained_product_ids.mapped('quantity'))

    def get_product_by_lot(self, barcode):
        result = {
            'code': barcode,
            'product': {}
        }
        lot = self.env['stock.production.lot'].search([('name', '=', barcode)], limit=1)
        if not lot:
            return result
        result.update({
            'product': {
                'id': lot.product_id.id,
                'name': lot.product_id.name,
                'price': lot.product_id.list_price
            }
        })
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        res = super(InheritedProductProduct, self)._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
        if name and not res:
            # If no results, try to find product in the product code definition
            product_codes = self.env['product.product.code']._search(
                [('name', '=', name)], access_rights_uid=name_get_uid)
            if product_codes:
                product_ids = self._search([('product_code_ids', 'in', product_codes)],
                                           limit=limit, access_rights_uid=name_get_uid)
                res += self.browse(product_ids).name_get()
        return res
