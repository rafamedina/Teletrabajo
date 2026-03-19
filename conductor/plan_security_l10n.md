# Plan de Mejora: Internacionalización y Reglas de Seguridad

Este plan aborda la implementación de la internacionalización de cadenas de texto y la creación de reglas de registro para el modelo de teletrabajo.

## Objetivos

1.  **Internacionalización (Punto 3):** Asegurar que todos los mensajes y etiquetas sean traducibles mediante el uso de `_()`.
2.  **Reglas de Registro (Punto 1):** Definir reglas de seguridad (`ir.rule`) para restringir el acceso a los datos de teletrabajo a nivel de registro.

## Cambios Propuestos

### 1. Modelos (`models/hr_employee.py`)

- Importar la función `_` desde `odoo`.
- Envolver etiquetas de campos, mensajes de `UserError`, y contenidos de actividades (`summary`, `note`) en `_()`.

### 2. Seguridad (`security/telework_security.xml`) - NUEVO

- Crear reglas de registro para el modelo `hr.employee`:
  - **Regla de Empleado:** Acceso de lectura a su propio registro.
  - **Regla de Gerente:** Acceso de lectura/escritura a los registros de sus subordinados directos.
  - _Nota:_ Estas reglas se diseñarán para complementar las de Odoo base sin restringir la visibilidad pública necesaria del directorio de empleados.

### 3. Manifiesto (`__manifest__.py`)

- Incluir el nuevo archivo `security/telework_security.xml` en la sección `data`.

## Verificación

1.  Verificar que el módulo carga sin errores.
2.  Comprobar que los mensajes de error aparecen correctamente (en el idioma base por ahora).
3.  Validar mediante los tests existentes que la lógica de permisos sigue funcionando.
