# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.addons import decimal_precision as dp


class ProductProductPackage(models.Model):
    _name = 'product.product.package'
    _description = 'Product Packaging'

    packaging_id = fields.Many2one(
        comodel_name='product.product',
        string='Packaging')
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product')
    quantity = fields.Float(
        string='Quantity', default=1.00,
        digits=dp.get_precision('Product Unit of Measure'))
