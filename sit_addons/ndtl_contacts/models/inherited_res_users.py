# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class InheritedResUsers(models.Model):
    _inherit = "res.users"

    default_shipping = fields.Selection(
        [
            ("many", "Deliver products many times"),
            ("one", "Deliver all products at once"),
        ],
        string="Default Shipping Progress",
        default="one",
    )
    sale_authorization_ids = fields.One2many(comodel_name='res.users.sale.authorization',
                                             inverse_name='res_user_id')
    stock_authorization_ids = fields.One2many(comodel_name='res.users.stock.authorization',
                                              inverse_name='res_user_id')

    @api.multi
    def write(self, values):
        super(InheritedResUsers, self).write(values)
        # clear caches linked to the users
        self.env['ir.model.access'].call_cache_clearing_methods()
        self.env['ir.rule'].clear_caches()
        self.has_group.clear_cache(self)

    def get_authorized_sa_owner(self):
        owner_list = [False, self.id]
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_agreement')
        if rules:
            for owner in rules[0].owner_ids:
                owner_list.append(owner.id)
        return owner_list

    def get_authorized_sa_partner(self):
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_agreement')
        if rules and rules[0].partner_ids:
            partner_list = rules.partner_ids.ids
        else:
            partner_list = self.env['res.partner'].sudo().search([('parent_id', '=', False)]).ids
        return partner_list

    def get_authorized_so_owner(self):
        owner_list = [False, self.id]
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_order')
        if rules:
            for owner in rules[0].owner_ids:
                owner_list.append(owner.id)
        return owner_list

    def get_authorized_so_partner(self):
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_order')
        if rules and rules[0].partner_ids:
            partner_list = rules.partner_ids.ids
        else:
            partner_list = self.env['res.partner'].sudo().search([('parent_id', '=', False)]).ids
        return partner_list

    def get_authorized_sa_owner_all_leads(self):
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_agreement')
        if rules and rules[0].owner_ids:
            owner_list = rules[0].owner_ids.ids
        else:
            owner_list = self.env['res.users'].sudo().search([]).ids
        return owner_list

    def get_authorized_sa_partner_all_leads(self):
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_agreement')
        if rules and rules[0].partner_ids:
            partner_list = rules.partner_ids.ids
        else:
            partner_list = self.env['res.partner'].sudo().search([('parent_id', '=', False)]).ids
        return partner_list

    def get_authorized_so_owner_all_leads(self):
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_order')
        if rules and rules[0].owner_ids:
            owner_list = rules[0].owner_ids.ids
        else:
            owner_list = self.env['res.users'].sudo().search([]).ids
        return owner_list

    def get_authorized_so_partner_all_leads(self):
        rules = self.sale_authorization_ids.filtered(lambda x: x.document_type == 'sale_order')
        if rules and rules[0].partner_ids:
            partner_list = rules.partner_ids.ids
        else:
            partner_list = self.env['res.partner'].sudo().search([('parent_id', '=', False)]).ids
        return partner_list

    def get_stock_authorized(self):
        stock_picking_type_list = []
        rules = self.stock_authorization_ids
        if rules:
            for rule in rules:
                stock_picking_type_list.extend(rule.stock_picking_type_ids.ids)
        else:
            stock_picking_type_list = self.env['stock.picking.type'].sudo().search([]).ids
        return stock_picking_type_list


class ResUsersSaleAuthorization(models.Model):
    _name = "res.users.sale.authorization"
    _description = "Sale Authorization"

    res_user_id = fields.Many2one(comodel_name='res.users')
    document_type = fields.Selection([
        ('sale_agreement', 'Sale Agreement'),
        ('sale_order', 'Sale Order'),
    ],
        required=True,
        string='Document Type'
    )
    owner_ids = fields.Many2many('res.users', 'sale_authorization_res_user_rel', 'sale_authorization_id',
                                 'owner_id', string='Owner')
    partner_ids = fields.Many2many('res.partner', 'sale_authorization_res_partner_rel',
                                   'sale_authorization_id', 'partner_id',
                                   domain=[('parent_id', '=', False)],
                                   string='Partner')


class ResUsersStockAuthorization(models.Model):
    _name = "res.users.stock.authorization"
    _description = "Stock Authorization"

    res_user_id = fields.Many2one(comodel_name='res.users')

    stock_warehouse_id = fields.Many2one('stock.warehouse', required=True, string='Warehouse')
    stock_picking_type_ids = fields.Many2many('stock.picking.type', 'stock_authorization_stock_picking_type_rel',
                                              'stock_authorization_id', 'stock_picking_type_id',
                                              string='Stock Picking Type')
