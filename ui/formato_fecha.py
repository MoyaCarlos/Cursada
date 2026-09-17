from datetime import date


def parsear_fecha(texto: str) -> date:
    """Acepta "DD/MM/AAAA" o "DD/MM" (usa el año actual si se omite)."""
    partes = texto.strip().split("/")
    if len(partes) == 2:
        dia_str, mes_str = partes
        anio = date.today().year
    elif len(partes) == 3:
        dia_str, mes_str, anio_str = partes
        anio = int(anio_str)
    else:
        raise ValueError("La fecha debe tener el formato DD/MM o DD/MM/AAAA.")
    return date(anio, int(mes_str), int(dia_str))


def formatear_fecha(fecha: date) -> str:
    return fecha.strftime("%d/%m/%Y")
