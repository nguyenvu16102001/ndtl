# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class InheritedResPartner(models.Model):
    _inherit = "res.partner"

    tax_code = fields.Char('Tax Code')
    default_warehouse = fields.Many2one(
        string="Default Warehouse",
        comodel_name="stock.warehouse"
    )
    invoice_name = fields.Char(
        string="Invoice Name"
    )
    misa_code = fields.Char('Customer Code Misa')
    brand_payment_term = fields.One2many('res.partner.payment', 'partner_id')
                 
    country_district_id = fields.Many2one(comodel_name="district.state", string='Country District', domain="[('state_id', '=?', state_id)]")

    @api.onchange('country_district_id')
    def _onchange_country_id(self):
        if self.country_district_id.state_id:
            self.state_id = self.country_district_id.state_id

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id and self.state_id != self.country_district_id.state_id:
            self.country_district_id = False
        super(InheritedResPartner, self)._onchange_state()
        
    street = fields.Char(track_visibility="onchange")
    street2 = fields.Char(track_visibility="onchange")
    zip = fields.Char(change_default=True, track_visibility="onchange")
    city = fields.Char(track_visibility="onchange")
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]", track_visibility="onchange")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', track_visibility="onchange")

    brand_payment_term = fields.One2many('res.partner.payment', 'partner_id')
    
    incharge_person_ids = fields.Many2many('res.users', 'incharge_person_rel', 'partner_id', 'user_id',
                                               groups='base.group_system')

    def check_incharge_person(self, user_id):
        if self.sudo().incharge_person_ids and user_id not in self.sudo().incharge_person_ids:
            raise ValidationError(_('You are not assigned to handle this customer. Please contact the administrator.'))
        return True

    def create_user(self):
        email = self.email
        form_view_id = self.env.ref('ndtl_contacts.ndtl_wizard_res_partner_form').id
        return {
            'name': 'Create User',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard.res.partner.form',
            'views': [(form_view_id, 'form')],
            'target': 'new',
            'context':  {'default_email': email},
        }

class ResPartnerPayment(models.Model):
    _name = 'res.partner.payment'
    _order = 'sequence'
    _description = 'Payment Term'

    sequence = fields.Integer()
    partner_id = fields.Many2one('res.partner', 'Account Holder', ondelete='cascade', index=True, domain=['|', ('is_company', '=', True), ('parent_id', '=', False)], required=True)
    payment_term_id = fields.Many2one('account.payment.term', index=True, required=True)
    # brand_id   = fields.Many2one("product.brand")
    brand_id   = fields.Many2one("product.brand", index=True, required=True)
