# -*- coding: utf-8 -*-
import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime as dt

from odoo import models


class AuthJwt(models.AbstractModel):
    _name = 'auth.jwt'
    _description = 'JWT Authentication'

    def secret(self):
        secret_key = self.env['ir.config_parameter'].sudo().get_param('jwt_secret')
        return secret_key

    def generate_token(self, uid):
        secret_key = self.secret()
        user = self.env['res.users'].browse(uid)
        payload = {
            'uid': uid,
            'pid': user.partner_id.id,
            'name': user.name,
            'iat': dt.utcnow()
        }
        # body['exp'] = dt.utcnow() + datetime.timedelta(hours=6)
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        token = str(token, 'UTF-8')
        return token

    def validate(self, token):
        secret_key = self.secret()
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        except InvalidTokenError:
            raise
        except Exception:
            raise
        return payload
