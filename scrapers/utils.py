"""
Funciones de ayuda compartidas por todos los scrapers.
"""
import re
import datetime
import requests

# Cabeceras para que las webs no nos bloqueen pensando que somos un bot raro.
# Cuantas más cabeceras "de navegador real" mandemos, menos posibilidades de
# que algún filtro anti-bot nos rechace con un error 403.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}

MESES_ES_ABR = {
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12,
}

MESES_EN_ABR = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def get_soup(url, timeout=20, referer=None):
    """Descarga una URL y la devuelve como objeto BeautifulSoup."""
    from bs4 import BeautifulSoup
    headers = dict(HEADERS)
    if referer:
        headers["Referer"] = referer
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_fecha_es(texto, anio_referencia=None):
    """
    Intenta extraer una fecha (datetime.date) de un texto en español.
    Soporta formatos como:
      - "10 de Septiembre 2026"
      - "10 septiembre 2026"
      - "10 Sep 2026"
    Devuelve None si no encuentra nada reconocible.
    """
    if not texto:
        return None
    texto = texto.strip().lower()

    # "10 de septiembre de 2026" / "10 de septiembre 2026" / "10 septiembre 2026"
    m = re.search(
        r"(\d{1,2})\s*(?:de)?\s*([a-záéíóúñ]+)\s*(?:de)?\s*(\d{4})",
        texto,
    )
    if m:
        dia, mes_txt, anio = m.groups()
        mes = MESES_ES.get(mes_txt) or MESES_ES_ABR.get(mes_txt[:3])
        if mes:
            try:
                return datetime.date(int(anio), mes, int(dia))
            except ValueError:
                return None

    # "10 Sep 2026" (abreviaturas en inglés, como en Oliva Nova)
    m = re.search(r"(\d{1,2})\s+([a-z]{3})\s+(\d{4})", texto)
    if m:
        dia, mes_txt, anio = m.groups()
        mes = MESES_EN_ABR.get(mes_txt)
        if mes:
            try:
                return datetime.date(int(anio), mes, int(dia))
            except ValueError:
                return None

    return None


def hoy():
    return datetime.date.today()


def obtener_torneos_golfdirecto(club_id, club_nombre, url_info):
    """
    Función genérica para clubes que usan la app GolfDirecto para publicar
    sus torneos (en vez de listarlos en su propia web). Llama a la API
    pública de GolfDirecto, encontrada inspeccionando las peticiones de red
    del navegador (pestaña Network de las herramientas de desarrollador).
    """
    import requests

    api_url = "https://www.golfdirecto.com/api/v2/public/tournament/last"
    params = {
        "limit": 50,
        "offset": 0,
        "filter[name]": "",
        "filter[gameStatus][0]": "scheduled",  # solo próximos, no ya jugados
        "filter[club]": club_id,
        "filter[withRegistration]": "false",
        "filter[profile]": "official",
        "sort": "-sortingDate",
        "fromSearchForm": "false",
    }

    resp = requests.get(api_url, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    torneos = []
    docs = data.get("data", {}).get("docs", [])

    for doc in docs:
        nombre = (doc.get("name") or "").strip()
        fecha_iso = doc.get("sortingDate")  # ej: "2026-09-13T07:30:14.080Z"
        if not nombre or not fecha_iso:
            continue

        fecha = fecha_iso[:10]  # nos quedamos solo con "AAAA-MM-DD"

        torneos.append({
            "club": club_nombre,
            "nombre": nombre,
            "fecha": fecha,
            "url": url_info,
        })

    return torneos
