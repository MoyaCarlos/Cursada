# Contrato: MateriaRepository

Puerto (interfaz) que `services/` usa para persistir materias, sin conocer
SQLite. Se define como `typing.Protocol` en `repository/materia_repository.py`.

```python
class MateriaRepository(Protocol):
    def guardar(self, materia: Materia) -> Materia:
        """Inserta o actualiza una materia. Devuelve la materia con id asignado."""

    def existe_nombre(self, nombre: str, excluir_id: int | None = None) -> bool:
        """True si ya existe una materia con ese nombre (case-insensitive).
        `excluir_id` se usa al editar, para no comparar la materia consigo misma."""

    def listar(self) -> list[Materia]:
        """Todas las materias existentes."""

    def obtener(self, id: int) -> Materia | None:
        """Una materia por id, o None si no existe."""

    def eliminar(self, id: int) -> None:
        """Elimina la materia. El llamador (service) ya validó que no tiene
        eventos asociados antes de invocar esto."""

    def tiene_eventos_asociados(self, materia_id: int) -> bool:
        """True si existe al menos una fila en `eventos` con ese materia_id."""
```

**Implementación de producción**: `SqliteMateriaRepository`, en
`repository/sqlite_materia_repository.py`.

**Implementación para tests**: un fake en memoria (diccionario), definido en
`tests/` — no un mock; un fake real que respeta el contrato completo, para
poder testear los `services/` sin tocar disco.
