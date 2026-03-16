# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TeleworkRequest(models.Model):
    _name = "telework.request"
    _description = "Telework Request"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
        default=lambda self: self.env.user.employee_id,
    )
    date = fields.Date(string="Date", required=True)
    state = fields.Selection(
        [("draft", "Draft"), ("confirm", "Confirmed"), ("validate", "Validated")],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
    )
    manager_id = fields.Many2one(
        "res.users", string="Manager", compute="_compute_manager_id", store=True
    )

    @api.depends(
        "employee_id", "employee_id.parent_id", "employee_id.parent_id.user_id"
    )
    def _compute_manager_id(self):
        for request in self:
            if request.employee_id.parent_id.user_id:
                request.manager_id = request.employee_id.parent_id.user_id
            else:
                request.manager_id = False

    def action_confirm(self):
        for request in self:
            request.state = "confirm"

    def action_validate(self):
        for request in self:
            request.state = "validate"
