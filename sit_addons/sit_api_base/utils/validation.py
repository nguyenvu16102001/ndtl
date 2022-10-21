# -*- coding: utf-8 -*- 

import re
from odoo import _
from enum import Enum, unique
from . import LIST_API_ERRORS, ENUM_API_ERRORS as ENUM_ERRORS

import logging, traceback
_logger = logging.getLogger(__name__)

@unique
class ENUM_FORMAT_TYPES(Enum):
    EMAIL           = (_("email"), r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_NUMBER_VN = (_("Vietnam's mobile phone number"),r'^(0[3|5|7|8|9])+([0-9]{8})$')

    def get_regex(self):
        if isinstance(self.value, tuple) and len(self.value) > 1:
            return self.value[1]
        else:
            return ""
    def get_title(self):
        if isinstance(self.value, tuple) and len(self.value) > 0:
            return self.value[0]
        else:
            return self.name

class Validation(object):
    def validate_require_params(self, payload=None, param_names:list=None):
        """ Validate required paramaters utility
        :param param_names list(): List of string or tuple param name that required

        :return LIST_API_ERRORS: Errors list
        """
        if not payload:
            payload = dict()
        errors = LIST_API_ERRORS()
        for param in param_names or []:
            if param not in payload:
                errors.append(ENUM_ERRORS.MISSING_REQUIRED_PARAMS, param)
        return errors

    def invalid_format(self, payload=None, param_name:str=None, param_format:ENUM_FORMAT_TYPES=None):
        """ Validate format of the provided param
        :param param_name str: Param's name
        :param param_format ENUM_FORMAT_TYPE: Format enum

        :return LIST_API_ERRORS: Errors list
        """
        if not payload:
            payload = dict()
        errors = LIST_API_ERRORS()
        if isinstance(param_format, ENUM_FORMAT_TYPES):
            regex = param_format.get_regex()
            value = payload.get(param_name)
            if value and not re.match(regex, value):
                errors.append(ENUM_ERRORS.INVALID_FORMAT_PARAM, (param_name, param_format.get_title()))
        return errors
