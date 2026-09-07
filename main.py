"""
Script principal.

Ejecuta todos los scrapers disponibles, junta los torneos, descarta los que
ya han pasado, los ordena por fecha, y guarda el resultado en
docs/data.json (esa carpeta "docs" es la que luego publicamos como web con
GitHub Pages).

Uso:
    python main.py
"""
import json
import datetime
import traceback
from pathlib import Path

from scrapers import escorpion, foressos, parador_saler, oliva_nova, el_bosque

SCRAPERS = [
    escorpion,
    foressos,
    parador_saler,
    oliva_nova,
    el_bosque,
]

SALIDA = Path(__file__).parent / "docs" / "data.json"


def main():
    todos_los_torneos = []
    resumen = []

    for modulo in SCRAPERS:
        nombre_club = getattr(modulo, "CLUB_NOMBRE", modulo.__name__)
        try:
            torneos = modulo.obtener_torneos()
            todos_los_torneos.extend(torneos)
            resumen.append(f"OK  - {nombre_club}: {len(torneos)} torneos encontrados")
        except Exception as e:
            resumen.append(f"FALLO - {nombre_club}: {e}")
            traceback.print_exc()

    hoy = datetime.date.today().isoformat()

    # Solo torneos de hoy en adelante
    proximos = [t for t in todos_los_torneos if t["fecha"] >= hoy]
    # Ordenados por fecha
    proximos.sort(key=lambda t: t["fecha"])

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(
            {
                "actualizado": datetime.datetime.now().isoformat(timespec="seconds"),
                "torneos": proximos,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("\n".join(resumen))
    print(f"\nTotal torneos próximos guardados: {len(proximos)}")
    print(f"Archivo generado en: {SALIDA}")


if __name__ == "__main__":
    main()
