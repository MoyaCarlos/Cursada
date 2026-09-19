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


def _validar_tema(tema: str) -> str:
    tema_limpio = tema.strip()
    if not tema_limpio:
        raise ValueError("El tema del examen no puede estar vacío.")
    return tema_limpio


def _validar_hora_y_modalidad(
    hora: time | None, modalidad: ModalidadExamen | None
) -> tuple[time, ModalidadExamen]:
    if hora is None:
        raise ValueError("La hora del examen es obligatoria.")
    if modalidad is None:
        raise ValueError("Debe elegir una modalidad para el examen.")
    return hora, modalidad


def crear_examen(
    materia_id: int,
    tema: str,
    fecha: date,
    hora: time | None,
    modalidad: ModalidadExamen | None,
    notas: str = "",
) -> Examen:
    tema_limpio = _validar_tema(tema)
    if fecha < date.today():
        raise ValueError("La fecha del examen no puede ser anterior a hoy.")
    hora, modalidad = _validar_hora_y_modalidad(hora, modalidad)
    return Examen(
        materia_id=materia_id,
        tema=tema_limpio,
        fecha=fecha,
        hora=hora,
        modalidad=modalidad,
        notas=notas.strip(),
    )


def editar_examen(
    examen_actual: Examen,
    materia_id: int,
    tema: str,
    fecha: date,
    hora: time | None,
    modalidad: ModalidadExamen | None,
    notas: str = "",
) -> Examen:
    tema_limpio = _validar_tema(tema)
    if fecha != examen_actual.fecha and fecha < date.today():
        raise ValueError("La fecha del examen no puede ser anterior a hoy.")
    hora, modalidad = _validar_hora_y_modalidad(hora, modalidad)
    return Examen(
        id=examen_actual.id,
        materia_id=materia_id,
        tema=tema_limpio,
        fecha=fecha,
        hora=hora,
        modalidad=modalidad,
        notas=notas.strip(),
    )
