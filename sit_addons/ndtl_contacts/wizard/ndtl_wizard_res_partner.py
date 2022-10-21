from odoo import api, fields, models, _, exceptions
import re
import logging

_logger = logging.getLogger(__name__)


class NdtlAnkerWizardResPartner(models.TransientModel):
    _name = "wizard.res.partner.form"
    _description = 'Wizard Res Partner Form'

    name = fields.Char()
    email = fields.Char(
        required=True
    )

    def create_account(self):
        email = self.email
        name = self.email.split('@')[0]
        partner_id = self._context.get('active_id', False)
        val = {'login': email, 'email': email, 'name': name}
        if self.env['res.users'].search([("login", "=", email)]):
            raise exceptions.ValidationError("Email existed!")
        elif self.env['res.users'].search([('partner_id', '=', partner_id)]):
            raise exceptions.ValidationError("The partner already has users!")
        else:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
            if match == None:
                raise exceptions.ValidationError('Not a valid E-mail ID')
            else:
                res = self.env['res.users'].create(val)
                res.partner_id = partner_id
