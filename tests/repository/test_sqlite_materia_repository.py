from domain.materia import Materia
from repository.db import conectar, crear_tablas
from repository.sqlite_materia_repository import SqliteMateriaRepository


def test_tiene_eventos_asociados_false_sin_eventos():
    conexion = conectar(":memory:")
    crear_tablas(conexion)
    repositorio = SqliteMateriaRepository(conexion)
    materia = repositorio.guardar(Materia(nombre="Redes"))

    assert repositorio.tiene_eventos_asociados(materia.id) is False


def test_tiene_eventos_asociados_true_con_un_evento():
    conexion = conectar(":memory:")
    crear_tablas(conexion)
    repositorio = SqliteMateriaRepository(conexion)
    materia = repositorio.guardar(Materia(nombre="Redes"))
    conexion.execute(
        "INSERT INTO eventos (materia_id, titulo, fecha) VALUES (?, ?, ?)",
        (materia.id, "TP1", "2026-10-01"),
    )
    conexion.commit()

    assert repositorio.tiene_eventos_asociados(materia.id) is True
