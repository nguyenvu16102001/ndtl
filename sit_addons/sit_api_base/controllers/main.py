# -*- coding: utf-8 -*-

import json
import logging
import requests
import jwt
import re
from typing import List

from odoo import http
from odoo.http import request, Response
from odoo.service import security
from odoo.addons.sit_api_base.utils import ENUM_API_ERRORS as ENUM_ERRORS
from odoo.addons.sit_api_base.utils import LIST_API_ERRORS as ERRORS
from odoo.addons.sit_api_base.utils import ENUM_FORMAT_TYPES
from odoo.addons.sit_api_base.utils import SITResponse, SITRequest, Validation


_logger = logging.getLogger(__name__)

class BaseAPI(http.Controller):

	def __init__(self):
		self.ENUM_ERRORS = ENUM_ERRORS
		self.ENUM_FORMAT_TYPES = ENUM_FORMAT_TYPES
		self.validation = Validation()


	def _get_params(self, payload:dict=None, required_params:list=None, optional_params:list=None):
		""" Returns list of values get from payload based on required & optional params in order
		:return list
		"""

		return SITRequest.get_params(payload or dict(), required_params or list(), optional_params or list())

	def _validate_required_params(self, payload=None, param_names:list=None):
		"""
		:return LIST_API_ERRORS
		"""
		return self.validation.validate_require_params(payload or dict(), param_names or list())

	def _validate_type_params(self, payload:dict=None, param_and_type:List[tuple]=None):
		errors = ERRORS()
		if not payload:
			payload = dict()
		if not param_and_type:
			param_and_type = list()
		if isinstance(param_and_type, list):
			for p in param_and_type:
				if p and isinstance(p, tuple):
					if p[0] in payload:
						# Not use isinstance because of True/False also instance of int
						if type(payload.get(p[0])) != p[1]:
							errors.append(ENUM_ERRORS.INVALID_PARAM_TYPE,(p[0],p[1].__name__))

		return errors

	def _validate_format_params(self, payload:dict=None, param_name_format:List[tuple]=None):
		"""Validate parameter's value format following the param name and format

		:param payload dict: Request Payload
		:param param_name_format list(tuple):
			Ex. [('email',ENUM_FORMAT_TYPES.EMAIL),
				 ('phone_number',ENUM_FORMAT_TYPES.PHONE_NUMBER_VN)]

		:return LIST_API_ERRORS
		"""
		errors = ERRORS()
		if not payload:
			payload = dict()
		if not param_name_format:
			param_name_format = list()
		if isinstance(param_name_format, list):
			for p in param_name_format:
				if p and isinstance(p, tuple):
					invalid_format_err = self.validation.invalid_format(payload = payload,
															param_name = p[0],
															param_format = p[1])

					errors.extend(invalid_format_err)
		return errors

	def prepare_data(self, payload, required_params, optional_params=None, validate_format_params=None, param_types=None):
		""" This method used to extra data from payload following provided params.
		Also validate required params or format of vale

		:param payload: Request's payload
		:param required_params list: List of required parameter name
		:param optional_params list: List of optional parameter name
		:param validate_format_params list: List of tuple that contain parameter name and format type
			Ex. [('email',ENUM_FORMAT_TYPES.EMAIL),
				 ('phone_number',ENUM_FORMAT_TYPES.PHONE_NUMBER_VN)]
		:param param_types list: List of type that contain prameter name and type of param
			Ex. [('email',str),('id',int),('price',float)]


		:return list of parameter's value and errors: Ex. ['param_value1','param_value2',None,LIST_API_ERRORS()]
		Errors object is the last element in return list.
		"""
		errors = ERRORS()
		invalid_type_errors = ERRORS()
		# Validate Required Parameters
		errors.extend(self._validate_required_params(payload, required_params))
		# Validate format value of parameters

		if param_types:
			invalid_type_errors = self._validate_type_params(payload, param_types)
			errors.extend(invalid_type_errors)
		if invalid_type_errors.isEmpty() and validate_format_params:
			errors.extend(self._validate_format_params(payload, validate_format_params))
		# Get parameter's value base on the following required and optional params
		param_values = self._get_params(payload, required_params, optional_params)
		results = param_values
		results.append(errors)
		return results

	def make_response(self, data=None, errors=None, status_code:str=None, msg_code:str=None, msg_str:str=None):
		return SITResponse(data=data,
						   errors=errors,
						   http_status_code=status_code,
						   msg_code=msg_code,
						   msg_str=msg_str).make_response()

	def raise_server_error(self, ex:Exception, msg_code:str=None, msg_str:str=None):
		_logger.error(str(ex),exc_info=True)
		errors = ERRORS([ENUM_ERRORS.INTERNAL_SERVER_ERROR])
		return SITResponse(errors=errors, msg_code=msg_code, msg_str=msg_str).make_response()
