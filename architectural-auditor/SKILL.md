---
name: architectural-auditor
description: Realiza auditorías críticas de arquitectura, planes de implementación y cambios de código para identificar riesgos de regresión, ambigüedad y fragilidad sistémica. Úsalo antes de aprobar cualquier plan no trivial o ante fallos críticos de integración.
---

# Architectural Auditor

Este skill actúa como un filtro de calidad senior antes de la ejecución. Su objetivo es destruir planes débiles para construir implementaciones robustas.

## Workflow de Auditoría

### 1. Análisis de Superficie de Impacto

Antes de validar un plan, rastrea las dependencias transversales:

- **Odoo Models**: Busca herencias (`_inherit`) del modelo afectado en todo el proyecto.
- **XML Views**: Verifica si hay Vistas (`xpath`) que dependan de los campos modificados.
- **Security**: Valida si el nuevo modelo requiere entradas en `ir.model.access.csv` o reglas de registro (`ir.rule`).

### 2. Checklist del Abogado del Diablo

Para cada cambio propuesto, responde con evidencia:

- **Fragilidad**: ¿El cambio depende de rutas absolutas o configuraciones locales del usuario?
- **Ambigüedad**: ¿La tarea usa verbos vagos como "refactorizar" o "limpiar" sin métricas de éxito?
- **Elegancia**: ¿Se está creando deuda técnica para solucionar un síntoma en lugar de la causa raíz?

## Verificación en Odoo/Python

### Reglas de Oro

1. **ORM sobre SQL**: Prohíbe consultas SQL directas si el ORM de Odoo puede resolverlo.
2. **Contexto Limpio**: Verifica que no se estén perdiendo claves de contexto (`lang`, `tz`, `force_company`) en llamadas entre métodos.
3. **Migrabilidad**: Los cambios deben ser compatibles con futuras actualizaciones (evitar modificar campos core de Odoo sin una justificación crítica).

## Recursos de Referencia

- **Checklist de Regresiones**: Ver [references/regression-patterns.md](references/regression-patterns.md) para patrones comunes de fallos en Odoo.
- **Auditoría de Seguridad**: Ver [references/security-audit.md](references/security-audit.md) para validación de permisos.

## Ejecución de Auditoría

Si el auditor detecta un riesgo bloqueante, la ejecución debe detenerse inmediatamente. Usa el comando `grep_search` para validar suposiciones de impacto antes de emitir el veredicto.
