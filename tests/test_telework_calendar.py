# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase  # noqa: F401
from odoo import fields  # noqa: F401


class TestTeleworkCalendar(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestTeleworkCalendar, cls).setUpClass()
        cls.employee = cls.env["hr.employee"].create({"name": "Test Employee"})
        cls.telework_model = cls.env["hr.telework.request"]

    def test_create_telework_request(self):
        """Comportamiento A: Se puede crear una solicitud de teletrabajo."""
        request = self.telework_model.create(
            {
                "employee_id": self.employee.id,
                "date_start": fields.Datetime.now(),
                "date_stop": fields.Datetime.now(),
            }
        )
        self.assertTrue(request.id, "No se pudo crear la solicitud de teletrabajo.")

    def test_employee_telework_count(self):
        """Comportamiento B: El empleado muestra el contador correcto de solicitudes."""
        # Creamos 2 solicitudes
        self.telework_model.create(
            [
                {
                    "employee_id": self.employee.id,
                    "date_start": fields.Datetime.now(),
                    "date_stop": fields.Datetime.now(),
                },
                {
                    "employee_id": self.employee.id,
                    "date_start": fields.Datetime.now(),
                    "date_stop": fields.Datetime.now(),
                },
            ]
        )
        self.assertEqual(
            self.employee.telework_count,
            2,
            "El contador de teletrabajo del empleado no es correcto.",
        )

    def test_smart_button_action(self):
        """Comportamiento C: El botón inteligente devuelve la acción correcta."""
        action = self.employee.action_open_telework_calendar()
        self.assertEqual(
            action["res_model"],
            "hr.telework.request",
            "La acción no apunta al modelo de teletrabajo.",
        )
        self.assertEqual(
            action["context"].get("default_employee_id"),
            self.employee.id,
            "El contexto de la acción no incluye el empleado por defecto.",
        )
