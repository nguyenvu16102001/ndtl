from email.policy import default
from odoo import models, fields, api

class CountryDistrict(models.Model):
    _description = "District state"
    _name = 'district.state'
    _order = 'code'

    name = fields.Char(string = 'District Name')
    code = fields.Char(string = 'District Code')
    state_id = fields.Many2one('res.country.state', string="State", store=True)
    inner_city = fields.Boolean(string="Inner city", default=False)
