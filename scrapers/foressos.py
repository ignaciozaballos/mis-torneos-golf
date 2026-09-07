"""
Foressos Club de Golf (Valencia)

Esta web lista los torneos en texto plano, agrupados por mes, con un patrón
repetido: primero el NOMBRE del torneo, y justo después una línea con el día
y el mes en formato "Torneo DD de Mes" (o "Sábado DD de Mes", "Viernes DD de
Mes", etc). Buscamos ese patrón de fecha y usamos el texto justo anterior
como nombre del torneo.

NOTA: es un scraper "best effort" por texto, no por estructura HTML exacta.
Si la web cambia de diseño, este es el primero que probablemente haya que
revisar.
"""
import re
from .utils import get_soup, MESES_ES, hoy
import datetime

CLUB_NOMBRE = "Foressos Club de Golf"
URL = "https://foressosclubgolf.com/torneos/"

# Detecta cosas como "27 de Noviembre", "31 de Octubre", "6 y 7 de mayo" (nos
# quedamos con el primer día en fechas de varios días).
PATRON_FECHA = re.compile(
    r"(\d{1,2})\s*(?:y\s*\d{1,2})?\s*de\s*([A-Za-zÁÉÍÓÚñÑ]+)", re.IGNORECASE
)


def _anio_para_mes(mes_num, mes_actual_cabecera):
    """
    La web no repite el año en cada torneo, solo en la cabecera de cada mes
    (ej: 'noviembre 2026'). Como aproximación, si no tenemos ese dato,
    asumimos el año en curso, o el siguiente si el mes ya pasó hace mucho
    (para no marcar como "próximo" un torneo de hace 10 meses).
    """
    hoy_ = hoy()
    anio = hoy_.year
    if mes_num < hoy_.month - 6:
        anio += 1
    return anio


def obtener_torneos():
    soup = get_soup(URL)
    texto_completo = soup.get_text(separator="\n")
    lineas = [l.strip() for l in texto_completo.splitlines() if l.strip()]

    torneos = []
    anio_actual = hoy().year

    for i, linea in enumerate(lineas):
        # ¿Es una cabecera de mes+año del tipo "NOVIEMBRE 2026"?
        m_cabecera = re.match(r"^([A-Za-zÁÉÍÓÚñÑ]+)\s+(\d{4})$", linea)
        if m_cabecera and m_cabecera.group(1).lower() in MESES_ES:
            anio_actual = int(m_cabecera.group(2))
            continue

        m_fecha = PATRON_FECHA.search(linea)
        if not m_fecha:
            continue

        mes_txt = m_fecha.group(2).lower()
        if mes_txt not in MESES_ES:
            continue

        dia = int(m_fecha.group(1))
        mes = MESES_ES[mes_txt]

        # El nombre del torneo suele ser la línea anterior a esta.
        nombre = lineas[i - 1] if i > 0 else "Torneo sin nombre"

        try:
            fecha = datetime.date(anio_actual, mes, dia)
        except ValueError:
            continue

        torneos.append({
            "club": CLUB_NOMBRE,
            "nombre": nombre,
            "fecha": fecha.isoformat(),
            "url": URL,
        })

    return torneos


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
