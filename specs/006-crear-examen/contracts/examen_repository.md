# Contrato: ExamenRepository

```python
class ExamenRepository(Protocol):
    def guardar(self, examen: Examen) -> Examen:
        """Inserta el examen (evento + examen). Devuelve el examen con id asignado."""

    def listar(self) -> list[Examen]:
        """Todos los exámenes existentes."""
```

Mismo criterio que `TareaRepository` en HU-02: mínimo necesario para esta
historia; `obtener`/`actualizar`/`eliminar` se agregan en HU-07.

**Implementación de producción**: `SqliteExamenRepository`.
**Implementación para tests**: `ExamenRepositoryFake` en `tests/fakes.py`.
