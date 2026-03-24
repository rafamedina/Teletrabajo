## Orquestación del Flujo de Trabajo

### 1. Predeterminado del Nodo de Planificación

- Entrar en modo de planificación para CUALQUIER tarea no trivial (3+ pasos o decisiones arquitectóni
- Si algo sale mal, PARAR y volver a planificar de inmediato no seguir forzando
- Usar el modo de planificación para los pasos de verificación, no solo para la construcción
- Escribir especificaciones detalladas por adelantado para reducir la ambiguedad

### 2. Estrategia de Subagentes

- Usar subagentes generosamente para mantener limpia la ventana de contexto principal Descargar la investigación, exploración y análisis paralelo en subagentes
- Para problemas complejos, asignar más cómputo a través de subagentes
- Un enfoque por subagente para una ejecución centrada

### 3. Ciclo de Automejora

Después de CUALQUIER corrección del usuario: actualizar `tasks/lessons.md` con el patrón

- Escribir reglas para ti mismo que eviten el mismo error
- Iterar sin pledad sobre estas lecciones hasta que disminuya la tasa de errores
- Revisar las lecciones al inicio de la sesión para el proyecto relevante

### 4. Verificación Antes de Finalizar

Nunca marcar una tarea coma completada sin demostrar que funciona

- Compara el comportamiento entre el principal y lus cambios cuando sea relevante
- Pregúntate: "¿Aprobaria esto un ingeniero senior?"
- Ejecutar pruebas, verificar registros, demostrar la corrección

### 5. Exigir Elegancia (Equilibrado)

- Para cambios no triviales: pauser y preguntar "¿hay una forma más elegante?"
- Si un arreglo se siente apresurado: "Sabiendo todo lo que sé ahora, implementa la solución elegante
- Omitir esto para arreglos simples y obvios - no sobre-diseñar
- Cuestionar tu propio trabajo antes de presentario

### 6. Corrección Autónoma de Errores

- Cuando se te dé un informe de error: simplemente arréglala. No pidas que te guién de la mano
- Señala los registros, errores, pruebas fallibas y luego resuelvales
  Cero cambio de contexto por parte del usuario
- Ve a arreglar las prubbas de CI que fallan sín que te digan cómo

## Gestión de Tareas

1. \*_Planificar Primero_: Escribir plan en `tasks/todo.md` con elementos marcables
2. \*_Verificar Plan_: Comprobar antes de comenzar la implementación
3. **Seguir Progress**: Harcer elementos como completados a medida que avanzas
4. \*_Explicar Cambios_: Resumen de alto nivel en cada paso
5. \*_Documentar Resultados_: Añadir sección de revisión en `tasks/todo.md`
6. \*_Capturar Lecciones_: Actualizar `tasks/lessons.md` después de las correcciones

## Principios Fundamentales

**Simplicidad Primero\*: Hacer que cada cambio sea to más simple posible. Impactar el código mínimo. **Sin Pereza*: Encontrar las causas raíz. Sin arreglos temporales. Estándares de desarrollador senior \*\*Impacto Minimo*: Los cambios solo deben tocar to necesario. Evitar introducir errores.
