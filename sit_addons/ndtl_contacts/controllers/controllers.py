import json
import logging

from odoo import http
from odoo.http import request

from . import utils

_logger = logging.getLogger(__name__)


class NdtlContacts(http.Controller):

    @http.route("/api/registation/retailer", type="json", auth="none", csrf=False)
    def retailer_request(self):
        ''' Retailer using app will create the account with authorize retailer
            parameters:
                "name":String - Retailer's name,
                "phone":String - Retailer's phone number,
                "email":String - Retailer's email
            output:
                "id": Number - registration id,
                "name":String - Retailer's name,
                "phone":String - Retailer's phone number,
                "email":String - Retailer's email
        '''
        payload = request.jsonrequest
        if not all([payload.get("name"), payload.get("phone"), payload.get("email")]):
            return utils.responseMessage(1, "Missing required information", None)

        err, result = request.env["retailer.request"]\
                             .sudo().retailer_registation(payload)

        if err:
            return utils.responseMessage(1, result, None)

        return_msg = {
            "id": result.id,
            "name": result.name,
            "phone": result.phone,
            "email": result.email,
        }
        return utils.responseMessage(0, "", return_msg)
