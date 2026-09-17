# language: es
Característica: Editar y eliminar examen

  Escenario: Editar el tema de un examen
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe un examen "Parcial 1" para "Bases de Datos" el "2026-11-10" a las "14:00" modalidad "presencial"
    Cuando el usuario edita el tema de "Parcial 1" a "Parcial 1 - Reprogramado"
    Entonces el examen "Parcial 1 - Reprogramado" aparece en el listado de exámenes

  Escenario: Rechazar la edición con tema vacío
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe un examen "Parcial 1" para "Bases de Datos" el "2026-11-10" a las "14:00" modalidad "presencial"
    Cuando el usuario intenta editar el tema de "Parcial 1" dejándolo vacío
    Entonces el sistema rechaza la edición del examen por tema obligatorio

  Escenario: Rechazar cambiar la fecha a una fecha pasada
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe un examen "Parcial 1" para "Bases de Datos" el "2026-11-10" a las "14:00" modalidad "presencial"
    Cuando el usuario intenta cambiar la fecha de "Parcial 1" a "2020-01-01"
    Entonces el sistema rechaza la edición del examen por fecha pasada

  Escenario: Rechazar reasignar un examen a una materia inexistente
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe un examen "Parcial 1" para "Bases de Datos" el "2026-11-10" a las "14:00" modalidad "presencial"
    Cuando el usuario intenta reasignar el examen "Parcial 1" a una materia inexistente
    Entonces el sistema rechaza la edición del examen por materia inexistente

  Escenario: Eliminar un examen
    Dado que existe una materia llamada "Bases de Datos"
    Y que existe un examen "Parcial 1" para "Bases de Datos" el "2026-11-10" a las "14:00" modalidad "presencial"
    Cuando el usuario elimina el examen "Parcial 1"
    Entonces el examen "Parcial 1" no aparece en el listado de exámenes
