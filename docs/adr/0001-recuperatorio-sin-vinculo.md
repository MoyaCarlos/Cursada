# Recuperatorio como Examen nuevo, sin vínculo al original

El modelo no distingue un examen recuperatorio de uno regular ni los vincula entre sí:
un recuperatorio se carga simplemente como un nuevo `Examen` de la misma `Materia`. Se
decidió así porque el dominio ya excluyó (YAGNI) trackear si un examen fue aprobado o
desaprobado — sin ese dato, un vínculo entre examen original y recuperatorio no aporta
nada al usuario, solo complejidad (columna de auto-referencia, reglas de qué pasa si se
borra el original). Si en el futuro se agrega seguimiento de resultados, se reevalúa.

**Status**: accepted
