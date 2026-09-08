"""
Panorámica Golf, Sports & Resort (Castellón)

La propia web de Panorámica prohíbe el acceso automático (robots.txt), pero
sus torneos también se publican a través de la app "GolfDirecto" (igual que
El Bosque). Como consultamos los datos desde GolfDirecto y no desde la web
de Panorámica, no estamos saltándonos ninguna restricción suya.
"""
from .utils import obtener_torneos_golfdirecto

CLUB_NOMBRE = "Panorámica Golf"

# Este ID identifica a "Panorámica" dentro de GolfDirecto.
CLUB_ID = "5de79a734d36dfe90dea38bf"

URL_INFO = "https://www.panoramicaclubdegolf.com/competiciones.html"


def obtener_torneos():
    return obtener_torneos_golfdirecto(CLUB_ID, CLUB_NOMBRE, URL_INFO)


if __name__ == "__main__":
    for t in obtener_torneos():
        print(t)
