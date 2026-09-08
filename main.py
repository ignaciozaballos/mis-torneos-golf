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
import re
import datetime
import traceback
from pathlib import Path

from scrapers import escorpion, foressos, parador_saler, oliva_nova, el_bosque, panoramica

SCRAPERS = [
    escorpion,
    foressos,
    parador_saler,
    oliva_nova,
    el_bosque,
    panoramica,
]

SALIDA = Path(__file__).parent / "docs" / "data.json"
MANUAL = Path(__file__).parent / "data" / "manual.json"


def cargar_torneos_manuales():
    """
    Lee data/manual.json (torneos de clubes que no se pueden automatizar) y
    los devuelve en el mismo formato que usan los scrapers automáticos.
    Si el archivo no existe, o tiene algún error de formato, no rompe el
    resto del proceso: simplemente avisa y sigue sin ellos.
    """
    if not MANUAL.exists():
        return [], "sin archivo data/manual.json (no pasa nada, es opcional)"

    try:
        with open(MANUAL, "r", encoding="utf-8") as f:
            contenido = json.load(f)
    except json.JSONDecodeError as e:
        return [], f"data/manual.json tiene un error de formato JSON: {e}"

    torneos = contenido.get("torneos", [])

    # Descartamos las filas de ejemplo que vienen de fábrica, para que no
    # aparezcan como si fueran un torneo real.
    torneos_validos = []
    for t in torneos:
        nombre = str(t.get("nombre", "")).strip()
        fecha = str(t.get("fecha", "")).strip()
        club = str(t.get("club", "")).strip()

        if nombre.upper().startswith("EJEMPLO"):
            continue
        if not (nombre and club and re.match(r"^\d{4}-\d{2}-\d{2}$", fecha)):
            # Entrada incompleta o con la fecha mal escrita (debe ser
            # AAAA-MM-DD, por ejemplo 2026-03-15). La ignoramos para no
            # romper el resto, pero avisamos por si acaso.
            print(f"[manual.json] AVISO: entrada ignorada por datos incompletos o fecha inválida: {t}")
            continue

        torneos_validos.append({
            "club": club,
            "nombre": nombre,
            "fecha": fecha,
            "url": t.get("url", ""),
        })

    return torneos_validos, f"{len(torneos_validos)} torneos manuales cargados"


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

    torneos_manuales, mensaje_manual = cargar_torneos_manuales()
    todos_los_torneos.extend(torneos_manuales)
    resumen.append(f"INFO - Torneos manuales: {mensaje_manual}")

    # Red de seguridad: si por lo que sea algún club aparece repetido (por
    # ejemplo, un fallo de paginación que devuelva el mismo torneo dos
    # veces), lo eliminamos aquí antes de guardar nada. Consideramos que es
    # el "mismo" torneo si coinciden club + nombre + fecha.
    vistos = set()
    torneos_sin_duplicados = []
    duplicados_eliminados = 0
    for t in todos_los_torneos:
        clave = (t.get("club"), t.get("nombre"), t.get("fecha"))
        if clave in vistos:
            duplicados_eliminados += 1
            continue
        vistos.add(clave)
        torneos_sin_duplicados.append(t)

    if duplicados_eliminados:
        resumen.append(f"INFO - Duplicados eliminados: {duplicados_eliminados}")

    todos_los_torneos = torneos_sin_duplicados

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
