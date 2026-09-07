"""
Oliva Nova Beach & Golf Resort (Valencia)

Esta web presenta los torneos en tablas HTML normales: una tabla de
"Próximos" torneos y otra de "Anteriores". Cada fila tiene el nombre del
torneo en la primera celda y la fecha en la segunda, con formato tipo
"24 Sep 2026".
"""
from .utils import get_soup, parse_fecha_es

CLUB_NOMBRE = "Oliva Nova Beach & Golf Resort"
URL = "https://www.olivanova.com/deporte-ocio-golf-torneos"


def obtener_torneos():
    soup = get_soup(URL)
    torneos = []

    tablas = soup.find_all("table")
    if not tablas:
        # Modo diagnóstico: si no hay ninguna <table>, probablemente los
        # torneos se cargan con JavaScript después de que llegue el HTML
        # inicial (que es lo único que ve 'requests'). Volcamos pistas al
        # log para poder confirmarlo y decidir el siguiente paso.
        print("[oliva_nova] DIAGNOSTICO: no se ha encontrado ninguna <table> en la página.")
        print(f"[oliva_nova] DIAGNOSTICO: longitud del HTML recibido: {len(str(soup))} caracteres")
        texto = soup.get_text(" ", strip=True)
        idx = texto.lower().find("torneo")
        fragmento = texto[max(0, idx - 100): idx + 300] if idx != -1 else texto[:300]
        print(f"[oliva_nova] DIAGNOSTICO: fragmento de texto alrededor de 'torneo': {fragmento}")

    for tabla in tablas:
        filas = tabla.find_all("tr")
        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) < 2:
                continue
            nombre = celdas[0].get_text(strip=True)
            fecha_txt = celdas[1].get_text(strip=True)
            if not nombre or not fecha_txt:
                continue

            fecha = parse_fecha_es(fecha_txt)
            if not fecha:
                continue

            # Si la fila tiene un enlace (cartel/reglamento), lo usamos de URL
            enlace = fila.find("a", href=True)
            url_evento = enlace["href"] if enlace else URL
            if url_evento.startswith("/"):
                url_evento = "https://www.olivanova.com" + url_evento

            torneos.append({
                "club": CLUB_NOMBRE,
                "nombre": nombre,
                "fecha": fecha.isoformat(),
                "url": url_evento,
            })

    return torneos


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
