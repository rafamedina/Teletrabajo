# Referencia Técnica: Módulo Teletrabajo

Este documento proporciona una descripción técnica detallada de la maquinaria interna del módulo **Teletrabajo**. Está destinado a desarrolladores y administradores de Odoo que necesiten comprender, mantener o extender su funcionalidad.

---

## 1. Información del Módulo

- **Nombre Técnico:** `Teletrabajo`
- **Versión Compatibilidad:** Odoo 18.0
- **Arquitectura:** Extensión tipo "Puzzle". No modifica código base, inyecta su funcionalidad mediante herencia estándar de modelos y vistas.
- **Dependencias Base (`__manifest__.py`):**
  - `base`
  - `mail` (Para la creación de actividades)
  - `hr` (Módulo de Recursos Humanos principal)
  - `hr_skills`

---

## 2. Referencia de Modelos (Models)

### `hr.employee` (Extensión)

El módulo hereda el modelo principal de empleados (`hr.employee`) para inyectar campos y lógica de control de estado.

#### Nuevos Campos

| Nombre de Campo       | Tipo Técnico         | Descripción / Propósito                                                                                                                                                                                                                                                            |
| :-------------------- | :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `telework_state`      | `Selection`          | Estado actual de la validación del teletrabajo. <br> **Opciones:** `draft` (Sin validar), `validated` (Validado). <br> **Default:** `draft`. Soporta `tracking=True` para auditoría en el chatter.                                                                                 |
| `is_telework_manager` | `Boolean` (Computed) | Campo bandera no almacenado (`compute`). Se calcula dinámicamente comparando si el `user_id` del `parent_id` (gerente directo) coincide con el usuario que está realizando la petición (`self.env.user`). Se usa exclusivamente para controlar la visibilidad en la interfaz (UI). |

#### Comportamientos Modificados (Overrides)

- **`write(self, vals)`:** Sobrescrito para interceptar cualquier cambio en los campos de planificación de ubicación diaria (`monday_location_id`, `tuesday_location_id`, etc.). Si se detecta un cambio, fuerza internamente el valor `telework_state = "draft"` antes de llamar a `super()`, y posteriormente dispara la creación de la actividad de notificación (`_create_telework_activity()`).

---

## 3. Referencia Lógica y de Negocio (Methods)

Las reglas de negocio están contenidas en el modelo `hr.employee`.

### `action_validate_telework(self)`

Método invocado directamente desde el botón en la vista del formulario del empleado.

- **Propósito:** Mover el estado de teletrabajo de `draft` a `validated`.
- **Controles de Seguridad:**
  - Recupera el empleado vinculado al usuario actual de la sesión (`self.env.user.employee_id`).
  - **Bloqueo Estricto:** Si el empleado actual no existe o no coincide exactamente con el gerente directo (`employee.parent_id`), levanta un `UserError` nativo de Odoo bloqueando la transacción de base de datos.
  - El mensaje de error informa dinámicamente del nombre del gerente autorizado.

### `_create_telework_activity(self)`

Método de utilidad interno llamado por la sobreescritura de `write()`.

- **Propósito:** Generar una alerta asíncrona para el gerente cuando el empleado modifica su horario.
- **Implementación Técnica:**
  - Verifica que el empleado tenga un `parent_id` asignado y que este a su vez tenga un `user_id`.
  - Utiliza el modelo `mail.activity` para crear una nueva actividad.
  - **Parámetros de la Actividad:**
    - `activity_type_id`: Usa la referencia XML `mail.mail_activity_data_todo` (Por Hacer).
    - `res_model_id`: ID del modelo `hr.employee`.
    - `res_id`: ID del registro del empleado modificado.
    - `user_id`: ID del usuario receptor (el gerente).
    - `note`: Mensaje parametrizado indicando el nombre del empleado que ha modificado el registro.

### `@api.onchange` Trigger

- **Método:** `_onchange_telework_days(self)`
- **Propósito:** Proporciona feedback inmediato en la Interfaz de Usuario (UI). Si el usuario cambia el valor de un día en el frontend, el estado visual cambia automáticamente a "Sin validar" (`draft`) antes incluso de guardar.

---

## 4. Referencia de Vistas UI (Views)

### `hr.employee.form.inherit.telework`

Hereda la vista base del formulario de empleado (`hr.view_employee_form`) definida en el módulo `hr`.

- **Anclaje Técnico (XPath):**
  - Utiliza `expr="//field[@name='monday_location_id']"` con la posición `before`.
  - Esto asegura que el bloque de validación se inserte inmediatamente antes de la matriz semanal de localizaciones estándar de Odoo 18.
- **Reglas de Visibilidad Condicional (UI Security):**
  - El campo `is_telework_manager` se inyecta en la vista con el modificador `invisible="1"`.
  - El botón `action_validate_telework` posee el modificador compuesto: `invisible="telework_state != 'draft' or not is_telework_manager"`.
  - **Resultado:** El motor web de Odoo ocultará el botón de validación a cualquier usuario de la base de datos que no sea el jefe directo del empleado visualizado, o si el estado ya está validado.

---

## 5. Seguridad y Permisos

La seguridad de este módulo está diseñada en dos capas o niveles de defensa ("Defense in Depth"):

1.  **Capa de Presentación (Blanda):** El uso del atributo `invisible` apoyado en el campo computado `is_telework_manager` asegura que la opción de validación ni siquiera se presente a usuarios no autorizados.
2.  **Capa Lógica (Dura):** El método `action_validate_telework` re-valida la relación en el backend (`parent_id == current_employee`). Esto previene manipulaciones, ejecuciones maliciosas por RPC o llamadas directas al servidor por parte de usuarios con permisos genéricos de RRHH que no sean el gerente directo del registro.
