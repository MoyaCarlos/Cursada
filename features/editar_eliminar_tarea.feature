# language: es
Característica: Editar y eliminar tarea

  Escenario: Editar el título de una tarea
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe una tarea "TP1" para "Bases de Datos" con fecha límite "2026-12-31"
    Cuando el usuario edita el título de "TP1" a "TP1 - Entrega final"
    Entonces la tarea "TP1 - Entrega final" aparece en el listado de tareas

  Escenario: Rechazar la edición con título vacío
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe una tarea "TP1" para "Bases de Datos" con fecha límite "2026-12-31"
    Cuando el usuario intenta editar el título de "TP1" dejándolo vacío
    Entonces el sistema rechaza la edición de la tarea por título obligatorio

  Escenario: Rechazar cambiar la fecha límite a una fecha pasada
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe una tarea "TP1" para "Bases de Datos" con fecha límite "2026-12-31"
    Cuando el usuario intenta cambiar la fecha límite de "TP1" a "2020-01-01"
    Entonces el sistema rechaza la edición de la tarea por fecha pasada

  Escenario: Permitir editar una tarea vencida sin tocar su fecha límite
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe una tarea vencida "TP viejo" para "Bases de Datos"
    Cuando el usuario edita la descripción de "TP viejo" a "actualizada" sin cambiar la fecha
    Entonces la tarea "TP viejo" conserva su fecha límite original

  Escenario: Rechazar reasignar una tarea a una materia inexistente
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe una tarea "TP1" para "Bases de Datos" con fecha límite "2026-12-31"
    Cuando el usuario intenta reasignar "TP1" a una materia inexistente
    Entonces el sistema rechaza la edición de la tarea por materia inexistente

  Escenario: Eliminar una tarea
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe una tarea "TP1" para "Bases de Datos" con fecha límite "2026-12-31"
    Cuando el usuario elimina la tarea "TP1"
    Entonces la tarea "TP1" no aparece en el listado de tareas
