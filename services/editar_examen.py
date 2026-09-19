from datetime import date, time

from domain.examen import Examen, ModalidadExamen, editar_examen
from domain.materia import Materia, MateriaInexistenteError
from repository.examen_repository import ExamenRepository
from repository.materia_repository import MateriaRepository


class EditarExamen:
    def __init__(
        self, examen_repositorio: ExamenRepository, materia_repositorio: MateriaRepository
    ) -> None:
        self._examenes = examen_repositorio
        self._materias = materia_repositorio

    def ejecutar(
        self,
        id: int,
        materia_id: int,
        tema: str,
        fecha: date,
        hora: time | None,
        modalidad: ModalidadExamen | None,
        notas: str = "",
    ) -> Examen:
        materia: Materia | None = self._materias.obtener(materia_id)
        if materia is None:
            raise MateriaInexistenteError(
                f"No existe ninguna materia con id {materia_id}."
            )
        examen_actual = self._examenes.obtener(id)
        examen_editado = editar_examen(
            examen_actual,
            materia_id=materia_id,
            tema=tema,
            fecha=fecha,
            hora=hora,
            modalidad=modalidad,
            notas=notas,
        )
        return self._examenes.actualizar(examen_editado)
