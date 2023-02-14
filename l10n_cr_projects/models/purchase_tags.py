# -*- coding: utf-8 -*-

from collections import defaultdict
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import ValidationError


class PurchaseTags(models.Model):

    _name = 'purchase.tag'
    _description = 'Compra Tags'

    name = fields.Char(string='Nombre', index=True, required=True)
    color = fields.Integer('Color')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Compañia',default=lambda self: self.env.company)
