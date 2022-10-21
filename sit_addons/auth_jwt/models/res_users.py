from odoo import models, fields


class InheritedResUsers(models.Model):
    _inherit = 'res.users'

    firebase_uid = fields.Char('Firebase UID')

    _sql_constraints = [
        ('firebase_uid_unique', 'unique (firebase_uid)', 'Firebase UID Exist.')
    ]