# Plan de Migración: Modalidades de Teletrabajo a `hr.telework.request`

## Objetivo

Mover la lógica de "modalidades de teletrabajo" (que antes residía en el módulo de ausencias `hr.leave`) hacia el nuevo modelo independiente `hr.telework.request`, manteniendo la paridad de funcionalidades.

## Archivos Clave & Contexto

- `models/telework_request.py`: Modelo principal de las solicitudes de teletrabajo.
- `views/telework_request_views.xml`: Vistas de formulario, lista y calendario.
- `tests/test_telework_request_fields.py`: Tests unitarios.

## Fases de Implementación (TDD Obligatorio)

### Fase 1: Tests (Red)

1. Modificar/crear tests en `tests/test_telework_request_fields.py` para asegurar que el modelo `hr.telework.request` contenga el campo `telework_type` (Modalidad de teletrabajo) y que su comportamiento sea correcto.
2. Ejecutar tests y comprobar que fallan.

### Fase 2: Implementación en Python (Green)

1. Añadir el campo `telework_type` en `models/telework_request.py`. Este campo debe ser un `Selection` (ej. Híbrido, 100% Remoto, Puntual) o un modelo relacionado si se requiere alta configurabilidad. _Se utilizará un campo Selection por defecto para mantener la simplicidad_.
2. Asegurar que las reglas de negocio (colores, descripciones) dependan de esta modalidad si es necesario.

### Fase 3: Vistas XML (Refactor)

1. Modificar `views/telework_request_views.xml`:
   - Añadir `telework_type` a la vista `<form>`.
   - Añadir `telework_type` a la vista `<tree>` (lista).
   - Añadir `telework_type` como campo de búsqueda y filtro (Group By) en la vista `<search>`.
   - Asegurar que la vista `<calendar>` muestre información relevante sobre la modalidad.

### Fase 4: Limpieza de Módulo de Ausencias

1. Verificar si existen datos huérfanos de `hr.leave.type` relacionados con teletrabajo en el proyecto y eliminarlos para evitar conflictos y cumplir con el mandato de "simplicidad quirúrgica".

## Verificación & Pruebas

- [ ] Los tests de `hr.telework.request` pasan correctamente (`pytest` o comando Odoo).
- [ ] La interfaz de usuario muestra el campo "Modalidad" en todas las vistas de `hr.telework.request`.
- [ ] No existen dependencias del módulo de ausencias para gestionar teletrabajo.
