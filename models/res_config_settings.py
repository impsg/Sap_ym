# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    url = fields.Char(string='url', config_parameter='SAP.url')
    CompanyDB = fields.Char(string='CompanyDB', config_parameter='SAP.CompanyDB')
    UserName = fields.Char(string='UserName', config_parameter='SAP.UserName')
    Password = fields.Char(string='Password', config_parameter='SAP.Password')
