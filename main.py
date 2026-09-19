from repository.db import conectar, crear_tablas
from repository.sqlite_examen_repository import SqliteExamenRepository
from repository.sqlite_materia_repository import SqliteMateriaRepository
from repository.sqlite_tarea_repository import SqliteTareaRepository
from ui.ventana_principal import VentanaPrincipal


def main() -> None:
    conexion = conectar()
    crear_tablas(conexion)
    materia_repositorio = SqliteMateriaRepository(conexion)
    tarea_repositorio = SqliteTareaRepository(conexion)
    examen_repositorio = SqliteExamenRepository(conexion)

    ventana = VentanaPrincipal(materia_repositorio, tarea_repositorio, examen_repositorio)
    ventana.mainloop()


if __name__ == "__main__":
    main()
