import sqlite3
from datetime import date, time

from domain.examen import Examen, ModalidadExamen

_SELECT_EXAMEN = """
    SELECT eventos.id, eventos.materia_id, eventos.titulo, eventos.fecha,
           eventos.hora, modalidades.nombre, examenes.notas
    FROM examenes
    JOIN eventos ON eventos.id = examenes.evento_id
    JOIN modalidades ON modalidades.id = examenes.modalidad_id
"""


class SqliteExamenRepository:
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self._conexion = conexion

    def guardar(self, examen: Examen) -> Examen:
        cursor = self._conexion.execute(
            "INSERT INTO eventos (materia_id, titulo, fecha, hora) VALUES (?, ?, ?, ?)",
            (examen.materia_id, examen.tema, examen.fecha.isoformat(), examen.hora.isoformat()),
        )
        evento_id = cursor.lastrowid
        self._conexion.execute(
            "INSERT INTO examenes (evento_id, modalidad_id, notas) VALUES (?, ?, ?)",
            (evento_id, self._id_modalidad(examen.modalidad), examen.notas),
        )
        self._conexion.commit()
        return Examen(
            id=evento_id,
            materia_id=examen.materia_id,
            tema=examen.tema,
            fecha=examen.fecha,
            hora=examen.hora,
            modalidad=examen.modalidad,
            notas=examen.notas,
        )

    def listar(self) -> list[Examen]:
        filas = self._conexion.execute(f"{_SELECT_EXAMEN} ORDER BY eventos.fecha").fetchall()
        return [self._examen_desde_fila(fila) for fila in filas]

    def _examen_desde_fila(self, fila) -> Examen:
        return Examen(
            id=fila[0],
            materia_id=fila[1],
            tema=fila[2],
            fecha=date.fromisoformat(fila[3]),
            hora=time.fromisoformat(fila[4]),
            modalidad=ModalidadExamen(fila[5]),
            notas=fila[6],
        )

    def _id_modalidad(self, modalidad: ModalidadExamen) -> int:
        fila = self._conexion.execute(
            "SELECT id FROM modalidades WHERE nombre = ?", (modalidad.value,)
        ).fetchone()
        return fila[0]
