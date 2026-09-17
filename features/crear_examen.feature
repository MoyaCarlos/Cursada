# language: es
Característica: Crear examen

  Escenario: Crear un examen con datos válidos
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario crea un examen "Parcial 1" para "Bases de Datos" el "2026-11-10" a las "14:00" modalidad "presencial"
    Entonces el examen "Parcial 1" aparece en el listado de exámenes

  Escenario: Rechazar un examen sin tema
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario intenta crear un examen sin tema para "Bases de Datos"
    Entonces el sistema rechaza la creación del examen por tema obligatorio

  Escenario: Rechazar un examen con fecha pasada
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario intenta crear un examen "Parcial 1" para "Bases de Datos" el "2020-01-01" a las "14:00" modalidad "presencial"
    Entonces el sistema rechaza la creación del examen por fecha pasada

  Escenario: Rechazar un examen sin hora
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario intenta crear un examen "Parcial 1" para "Bases de Datos" sin indicar hora
    Entonces el sistema rechaza la creación del examen por hora obligatoria

  Escenario: Rechazar un examen sin modalidad
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario intenta crear un examen "Parcial 1" para "Bases de Datos" sin indicar modalidad
    Entonces el sistema rechaza la creación del examen por modalidad obligatoria

  Escenario: Rechazar la creación sin ninguna materia cargada
    Cuando el usuario intenta crear un examen "Parcial 1" para una materia inexistente
    Entonces el sistema rechaza la creación del examen por materia inexistente
