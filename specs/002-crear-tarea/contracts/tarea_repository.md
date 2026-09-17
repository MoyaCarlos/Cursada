# Contrato: TareaRepository

Puerto que `services/` usa para persistir tareas, sin conocer SQLite.
Definido como `typing.Protocol` en `repository/tarea_repository.py`.

```python
class TareaRepository(Protocol):
    def guardar(self, tarea: Tarea) -> Tarea:
        """Inserta la tarea (evento + tarea en una sola operación).
        Devuelve la tarea con id asignado. En esta historia solo se usa
        para alta; actualizar es HU-03/HU-04."""

    def listar(self) -> list[Tarea]:
        """Todas las tareas existentes."""
```

Se mantiene mínimo a propósito (solo lo que HU-02 necesita — `obtener`,
`eliminar`, `actualizar_estado`, etc. se agregan en HU-03/HU-04 cuando haga
falta, no antes).

**Implementación de producción**: `SqliteTareaRepository`, en
`repository/sqlite_tarea_repository.py` — inserta en `eventos` y `tareas`
dentro de la misma llamada a `guardar()`, y hace el join correspondiente en
`listar()`.

**Implementación para tests**: fake en memoria en `tests/fakes.py` (junto a
`MateriaRepositoryFake`).
