# -*- coding: utf-8 -*-
from odoo import models
from odoo.http import Response, request
from ..utils import APIAuthException
import werkzeug
import json
import logging
_logger = logging.getLogger(__name__)

class SITIrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _handle_exception(cls, exception):

        if isinstance(exception, APIAuthException):
            
            response =  {
                'jsonrpc': '2.0',
                'result':{
                    'data': {},
                    'errors': [exception.get_formatted_values()]
                }
            }
            
            mime = 'application/json'
            body = json.dumps(response)
            status = exception.get_http_status_code() or '500'
            res= Response(
                body, status=status, headers=[('Content-Type', mime), ('Content-Length', len(body))]
            )
            _logger.info('type of response: {}'.format(type(res)))
            _logger.info(res.__dict__)
            return res
        elif request._request_type == 'json' and isinstance(exception,werkzeug.exceptions.NotFound):
            response =  {
                'jsonrpc': '2.0',
                'result':{
                    'data': {},
                    'errors': []
                }
            }
            mime = 'application/json'
            body = json.dumps(response)
            status = exception.code
            res= Response(
                body, status=status,
                headers=[('Content-Type', mime), ('Content-Length', len(body))]
            )
            return res
        else:
            return super(SITIrHttp, cls)._handle_exception(exception)

        