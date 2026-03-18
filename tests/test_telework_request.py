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

    def test_03_telework_request_access_rules(self):
        """Test record rules for telework.request"""
        # Create another employee and their request
        other_employee = self.env["hr.employee"].create({"name": "Other Employee"})
        other_request = self.env["telework.request"].create(
            {
                "employee_id": other_employee.id,
                "date": "2026-03-22",
            }
        )

        # Test Employee Access (should only see their own)
        # We need a user for the employee to test access rules properly
        employee_user = self.env["res.users"].create(
            {
                "name": "Employee User",
                "login": "emp_user",
                "email": "emp@test.com",
                "groups_id": [(4, self.env.ref("base.group_user").id)],
            }
        )
        self.employee.user_id = employee_user.id

        request_emp = self.env["telework.request"].create(
            {
                "employee_id": self.employee.id,
                "date": "2026-03-23",
            }
        )

        # As Employee User
        emp_env = self.env(user=employee_user)
        visible_requests = emp_env["telework.request"].search([])

        self.assertIn(
            request_emp.id,
            visible_requests.ids,
            "Employee should see their own request",
        )
        # This will fail until record rules are implemented (currently sees all due to ir.model.access.csv)
        self.assertNotIn(
            other_request.id,
            visible_requests.ids,
            "Employee should NOT see other's request",
        )

        # Test Manager Access (should see subordinates)
        manager_env = self.env(user=self.manager)
        manager_requests = manager_env["telework.request"].search([])

        self.assertIn(
            request_emp.id,
            manager_requests.ids,
            "Manager should see subordinate's request",
        )
