from repository.db import conectar, crear_tablas
from repository.sqlite_examen_repository import SqliteExamenRepository
from repository.sqlite_materia_repository import SqliteMateriaRepository
from repository.sqlite_tarea_repository import SqliteTareaRepository
from ui.ventana_examenes import VentanaExamenes
from ui.ventana_materias import VentanaMaterias
from ui.ventana_tareas import VentanaTareas


def main() -> None:
    conexion = conectar()
    crear_tablas(conexion)
    materia_repositorio = SqliteMateriaRepository(conexion)
    tarea_repositorio = SqliteTareaRepository(conexion)
    examen_repositorio = SqliteExamenRepository(conexion)

    ventana = VentanaMaterias(materia_repositorio)
    VentanaTareas(ventana, tarea_repositorio, materia_repositorio)
    VentanaExamenes(ventana, examen_repositorio, materia_repositorio)
    ventana.mainloop()


if __name__ == "__main__":
    main()
