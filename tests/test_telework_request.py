# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestTeleworkRequest(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env["hr.employee"].create({"name": "Test Employee"})
        cls.manager = cls.env["res.users"].create(
            {
                "name": "Test Manager",
                "login": "test_manager",
                "email": "manager@test.com",
            }
        )
        cls.employee.parent_id = (
            cls.env["hr.employee"]
            .create({"name": "Manager Employee", "user_id": cls.manager.id})
            .id
        )

    def test_01_telework_request_creation(self):
        """Test basic creation and default values of telework.request"""
        request = self.env["telework.request"].create(
            {
                "employee_id": self.employee.id,
                "date": "2026-03-20",
            }
        )
        self.assertEqual(request.state, "draft", "Default state should be 'draft'")
        self.assertEqual(request.employee_id, self.employee, "Employee should match")
        self.assertEqual(
            request.manager_id,
            self.manager,
            "Manager should be automatically assigned from employee",
        )

    def test_02_telework_request_workflow(self):
        """Test the state transition of telework.request"""
        request = self.env["telework.request"].create(
            {
                "employee_id": self.employee.id,
                "date": "2026-03-21",
            }
        )
        request.action_confirm()
        self.assertEqual(
            request.state, "confirm", "State should be 'confirm' after confirmation"
        )

        # Mocking manager validation would require switching user context
        # For now, just test the method exists and changes state
        request.action_validate()
        self.assertEqual(
            request.state, "validate", "State should be 'validate' after validation"
        )
