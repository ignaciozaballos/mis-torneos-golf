"""
Club de Golf Escorpión (Valencia)

Este club usa el plugin "The Events Calendar" de WordPress, que ofrece un
feed de calendario estándar en formato .ics (el mismo formato que usan
Google Calendar / Outlook). Es el caso más fácil: en vez de "leer" el HTML
visual, leemos directamente ese feed de datos.
"""
import re
import datetime
from .utils import HEADERS

CLUB_NOMBRE = "Club de Golf Escorpión"
ICS_URL = "https://clubescorpion.com/?post_type=tribe_events&ical=1&eventDisplay=list"


def _parse_ics_datetime(valor):
    """Convierte un valor de fecha .ics tipo 20260909T000000Z o 20260909 en date."""
    valor = valor.strip()
    m = re.match(r"(\d{4})(\d{2})(\d{2})", valor)
    if not m:
        return None
    anio, mes, dia = m.groups()
    try:
        return datetime.date(int(anio), int(mes), int(dia))
    except ValueError:
        return None


def _unfold_ics(texto):
    """
    En formato .ics, las líneas largas se parten en varias líneas donde las
    continuaciones empiezan con un espacio. Hay que "desplegarlas" primero.
    """
    lineas = texto.splitlines()
    resultado = []
    for linea in lineas:
        if linea.startswith(" ") and resultado:
            resultado[-1] += linea[1:]
        else:
            resultado.append(linea)
    return resultado


def obtener_torneos():
    import requests

    resp = requests.get(ICS_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    lineas = _unfold_ics(resp.text)

    torneos = []
    evento_actual = {}
    dentro_evento = False

    for linea in lineas:
        if linea.strip() == "BEGIN:VEVENT":
            dentro_evento = True
            evento_actual = {}
            continue
        if linea.strip() == "END:VEVENT":
            dentro_evento = False
            nombre = evento_actual.get("SUMMARY")
            fecha = evento_actual.get("DTSTART")
            if nombre and fecha:
                torneos.append({
                    "club": CLUB_NOMBRE,
                    "nombre": nombre,
                    "fecha": fecha.isoformat(),
                    "url": evento_actual.get("URL", ICS_URL),
                })
            continue

        if not dentro_evento or ":" not in linea:
            continue

        clave, _, valor = linea.partition(":")
        clave_base = clave.split(";")[0]  # p.ej. "DTSTART;VALUE=DATE" -> "DTSTART"

        if clave_base == "SUMMARY":
            # Quitamos el escapado típico de .ics (\, \; \n)
            evento_actual["SUMMARY"] = (
                valor.replace("\\,", ",").replace("\\;", ";").replace("\\n", " ").strip()
            )
        elif clave_base == "DTSTART":
            evento_actual["DTSTART"] = _parse_ics_datetime(valor)
        elif clave_base == "URL":
            evento_actual["URL"] = valor.strip()

    return torneos


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
