# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase  # noqa: F401


class TestTeleworkRequestSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestTeleworkRequestSecurity, cls).setUpClass()
        # Empleados y Usuarios
        cls.user_1 = cls.env["res.users"].create(
            {
                "name": "User 1",
                "login": "user1",
                "email": "user1@test.com",
                "groups_id": [(4, cls.env.ref("base.group_user").id)],
            }
        )
        cls.employee_1 = cls.env["hr.employee"].create(
            {
                "name": "Employee 1",
                "user_id": cls.user_1.id,
            }
        )

        cls.user_2 = cls.env["res.users"].create(
            {
                "name": "User 2",
                "login": "user2",
                "email": "user2@test.com",
                "groups_id": [(4, cls.env.ref("base.group_user").id)],
            }
        )
        cls.employee_2 = cls.env["hr.employee"].create(
            {
                "name": "Employee 2",
                "user_id": cls.user_2.id,
            }
        )

        # Solicitudes
        cls.telework_model = cls.env["hr.telework.request"]
        cls.request_1 = cls.telework_model.create(
            {
                "employee_id": cls.employee_1.id,
                "date_start": "2026-03-20 08:00:00",
                "date_stop": "2026-03-20 17:00:00",
            }
        )

    def test_user_can_see_own_requests(self):
        """Verificar que un usuario puede ver sus propias solicitudes."""
        requests = self.telework_model.with_user(self.user_1).search([])
        self.assertIn(
            self.request_1, requests, "El usuario 1 debería ver su propia solicitud."
        )

    def test_user_cannot_see_others_requests(self):
        """Verificar que un usuario no puede ver solicitudes de otros."""
        requests = self.telework_model.with_user(self.user_2).search([])
        self.assertNotIn(
            self.request_1,
            requests,
            "El usuario 2 no debería ver la solicitud del usuario 1.",
        )

    def test_manager_can_see_subordinates_requests(self):
        """Verificar que un gerente puede ver las solicitudes de sus subordinados."""
        manager_user = self.env["res.users"].create(
            {
                "name": "Manager",
                "login": "manager",
                "email": "manager@test.com",
                "groups_id": [(4, self.env.ref("base.group_user").id)],
            }
        )
        manager_employee = self.env["hr.employee"].create(
            {
                "name": "Manager Employee",
                "user_id": manager_user.id,
            }
        )

        self.employee_1.parent_id = manager_employee.id

        requests = self.telework_model.with_user(manager_user).search([])
        self.assertIn(
            self.request_1,
            requests,
            "El gerente debería ver la solicitud de su subordinado.",
        )
