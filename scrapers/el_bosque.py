"""
Club de Golf El Bosque (Valencia)

Este club no lista los torneos en su propia web, sino que usa una app
externa llamada "GolfDirecto" que carga los datos con JavaScript. Gracias a
inspeccionar las herramientas de desarrollador del navegador (pestaña
Network), encontramos la llamada real que hace esa app para pedir los
datos: una API pública en formato JSON, sin necesidad de iniciar sesión.
"""
import requests
from .utils import HEADERS

CLUB_NOMBRE = "Club de Golf El Bosque"
API_URL = "https://www.golfdirecto.com/api/v2/public/tournament/last"

# Este ID identifica a "CLUB DE GOLF EL BOSQUE" dentro de GolfDirecto.
CLUB_ID = "5de79a724d36dfe90dea37c7"

URL_INFO = "https://www.elbosquegolf.com/torneos/"


def obtener_torneos():
    params = {
        "limit": 50,
        "offset": 0,
        "filter[name]": "",
        "filter[gameStatus][0]": "scheduled",  # solo próximos, no ya jugados
        "filter[club]": CLUB_ID,
        "filter[withRegistration]": "false",
        "filter[profile]": "official",
        "sort": "-sortingDate",
        "fromSearchForm": "false",
    }

    resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=20)
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
            "club": CLUB_NOMBRE,
            "nombre": nombre,
            "fecha": fecha,
            "url": URL_INFO,
        })

    return torneos


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
