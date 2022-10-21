# -*- coding: utf-8 -*-
from odoo import http

# class AuthJwt(http.Controller):
#     @http.route('/auth_jwt/auth_jwt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/auth_jwt/auth_jwt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('auth_jwt.listing', {
#             'root': '/auth_jwt/auth_jwt',
#             'objects': http.request.env['auth_jwt.auth_jwt'].search([]),
#         })

#     @http.route('/auth_jwt/auth_jwt/objects/<model("auth_jwt.auth_jwt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('auth_jwt.object', {
#             'object': obj
#         })