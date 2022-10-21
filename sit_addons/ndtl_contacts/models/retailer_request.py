from odoo import models, fields, api

class RetailerRequest(models.Model):
    _name = 'retailer.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Retailer request'
    
    name = fields.Char(string='Name',track_visibility='onchange')
    company = fields.Char(string='Company Name',track_visibility='onchange')
    email = fields.Char(string='Email',track_visibility='onchange')
    note = fields.Text(string='Note')
    phone = fields.Char(string='Phone Number',track_visibility='onchange')
    street = fields.Text(string='Street',track_visibility='onchange')
    state = fields.Selection([
        ('request', 'Request'),
        ('approval','Approval'),
        ('cancel','Cancel')
    ], default='request',track_visibility='onchange')
    approval_by = fields.Many2one('res.users',track_visibility='onchange')
    
    def retailer_registation(self,vals):
        # Check user in partner
        partner = self.env['res.partner'].search(['|','|',('name','=',vals.get('name')),('phone','=',vals.get('phone')),
                ('email','=',vals.get('email'))])
        if partner:
            return True,'Retailer already in system'
        # Check user in pendding form
        request = self.search(['|','|',('name','=',vals.get('name')),('phone','=',vals.get('phone')),
                ('email','=',vals.get('email'))])
        if request:
            return True,'Retailer requested, on pending, waitting for Administrator approval'
        return False,super(RetailerRequest,self).create(vals)

    def approval_form_request(self):
        # TODO: create partner, users and send email
        # create partner
        vals = {
            'name':self.name,
            'email':self.email,
            'phone':self.phone,
            'street':self.street
        }
        partner = self.env['res.partner'].create(vals)
        # create account link with partner
        data = {
            'login':vals.get('email'),
            'partner_id':partner.id
        }
        user = self.env['res.users'].create(data)
        self.write({
            'state': 'approval',
            'approval_by':self.env.context.get('uid')
        })


    def cancel_form_request(self):
        self.write({
            'state': 'cancel',
            'approval_by':self.env.context.get('uid')
        })
