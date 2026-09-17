import sqlite3

from domain.materia import Materia


def _normalizar(nombre: str) -> str:
    return nombre.strip().lower()


class SqliteMateriaRepository:
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self._conexion = conexion

    def guardar(self, materia: Materia) -> Materia:
        normalizado = _normalizar(materia.nombre)
        if materia.id is None:
            cursor = self._conexion.execute(
                "INSERT INTO materias (nombre, nombre_normalizado) VALUES (?, ?)",
                (materia.nombre, normalizado),
            )
            self._conexion.commit()
            return Materia(id=cursor.lastrowid, nombre=materia.nombre)
        self._conexion.execute(
            "UPDATE materias SET nombre = ?, nombre_normalizado = ? WHERE id = ?",
            (materia.nombre, normalizado, materia.id),
        )
        self._conexion.commit()
        return materia

    def existe_nombre(self, nombre: str, excluir_id: int | None = None) -> bool:
        normalizado = _normalizar(nombre)
        if excluir_id is None:
            fila = self._conexion.execute(
                "SELECT 1 FROM materias WHERE nombre_normalizado = ?", (normalizado,)
            ).fetchone()
        else:
            fila = self._conexion.execute(
                "SELECT 1 FROM materias WHERE nombre_normalizado = ? AND id != ?",
                (normalizado, excluir_id),
            ).fetchone()
        return fila is not None

    def listar(self) -> list[Materia]:
        filas = self._conexion.execute(
            "SELECT id, nombre FROM materias ORDER BY nombre"
        ).fetchall()
        return [Materia(id=fila[0], nombre=fila[1]) for fila in filas]

    def obtener(self, id: int) -> Materia | None:
        fila = self._conexion.execute(
            "SELECT id, nombre FROM materias WHERE id = ?", (id,)
        ).fetchone()
        return Materia(id=fila[0], nombre=fila[1]) if fila else None

    def eliminar(self, id: int) -> None:
        self._conexion.execute("DELETE FROM materias WHERE id = ?", (id,))
        self._conexion.commit()

    def tiene_eventos_asociados(self, materia_id: int) -> bool:
        fila = self._conexion.execute(
            "SELECT 1 FROM eventos WHERE materia_id = ? LIMIT 1", (materia_id,)
        ).fetchone()
        return fila is not None
