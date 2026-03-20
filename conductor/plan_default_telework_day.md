# Plan: Día Predeterminado de Teletrabajo en Calendario

Este plan detalla la implementación para que el empleado elija un día de la semana (Lunes-Viernes) como su día predeterminado de teletrabajo y este se sincronice automáticamente en el calendario.

## Objetivo

- Añadir un selector de día predeterminado en `hr.employee`.
- Generar automáticamente entradas en `hr.telework.request` para ese día de la semana.

## Cambios Propuestos

### 1. Modelo `hr.employee`

- Añadir campo `default_telework_day` (Selection) con opciones: Monday, Tuesday, Wednesday, Thursday, Friday.
- Añadir un método `_generate_telework_recurring_entries()` que:
  - Busque la fecha de los próximos 4 (o N) días de la semana seleccionados.
  - Cree registros en `hr.telework.request` si no existen para esas fechas.
- Añadir un trigger en `write` para llamar a este método cuando cambie `default_telework_day`.

### 2. Modelo `hr.telework.request`

- Asegurar que no se creen duplicados para el mismo empleado y día mediante una restricción de SQL o lógica en `create`.

### 3. Interfaz de Usuario

- Añadir el campo `default_telework_day` en `views/hr_employee_views.xml` cerca del botón inteligente de teletrabajo.

## Pasos de Implementación (TDD)

### 1. Tests (`tests/test_telework_default_day.py`)

- Crear un test que:
  - Asigne "Lunes" como día predeterminado a un empleado.
  - Verifique que se han creado las solicitudes de teletrabajo para los próximos lunes.

### 2. Extensión de `hr.employee`

- Añadir el campo y la lógica de generación recurrente.

### 3. Vistas

- Modificar `views/hr_employee_views.xml` para incluir el desplegable.

## Verificación

- Abrir la ficha del empleado.
- Seleccionar "Miércoles" en el nuevo desplegable.
- Guardar.
- Entrar en el calendario de teletrabajo y verificar que los próximos miércoles están marcados.
