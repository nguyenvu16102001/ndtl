# -*- coding: utf-8 -*- 

from odoo.http import JsonRequest, Response
from odoo.tools import date_utils
import json

def _sit_json_response(self, result=None, error=None):
	if isinstance(result, Response):
		return result
	else:
		response = {
			'jsonrpc': '2.0',
			'id': self.jsonrequest.get('id')
			}
		if error is not None:
			response['error'] = error
		if result is not None:
			response['result'] = result

		if self.jsonp:
			# If we use jsonp, that's mean we are called from another host
			# Some browser (IE and Safari) do no allow third party cookies
			# We need then to manage http sessions manually.
			response['session_id'] = self.session.sid
			mime = 'application/javascript'
			body = "%s(%s);" % (self.jsonp, json.dumps(response, default=date_utils.json_default))
		else:
			mime = 'application/json'
			body = json.dumps(response, default=date_utils.json_default)

		return Response(
			body, status=error and error.pop('http_status', 200) or 200,
			headers=[('Content-Type', mime), ('Content-Length', len(body))]
		)
# Override core json request to adapt SIT API core. This will not impacte to backend
JsonRequest._json_response = _sit_json_response