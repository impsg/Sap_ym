import requests
import json
import traceback
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SapRef(models.TransientModel):
    _name = 'cron.sap'

    required_fields = ["Cellular"]


    def login(self):
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
        response = requests.request("POST", url, headers=headers, data=payload)
        sessionId = response.json().get("SessionId")
        return sessionId

    def makeRequest(self, endpoint, payload):

        url = "https://analytics10.uneeccch.com:50000/b1s/v1/" + endpoint
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'B1SESSION='+self.login()+'; ROUTEID=.node1'

        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        return response

    def makeRequestWithRetry(self, endpoint, payload):
        try:
            response = self.makeRequest(endpoint, payload)
            if response.status_code == 401:
                self.login()
                self.makeRequest(endpoint, payload)
        except:
            tb = traceback.format_exc()
            _logger.error(tb)
            raise ValueError("Login not allowed")  # Todo: return message from sap

    def create_customer(self):
        payload = json.dumps({
            "CardCode": 10279,
            "CardName": "RAJENDRA MECHANICAL PRIVATE LIMITED",
            "Address": "M.S KHATA NO.1212/3353, PLOT NO.5894/8834 and 5894/8835MOUZA- JHARSUGUDA UNIT NO.5 VEDANTA CHOWK",
            "ZipCode": 768201,
            "MailAddress": "M.S KHATA NO.1212/3353, PLOT NO.5894/8834 and 5894/8835MOUZA- JHARSUGUDA UNIT NO.5 VEDANTA CHOWK",
            "MailZipCode": 768201,
            "Cellular": None,
            "City": "0",
            "MailCity": "0",
            "EmailAddress": "anupranjan92@gmail.com",
            "BPFiscalTaxIDCollection": [
                {
                    "TaxId0": "AAJCR8812M",
                    "BPCode": 10267
                }
            ],
            "BPAddresses": [
                {
                    "AddressName": "Odisha",
                    "ZipCode": 768201,
                    "City": "0",
                    "State": "OD",
                    "BuildingFloorRoom": "M.S KHATA NO.1212/3353, PLOT NO.5894/8834 and 5894/8835MOUZA- JHARSUGUDA UNIT NO.5 VEDANTA CHOWK",
                    "AddressType": "bo_BillTo",
                    "BPCode": 10267,
                    "GSTIN": "21AAJCR8812M1Z3",
                    "GstType": "gstRegularTDSISD"
                },
                {
                    "AddressName": "Odisha",
                    "ZipCode": 768201,
                    "City": "0",
                    "State": "OD",
                    "BuildingFloorRoom": "M.S KHATA NO.1212/3353, PLOT NO.5894/8834 and 5894/8835MOUZA- JHARSUGUDA UNIT NO.5 VEDANTA CHOWK",
                    "AddressType": "bo_ShipTo",
                    "BPCode": 10267,
                    "GSTIN": "21AAJCR8812M1Z3",
                    "GstType": "gstRegularTDSISD"
                }
            ],
            "ShipToDefault": "Odisha",
            "BilltoDefault": "Odisha"
        })


        for val in payload:
            if val == "Cellular" and payload[val] is not None:
                raise ValueError("Fields are not complete")

        response = self.makeRequestWithRetry("BusinessPartners", payload)

        print(response)

    def build_customer_request(self, code):
        self.env.cr.execute('''select code,name from res_country_state where l10n_in_tin=%s;''' % code)
        data = self._cr.fetchall()
        return data

    def read_sap(self):
        payload = {}
        headers = {
            'Cookie': 'B1SESSION='+SapRef.sessionId+'; ROUTEID=.node1'
        }
        url = "https://analytics10.uneeccch.com:50000/b1s/v1/BusinessPartners('977')"
        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()
        print(data)
