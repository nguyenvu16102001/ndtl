# -*- coding: utf-8 -*-

from odoo import _, http
from enum import Enum, unique
from typing import List
from odoo.http import JsonRequest
from odoo.tools import ustr
import odoo, copy


import logging, traceback
_logger = logging.getLogger(__name__)

@unique
class ENUM_API_ERRORS(Enum):

    # 400 - Bad Request
    MISSING_REQUIRED_PARAMS     = (400, _("'%s' is required parameter"))
    INVALID_PARAM_VALUE         = (400, _("Invalid %s's value"))
    INVALID_FORMAT_PARAM        = (400, _("'%s' is invalid format of %s"))
    INVALID_PARAM_TYPE          = (400, _("'%s' must be type %s"))
    NOT_EXIST_RESOURCE          = (400, _("%s '%s' is not exist"))
    ACCESS_ANOTHER_WARRANTY     = (400, _("Cannot access to warranty that belong to another one"))
    NOT_BELONG_TO_OWNER         = (400, _("%s is not belong to %s"))
    CANNOT_TRANSFER_SAME_USER   = (400, _("The warranty cannot transfer to the same user"))
    NOT_ALLOW_TO_APPROVE        = (400, _("Your are not allowed to approve this %s"))
    NOT_READY_TO_PERFORM        = (400, _("%s is not ready to %s"))
    IN_STATUS_MODE              = (400, _("%s is in %s mode"))
    INVALID_FILE_FORMAT         = (400, _("The uploaded file must have a valid image format %s"))
    INVALID_PARAM_LENGTH        = (400, _("%s are required"))
    INVALID_UPDATE_DOCUMENT     = (400, _("You are updating an invalid document need update"))

    # 401 - Unauthorized
    INVALID_AUTHORIZATION_TOKEN = (401, _("Invalid Authorization Token"))
    INVALID_FORMAT_TOKEN        = (401, _("Invalid Format Token"))
    USER_NOT_EXIST_FIREBASE_UID = (401, _("User is missing firebase uid"))
    TOKEN_EXPIRED               = (401, _("Authorization Token is expired"))
    AUTH_FAILED                 = (401, _("Authentication is failed. The token is valid but no user related to it."))
    INVALID_FIREBASE_UID        = (401, _("Firebase UID is invalid. This should be extract from a valid token"))

    # 409 - Conflict
    EXISTED_RESOURCE            = (409, _("'%s' as '%s' is belong to another %s"))

    # 500 - Internal Server Error
    INTERNAL_SERVER_ERROR       = (500, _("Internal server error"))


    def get_formatted_values(self, args:tuple=None):
        msg_formated = self.value[1] if not args else self.value[1] % args
        msg_formated = msg_formated.strip()
        # Upercase first letter of sentence without lowercase the rest
        msg_formated = msg_formated[0].capitalize() + msg_formated[1:]
        return {
                'code': self.name,
                'msg': msg_formated
        }
    def get_status_code(self):
        return str(self.value[0])


class LIST_API_ERRORS(object):
    def __init__(self, errors:List[ENUM_API_ERRORS] = None, http_status_code: str = None):
        self.errors = errors or []
        self.http_status_code = http_status_code


    def get_formatted_values(self):
        lst = [x.get_formatted_values() if not isinstance(x,tuple)
                else x[0].get_formatted_values(x[1])
                for x in self.errors]
        return lst

    def get_list(self):
        return self.errors

    def append(self, error, params:tuple=None):
        if params:
            self.errors.append((error,params))
        else:
            self.errors.append(error)

    def extend(self, errors):
        if errors and isinstance(errors, list):
            self.errors.extend(errors)
        elif isinstance(errors, LIST_API_ERRORS) and not errors.isEmpty():

            self.errors.extend(errors.get_list())

    def get_http_status_code(self):
        if not self.http_status_code:
            if len(self.errors) > 0:
                if isinstance(self.errors[0],tuple):
                    self.http_status_code = self.errors[0][0].get_status_code() if len(self.errors) > 0 else ''
                else:
                    self.http_status_code = self.errors[0].get_status_code() if len(self.errors) > 0 else ''
        return self.http_status_code

    def set_http_statuts_code(self, status):
        self.http_status_code = status

    def isEmpty(self):
        return not self.errors


class APIAuthException(Exception):
    def __init__(self, code:ENUM_API_ERRORS=None, http_status_code:str=None):
        self.code = code
        self.http_status_code = http_status_code

    def get_formatted_values(self):
        return self.code.get_formatted_values()

    def get_http_status_code(self):
        return self.http_status_code or self.code.get_status_code()

