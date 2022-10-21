# -*- coding: utf-8 -*- 

import unittest,json
from odoo.tests import tagged
from odoo.tests.common import BaseCase,TransactionCase

from odoo.addons.sit_api_base import utils
from odoo.addons.sit_api_base.utils import ENUM_API_ERRORS
from odoo.addons.sit_api_base.utils import LIST_API_ERRORS
from odoo.addons.sit_api_base.utils import SITResponse


@tagged('post_install')
class TestSITAPIBase(BaseCase):

	def setUp(self):
		super(TestSITAPIBase, self).setUp()
		
	
	def test_util_exception_defautl_code(self):
		errors = LIST_API_ERRORS()
		errors.append(ENUM_API_ERRORS.INVALID_AUTHORIZATION_TOKEN)
		self.assertEqual(errors.get_http_status_code(), '401')

	
	def test_util_exception_default_code_empty_list(self):
		errors = LIST_API_ERRORS()
		self.assertEqual(errors.get_http_status_code(), '')
		

	def test_util_exception_new_code(self):
		errors = LIST_API_ERRORS([ENUM_API_ERRORS.INVALID_FORMAT_TOKEN],'402')
		self.assertEqual(errors.get_http_status_code(), '402')

	def test_util_exception_formatted_values(self):
		errors = LIST_API_ERRORS()
		errors.append(ENUM_API_ERRORS.INVALID_AUTHORIZATION_TOKEN)
		expected = [
					{
						'code': ENUM_API_ERRORS.INVALID_AUTHORIZATION_TOKEN.name,
						'msg': ENUM_API_ERRORS.INVALID_AUTHORIZATION_TOKEN.value[1]
					}
			]
		self.assertEqual(expected, errors.get_formatted_values())
	
	def test_util_exception_formatted_values_2(self):
		errors = LIST_API_ERRORS()
		errors.append(ENUM_API_ERRORS.INVALID_AUTHORIZATION_TOKEN)
		errors.append(ENUM_API_ERRORS.USER_NOT_EXIST_FIREBASE_UID)
		expected = [
					{
						'code': ENUM_API_ERRORS.INVALID_AUTHORIZATION_TOKEN.name,
						'msg': ENUM_API_ERRORS.INVALID_AUTHORIZATION_TOKEN.value[1]
					},
					{
						'code': ENUM_API_ERRORS.USER_NOT_EXIST_FIREBASE_UID.name,
						'msg': ENUM_API_ERRORS.USER_NOT_EXIST_FIREBASE_UID.value[1]
					}
			]
			
		
		print("Error list formatted: ", errors.get_formatted_values())
		self.assertEqual(expected, errors.get_formatted_values())

	def test_utils_response_1(self):
		res = SITResponse()
		self.assertEqual(res.make_response(), {'http_status_code':'200'})


	def test_utils_response_2(self):
		errors = LIST_API_ERRORS()
		errors.append(ENUM_API_ERRORS.USER_NOT_EXIST_FIREBASE_UID)
		res = SITResponse(errors=errors)
		
	
		expected = {
				'http_status_code':'401',
				
				'errors':[
					ENUM_API_ERRORS.USER_NOT_EXIST_FIREBASE_UID.get_formatted_values()
				]
		}
		print('Response with errors: ', res.make_response())
		self.assertEqual(res.make_response(), expected)

	def test_utils_response_3(self):
		errors = LIST_API_ERRORS()
		errors.append(ENUM_API_ERRORS.USER_NOT_EXIST_FIREBASE_UID)
		res = SITResponse(errors=errors,http_status_code='403')
		
	
		expected = {
				'http_status_code':'403',
				
				'errors':[
					ENUM_API_ERRORS.USER_NOT_EXIST_FIREBASE_UID.get_formatted_values()
				]
		}
		self.assertEqual(res.make_response(), expected)

	def test_utils_response_4(self):
		data = {
			'product': {
				'name': 'IPhone 11',
				'price': '$5000'
			}
		}
		
		res = SITResponse(data=data)
		
	
		expected = {
				'http_status_code':'200',
				'data': data,
				
		}
		print('Resonse format: ', res.make_response())
		self.assertEqual(res.make_response(), expected)


