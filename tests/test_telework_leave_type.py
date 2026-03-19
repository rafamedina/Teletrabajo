# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase  # noqa: F401


class TestTeleworkLeaveType(TransactionCase):
    def test_telework_leave_type_exists(self):
        """Comportamiento C: El tipo de ausencia Teletrabajo existe y tiene el color correcto (10)."""
        # Buscamos el registro por su External ID definido en el XML
        leave_type = self.env.ref(
            "Teletrabajo.holiday_status_telework", raise_if_not_found=False
        )

        self.assertTrue(
            leave_type,
            "El tipo de ausencia 'Teletrabajo' no se encontró en la base de datos.",
        )
        self.assertEqual(
            leave_type.color,
            10,
            "El color del tipo de ausencia 'Teletrabajo' debería ser 10.",
        )
        self.assertEqual(
            leave_type.requires_allocation,
            "no",
            "El teletrabajo no debería requerir asignación previa.",
        )
