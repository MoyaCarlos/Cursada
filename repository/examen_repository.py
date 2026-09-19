from typing import Protocol

from domain.examen import Examen


class ExamenRepository(Protocol):
    def guardar(self, examen: Examen) -> Examen:
        """Inserta el examen (evento + examen). Devuelve el examen con id asignado."""

    def listar(self) -> list[Examen]:
        """Todos los exámenes existentes."""

    def obtener(self, id: int) -> Examen | None:
        """Un examen por id, o None si no existe."""

    def actualizar(self, examen: Examen) -> Examen:
        """Actualiza un examen existente (examen.id no es None)."""

    def eliminar(self, id: int) -> None:
        """Elimina el examen y su evento asociado."""
