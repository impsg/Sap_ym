# -*- coding: utf-8 -*-

from odoo import fields, models, api

import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # @api.model_create_multi
    # def create(self, vals):
    #
    #     self.env.cr.execute("""SELECT FROM res_partner""")



