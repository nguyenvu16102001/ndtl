# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InheritedProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    attribute_value = fields.Char(
        string='Attribute Value', store=True,
        compute='_compute_attribute_value')

    @api.depends('attribute_id.name', 'name')
    def _compute_attribute_value(self):
        for record in self:
            record.attribute_value = '%s: %s' % (record.attribute_id.name, record.name)
        return True
