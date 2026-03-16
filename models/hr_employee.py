# -*- coding: utf-8 -*-
from odoo import models, fields, api

# PIEZA 1 (Modelo) - INICIO
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    telework_state = fields.Selection([
        ('draft', 'Borrador'),
        ('validated', 'Validado'),
    ], string='Estado de Teletrabajo', default='draft', tracking=True)

    telework_manager_id = fields.Many2one(
        'hr.employee', 
        string='Manager de Teletrabajo',
        help="Manager encargado de validar las solicitudes de teletrabajo."
    )
# PIEZA 1 (Modelo) - FIN
