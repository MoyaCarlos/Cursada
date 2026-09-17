from dataclasses import dataclass
from datetime import date
from enum import Enum


class EstadoTarea(Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"


class PrioridadTarea(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class MateriaInexistenteError(ValueError):
    pass


@dataclass
class Tarea:
    materia_id: int
    titulo: str
    fecha_limite: date
    descripcion: str = ""
    prioridad: PrioridadTarea = PrioridadTarea.MEDIA
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    id: int | None = None


def _validar_titulo(titulo: str) -> str:
    titulo_limpio = titulo.strip()
    if not titulo_limpio:
        raise ValueError("El título de la tarea no puede estar vacío.")
    return titulo_limpio


def crear_tarea(
    materia_id: int,
    titulo: str,
    fecha_limite: date,
    descripcion: str = "",
    prioridad: PrioridadTarea = PrioridadTarea.MEDIA,
) -> Tarea:
    titulo_limpio = _validar_titulo(titulo)
    if fecha_limite < date.today():
        raise ValueError("La fecha límite no puede ser anterior a hoy.")
    return Tarea(
        materia_id=materia_id,
        titulo=titulo_limpio,
        fecha_limite=fecha_limite,
        descripcion=descripcion.strip(),
        prioridad=prioridad,
        estado=EstadoTarea.PENDIENTE,
    )


def editar_tarea(
    tarea_actual: Tarea,
    materia_id: int,
    titulo: str,
    fecha_limite: date,
    descripcion: str = "",
    prioridad: PrioridadTarea = PrioridadTarea.MEDIA,
) -> Tarea:
    titulo_limpio = _validar_titulo(titulo)
    if fecha_limite != tarea_actual.fecha_limite and fecha_limite < date.today():
        raise ValueError("La fecha límite no puede ser anterior a hoy.")
    return Tarea(
        id=tarea_actual.id,
        materia_id=materia_id,
        titulo=titulo_limpio,
        fecha_limite=fecha_limite,
        descripcion=descripcion.strip(),
        prioridad=prioridad,
        estado=tarea_actual.estado,
    )
