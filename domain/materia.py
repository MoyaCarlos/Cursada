from dataclasses import dataclass


@dataclass
class Materia:
    nombre: str
    id: int | None = None


class NombreDuplicadoError(ValueError):
    pass


class EventosAsociadosError(ValueError):
    pass


class MateriaInexistenteError(ValueError):
    pass


def crear_materia(nombre: str) -> Materia:
    nombre_limpio = nombre.strip()
    if not nombre_limpio:
        raise ValueError("El nombre de la materia no puede estar vacío.")
    return Materia(nombre=nombre_limpio)
