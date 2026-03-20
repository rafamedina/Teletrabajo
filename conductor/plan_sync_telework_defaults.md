# Plan: Sincronización de Días Predeterminados de Teletrabajo

Este plan detalla la implementación para que los empleados elijan sus días de teletrabajo predeterminados y estos se reflejen automáticamente en el calendario.

## Objetivo

- Permitir al empleado marcar qué ubicaciones de trabajo corresponden a teletrabajo.
- Sincronizar automáticamente el calendario (`hr.telework.request`) basado en las ubicaciones de la semana.

## Cambios Propuestos

### 1. Modelo `hr.work.location`

- Añadir campo `is_telework` (Boolean) para identificar qué ubicaciones son remotas (ej. "Home").

### 2. Modelo `hr.employee`

- Añadir lógica para detectar cambios en las ubicaciones diarias.
- Implementar un método `action_sync_telework_calendar()` que genere registros en `hr.telework.request` para las próximas 4 semanas basándose en los días que tengan asignada una ubicación marcada como `is_telework`.

### 3. Modelo `hr.telework.request`

- Añadir un campo `is_recurrent` (Boolean) para distinguir las entradas automáticas de las manuales (opcional).

### 4. Interfaz de Usuario

- Mostrar el campo `is_telework` en la vista de ubicaciones de trabajo.
- Añadir un botón en la ficha del empleado: "Sincronizar Calendario de Teletrabajo".

## Pasos de Implementación (TDD)

### 1. Tests (`tests/test_telework_sync.py`)

- Verificar que al marcar una ubicación como teletrabajo y asignarla a un lunes, la sincronización genera una solicitud para el próximo lunes.

### 2. Extensión de `hr.work.location`

- Crear `models/hr_work_location.py` con el campo `is_telework`.

### 3. Lógica de Sincronización en `hr.employee`

- Método para calcular fechas de los próximos días de la semana.
- Creación masiva de registros `hr.telework.request`.

### 4. Vistas

- Actualizar `views/hr_employee_views.xml` para incluir el botón de sincronización.
- Crear `views/hr_work_location_views.xml` para el check `is_telework`.

## Verificación

- Abrir el empleado, configurar lunes como "Home" (marcada como teletrabajo).
- Pulsar "Sincronizar".
- Abrir el Smart Button de Teletrabajo y verificar que el calendario tiene los próximos lunes ocupados.
