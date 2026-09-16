# Modelo de datos

Esquema normalizado a 3FN. Decisiones clave explicadas al final de cada bloque.

```
materias
  id (PK)
  nombre

estados            -- lookup: "pendiente", "en_progreso", "completada"
  id (PK)
  nombre

prioridades        -- lookup: "baja", "media", "alta"
  id (PK)
  nombre

modalidades        -- lookup: "presencial", "virtual"
  id (PK)
  nombre

eventos            -- tabla padre: lo que tienen en común tarea y examen
  id (PK)
  materia_id (FK -> materias)
  titulo
  fecha
  hora

tareas             -- extiende eventos (1 a 1)
  evento_id (PK, FK -> eventos.id)
  descripcion
  estado_id (FK -> estados)
  prioridad_id (FK -> prioridades)

examenes           -- extiende eventos (1 a 1)
  evento_id (PK, FK -> eventos.id)
  modalidad_id (FK -> modalidades)
  notas

recordatorios
  id (PK)
  evento_id (FK -> eventos.id)
  anticipacion_minutos    -- unidad única (ej: 4320 = 3 días antes)

canales_notificacion
  id (PK)
  nombre                  -- "email", "escritorio" (telegram se agrega después)
  activo

configuracion_email       -- solo existe si el canal email está en uso
  canal_id (PK, FK -> canales_notificacion.id)
  smtp_host
  smtp_port
  usuario
  password_encriptada
  email_destino

recordatorio_envios       -- historial/registro de disparos, por canal
  id (PK)
  recordatorio_id (FK -> recordatorios.id)
  canal_id (FK -> canales_notificacion.id)
  fecha_hora_envio
  estado                  -- "enviado", "fallido"
```

## Por qué cumple 3FN
- `eventos` como padre de `tareas`/`examenes` elimina la necesidad de una FK
  polimórfica en `recordatorios` (que a veces apunte a una tarea, a veces a un
  examen): `recordatorios.evento_id` es siempre del mismo tipo de referencia.
- Los lookup (`estados`, `prioridades`, `modalidades`) evitan que el nombre del
  estado/prioridad sea un atributo transitivo repetido en `tareas`/`examenes`.
- `configuracion_email` está separada de `canales_notificacion` en vez de una
  tabla ancha con columnas de credenciales de todos los canales — si se suma
  `configuracion_telegram` a futuro, es una tabla nueva, no columnas nulas en
  una tabla compartida.
- `recordatorio_envios` separa el intento de envío (que puede fallar, es
  distinto por canal, y se reintenta) de la definición del recordatorio.

## Decisiones que no están en el esquema (viven en el dominio)
- **`fecha_disparo`** de un recordatorio NO se guarda calculada: se deriva de
  `eventos.fecha` y `recordatorios.anticipacion_minutos` al vuelo. Guardarla
  sería un atributo redundante (derivable de datos ya presentes).
- **"Completado"** no es una columna en `examenes`: se infiere en el dominio
  (`esta_completado(evento)`) comparando la fecha del examen con hoy. Para
  `tareas` sí es explícito (`estado_id`), porque una tarea puede seguir
  pendiente después de su fecha límite (vencida), cosa que un examen no puede.
