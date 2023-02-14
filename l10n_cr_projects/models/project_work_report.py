# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectWorkReport(models.Model):
    _name = 'project.work.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Reporte de proyectos - Validación'
    _rec_name = 'name'
    _order = "id desc"

    name = fields.Char(default='Nuevo', store=True,copy=False)
    fecha = fields.Date(string='Fecha', required=True)
    camino_id = fields.Many2one('project.camino', string='Camino',copy=False)
    distrito_id = fields.Many2one('res.country.district',string='Distrito', related='camino_id.distrito_id',store=True)
    proyecto_id = fields.Many2one('project.project', string='Proyecto', copy=False, store=True)
    orden_purchase_id = fields.Many2one('purchase.order',string='Orden de Compra',copy=False)
    analytic_tag_ids = fields.Many2many('purchase.tag', string='Departamento', copy=False, store=True)
    departamento = fields.Char(related='analytic_tag_ids.name',string='Departamento Nombre', store=True, readonly=False)
    order_line_id = fields.Many2one('purchase.order.line', copy=False, string=u'Producto/Descripción')
    recurso_id = fields.Many2one('product.product', string='Recurso neto', required=True, copy=False, store=True)
    identificacion_equipo = fields.Char(string=u'Identificación del Equipo', required=True,copy=False)
    cantidad_disponible = fields.Float(string='Cantidad Disponible',required=True,copy=False)
    cantidad_reportar = fields.Float(string='Cantidad a Reportar', store=True,required=True,copy=False)
    #imagen = fields.
    company_id = fields.Many2one('res.company',string='Company', store=True, readonly=True,default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency',string='Moneda',related='company_id.currency_id')
    costo_recurso = fields.Monetary(string='Costo Recurso', required=True, store=True,copy=False)
    costo_total = fields.Monetary(string='Costo Total', required=True, store=True,copy=False)

    state = fields.Selection([('draft','Borrador'),
                               ('validate', 'Validado')], string='Estado', readonly=True, default='draft')

    show_msn = fields.Integer(default=0, store=True)

    @api.constrains('cantidad_reportar')
    def _check_cantidad_reportar(self):
        for rec in self:
            if rec.cantidad_reportar:
                if rec.cantidad_reportar > rec.cantidad_disponible:
                    rec.cantidad_reportar = 0
                    raise UserError(_("La CANTIDAD A REPORTAR no puede ser mayor a la CANTIDAD DISPONIBLE !"))
                if rec.cantidad_reportar <= 0.00:
                    raise UserError(_("La CANTIDAD A REPORTAR no puede menor o igual a CERO !"))

    # @api.onchange("proyecto_id","analytic_tag_ids")
    # def _onchange_orden_purchase_id_ex(self):
    #     po = self.env['purchase.order']
    #     for rec in self:
    #         rec.orden_purchase_id = [(6, 0, [])]
    #         if rec.proyecto_id or rec.analytic_tag_ids:
    #             if rec.proyecto_id and not rec.analytic_tag_ids:
    #                 domain = [('state','=','purchase'),('project_id', '=', rec.proyecto_id.id)]
    #             elif not rec.proyecto_id and rec.analytic_tag_ids:
    #                 domain = [('state', '=', 'purchase'), ('analytic_tag_ids', 'in', rec.analytic_tag_ids.ids)]
    #
    #             elif rec.proyecto_id and rec.analytic_tag_ids:
    #                 domain = [('state', '=', 'purchase'), ('analytic_tag_ids', 'in', rec.analytic_tag_ids.ids),('project_id', '=', rec.proyecto_id.id)]
    #             else:
    #                 domain = []
    #
    #             if domain==[]:
    #                 rec.show_msn = 2
    #                 rec.orden_purchase_id = [(6, 0, [])]
    #             else:
    #                 po_s = po.search(domain)
    #
    #                 ids = []
    #                 def function(line):
    #                     for x in line:
    #                         if x.product_qty > x.qty_received:
    #                             return True
    #
    #                 pos_ids = po_s.filtered(lambda x: function(x.order_line)==True).ids
    #
    #                 if len(pos_ids)>0:
    #                     rec.show_msn = 1
    #                 else:
    #                     rec.show_msn = 2
    #                 return {'domain': {'orden_purchase_id': [('id', 'in', pos_ids)]}}
    #         else:
    #             rec.show_msn = 0

    def validate(self):
        for rec in self:
            if rec.state=='draft':
                rec.update_line_product_qty(rec)
                rec.name = self.env['ir.sequence'].next_by_code('project.work.report.sequence')
                rec.state = 'validate'

    def update_line_product_qty(self, rec):
        for pick in self.orden_purchase_id.picking_ids:
            if pick not in ('done','cancel'):
                for line in pick.move_ids_without_package:
                    if line.purchase_line_id.id == rec.order_line_id.id and line.state not in ('done','cancel','draft'):
                        line.write({'quantity_done': line.quantity_done + rec.cantidad_reportar})


    # @api.onchange("orden_purchase_id")
    # def _onchange_orden_purchase_id(self):
    #     for rec in self:
    #         products_ids = []
    #         for line in rec.orden_purchase_id.order_line:
    #             products_ids.append(line.product_id.id)
    #
    #         if len(products_ids) >0:
    #             return {'domain': {'recurso_id': [('id', 'in', products_ids)]}}
    #         else:
    #             return {'domain': {'recurso_id': [('id', 'in', [(6, 0, [])])]}}

    @api.onchange("orden_purchase_id")
    def _onchange_orden_purchase_id(self):
        for rec in self:
            lines_ids = []
            #products_ids = []
            for line in rec.orden_purchase_id.order_line:
                lines_ids.append(line.id)
                #products_ids.append(line.product_id.id)

            if len(lines_ids) > 0:
                #return {'domain': {'recurso_id': [('id', 'in', products_ids)]}}
                return {'domain': {'order_line_id': [('id', 'in', lines_ids)]}}
            else:
                return {'domain': {'order_line_id': [('id', 'in', [(6, 0, [])])]}}

    # @api.onchange("recurso_id")
    # def _onchange_recurso_id(self):
    #     for rec in self:
    #         for line in rec.orden_purchase_id.order_line:
    #             if line.product_id == rec.recurso_id:
    #                 rec.order_line_id = line
    #                 rec.cantidad_disponible = line.product_qty - line.qty_received
    #                 rec.costo_recurso = line.price_unit

    @api.onchange("order_line_id")
    def _onchange_order_line_id(self):
        if self.order_line_id:
            self.recurso_id = self.order_line_id.product_id
            self.cantidad_disponible = self.order_line_id.product_qty - self.order_line_id.qty_received
            self.costo_recurso = self.order_line_id.price_unit
            return {'domain': {'recurso_id': [('id', 'in', [self.order_line_id.product_id.id])]}}
            #'recurso_id': [('id', 'in', products_ids)],


    @api.onchange("cantidad_reportar")
    def _onchange_cantidad_reportar(self):
        for rec in self:
            self._check_cantidad_reportar()
            rec.costo_total = rec.cantidad_reportar * rec.costo_recurso

