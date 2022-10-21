# -*- coding: utf-8 -*-

from odoo import _
from odoo.http import Response
from . import LIST_API_ERRORS
import json
import logging
_logger = logging.getLogger(__name__)


class SITResponse(object):
	def __init__(self, data:dict = None, http_status_code:str = None, errors:LIST_API_ERRORS = None, msg_code:str=None, msg_str:str=None):
		self.data = data or dict()
		self.errors = errors or LIST_API_ERRORS()
		self.http_status_code = http_status_code
		self.message_code = msg_code
		self.message_str = msg_str

	def formatted_response(self, data: dict = {}, errors: list=[], http_status_code:str=None, msg_code:str=None, msg_str:str=None):
		
		result = {
			'message_code' : msg_code or self.message_code or '',
			'message'      : msg_str or self.message_str or ''
		}

		if data:
			result['data']   = data
		if errors:
			result['errors'] = errors

		# Response.status = http_status_code if http_status_code else self.http_status_code
		# return result
		response = {
			'jsonrpc': '2.0',
			'result': result
		}

		mime = 'application/json'
		body = json.dumps(response)
		status = http_status_code if http_status_code else self.http_status_code
		return Response(body, status=status,
			headers=[('Content-Type', mime), ('Content-Length', len(body))]

			)
	def make_response(self):

		if not self.errors.isEmpty():
			return self.formatted_response(errors=self.errors.get_formatted_values(),
										   http_status_code=self.http_status_code or self.errors.get_http_status_code())
		else:
			return self.formatted_response(data=self.data,
											http_status_code=self.http_status_code  or '200')