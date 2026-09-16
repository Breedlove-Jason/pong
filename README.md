# Pong · The Arcade

Jason Breedlove’s Python Pong, playable on desktop and in a browser. The original Turtle project is preserved in `legacy_turtle/app.py`.

## Play

You control the left paddle; the computer plays on the right. First to seven wins.

- **↑ / ↓** or **W / S**: move
- **Space**: start or pause
- **R**: reset
- **Browser touch**: drag on the court or hold the arrow buttons

The ball accelerates with each return; hitting near a paddle edge changes its angle. The computer has a limited movement speed. Browser play pauses when focus leaves the court or the tab becomes hidden.

## Python, in both places

`engine.py` owns movement, collisions, scoring, the opponent, and match state. `app.py` renders it using Turtle. The browser loads that same engine with Pyodide (Python/WebAssembly); JavaScript handles canvas drawing and input, with a fixed physics timestep.

### Desktop

```sh
python app.py
```

Python 3 and Tk/Turtle are required. No third-party Python packages are needed.

### Browser

```sh
npm run build
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. The first load downloads Pyodide from jsDelivr and requires internet access. Fonts fall back to system fonts if Google Fonts is unavailable.

### Tests

```sh
python3 -m unittest discover -s tests -v
```

### Vercel

Import this repository. Use **Other** as the framework preset, `npm run build` as the build command, and `dist` as output. `vercel.json` supplies those settings. No environment variables, database, or Python server are required. The intended custom domain is `pong.jasonbreedlove.dev`.
