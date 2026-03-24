# -*- coding: utf-8 -*-
from odoo import models, fields, api, _  # noqa: F401
from odoo.exceptions import UserError  # noqa: F401


class HrTeleworkRequest(models.Model):
    """Modelo independiente para la gestión de días de teletrabajo."""

    _name = "hr.telework.request"
    _description = "Solicitud de Teletrabajo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_start desc"

    name = fields.Char(
        string="Descripción",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("Nuevo"),
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Empleado",
        required=True,
        default=lambda self: self.env.user.employee_id,
        tracking=True,
    )
    date_start = fields.Datetime(string="Inicio", required=True, tracking=True)
    date_stop = fields.Datetime(string="Fin", required=True, tracking=True)
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("validated", "Validado"),
            ("refused", "Rechazado"),
        ],
        string="Estado",
        default="draft",
        tracking=True,
    )
    telework_type = fields.Selection(
        [
            ("hybrid", "Híbrido"),
            ("full_remote", "100% Remoto"),
            ("punctual", "Puntual"),
        ],
        string="Modalidad",
        default="hybrid",
        required=True,
        tracking=True,
    )
    is_hatched = fields.Boolean(
        compute="_compute_is_hatched", string="Hatched", store=True
    )
    reason = fields.Text(string="Motivo", tracking=True)
    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Adjuntos",
        help="Archivos adjuntos a la solicitud de teletrabajo.",
    )

    @api.depends("state")
    def _compute_is_hatched(self):
        """Indica si el evento debe aparecer rayado (draft)."""
        for request in self:
            request.is_hatched = request.state == "draft"

    @api.model
    def create(self, vals):
        """Genera un nombre descriptivo para la solicitud si no se proporciona."""
        if vals.get("name", _("Nuevo")) == _("Nuevo"):
            employee = self.env["hr.employee"].browse(vals.get("employee_id"))
            vals["name"] = _("Teletrabajo: %s") % (employee.name or "")
        return super().create(vals)

    def action_validate(self):
        """Valida la solicitud de teletrabajo. Solo permitido para el gerente del empleado."""
        for request in self:
            current_user = self.env.user
            if request.employee_id.parent_id.user_id != current_user:
                raise UserError(
                    _(
                        "Acceso denegado: Solo el responsable directo (%s) puede validar esta solicitud."
                    )
                    % (request.employee_id.parent_id.name or _("asignado"))
                )
            request.write({"state": "validated"})

    def action_refuse(self):
        """Rechaza la solicitud de teletrabajo. Solo permitido para el gerente del empleado."""
        for request in self:
            current_user = self.env.user
            if request.employee_id.parent_id.user_id != current_user:
                raise UserError(
                    _(
                        "Acceso denegado: Solo el responsable directo (%s) puede validar esta solicitud."
                    )
                    % (request.employee_id.parent_id.name or _("asignado"))
                )
            request.write({"state": "refused"})
