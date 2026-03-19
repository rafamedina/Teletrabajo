# Plan de Reubicación de Interfaz de Teletrabajo

Este plan detalla los pasos para mover el bloque de teletrabajo a la pestaña "Información de trabajo" del formulario de empleado, situándolo bajo un nuevo título específico.

## Objetivos

1.  **Reubicación en Pestaña:** Mover toda la lógica visual de teletrabajo a la página `work_information` (pestaña "Información de trabajo").
2.  **Jerarquía Visual:** Colocar el botón de validación y los campos de ubicación bajo el título "Teletrabajo".

## Cambios Propuestos

### 1. Vistas (`views/hr_employee_views.xml`)

- Cambiar el punto de anclaje (XPath) para apuntar a la pestaña `work_information`.
- En Odoo 18, la pestaña de información de trabajo suele identificarse por el nombre `work_information`.
- Se insertará un nuevo grupo con el título "Teletrabajo" que contendrá:
  - El indicador de estado y el botón de validación.
  - La matriz de ubicaciones diarias.

## Verificación

1.  **Carga del Módulo:** Asegurar que el XML es válido y que el XPath encuentra el objetivo en Odoo 18.
2.  **UX Check:** Confirmar visualmente (o mediante revisión de estructura) que el bloque aparece en la pestaña correcta.
