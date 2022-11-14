import requests
import json
import traceback
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
class SapRef(models.TransientModel):
    _name = 'cron.sap'

    required_fields = ["Cellular"]
    sessionId = None

    def _login(self):
        url = "https://analytics10.uneeccch.com:50000/b1s/v1/Login"

        payload = json.dumps({
            "CompanyDB": self.env['ir.config_parameter'].sudo().get_param('SAP.CompanyDB'),
            "UserName": self.env['ir.config_parameter'].sudo().get_param('SAP.UserName'),
            "Password": self.env['ir.config_parameter'].sudo().get_param('SAP.Password')

        })
        headers = {
            'Accept': 'application/json',
            'Cache-Control': 'no-cache',
            'Postman-Token': '<calculated when request is sent>',
            'Content-Type': 'application/json'
        }
        print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        sessionId = response.json().get("SessionId")

    def _makeRequest(self, endpoint, payload):
        headers = {
            'Content-Type': 'application/json',
            'B1SESSION': SapRef.sessionId
        }
        url = "https://analytics10.uneeccch.com:50000/b1s/v1/" + endpoint
        response = requests.request("POST", url, headers=headers, data=payload).json()
        return response

    def _makeRequestWithRetry(self, endpoint, payload):
        try:
            response = SapRef._makeRequest(endpoint, payload)
            if response.status_code is 401:
                self._login()
                self._makeRequest(endpoint, payload)
        except:
            tb = traceback.format_exc()
            _logger.error(tb)
            raise ValueError("Login not allowed") #Todo: return message from sap

    def create_customer(self, payload):
        for val in payload:
            if payload[val] is None and val not in self.required_fields:
                raise ValueError("Fields are not complete")

        response = SapRef._makeRequestWithRetry("BusinessPartners", payload)

        return response

    def build_customer_request(self, code):
        self.env.cr.execute('''select code,name from res_country_state where l10n_in_tin=%s;'''%code)
        data = self._cr.fetchall()
        return data