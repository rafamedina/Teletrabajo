# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase  # noqa: F401
from odoo import fields  # noqa: F401


class TestTeleworkRequestFields(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestTeleworkRequestFields, cls).setUpClass()
        cls.employee = cls.env["hr.employee"].create({"name": "Test Employee"})
        cls.telework_model = cls.env["hr.telework.request"]

    def test_new_fields_exist(self):
        """Verificar que los nuevos campos existen en el modelo."""
        request = self.telework_model.create(
            {
                "employee_id": self.employee.id,
                "date_start": fields.Datetime.now(),
                "date_stop": fields.Datetime.now(),
                "reason": "Test reason",
            }
        )
        self.assertEqual(
            request.reason,
            "Test reason",
            "El campo 'reason' no se guardó correctamente.",
        )
        self.assertTrue(
            hasattr(request, "attachment_ids"),
            "El campo 'attachment_ids' no existe en el modelo.",
        )

    def test_attachments_behavior(self):
        """Verificar que se pueden adjuntar archivos a la solicitud."""
        attachment = self.env["ir.attachment"].create(
            {
                "name": "test_file.txt",
                "datas": "dGVzdCBjb250ZW50",  # "test content" in base64
                "res_model": "hr.telework.request",
            }
        )

        request = self.telework_model.create(
            {
                "employee_id": self.employee.id,
                "date_start": fields.Datetime.now(),
                "date_stop": fields.Datetime.now(),
                "attachment_ids": [(4, attachment.id)],
            }
        )

        self.assertIn(
            attachment,
            request.attachment_ids,
            "El archivo no se adjuntó correctamente a la solicitud.",
        )
