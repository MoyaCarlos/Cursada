from repository.db import conectar, crear_tablas
from repository.sqlite_materia_repository import SqliteMateriaRepository
from ui.ventana_materias import VentanaMaterias


def main() -> None:
    conexion = conectar()
    crear_tablas(conexion)
    repositorio = SqliteMateriaRepository(conexion)
    ventana = VentanaMaterias(repositorio)
    ventana.mainloop()


if __name__ == "__main__":
    main()
