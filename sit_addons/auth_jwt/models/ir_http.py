# -*- coding: utf-8 -*-
import os
import logging
import werkzeug

from odoo import models, http
from odoo.http import request, Response
from odoo.exceptions import ValidationError
from odoo.tools import config
from odoo.exceptions import AccessDenied, AccessError
from odoo.addons.sit_api_base.utils import ENUM_API_ERRORS as ENUM_ERRORS
from odoo.addons.sit_api_base.utils import LIST_API_ERRORS as ERRORS
from odoo.addons.sit_api_base.utils import SITResponse
from odoo.addons.sit_api_base.utils import APIAuthException

_logger = logging.getLogger(__name__)

try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import auth

    firebase_config_path = (
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        or config.get("firebase_config_path")
    )
    firebase_app_name = (
        os.getenv("FIREBASE_APP_NAME")
        or config.get("firebase_app_name")
    )
    _logger.info("Use firebase config at path %s" % firebase_config_path)
    if not firebase_config_path:
        _logger.error("Firebase configuration file path not found.")
        raise ValidationError("Cannot find firebase configuration path")

    cred = credentials.Certificate(firebase_config_path)

    firebase_admin.initialize_app(cred, name=firebase_app_name or "NDTL")

    ndtl_app = firebase_admin.get_app(firebase_app_name or "NDTL")
    _logger.info("Successfully initializing app %s" % ndtl_app.project_id)

except ImportError:
    _logger.error("SDK isn't available, cannot use Firebase Auth.")
except Exception:
    _logger.error("Failed trying to initialize application", exc_info=True)


class InheritedIrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_jwt(cls):
        bearer = request.httprequest.headers.get('Authorization', '')
        if not bearer or not bearer.startswith('Bearer '):
            raise http.AuthenticationError('Invalid Authorization Token')
        # bearer has the format of `Bearer <TOKEN>`
        token = bearer[7:]
        if not token:
            raise http.AuthenticationError('Invalid Authorization Token')
        try:
            ndtl_client = auth.Client(firebase_admin.get_app(firebase_app_name or "NDTL"))
            decoded_token = ndtl_client.verify_id_token(token)
        except Exception:
            _logger.error("Failed verifying token", exc_info=True)
            raise http.AuthenticationError('Invalid Authorization Token')
        firebase_uid = decoded_token['uid']
        user = request.env['res.users'].search(
            [('firebase_uid', '=', firebase_uid)], limit=1)
        request.uid = user.id
        if not request.uid:
            raise http.AuthenticationError('Invalid Authorization Token')
    
    @classmethod
    def _auth_method_jwt2(cls):
        bearer = request.httprequest.headers.get('Authorization', '')
        if not bearer or not bearer.startswith('Bearer '):

            raise APIAuthException(ENUM_ERRORS.INVALID_FORMAT_TOKEN)
        # bearer has the format of `Bearer <TOKEN>`
        token = bearer[7:]
        if not token:
            raise APIAuthException(ENUM_ERRORS.INVALID_FORMAT_TOKEN)
        try:
            ndtl_client = auth.Client(firebase_admin.get_app(firebase_app_name or "NDTL"))
            decoded_token = ndtl_client.verify_id_token(token)
        except auth.ExpiredIdTokenError:
            _logger.warning("ID Token is expired")
            raise APIAuthException(ENUM_ERRORS.TOKEN_EXPIRED)
        except Exception as ex:
            _logger.warning("Failed verifying token")
            _logger.warning(str(ex))
            raise APIAuthException(ENUM_ERRORS.INVALID_AUTHORIZATION_TOKEN)

        firebase_uid = decoded_token['uid']
        user = request.env['res.users'].search(
            [('firebase_uid', '=', firebase_uid)], limit=1)
        
        if not user:
            raise APIAuthException(ENUM_ERRORS.AUTH_FAILED)
        
        request.uid = user.id
        request.pid = user.partner_id.id


    @classmethod
    def _authenticate(cls, auth_method='user'):
        try:
            if request.session.uid:
                try:
                    request.session.check_security()
                    # what if error in security.check()
                    #   -> res_users.check()
                    #   -> res_users._check_credentials()
                except (AccessDenied, http.SessionExpiredException):
                    # All other exceptions mean undetermined status (e.g. connection pool full),
                    # let them bubble up
                    request.session.logout(keep_db=True)
            if request.uid is None:
                getattr(cls, "_auth_method_%s" % auth_method)()
        except (AccessDenied, http.SessionExpiredException, werkzeug.exceptions.HTTPException):
            raise
        # SIT Custom API Exception and remaining code is copied from core odoo
        except APIAuthException:
            raise
        except Exception:
            _logger.info("Exception during request Authentication.", exc_info=True)
            raise AccessDenied()
        return auth_method

    @classmethod
    def get_user_firebase_by_uid(cls, uid):
        user = None
        try:
            ndtl_client = auth.Client(firebase_admin.get_app(firebase_app_name or "NDTL"))
            user = ndtl_client.get_user(uid)
        except auth.UserNotFoundError as ex:
            _logger.warning(str(ex))
        return user
