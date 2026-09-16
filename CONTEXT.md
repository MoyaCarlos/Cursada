# Cursada

Glosario del dominio: seguimiento de tareas y exámenes de la facultad, con
recordatorios configurables.

## Language

**Materia**:
Una asignatura de la facultad a la que pertenecen tareas y exámenes.

**Evento**:
Concepto técnico interno que agrupa lo que Tarea y Examen tienen en común
(materia, título, fecha, hora). No se expone al usuario final: la interfaz
siempre habla de "tareas y exámenes" o "pendientes", nunca de "eventos".

**Tarea**:
Un trabajo pendiente de una Materia, con fecha límite, descripción, prioridad
y un estado propio (pendiente / en progreso / completada).

**Examen**:
Una instancia de evaluación de una Materia, con fecha, hora y modalidad. No
tiene un estado propio: se considera completado cuando su fecha ya pasó.

**Completado**:
Para una Tarea es un valor explícito de su estado. Para un Examen se infiere:
está completado si su fecha ya pasó. No existe una columna "completado" para
Examen — sería un dato redundante, derivable de la fecha.

**Vencida** (dicho de una Tarea):
Condición derivada, no un estado guardado: una Tarea está vencida cuando su
estado sigue siendo "pendiente" y su `fecha_limite` ya pasó. Se calcula en el
dominio; la base de datos no distingue "vencida" de "pendiente".

**Reprogramar** (dicho de un Examen):
Editar la fecha de un Examen ya existente — sigue siendo el mismo Evento, no
se crea un registro nuevo. Los recordatorios ya disparados quedan en el
historial (`recordatorio_envios`); los pendientes se recalculan contra la
nueva fecha.
_Avoid_: usar "reprogramar" como sinónimo de "recuperatorio" — son conceptos
distintos, ver **Recuperatorio**.

**Recuperatorio**:
Una segunda instancia de evaluación de una Materia (si se desaprobó o faltó a
la primera). Se modela como un **Examen nuevo**, sin vínculo formal al
examen original (ver `docs/adr/0001-recuperatorio-sin-vinculo.md`).
_Avoid_: confundir con "reprogramar" (eso edita el examen existente; esto
crea uno distinto).

**Recordatorio**:
Una regla de "avisar con tanta anticipación" asociada a un Evento (ej. 3 días
antes). Es la configuración de cuándo debe dispararse un aviso, no el aviso
en sí mismo.

**Anticipación**:
Tiempo, en minutos, entre el momento en que corresponde notificar y la fecha
del Evento. Unidad única (minutos) para no tener columnas separadas por
días/horas.

**Canal de notificación**:
El medio por el que se entrega un Recordatorio disparado (email, escritorio;
Telegram pendiente). Cada canal es una Strategy intercambiable — no conoce a
los demás ni al motor que los invoca.
