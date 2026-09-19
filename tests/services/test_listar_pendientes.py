from datetime import date, time

from domain.examen import Examen, ModalidadExamen
from domain.materia import Materia
from domain.tarea import EstadoTarea, Tarea
from services.listar_pendientes import ListarPendientes
from tests.fakes import ExamenRepositoryFake, MateriaRepositoryFake, TareaRepositoryFake


def test_listar_pendientes_combina_tareas_y_examenes_ordenados_por_fecha():
    materias = MateriaRepositoryFake()
    materia = materias.guardar(Materia(nombre="Bases de Datos"))
    tareas = TareaRepositoryFake()
    examenes = ExamenRepositoryFake()

    tareas.guardar(
        Tarea(materia_id=materia.id, titulo="TP tardío", fecha_limite=date(2026, 12, 20))
    )
    examenes.guardar(
        Examen(
            materia_id=materia.id,
            tema="Parcial temprano",
            fecha=date(2026, 10, 1),
            hora=time(14, 0),
            modalidad=ModalidadExamen.PRESENCIAL,
        )
    )
    tareas.guardar(
        Tarea(materia_id=materia.id, titulo="TP medio", fecha_limite=date(2026, 11, 1))
    )

    servicio = ListarPendientes(tareas, examenes, materias)
    items = servicio.ejecutar()

    assert [item.titulo for item in items] == [
        "Parcial temprano",
        "TP medio",
        "TP tardío",
    ]
    assert [item.tipo for item in items] == ["examen", "tarea", "tarea"]
    assert items[1].materia_nombre == "Bases de Datos"
    assert items[1].estado == EstadoTarea.PENDIENTE.value
    assert items[0].estado is None
    assert items[0].hora == time(14, 0)
    assert items[1].hora is None


def test_listar_pendientes_vacio_sin_tareas_ni_examenes():
    servicio = ListarPendientes(
        TareaRepositoryFake(), ExamenRepositoryFake(), MateriaRepositoryFake()
    )

    assert servicio.ejecutar() == []
