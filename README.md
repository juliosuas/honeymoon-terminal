<p align="center">
  <img
    width="100%"
    src="https://capsule-render.vercel.app/api?type=blur&height=230&color=0:06070b,45:bd93f9,70:ff79c6,100:8be9fd&text=honeymoon&fontColor=f8f3ff&fontAlign=50&fontAlignY=45&desc=una%20carta%20de%20amor%20hecha%20con%20codigo&descAlign=50&descAlignY=66&animation=twinkling"
    alt="honeymoon"
  />
</p>

<p align="center">
  <a href="#ver-la-pieza"><img alt="Open in browser" src="https://img.shields.io/badge/open-index.html-ff79c6?style=for-the-badge&logo=html5&logoColor=white"></a>
  <a href="#en-terminal"><img alt="Run in terminal" src="https://img.shields.io/badge/run-python3-8be9fd?style=for-the-badge&logo=python&logoColor=111111"></a>
  <a href="#stack"><img alt="No dependencies" src="https://img.shields.io/badge/deps-zero-50fa7b?style=for-the-badge&logo=dependabot&logoColor=111111"></a>
  <a href="#privacidad"><img alt="Privacy first" src="https://img.shields.io/badge/privacy-initials_only-bd93f9?style=for-the-badge&logo=github&logoColor=white"></a>
</p>

<p align="center">
  <img alt="HTML5" src="https://img.shields.io/badge/HTML5-06070b?style=flat-square&logo=html5&logoColor=ff79c6">
  <img alt="CSS3" src="https://img.shields.io/badge/CSS3-06070b?style=flat-square&logo=css3&logoColor=8be9fd">
  <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-06070b?style=flat-square&logo=javascript&logoColor=f1fa8c">
  <img alt="Python" src="https://img.shields.io/badge/Python-06070b?style=flat-square&logo=python&logoColor=50fa7b">
  <img alt="SVG" src="https://img.shields.io/badge/SVG-06070b?style=flat-square&logo=svg&logoColor=bd93f9">
  <img alt="Web Audio API" src="https://img.shields.io/badge/Web_Audio_API-06070b?style=flat-square&logo=webauthn&logoColor=ff79c6">
</p>

<p align="center">
  <img
    src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&duration=3600&pause=900&color=FF79C6&center=true&vCenter=true&width=760&lines=ASCII%2C+ANSI%2C+Web+Audio+y+memoria;una+terminal+tambien+puede+recordar;AI+como+puente%2C+no+como+protagonista"
    alt="honeymoon typing intro"
  />
</p>

<p align="center">
  <a href="live/honeymoon-github.svg">
    <img
      src="live/honeymoon-github.svg"
      alt="honeymoon GitHub public preview"
      width="100%"
    />
  </a>
</p>

> Una carta de amor contada como si una terminal tambien pudiera recordar.

`honeymoon` es una historia de amor hecha con codigo: ASCII, color ANSI,
animacion de terminal, musica 8-bit original y una pequena verdad humana sobre
J., C. y un agente de IA que sirvio como puente.

No es una demo tecnica. Es una memoria.

Dos personas se encontraron en una ciudad enorme. Un mensaje asistido por IA
abrio una puerta. Hubo una primera cita, un concierto, nervios, besos, una
habitacion llena de codigo, sistemas vivos, ternura rara, senales cruzadas,
CDMX vacia y una promesa final:

> I'll see you in another life when we are both cats.

## La historia

Ella penso que hablaba con un humano.

Era su agente.

Pero el amor era de J.

Esa es la chispa de `honeymoon`: una escena contemporanea donde la tecnologia no
reemplaza el afecto, sino que lo traduce. El agente de IA no es el protagonista
ni el amante. Es el puente. Lo que importa es lo que habia del otro lado: dos
personas intentando entenderse.

La pieza sigue ese arco con lenguaje de terminal:

- J. y C. aparecen como dos caritas raras en una ciudad demasiado grande.
- Un agente ayuda a convertir cuidado en palabras.
- La primera cita se vuelve luces, musica, besitos y nervios.
- C. descubre el mundo de J.: codigo, bots, pantallas, caos bonito.
- El codigo deja de ser herramienta y se vuelve cortejo.
- Una llamada dificil cruza las senales.
- CDMX sigue encendida, pero algo queda en pausa.
- Al final, dos gatos se encuentran en otra vida.

## Ver la pieza

### En navegador

Abre:

```text
index.html
```

Es autocontenido: no necesita build, dependencias ni red. Al abrirlo, la pieza
arranca como una terminal fullscreen. El audio intenta activarse al inicio; si
el navegador lo bloquea, toca/clickea la terminal o el boton de musica.

