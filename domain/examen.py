from dataclasses import dataclass
from datetime import date, time
from enum import Enum


class ModalidadExamen(Enum):
    PRESENCIAL = "presencial"
    VIRTUAL = "virtual"


@dataclass
class Examen:
    materia_id: int
    tema: str
    fecha: date
    hora: time
    modalidad: ModalidadExamen
    notas: str = ""
    id: int | None = None
