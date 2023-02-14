# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    project_id = fields.Many2one('project.project',string='Proyecto')
    analytic_tag_ids = fields.Many2many('purchase.tag', string='Departamento')

    #<field name="analytic_tag_ids" groups="analytic.group_analytic_accounting" widget="many2many_tags"/>


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def name_get(self):
        result = []
        for pol in self:
            product= pol.product_id.name or ''
            description= pol.name or ''
            result.append((pol.id, (product+'/'+description)))
        return result


