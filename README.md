# honeymoon

`honeymoon` es una carta de amor moderna contada en la terminal: ASCII, emojis,
musica 8-bit generada localmente y una historia sobre J., C. y un agente de IA
que sirvio como puente.

La pieza no busca demostrar tecnologia por si sola. Busca guardar una memoria:
dos personas que se encontraron, codigo que se volvio lenguaje emocional, una
ciudad vacia, y la promesa final de otra vida.

## Ejecutar

```bash
./honeymoon.py
```

Opciones utiles:

```bash
./honeymoon.py --no-audio
./honeymoon.py --speed 0.75
./honeymoon.py --audio-file "/ruta/a/audio-8bit-legal.mp3"
```

## Live private cut

Para mostrar la pieza desde el repo privado sin instalar dependencias, abre:

```bash
xdg-open live/honeymoon-live.html
```

Tambien puedes servir el repo localmente:

```bash
python3 -m http.server 8080
```

Y abrir:

```text
http://127.0.0.1:8080/live/honeymoon-live.html
```

El navegador pide un click para iniciar el audio. El archivo es autocontenido:
no usa assets externos ni red.

## Estado actual

- Animacion terminal con narrativa completa.
- Musica original estilo chiptune/8-bit generada en Python.
- Iniciales `J.` y `C.` para cuidar privacidad.
- Caritas ASCII que cambian de emocion segun la escena.
- Cierre con CDMX vacia y dos gatos enamorandose.
- Version live privada en navegador para demo/screen share.

## Intencion

La obra debe sentirse como una carta de amor hecha con codigo, no como una demo
tecnica. Cada efecto visual debe ayudar a que el espectador sienta ternura,
nostalgia, curiosidad o silencio.

## Privacidad

Mantener los nombres reales fuera de la pieza publica. Si algun dia se publica
como video, cuidar que no haya datos privados, lugares especificos reconocibles
o mensajes reales que puedan exponer a C.
