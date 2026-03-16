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

    # PIEZA 3 (Lógica) - INICIO
    def action_validate_telework(self):
        """ Valida el estado de teletrabajo del empleado.
        Solo el gerente asignado puede realizar esta acción.
        """
        for employee in self:
            # Verificamos si el usuario actual está vinculado a un empleado
            current_employee = self.env.user.employee_id
            
            if not current_employee or employee.telework_manager_id != current_employee:
                from odoo.exceptions import UserError
                raise UserError("Solo el gerente de teletrabajo asignado puede validar esta solicitud.")
            
            employee.telework_state = 'validated'
    # PIEZA 3 (Lógica) - FIN
# PIEZA 1 (Modelo) - FIN
