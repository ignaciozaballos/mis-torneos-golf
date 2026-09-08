"""
Club de Golf El Bosque (Valencia)

Este club no lista los torneos en su propia web, sino que usa una app
externa llamada "GolfDirecto" que carga los datos con JavaScript. Gracias a
inspeccionar las herramientas de desarrollador del navegador (pestaña
Network), encontramos la llamada real que hace esa app para pedir los
datos: una API pública en formato JSON, sin necesidad de iniciar sesión.
"""
from .utils import obtener_torneos_golfdirecto

CLUB_NOMBRE = "Club de Golf El Bosque"

# Este ID identifica a "CLUB DE GOLF EL BOSQUE" dentro de GolfDirecto.
CLUB_ID = "5de79a724d36dfe90dea37c7"

URL_INFO = "https://www.elbosquegolf.com/torneos/"


def obtener_torneos():
    return obtener_torneos_golfdirecto(CLUB_ID, CLUB_NOMBRE, URL_INFO)


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
