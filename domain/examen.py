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


def crear_examen(
    materia_id: int,
    tema: str,
    fecha: date,
    hora: time | None,
    modalidad: ModalidadExamen | None,
    notas: str = "",
) -> Examen:
    tema_limpio = tema.strip()
    if not tema_limpio:
        raise ValueError("El tema del examen no puede estar vacío.")
    if fecha < date.today():
        raise ValueError("La fecha del examen no puede ser anterior a hoy.")
    if hora is None:
        raise ValueError("La hora del examen es obligatoria.")
    if modalidad is None:
        raise ValueError("Debe elegir una modalidad para el examen.")
    return Examen(
        materia_id=materia_id,
        tema=tema_limpio,
        fecha=fecha,
        hora=hora,
        modalidad=modalidad,
        notas=notas.strip(),
    )
