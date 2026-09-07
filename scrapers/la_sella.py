"""
La Sella Golf Resort & Spa (Alicante)

Esta web muestra un calendario anual en forma de tabla, con una celda por
día. Cada torneo aparece como un enlace de texto "Detalles y reserva" dentro
de la celda; el resto del texto de esa celda es el nombre del torneo y la
fecha completa (ej: "10 enero 2026").
"""
from .utils import get_soup, parse_fecha_es

CLUB_NOMBRE = "La Sella Golf Resort & Spa"
URL = "https://lasellagolf.com/competiciones"


def obtener_torneos():
    soup = get_soup(URL)
    torneos = []

    enlaces = soup.find_all("a", string=lambda s: s and "detalles y reserva" in s.lower())

    for enlace in enlaces:
        href = enlace.get("href", "")
        celda = enlace.find_parent("td") or enlace.find_parent("div")
        if not celda:
            continue

        texto_celda = celda.get_text(" ", strip=True)
        # Quitamos el texto del propio enlace para quedarnos con "nombre + fecha"
        texto_sin_enlace = texto_celda.replace(enlace.get_text(strip=True), "").strip()

        fecha = parse_fecha_es(texto_sin_enlace)
        if not fecha:
            continue

        # El nombre es el texto antes de la fecha (quitamos la fecha del final)
        nombre = texto_sin_enlace
        # Intentamos recortar la parte de la fecha del nombre
        for palabra_fecha in [str(fecha.day)]:
            idx = nombre.find(palabra_fecha)
            if idx > 0:
                nombre = nombre[:idx].strip()
                break

        if not nombre:
            nombre = "Torneo en La Sella"

        url_evento = href if href.startswith("http") else f"https://lasellagolf.com{href}"

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
