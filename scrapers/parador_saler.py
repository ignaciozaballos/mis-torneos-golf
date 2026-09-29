"""
Golf Parador El Saler (Valencia)

Esta web tiene una página de torneos con paginación (?page=0, ?page=1, ...).
Cada torneo es un enlace a una ficha tipo /es/node/12345, con el título del
torneo como texto del enlace, seguido de una línea con la fecha.

Notas sobre esta web en concreto:

1. Certificado SSL mal configurado por su parte (no envía la cadena
   completa del certificado), así que desactivamos esa comprobación solo
   para este club en concreto.

2. La web bloquea peticiones que le "huelen" a bot (error 403 Forbidden).
   Para evitarlo, primero entramos por la portada (como haría una persona
   real) y reutilizamos esas cookies para pedir cada página de torneos con
   la anterior como "Referer" — ver crear_sesion_navegador() en utils.py.
   Si aun así el sitio sigue bloqueando (por ejemplo, si exige ejecutar
   JavaScript, algo que no podemos simular sin un navegador completo), lo
   intentamos una segunda vez con "cloudscraper", una librería pensada
   específicamente para superar ese tipo de comprobaciones automáticas.

   Si en algún momento ninguna de las dos formas funciona, lo más sencillo
   es volver a añadir este club a mano en data/manual.json (como ya
   hacemos con La Sella y Mediterráneo) en vez de seguir peleando con el
   bloqueo.
"""
import time
from .utils import get_soup, parse_fecha_es, crear_sesion_navegador

CLUB_NOMBRE = "Golf Parador El Saler"
URL_PORTADA = "https://paradores.es/es"
BASE_URL = "https://paradores.es/es/torneos"
MAX_PAGINAS = 6  # límite de seguridad para no quedarnos atascados


def _extraer_torneos_de_pagina(soup, vistos):
    """Saca los torneos de una página ya descargada. Devuelve la lista de
    torneos nuevos encontrados en esa página (puede estar vacía)."""
    torneos = []
    enlaces = soup.select('a[href*="/es/node/"]')

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

    return torneos


def _intentar_con_sesion_humana():
    """
    Primer intento: sesión de requests que entra por la portada, recoge
    cookies, y va pidiendo cada página de torneos con la anterior como
    referer, igual que una persona navegando con clics.
    """
    sesion = crear_sesion_navegador(URL_PORTADA, verificar_ssl=False)

    torneos = []
    vistos = set()
    referer_actual = URL_PORTADA

    for pagina in range(MAX_PAGINAS):
        url = BASE_URL if pagina == 0 else f"{BASE_URL}?page={pagina}"
        soup = get_soup(url, verificar_ssl=False, sesion=sesion, referer=referer_actual)
        referer_actual = url

        nuevos = _extraer_torneos_de_pagina(soup, vistos)
        torneos.extend(nuevos)

        # Si esta página no ha traído NINGÚN enlace nuevo, la paginación
        # ha dejado de avanzar de verdad: paramos para no repetir contenido.
        if not nuevos and not soup.select('a[href*="/es/node/"]'):
            break

        time.sleep(0.8)  # pequeña pausa entre páginas, como tardaría una persona

    return torneos


def _intentar_con_cloudscraper():
    """
    Segundo intento (solo si el primero falla con 403): usa la librería
    cloudscraper, que sabe resolver el tipo de comprobación anti-bot basada
    en JavaScript que usan servicios como Cloudflare, sin necesitar un
    navegador completo instalado.
    """
    import cloudscraper
    from bs4 import BeautifulSoup

    scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "mobile": False})
    scraper.get(URL_PORTADA, timeout=20, verify=False)

    torneos = []
    vistos = set()

    for pagina in range(MAX_PAGINAS):
        url = BASE_URL if pagina == 0 else f"{BASE_URL}?page={pagina}"
        resp = scraper.get(url, timeout=20, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        nuevos = _extraer_torneos_de_pagina(soup, vistos)
        torneos.extend(nuevos)

        if not nuevos and not soup.select('a[href*="/es/node/"]'):
            break

        time.sleep(0.8)

    return torneos


def obtener_torneos():
    try:
        return _intentar_con_sesion_humana()
    except Exception as e:
        print(f"AVISO - El Saler: la sesión normal falló ({e}), probando con cloudscraper...")
        return _intentar_con_cloudscraper()


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
