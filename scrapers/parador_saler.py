"""
Golf Parador El Saler (Valencia)

Esta web tiene una página de torneos con paginación (?page=0, ?page=1, ...).
Cada torneo es un enlace a una ficha tipo /es/node/12345, con el título del
torneo como texto del enlace, seguido de una línea con la fecha.
"""
import re
from .utils import get_soup, parse_fecha_es

CLUB_NOMBRE = "Golf Parador El Saler"
BASE_URL = "https://paradores.es/es/torneos"
MAX_PAGINAS = 6  # límite de seguridad para no quedarnos atascados


def obtener_torneos():
    torneos = []
    vistos = set()  # ahora es global a TODAS las páginas, no se reinicia en cada una

    for pagina in range(MAX_PAGINAS):
        url = BASE_URL if pagina == 0 else f"{BASE_URL}?page={pagina}"
        soup = get_soup(url)

        # Los torneos enlazan a fichas individuales tipo /es/node/22236
        enlaces = soup.select('a[href*="/es/node/"]')
        if not enlaces:
            break

        encontrados_en_pagina = 0

        for enlace in enlaces:
            titulo = enlace.get_text(strip=True)
            href = enlace.get("href", "")
            if not titulo or href in vistos:
                continue
            vistos.add(href)

            # La fecha suele estar en el texto del bloque contenedor (la
            # tarjeta) justo después del título.
            contenedor = enlace.find_parent(["article", "div", "li"])
            texto_contenedor = contenedor.get_text(" ", strip=True) if contenedor else ""

            fecha = parse_fecha_es(texto_contenedor)
            if not fecha:
                continue

            url_completa = href if href.startswith("http") else f"https://paradores.es{href}"

            torneos.append({
                "club": CLUB_NOMBRE,
                "nombre": titulo,
                "fecha": fecha.isoformat(),
                "url": url_completa,
            })
            encontrados_en_pagina += 1

        # Si esta página no ha traído NINGÚN enlace nuevo (todos ya vistos
        # en páginas anteriores), significa que la paginación ha dejado de
        # avanzar de verdad. Paramos aquí para no repetir contenido.
        if encontrados_en_pagina == 0:
            break

    return torneos


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
