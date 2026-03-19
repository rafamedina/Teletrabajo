# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


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

        return super().write(vals)

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
