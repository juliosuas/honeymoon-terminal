# Live Private Cut

This folder contains a standalone browser version of `honeymoon` for private
screening.

Open:

```bash
xdg-open live/honeymoon-live.html
```

Or serve it locally:

```bash
python3 -m http.server 8080
```

Then visit:

```text
http://127.0.0.1:8080/live/honeymoon-live.html
```

Notes:

- The browser requires a click before audio can start.
- The file is self-contained: no external assets, no network, no dependencies.
- It is intended for private repo viewing, screen sharing, and early live demos.
- Keep the repo private until the festival strategy is decided.
