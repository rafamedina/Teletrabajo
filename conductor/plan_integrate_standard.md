# Plan de Integración de Teletrabajo en Sección Estándar

Este plan tiene como objetivo integrar el botón de validación y el estado del teletrabajo en la sección nativa de Odoo 18, evitando duplicidades.

## Objetivos

1.  **Eliminar Redundancia de Campos:** Dado que Odoo 18 ya incluye los campos de ubicación diaria, eliminaremos su definición de nuestro modelo y solo añadiremos la lógica y el estado.
2.  **Fusión de Vistas:** Integrar el estado y el botón de validación dentro del grupo existente "Teletrabajo" en la pestaña de "Información de trabajo".

## Cambios Propuestos

### 1. Modelos (`models/hr_employee.py`)

- Eliminar las definiciones de `monday_location_id`, `tuesday_location_id`, etc., ya que son campos base en Odoo 18.
- Mantener los métodos de negocio (`write`, `action_validate_telework`, `_create_telework_activity`) que ahora actuarán sobre los campos estándar.

### 2. Vistas (`views/hr_employee_views.xml`)

- Cambiar el XPath para apuntar directamente al campo `monday_location_id` existente en la vista base.
- Insertar el bloque de estado y validación _antes_ de este campo, dentro del grupo nativo de Odoo.
- No re-declarar los campos de ubicación en el XML, solo inyectar nuestras piezas personalizadas.

## Verificación

1.  **Unit Tests:** Comprobar que los tests siguen funcionando al usar los campos nativos de Odoo 18.
2.  **Integridad de la Vista:** Asegurar que no hay errores de XPath y que el botón aparece en la posición solicitada.
