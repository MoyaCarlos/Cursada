# language: es
Característica: Gestión de materias

  Escenario: Crear una materia con nombre nuevo
    Dado que no existe ninguna materia llamada "Bases de Datos"
    Cuando el usuario crea una materia llamada "Bases de Datos"
    Entonces la materia "Bases de Datos" aparece en el listado de materias

  Escenario: Rechazar un nombre de materia duplicado
    Dado que existe una materia llamada "Redes"
    Cuando el usuario intenta crear una materia llamada "redes"
    Entonces el sistema rechaza la creación por nombre duplicado

  Escenario: Rechazar un nombre de materia vacío
    Cuando el usuario intenta crear una materia con nombre vacío
    Entonces el sistema rechaza la creación por nombre obligatorio
