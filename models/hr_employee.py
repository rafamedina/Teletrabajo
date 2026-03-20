# -*- coding: utf-8 -*-
from odoo import models, fields, api, _  # noqa: F401
from odoo.exceptions import UserError  # noqa: F401
from datetime import datetime, timedelta


class HrEmployee(models.Model):
    """Extensión de hr.employee para la gestión de teletrabajo utilizando campos nativos de Odoo 18."""

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

    monday_location_id = fields.Many2one("hr.work.location", string=("Lunes"))
    tuesday_location_id = fields.Many2one("hr.work.location", string=("Martes"))
    wednesday_location_id = fields.Many2one("hr.work.location", string=("Miércoles"))
    thursday_location_id = fields.Many2one("hr.work.location", string=("Jueves"))
    friday_location_id = fields.Many2one("hr.work.location", string=("Viernes"))
    saturday_location_id = fields.Many2one("hr.work.location", string=("Sábado"))
    sunday_location_id = fields.Many2one("hr.work.location", string=("Domingo"))

    is_telework_manager = fields.Boolean(
        compute="_compute_is_telework_manager",
        help="Indica si el usuario actual es el gerente del empleado.",
    )

    telework_count = fields.Integer(
        compute="_compute_telework_count", string="Días de Teletrabajo"
    )

    default_telework_day = fields.Selection(
        [
            ("0", "Lunes"),
            ("1", "Martes"),
            ("2", "Miércoles"),
            ("3", "Jueves"),
            ("4", "Viernes"),
        ],
        string="Día Predeterminado de Teletrabajo",
        tracking=True,
    )

    def _compute_telework_count(self):
        """Calcula el número de solicitudes de teletrabajo para el botón inteligente."""
        for employee in self:
            employee.telework_count = self.env["hr.telework.request"].search_count(
                [("employee_id", "=", employee.id)]
            )

    def action_open_telework_calendar(self):
        """Abre la vista de calendario de teletrabajo filtrada por el empleado actual."""
        self.ensure_one()
        return {
            "name": _("Calendario de Teletrabajo"),
            "type": "ir.actions.act_window",
            "res_model": "hr.telework.request",
            "view_mode": "calendar,list,form",
            "domain": [("employee_id", "=", self.id)],
            "context": {
                "default_employee_id": self.id,
                "search_default_employee_id": self.id,
            },
            "help": _(
                """
                <p class="o_view_nocontent_smiling_face">
                    No se han encontrado días de teletrabajo.
                </p>
            """
            ),
        }

    @api.depends("parent_id")
    def _compute_is_telework_manager(self):
        """Calcula si el usuario conectado es el responsable directo del empleado."""
        current_user = self.env.user
        for employee in self:
            employee.is_telework_manager = employee.parent_id.user_id == current_user

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
        """Reset de estado en la interfaz de usuario al modificar ubicaciones nativas."""
        self.telework_state = "draft"

    def _generate_telework_recurring_entries(self):
        """Genera registros en el calendario de teletrabajo para las próximas 4 semanas."""
        self.ensure_one()
        if not self.default_telework_day:
            return

        target_weekday = int(self.default_telework_day)
        today = datetime.now().date()

        # Generamos para las próximas 4 semanas
        for i in range(4):
            # Encontramos el día de la semana objetivo en la semana i
            days_ahead = target_weekday - today.weekday()
            if days_ahead <= 0:  # Si ya pasó esta semana, vamos a la siguiente
                days_ahead += 7
            days_ahead += i * 7

            target_date = today + timedelta(days=days_ahead)

            # Evitar duplicados para el mismo día
            existing = self.env["hr.telework.request"].search(
                [
                    ("employee_id", "=", self.id),
                    (
                        "date_start",
                        ">=",
                        datetime.combine(target_date, datetime.min.time()),
                    ),
                    (
                        "date_start",
                        "<=",
                        datetime.combine(target_date, datetime.max.time()),
                    ),
                ]
            )

            if not existing:
                self.env["hr.telework.request"].create(
                    {
                        "employee_id": self.id,
                        "date_start": datetime.combine(
                            target_date, datetime.min.time().replace(hour=8)
                        ),
                        "date_stop": datetime.combine(
                            target_date, datetime.min.time().replace(hour=17)
                        ),
                        "state": "draft",
                    }
                )

    def write(self, vals):
        """Control de integridad y notificaciones al modificar el horario nativo de Odoo 18."""
        day_fields = {
            "monday_location_id",
            "tuesday_location_id",
            "wednesday_location_id",
            "thursday_location_id",
            "friday_location_id",
            "saturday_location_id",
            "sunday_location_id",
        }

        # Si se modifican campos de ubicación nativos, forzamos estado draft y preparamos actividad
        if day_fields & set(vals.keys()):
            vals["telework_state"] = "draft"
            res = super().write(vals)
            self._create_telework_activity()
            return res

        res = super().write(vals)
        if "default_telework_day" in vals:
            for employee in self:
                employee._generate_telework_recurring_entries()
        return res

    def _create_telework_activity(self):
        """Genera una actividad para el gerente informando de cambios pendientes de validar."""
        activity_type = self.env.ref(
            "mail.mail_activity_data_todo", raise_if_not_found=False
        )
        model_id = self.env.ref("hr.model_hr_employee").id

        for employee in self.filtered(lambda e: e.parent_id.user_id):
            self.env["mail.activity"].create(
                {
                    "res_id": employee.id,
                    "res_model_id": model_id,
                    "activity_type_id": activity_type.id if activity_type else False,
                    "summary": _("Validación de Teletrabajo"),
                    "note": _(
                        "El empleado %s ha modificado su horario. Por favor, valide los cambios."
                    )
                    % employee.name,
                    "user_id": employee.parent_id.user_id.id,
                }
            )

    def action_validate_telework(self):
        """Acción de validación restringida al responsable directo."""
        for employee in self:
            if not employee.is_telework_manager:
                raise UserError(
                    _(
                        "Acceso denegado: Solo el responsable directo (%s) puede validar esta solicitud."
                    )
                    % (employee.parent_id.name or _("asignado"))
                )

            employee.telework_state = "validated"
