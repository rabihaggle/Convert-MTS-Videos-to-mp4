# Convert MTS Videos to mp4

Convierte archivos MTS/M2TS a mp4 de forma simple y rapida.

## How to use

```bash
python3.11 ./decode_video.py <path> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir` | Directorio de salida | `./converted` |
| `--workers` | Workers paralelos | `2` |
| `--keep-original` | Conservar archivo original | `false` |
| `--crf` | Calidad de video (0-51, menor es mejor) | `23` |
| `--preset` | Preset de encoding | `medium` |
| `--formats` | Formatos de entrada | `.mts .MTS .m2ts .M2TS` |

### Presets disponibles

`ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `veryslow`

## Ejemplos

```bash
#Basic
python3.11 ./decode_video.py ./videos

#Alta calidad
python3.11 ./decode_video.py ./videos --crf 18 --preset slow

#4 workers sin borrar originales
python3.11 ./decode_video.py ./videos --workers 4 --keep-original
```

## Requisitos

- ffmpeg

### Ubuntu
```bash
apt update ffmpeg
```

### MacOS
```bash
brew install ffmpeg
```

## Output specs

| Format | Details |
|--------|---------|
| Video | H.264 (libx264) |
| Audio | AAC 128k |

## Logs

El log se guarda en `conversion.log` (consola + archivo)