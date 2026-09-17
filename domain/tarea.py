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


@dataclass
class Tarea:
    materia_id: int
    titulo: str
    fecha_limite: date
    descripcion: str = ""
    prioridad: PrioridadTarea = PrioridadTarea.MEDIA
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    id: int | None = None
