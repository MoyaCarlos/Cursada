from dataclasses import dataclass


@dataclass
class Materia:
    nombre: str
    id: int | None = None
