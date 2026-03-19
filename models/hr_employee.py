# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


# creamos el modelo que hereda de hr.employee para agregar el campo de estado del teletrabajo y el campo booleano para identificar a los gerentes de teletrabajo. También agregamos la lógica para validar el teletrabajo y crear actividades para los gerentes cuando se cambian los días de teletrabajo.
class HrEmployee(models.Model):
    _inherit = "hr.employee"  # Heredamos del modelo hr.employee para agregar campos y lógica relacionada con el teletrabajo

    telework_state = fields.Selection(
        [
            ("draft", "Sin validar"),
            ("validated", "Validado"),
        ],  # Definimos los estados posibles para el teletrabajo: "draft" para sin validar y "validated" para validado
        string="Estado de Teletrabajo",
        default="draft",
        tracking=True,
    )

    monday_location_id = fields.Many2one("hr.work.location", string="Lunes")
    tuesday_location_id = fields.Many2one("hr.work.location", string="Martes")
    wednesday_location_id = fields.Many2one("hr.work.location", string="Miércoles")
    thursday_location_id = fields.Many2one("hr.work.location", string="Jueves")
    friday_location_id = fields.Many2one("hr.work.location", string="Viernes")
    saturday_location_id = fields.Many2one("hr.work.location", string="Sábado")
    sunday_location_id = fields.Many2one("hr.work.location", string="Domingo")

    is_telework_manager = fields.Boolean(
        compute="_compute_is_telework_manager"
    )  # Creamos un campo booleano computado para identificar si el empleado es gerente de teletrabajo

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
        should_create_activity = False
        if any(field in vals for field in day_fields):
            vals["telework_state"] = "draft"
            should_create_activity = True

        res = super(HrEmployee, self).write(vals)

        if should_create_activity:
            self._create_telework_activity()

        return res

    def _create_telework_activity(self):
        """Crea una actividad para el gerente del empleado cuando se cambia el horario de teletrabajo."""
        for employee in self:
            if employee.parent_id and employee.parent_id.user_id:
                # Buscamos el tipo de actividad 'To Do' o similar
                activity_type = self.env.ref(
                    "mail.mail_activity_data_todo", raise_if_not_found=False
                )

                self.env["mail.activity"].create(
                    {
                        "res_id": employee.id,
                        "res_model_id": self.env.ref("hr.model_hr_employee").id,
                        "activity_type_id": activity_type.id
                        if activity_type
                        else False,
                        "summary": "Validación de Teletrabajo",
                        "note": "El empleado %s ha cambiado la fecha del teletrabajo, por favor entre a validar los cambios."
                        % employee.name,
                        "user_id": employee.parent_id.user_id.id,
                    }
                )

    # (Lógica) - INICIO
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
