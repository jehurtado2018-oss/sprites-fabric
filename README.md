# Fábrica de sprites

![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-green.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)

Herramienta de software libre que toma fotos reales de personas (estudiantes o profesores) y, sin edición manual, las convierte en personajes listos para un videojuego de peleas: quita el fondo, normaliza la altura a 250 px, genera el `spritesheet.png` y un `portrait.png` por persona, produce una versión **pixelart** con expresiones exageradas (alegría, miedo, susto, rabia, tristeza) y escribe un `config.json` estandarizado. Incluye una aplicación web local para tomar fotos, controlar el render a distancia (desde el celular), ver el avance y revisar los resultados.

## Integrantes

| Nombre | Rol / módulo |
|---|---|
| _Integrante 1_ | Pipeline de imagen (`background`, `normalize`, `packing`) |
| _Integrante 2_ | Pixelart y expresiones (`pixelart`, `expressions`) |
| _Integrante 3_ | API y base de datos (`web/server`, `web/db`, `web/worker`) |
| _Integrante 4_ | Interfaz web y documentación (`web/static`, `docs`) |

## Instalación y uso rápido

```bash
git clone <URL-del-repo> && cd fabrica-de-sprites
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python fabrica.py warmup      # UNA vez, con internet: descarga el modelo de recorte (rembg)
python run.py                 # abre http://localhost:8000
```

Con Docker: `docker-compose up` y abre http://localhost:8000.

Al arrancar, la app ya trae **5 personajes de semilla** (`assets/characters/`) para poder revisarla sin completar pasos.

### Usar el celular como cámara y control remoto
Conecta el celular a la **misma red WiFi** y abre la dirección que imprime `python run.py` (por ejemplo `http://192.168.1.20:8000`). En el celular, el botón de archivo abre la cámara directamente. (Los navegadores solo permiten `getUserMedia` en `localhost` o HTTPS, por eso en el celular se usa la cámara nativa.)

### Línea de comandos (Corte 1)
```bash
python fabrica.py build assets/photos_demo salida/ --no-pixel   # recorte + escala + spritesheet.png + portrait.png
python fabrica.py build assets/photos_demo salida/              # además pixelart + expresiones
python fabrica.py one foto.jpg salida/ --name "Ana Pérez"
```

## Qué genera por personaje (`assets/characters/<id>/`)

| Archivo | Contenido |
|---|---|
| `sprite.png` | Persona sin fondo, altura exacta de 250 px, pies como ancla |
| `portrait.png` | Retrato cuadrado centrado en el rostro (256×256) para la selección de luchador |
| `pixel_sprite.png` | Cuerpo en pixelart (paleta de 16 colores + contorno), también 250 px de alto |
| `pixel/<expresión>.png` y `expressions_sheet.png` | Retratos pixelart: neutral, alegría, miedo, susto, rabia, tristeza |
| `config.json` | Datos estandarizados (ver abajo) |

Además, en `assets/characters/` queda `spritesheet.png` + `spritesheet.json` con **todos** los personajes en una lámina ordenada.

```jsonc
{
  "schema_version": 1, "id": "ana_demo", "name": "Ana Demo", "standard_height": 250,
  "sprite":   { "file": "sprite.png", "size": [67, 250], "anchor": [0.5, 1.0] },
  "portrait": { "file": "portrait.png", "size": [256, 256] },
  "pixelart": {
    "block_size": 5, "palette_colors": 16,
    "sprite": { "file": "pixel_sprite.png", "size": [75, 250], "anchor": [0.5, 1.0] },
    "expressions": { "sheet": "expressions_sheet.png", "frame_size": [256, 256],
      "frames": { "neutral": 0, "alegria": 1, "miedo": 2, "susto": 3, "rabia": 4, "tristeza": 5 } }
  },
  "meta": { "background_backend": "rembg", "face_detected": true }
}
```

## Estructura

```
src/spritefactory/   núcleo: background, face, normalize, packing, pixelart, expressions, pipeline, cli
src/spritefactory/web/   API FastAPI, SQLite, worker de renders e interfaz (static/index.html)
assets/              fotos de prueba y personajes de semilla
docs/                informe técnico de arquitectura y guía de la demo
scripts/             generador de fotos sintéticas de prueba
tests/               pruebas automáticas
```

## Pruebas
```bash
pip install -r requirements-dev.txt && pytest
```

## Fotos reales
Reemplaza o agrega fotos en una carpeta y corre `python fabrica.py build <carpeta> assets/characters`. Pide consentimiento a las personas fotografiadas. Para mejores resultados: cuerpo completo, fondo liso y buena luz. Si tus fotos son de medio cuerpo y no se detecta el rostro, sube `SPRITE_FACE_RATIO` (por ejemplo `SPRITE_FACE_RATIO=0.30`).

## Licencias de las dependencias
Pillow (HPND), NumPy (BSD), OpenCV (Apache-2.0), rembg (MIT) con el modelo U²-Net (Apache-2.0), FastAPI (MIT), Uvicorn (BSD). El proyecto se distribuye bajo licencia MIT (ver `LICENSE`).
