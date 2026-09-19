from datetime import date, time

from domain.examen import Examen, ModalidadExamen
from domain.materia import Materia
from repository.db import conectar, crear_tablas
from repository.sqlite_examen_repository import SqliteExamenRepository
from repository.sqlite_materia_repository import SqliteMateriaRepository


def test_listar_devuelve_los_examenes_ordenados_por_fecha_ascendente():
    conexion = conectar(":memory:")
    crear_tablas(conexion)
    materias = SqliteMateriaRepository(conexion)
    examenes = SqliteExamenRepository(conexion)
    materia = materias.guardar(Materia(nombre="Bases de Datos"))

    examenes.guardar(
        Examen(
            materia_id=materia.id,
            tema="Tercero",
            fecha=date(2026, 12, 15),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    )
    examenes.guardar(
        Examen(
            materia_id=materia.id,
            tema="Primero",
            fecha=date(2026, 10, 5),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    )
    examenes.guardar(
        Examen(
            materia_id=materia.id,
            tema="Segundo",
            fecha=date(2026, 11, 20),
            hora=time(14, 0),
            modalidad=ModalidadExamen.VIRTUAL,
        )
    )

    temas = [e.tema for e in examenes.listar()]

    assert temas == ["Primero", "Segundo", "Tercero"]
