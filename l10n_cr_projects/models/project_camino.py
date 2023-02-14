# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectCamino(models.Model):
    _name = 'project.camino'
    _inherit = 'mail.thread'
    _description = 'Caminos en Proyectos'
    _rec_name = 'codigo'
    _order = "id desc"

    codigo = fields.Char(string='Código', required=True, copy=False)
    nombre = fields.Char(string='Nombre', required=True, copy=False)
    company_id = fields.Many2one('res.company', string='Compañia',readonly=True, default=lambda self: self.env.company)
    county_id = fields.Many2one('res.country.county',related='company_id.county_id', readonly=False)
    distrito_id = fields.Many2one('res.country.district',string='Distrito', required=True)
    estado = fields.Boolean(string='Activo')



    def name_get(self):
        result = []
        for camino in self:
            name = "%s | %s | %s" % (camino.codigo, camino.nombre, camino.distrito_id.name)
            result.append((camino.id, name))
        return result

