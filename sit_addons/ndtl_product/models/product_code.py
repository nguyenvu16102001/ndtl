# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductCode(models.Model):
    _name = 'product.product.code'
    _description = 'Product List Default Codes'

    name = fields.Char(string='Code', required=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product', required=True)
