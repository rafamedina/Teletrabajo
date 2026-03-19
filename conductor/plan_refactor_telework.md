# Plan de Refactorización y Simplificación - Odoo 18

Este plan tiene como objetivo optimizar el código del módulo `Teletrabajo`, eliminando redundancias y aprovechando mejor las características nativas de Odoo 18.

## Objetivos

1.  **Eliminar Redundancia en `write`:** Centralizar la lógica de cambio de estado a "Sin validar" aprovechando que `onchange` ya se activa en la UI, pero asegurando la integridad en el servidor.
2.  **Optimizar el Cálculo de `is_telework_manager`:** Simplificar la lógica de visibilidad del botón de validación.
3.  **Mejorar la Legibilidad:** Refactorizar la creación de actividades para que sea más limpia y robusta.
4.  **Consolidar la Vista:** Limpiar comentarios innecesarios y asegurar que el XML sea lo más compacto posible.

## Cambios Propuestos

### 1. Modelos (`models/hr_employee.py`)

- **Simplificación de `write`:** Mantener solo la lógica esencial para resetear el estado y crear la actividad, evitando comprobaciones duplicadas.
- **Refactorización de `_create_telework_activity`:** Usar un enfoque más declarativo para la creación de la actividad.
- **Ajuste en `_compute_is_telework_manager`:** Asegurar que el cálculo sea eficiente y maneje correctamente casos sin gerente.

### 2. Vistas (`views/hr_employee_views.xml`)

- Eliminar comentarios redundantes ("PIEZA 2").
- Ajustar la disposición de los campos para una mejor experiencia de usuario (UX).

### 3. Seguridad (`security/ir.model.access.csv`)

- Mantener el archivo limpio con solo el encabezado si no hay nuevos modelos.

## Verificación

1.  **Pruebas Automatizadas:** Ejecutar `scripts/run-tests.sh unit` para asegurar que el flujo de validación y el reseteo de estado siguen funcionando.
2.  **Verificación Manual (Lógica):** Revisar que el código resultante sea más legible y siga las PEP 8 y las guías de Odoo 18.
