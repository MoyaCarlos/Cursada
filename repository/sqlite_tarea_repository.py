import sqlite3
from datetime import date

from domain.tarea import EstadoTarea, PrioridadTarea, Tarea

_SELECT_TAREA = """
    SELECT eventos.id, eventos.materia_id, eventos.titulo, eventos.fecha,
           tareas.descripcion, estados.nombre, prioridades.nombre
    FROM tareas
    JOIN eventos ON eventos.id = tareas.evento_id
    JOIN estados ON estados.id = tareas.estado_id
    JOIN prioridades ON prioridades.id = tareas.prioridad_id
"""


class SqliteTareaRepository:
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self._conexion = conexion

    def guardar(self, tarea: Tarea) -> Tarea:
        cursor = self._conexion.execute(
            "INSERT INTO eventos (materia_id, titulo, fecha) VALUES (?, ?, ?)",
            (tarea.materia_id, tarea.titulo, tarea.fecha_limite.isoformat()),
        )
        evento_id = cursor.lastrowid
        self._conexion.execute(
            "INSERT INTO tareas (evento_id, descripcion, estado_id, prioridad_id) "
            "VALUES (?, ?, ?, ?)",
            (
                evento_id,
                tarea.descripcion,
                self._id_estado(tarea.estado),
                self._id_prioridad(tarea.prioridad),
            ),
        )
        self._conexion.commit()
        return Tarea(
            id=evento_id,
            materia_id=tarea.materia_id,
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            fecha_limite=tarea.fecha_limite,
            prioridad=tarea.prioridad,
            estado=tarea.estado,
        )

    def listar(self) -> list[Tarea]:
        filas = self._conexion.execute(f"{_SELECT_TAREA} ORDER BY eventos.fecha").fetchall()
        return [self._tarea_desde_fila(fila) for fila in filas]

    def obtener(self, id: int) -> Tarea | None:
        fila = self._conexion.execute(
            f"{_SELECT_TAREA} WHERE eventos.id = ?", (id,)
        ).fetchone()
        return self._tarea_desde_fila(fila) if fila else None

    def actualizar(self, tarea: Tarea) -> Tarea:
        self._conexion.execute(
            "UPDATE eventos SET materia_id = ?, titulo = ?, fecha = ? WHERE id = ?",
            (tarea.materia_id, tarea.titulo, tarea.fecha_limite.isoformat(), tarea.id),
        )
        self._conexion.execute(
            "UPDATE tareas SET descripcion = ?, estado_id = ?, prioridad_id = ? "
            "WHERE evento_id = ?",
            (
                tarea.descripcion,
                self._id_estado(tarea.estado),
                self._id_prioridad(tarea.prioridad),
                tarea.id,
            ),
        )
        self._conexion.commit()
        return tarea

    def eliminar(self, id: int) -> None:
        self._conexion.execute("DELETE FROM tareas WHERE evento_id = ?", (id,))
        self._conexion.execute("DELETE FROM eventos WHERE id = ?", (id,))
        self._conexion.commit()

    def _tarea_desde_fila(self, fila) -> Tarea:
        return Tarea(
            id=fila[0],
            materia_id=fila[1],
            titulo=fila[2],
            fecha_limite=date.fromisoformat(fila[3]),
            descripcion=fila[4],
            estado=EstadoTarea(fila[5]),
            prioridad=PrioridadTarea(fila[6]),
        )

    def _id_estado(self, estado: EstadoTarea) -> int:
        fila = self._conexion.execute(
            "SELECT id FROM estados WHERE nombre = ?", (estado.value,)
        ).fetchone()
        return fila[0]

    def _id_prioridad(self, prioridad: PrioridadTarea) -> int:
        fila = self._conexion.execute(
            "SELECT id FROM prioridades WHERE nombre = ?", (prioridad.value,)
        ).fetchone()
        return fila[0]
