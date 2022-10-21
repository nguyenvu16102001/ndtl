import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class NdtlAnkerProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    product_number = fields.Char(string='Product Number')
    package_type = fields.Selection([
        ('package', 'Package'),
        ('box', 'Box'),
        ('product', 'Unit Product')],
        string='Packaging Unit',
        help='Are the products come in package, box, or single unit.'
    )
    external_link = fields.Char('External Link')