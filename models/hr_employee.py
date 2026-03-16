# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


# PIEZA 1 (Modelo) - INICIO
class HrEmployee(models.Model):
    _inherit = "hr.employee"

    telework_state = fields.Selection(
        [
            ("draft", "Sin validar"),
            ("validated", "Validado"),
        ],
        string="Estado de Teletrabajo",
        default="draft",
        tracking=True,
    )

    is_telework_manager = fields.Boolean(compute="_compute_is_telework_manager")

    @api.depends("parent_id")
    def _compute_is_telework_manager(self):
        for employee in self:
            # Comprobamos si el usuario actual es el gerente directo
            employee.is_telework_manager = employee.parent_id.user_id == self.env.user

    @api.onchange(
        "monday_location_id",
        "tuesday_location_id",
        "wednesday_location_id",
        "thursday_location_id",
        "friday_location_id",
        "saturday_location_id",
        "sunday_location_id",
    )
    def _onchange_telework_days(self):
        """Si se cambia cualquier día de la semana, el estado vuelve a Sin validar."""
        self.telework_state = "draft"

    def write(self, vals):
        """Sobrescribimos write para asegurar que si se cambian los días,
        el estado pase a sin validar incluso si se hace por API o importación.
        """
        day_fields = [
            "monday_location_id",
            "tuesday_location_id",
            "wednesday_location_id",
            "thursday_location_id",
            "friday_location_id",
            "saturday_location_id",
            "sunday_location_id",
        ]
        # Si alguno de los campos de días está en los valores a cambiar, forzamos sin validar
        if any(field in vals for field in day_fields):
            vals["telework_state"] = "draft"

        return super(HrEmployee, self).write(vals)

    # PIEZA 3 (Lógica) - INICIO
    def action_validate_telework(self):
        """Valida el teletrabajo. Solo el gerente (parent_id) puede validar."""
        for employee in self:
            current_employee = self.env.user.employee_id
            if not current_employee or employee.parent_id != current_employee:
                raise UserError(
                    "Acceso denegado: Solo tu gerente directo (%s) puede validar esta solicitud."
                    % (employee.parent_id.name or "asignado")
                )

            employee.telework_state = "validated"

    # PIEZA 3 (Lógica) - FIN


# PIEZA 1 (Modelo) - FIN
