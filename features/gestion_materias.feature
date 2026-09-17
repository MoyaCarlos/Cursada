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

  Escenario: Editar el nombre de una materia
    Dado que existe una materia llamada "Analisis Matematico"
    Cuando el usuario edita "Analisis Matematico" para que se llame "Análisis Matemático"
    Entonces la materia "Análisis Matemático" aparece en el listado de materias

  Escenario: Rechazar la edición a un nombre usado por otra materia
    Dado que existe una materia llamada "Redes"
    Y que existe una materia llamada "Sistemas Operativos"
    Cuando el usuario intenta editar "Sistemas Operativos" para que se llame "redes"
    Entonces el sistema rechaza la edición por nombre duplicado

  Escenario: Eliminar una materia sin tareas ni exámenes asociados
    Dado que existe una materia llamada "Redes"
    Cuando el usuario elimina "Redes"
    Entonces la materia "Redes" no aparece en el listado de materias

  Escenario: Rechazar la eliminación de una materia con eventos asociados
    Dado que existe una materia llamada "Bases de Datos"
    Y que la materia "Bases de Datos" tiene un evento asociado
    Cuando el usuario intenta eliminar "Bases de Datos"
    Entonces el sistema rechaza la eliminación por tener eventos asociados
