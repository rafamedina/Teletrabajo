# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase  # noqa: F401


class TestTeleworkEmployee(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestTeleworkEmployee, cls).setUpClass()
        # Obtenemos la dirección de la compañía para las ubicaciones
        cls.company_address = cls.env.company.partner_id

        # Gerente de prueba (buscamos el empleado ya vinculado al admin para evitar duplicados)
        admin_user = cls.env.ref("base.user_admin")
        cls.manager = cls.env["hr.employee"].search(
            [("user_id", "=", admin_user.id)], limit=1
        )
        if not cls.manager:
            # Si por alguna razón no existe (ej. base de datos vacía sin demo), lo creamos
            cls.manager = cls.env["hr.employee"].create(
                {
                    "name": "Manager Employee",
                    "user_id": admin_user.id,
                }
            )

        # Ubicaciones de prueba
        cls.location_office = cls.env["hr.work.location"].create(
            {"name": "Office", "address_id": cls.company_address.id}
        )
        cls.location_home = cls.env["hr.work.location"].create(
            {"name": "Home", "address_id": cls.company_address.id}
        )

        # Empleado de prueba (empezamos en estado validado)
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "telework_state": "validated",
                "monday_location_id": cls.location_office.id,
                "parent_id": cls.manager.id,
            }
        )

    def test_onchange_locations_resets_state(self):
        """Comportamiento A: El estado debe volver a 'draft' al cambiar un día."""
        # Cambiamos el lunes a teletrabajo
        self.employee.write({"monday_location_id": self.location_home.id})

        # El estado debería haber cambiado a 'draft' por la lógica en write o onchange
        self.assertEqual(
            self.employee.telework_state,
            "draft",
            "El estado de teletrabajo no se reinició a 'draft' tras cambiar la ubicación.",
        )

    def test_validate_telework_manager_success(self):
        """Comportamiento B: El gerente directo puede validar."""
        # Ponemos el estado en draft
        self.employee.telework_state = "draft"

        # Simulamos que el gerente (vinculado al parent_id) valida usando su usuario exacto
        manager_user = self.manager.user_id
        self.employee.with_user(manager_user).action_validate_telework()
        self.assertEqual(self.employee.telework_state, "validated")

    def test_validate_telework_unauthorized_fails(self):
        """Comportamiento B: Un usuario que no es el gerente no puede validar."""
        # Creamos otro usuario
        other_user = self.env["res.users"].create(
            {
                "name": "Other User",
                "login": "other_user_test",
                "email": "other@test.com",
                "groups_id": [(4, self.env.ref("base.group_user").id)],
            }
        )

        # Odoo 18 crea automáticamente el empleado al crear el usuario en entornos con RRHH.
        # Buscamos el empleado generado.
        other_employee = self.env["hr.employee"].search(
            [("user_id", "=", other_user.id)], limit=1
        )
        if not other_employee:
            other_employee = self.env["hr.employee"].create(
                {
                    "name": "Other Employee",
                    "user_id": other_user.id,
                }
            )

        self.employee.telework_state = "draft"

        # Intentamos validar con el otro usuario
        from odoo.exceptions import UserError

        with self.assertRaises(
            UserError, msg="Debería lanzar UserError al validar sin ser el gerente"
        ):
            self.employee.with_user(other_user).action_validate_telework()
