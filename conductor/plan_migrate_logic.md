# Plan: Migración de Lógica al Modelo Teletrabajo

Este plan detalla cómo trasladar la lógica visual (rayado/sólido) y funcional (validación por gerente) al nuevo modelo `hr.telework.request`.

## Objetivo

- Replicar el comportamiento visual del antiguo calendario de ausencias (amarillo/verde rayado para borrador, sólido para validado).
- Restringir la validación de solicitudes únicamente al responsable del empleado.

## Cambios Propuestos

### 1. Modelo `hr.telework.request`

- Añadir campo computado `color` (Integer) para controlar las clases CSS del calendario.
  - `draft` -> Valor que represente el estado rayado.
  - `validated` -> Valor que represente el estado sólido.
- Mejorar el método `action_validate()`:
  - Verificar que el usuario sea el `parent_id.user_id` del empleado.
  - Lanzar `UserError` si no tiene permiso.

### 2. Estilos CSS (`static/src/css/telework_timeoff.css`)

- Adaptar los selectores para que funcionen con las clases generadas por el nuevo modelo.
- Asegurar que el estado `draft` añada la clase `o_event_hatched` o similar, o simplemente usar un color distinto que el CSS pinte como rayado.

### 3. Vista Calendario

- Asegurar que el atributo `color` apunte al nuevo campo.

## Pasos de Implementación (TDD)

### 1. Tests (`tests/test_telework_logic_migration.py`)

- Verificar que un usuario no responsable no puede validar una solicitud de teletrabajo.
- Verificar que el campo `color` cambia según el `state`.

### 2. Actualización de Modelo `hr.telework.request`

- Añadir campo `color`.
- Refactorizar `action_validate`.

### 3. Actualización de CSS

- Limpiar y simplificar los selectores para que sean específicos al modelo de teletrabajo.

## Verificación

- Crear una solicitud de teletrabajo.
- Verificar visualmente que aparece "rayada" en el calendario.
- Validar con el gerente y verificar que cambia a "sólida".
- Intentar validar con otro usuario y verificar el error.