Tambien puede publicarse como sitio estatico en GitHub Pages, Vercel, Netlify o
cualquier hosting que sirva HTML. Como `index.html` vive en la raiz, la URL abre
directo en la obra.

### En terminal

```bash
python3 honeymoon.py --no-audio
```

O, si tu sistema tiene un reproductor compatible para audio generado localmente:

```bash
python3 honeymoon.py
```

Opciones utiles:

```bash
python3 honeymoon.py --song waltz
python3 honeymoon.py --song both
python3 honeymoon.py --speed 0.9
python3 honeymoon.py --audio-file "/ruta/a/honeymoon-8bit.mp3"
```

## Stack

| Capa | Lenguajes / librerias | Uso en la pieza |
| --- | --- | --- |
| Web cut | HTML5, CSS3, JavaScript vanilla | Terminal fullscreen, escenas ASCII, controles, progreso y audio en navegador. |
| Audio web | Web Audio API | Sintesis chiptune en vivo sin archivos externos. |
| Terminal cut | Python 3, ANSI escape codes | Animacion en consola, color, timing, musica local y CLI. |
| Python stdlib | `argparse`, `dataclasses`, `math`, `random`, `wave`, `tempfile`, `subprocess`, `shutil` | Configuracion, render terminal, generacion WAV y reproduccion opcional. |
| Preview GitHub | SVG, CSS animations | Corte silencioso que GitHub puede renderizar dentro del README. |
| Distribucion | GitHub Pages, Vercel, Netlify, static hosting | Publicacion directa como sitio estatico. |

## Features

- `index.html` listo para abrir en navegador, sin instalar paquetes.
- `honeymoon.py` ejecutable en terminal con modo sin audio.
- Musica 8-bit original generada localmente, no una melodia comercial copiada.
- Version SVG animada para que GitHub muestre la obra desde el README.
- Paleta terminal romantica: rose, cyan, gold, mint, violet y sombras.
- Escenas con J., C., agente IA, concierto, cuarto nerd, CDMX y final de gatos.
- Narrativa publica con iniciales para cuidar la intimidad.

## Estructura

```text
.
|-- index.html                  # experiencia web principal
|-- honeymoon.py                # version viva para terminal
|-- live/
|   |-- honeymoon-github.svg    # preview animado para README
|   |-- honeymoon-live.html     # corte alternativo de navegador
|   `-- README.md
|-- NARRATIVE_NOTES.md          # direccion emocional
|-- PRODUCTION_PLAN.md          # ruta de produccion
`-- FESTIVAL_STRATEGY.md        # estrategia de festival y publicacion
```

## Por que una terminal

Porque para J. el codigo no era una pose. Era lenguaje emocional.

La terminal aqui no intenta verse futurista por moda. Es el lugar donde una
persona que construye aprende a decir: esto me importo, esto paso, esto dolio,
esto todavia brilla.

`honeymoon` usa texto, coordenadas, color, ritmo y pequenas criaturas ASCII para
contar algo que normalmente se contaria con camaras. Es una pelicula hecha desde
el lugar donde tambien nacen los programas.

## IA y autoria

Esta obra habla de IA sin convertirla en el alma de la obra.

La IA aparece como mediadora: una herramienta que ayudo a escribir, ordenar,
traducir o acercar. Pero el centro emocional es humano. La historia, la
estructura, la memoria, el pudor, el dolor y el deseo de contarla pertenecen a
la persona que la vivio.

El punto no es "un agente enamoro a alguien".

El punto es mas raro y mas humano:

> alguien uso las herramientas de su tiempo para intentar amar mejor.

## Privacidad

La version publica usa iniciales: `J.` y `C.`

No hay nombres completos, capturas de conversaciones privadas ni datos que
busquen exponer a nadie. La historia se comparte porque el sentimiento merece
existir en el mundo, pero la intimidad de las personas sigue importando.

## Roadmap

- Modo recordable con timing determinista.
- Aspect ratios `16:9` y `9:16` para festival y social cut.
- Export workflow documentado para captura limpia.
- Subtitulos en ingles y espanol.
- Stills, poster, logline y statement de direccion.

## Estado

`honeymoon` ya puede leerse, abrirse y sentirse. La version actual es una pieza
publica pequena, tierna y completa, pero tambien es una semilla para cortes mas
grandes: festival, video social, instalacion o performance de codigo en vivo.

Si llegaste aqui sin conocer a J. ni a C., esa es la idea.

No necesitas conocerlos.

Solo necesitas entender que, por un momento, el codigo fue una forma de decir
"te quiero".

<p align="center">
  <img
    width="100%"
    src="https://capsule-render.vercel.app/api?type=waving&height=110&color=0:8be9fd,45:bd93f9,100:ff79c6&section=footer"
    alt="honeymoon footer"
  />
</p>
