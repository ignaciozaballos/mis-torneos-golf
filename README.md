# Mis Torneos de Golf

Web personal que centraliza los torneos próximos de varios clubes de golf.

## Estado actual de cada club

| Club | Estado | Notas |
|---|---|---|
| Club de Golf Escorpión | ✅ Automático | Usa un feed de calendario estándar (.ics), el más fiable de todos |
| Foressos Club de Golf | ✅ Automático | Extracción por patrones de texto; si el club rediseña la web, tocará ajustarlo |
| Golf Parador El Saler | ✅ Automático | Con paginación |
| Oliva Nova Beach & Golf Resort | ✅ Automático | Tablas HTML normales |
| Club de Golf El Bosque | ✅ Automático | Usa la API pública de GolfDirecto (encontrada con las DevTools del navegador) |
| Panorámica Golf | ✅ Automático | También usa la API pública de GolfDirecto, así que no depende de su web (que sí bloquea el acceso automático) |
| La Sella Golf Resort & Spa | ✋ Manual | Su web bloquea las peticiones automáticas (error 403), probablemente por IP de centro de datos |
| Mediterráneo Golf | ✋ Manual | Su web bloquea el acceso automático (robots.txt), y aunque también aparece en GolfDirecto, esa fuente está incompleta (le faltan torneos), así que no es fiable usarla |

El scraper se ejecuta automáticamente **una vez por semana** (los lunes),
ya que los torneos se anuncian con meses de antelación y no hace falta
revisar más a menudo. También puedes lanzarlo a mano cuando quieras desde
la pestaña "Actions" > "Actualizar torneos" > "Run workflow".

## Cómo publicarlo (paso a paso, sin experiencia previa)

### 1. Crear una cuenta de GitHub (si no tienes)
Ve a [github.com](https://github.com) y crea una cuenta gratuita.

### 2. Crear un repositorio nuevo
1. Pulsa el botón "+" arriba a la derecha → "New repository".
2. Ponle un nombre, por ejemplo `mis-torneos-golf`.
3. Marca que sea **público** (necesario para usar GitHub Pages gratis).
4. Pulsa "Create repository".

### 3. Subir estos archivos
La forma más fácil sin usar la terminal:
1. En la página de tu nuevo repositorio, pulsa "uploading an existing file".
2. Arrastra **todos** los archivos y carpetas de este proyecto manteniendo
   la misma estructura de carpetas (`scrapers/`, `docs/`, `.github/`, etc).
3. Pulsa "Commit changes".

### 4. Activar GitHub Pages (para ver la web)
1. En tu repositorio, ve a "Settings" → "Pages" (menú de la izquierda).
2. En "Source", elige la rama `main` y la carpeta `/docs`.
3. Guarda. En un par de minutos tu web estará en algo como:
   `https://tu-usuario.github.io/mis-torneos-golf/`

### 5. Ejecutar el scraper por primera vez (a mano)
1. Ve a la pestaña "Actions" de tu repositorio.
2. Verás el workflow "Actualizar torneos". Ábrelo.
3. Pulsa "Run workflow" → "Run workflow" (botón verde).
4. Espera 1-2 minutos y refresca la página. Debería aparecer una marca ✅
   (o ❌ si algo ha fallado — en ese caso, pincha para ver el error y me lo
   pasas).
5. Después de esto, se actualizará solo cada día automáticamente.

### 6. ¡Listo!
Visita la URL de tu web (paso 4) y deberías ver tus torneos.

## Si algo falla

Lo más probable es que algún scraper individual falle sin afectar a los
demás (el script está diseñado para seguir adelante aunque uno se rompa).
Ve a "Actions" → la última ejecución → "actualizar" para ver el log
completo, cópiame el mensaje de error de la línea que empiece por "FALLO"
y lo arreglamos.

## Próximos pasos pendientes de decidir juntos

Ya no quedan pasos pendientes de decidir — el proyecto está completo con
6 clubes automáticos y 2 gestionados a mano (ver siguiente sección).

## Añadir torneos a mano (La Sella y Mediterráneo)

Estos 2 clubes no se pueden leer automáticamente de forma fiable, así que
sus torneos se añaden a mano en el archivo `data/manual.json`.

### Cómo añadir un torneo

1. Ve a ese archivo en GitHub y pulsa el lápiz para editar.
2. Copia una de las líneas que hay dentro de `"torneos": [ ... ]` (un bloque
   entre `{` y `}`) y pégala justo debajo, separada por una coma. Por
   ejemplo, así quedaría con dos torneos de La Sella:

```json
{
  "torneos": [
    {
      "club": "La Sella Golf Resort & Spa",
      "nombre": "I Torneo Circuito Invierno 2026",
      "fecha": "2026-01-10",
      "url": "https://lasellagolf.com/competiciones"
    },
    {
      "club": "La Sella Golf Resort & Spa",
      "nombre": "Torneo Aniversario",
      "fecha": "2026-02-14",
      "url": "https://lasellagolf.com/competiciones"
    }
  ]
}
```

3. Rellena cada torneo con:
   - `club`: el nombre del club, tal cual (respeta mayúsculas/acentos).
   - `nombre`: el nombre del torneo.
   - `fecha`: la fecha en formato `AAAA-MM-DD` (año-mes-día), por ejemplo
     el 5 de marzo de 2026 se escribe `"2026-03-05"`.
   - `url`: un enlace donde se pueda ver más información (puedes dejar
     siempre el mismo, el de la página de torneos del club).
4. **Importante**: cada bloque `{ ... }` menos el último debe terminar con
   una coma `,`. El último bloque de la lista NO lleva coma después de su
   `}`.
5. Guarda con "Commit changes". Los cambios aparecerán en tu web:
   - En cuanto se ejecute el scraper (cada lunes, o si lo lanzas a mano
     desde "Actions" → "Run workflow").

### Si algo se rompe al editar este archivo

Es un formato llamado JSON y es muy sensible a comas y comillas. Si te
equivocas, no pasa nada grave: el scraper detecta el error, avisa en el
log de "Actions" con un mensaje que empieza por "INFO - Torneos manuales:"
y sigue funcionando con normalidad para el resto de clubes (solo se
quedarán sin actualizar los torneos manuales hasta que arregles el
archivo). Cópiame ese mensaje si no sabes qué está mal y lo revisamos.
