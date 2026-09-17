from typing import Protocol

from domain.examen import Examen


class ExamenRepository(Protocol):
    def guardar(self, examen: Examen) -> Examen:
        """Inserta el examen (evento + examen). Devuelve el examen con id asignado."""

    def listar(self) -> list[Examen]:
        """Todos los exámenes existentes."""
