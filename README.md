# Mis Torneos de Golf

Web personal que centraliza los torneos próximos de varios clubes de golf.

## Estado actual de cada club

| Club | Estado | Notas |
|---|---|---|
| Club de Golf Escorpión | ✅ Automático | Usa un feed de calendario estándar (.ics), el más fiable de todos |
| Foressos Club de Golf | ✅ Automático | Extracción por patrones de texto; si el club rediseña la web, tocará ajustarlo |
| Golf Parador El Saler | ✅ Automático | Con paginación |
| Oliva Nova Beach & Golf Resort | ✅ Automático | Tablas HTML normales |
| La Sella Golf Resort & Spa | ✋ Manual | Su web bloquea las peticiones automáticas (error 403), probablemente por IP de centro de datos |
| Club de Golf El Bosque | ⏳ Pendiente | Sus torneos se muestran con una app externa (GolfDirecto) que carga los datos con JavaScript; necesita otro enfoque |
| Panorámica Golf | ✋ Manual | Su web prohíbe expresamente el acceso automático (robots.txt) |
| Mediterráneo Golf | ✋ Manual | Igual que Panorámica |

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

- **El Bosque**: requiere automatizar un navegador (Selenium/Playwright) o
  bien contactar con el club para pedir sus datos directamente. Se puede
  añadir como fase 2.
- **Panorámica, Mediterráneo y La Sella**: como no se pueden automatizar
  por ahora (bloqueo por robots.txt o por IP), sus torneos se pueden añadir
  a mano. Una opción sencilla para una fase futura: crear un pequeño
  archivo `data/manual.json` con los torneos de estos 3 clubes escritos a
  mano, y hacer que `main.py` los añada al resultado final junto a los
  automáticos.
