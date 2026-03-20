# Plan: Reestructuración de Módulo de Teletrabajo

Este plan detalla la independización del calendario de teletrabajo del módulo de ausencias y su reubicación en un Botón Inteligente en la ficha del empleado.

## Objetivo

- Eliminar la dependencia funcional del calendario de teletrabajo con el modelo `hr.leave`.
- Crear un modelo específico para registrar los días de teletrabajo.
- Añadir un Smart Button en `hr.employee` para visualizar el calendario de teletrabajo del empleado.

## Archivos Clave

- `models/telework_request.py` (Nuevo): Modelo para las solicitudes/días de teletrabajo.
- `models/hr_employee.py`: Lógica para el Smart Button y contador.
- `views/telework_request_views.xml` (Nuevo): Vistas de calendario, lista y formulario para el nuevo modelo.
- `views/hr_employee_views.xml`: Herencia para añadir el Smart Button y eliminar la pestaña antigua (si existiera).

## Pasos de Implementación

### 1. Preparación de Pruebas (TDD)

- Crear `tests/test_telework_calendar.py` para verificar:
  - Creación de registros de teletrabajo.
  - El Smart Button en el empleado devuelve la acción correcta con el filtro de empleado.
  - El contador del Smart Button refleja el número de días/solicitudes futuras.

### 2. Modelo de Teletrabajo (`telework.request`)

- Campos:
  - `name`: Descripción breve.
  - `employee_id`: Many2one a `hr.employee`.
  - `date_start`: Fecha/hora de inicio.
  - `date_stop`: Fecha/hora de fin.
  - `state`: Selección ('draft', 'validated').
- Lógica de validación (similar a la existente en el empleado).

### 3. Vistas del nuevo modelo

- Vista **Calendar**: Para visualizar los días de teletrabajo de forma intuitiva.
- Vista **Tree/Form**: Para gestión individual.
- Acción de ventana: Apuntando a la vista de calendario por defecto.

### 4. Integración en Empleado

- Añadir campo computado `telework_count` en `hr.employee`.
- Añadir Smart Button en la vista `hr.employee.form`.
- Eliminar cualquier pestaña o integración previa con `hr.leave` que sea redundante.

### 5. Limpieza de Dependencias

- Evaluar si `hr_holidays` sigue siendo necesario en `__manifest__.py`.
- Eliminar `data/hr_leave_type_data.xml` si el tipo de ausencia ya no se usará.

## Verificación

- Ejecutar los nuevos tests de calendario.
- Verificar visualmente en Odoo que el botón inteligente abre el calendario filtrado.
