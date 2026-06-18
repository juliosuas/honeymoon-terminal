# Festival Strategy

Research date: 2026-06-18

Goal: turn `honeymoon` from a terminal animation into a festival-ready short
film / digital-art piece while keeping the emotional core intact.

## Positioning

`honeymoon` should not be submitted as "AI slop" or a generic AI experiment.
The strongest angle is:

> A private love story told through the language of code, AI mediation, terminal
> animation, 8-bit music, CDMX loneliness, and anonymous initials.

Primary categories:

- experimental short
- animated short
- digital/new media short
- AI-assisted film
- music video / audiovisual poem
- vertical micro-short for social platforms

## Versions to produce

### V1 - Festival Short

- Runtime: 3 to 6 minutes.
- Format: 16:9, 1080p or 4K.
- Keep terminal/ASCII as the main visual language.
- Add restrained editing: fades, cuts, zooms, subtitles.
- Sound: original 8-bit/piano hybrid, no commercial melodies.
- Privacy: only `J.` and `C.`, no identifying details.

### V2 - Social Cut

- Runtime: 60 to 90 seconds.
- Format: 9:16.
- Strong first line:
  `Ella penso que hablaba con un humano. Era mi agente. Pero el amor era mio.`
- Fewer chapters, more emotional compression.
- End with CDMX empty and the two cats.

### V3 - Installation / Live Code Version

- Runtime: variable.
- Runs live in terminal.
- Could be shown in AI/new-media contexts as a code performance.
- Add a `--record-mode` flag later for stable capture timing.

## Priority Targets

### Sundance Film Festival 2027

Why it fits:

- Sundance accepts U.S. and International Short Films under 50 minutes.
- The short-film category includes fiction, nonfiction, experimental video,
  animation, music video, and other short-form film/video.
- Good target for a polished experimental version.

Current deadlines for short films:

- Early: 2026-07-13
- Official: 2026-08-03
- Late: 2026-08-31

Source:

- https://www.sundance.org/festivals/sundance-film-festival/submit/

Action:

- Aim for rough festival export by 2026-07-10.
- Submit only if the piece is emotionally coherent, not just visually novel.

### Annecy International Animation Film Festival 2027

Why it fits:

- Strong target if the ASCII/terminal language is framed as animation.
- The official page says 2026 submissions are closed, and the festival received
  over 4,000 films between November and April for the 2026 edition.

Source:

- https://www.annecyfestival.com/en/take-part/submit-film

Action:

- Monitor for 2027 submissions around late 2026.
- Prepare an animation-forward export with strong visual rhythm.

### Tribeca Festival 2027

Why it fits:

- Tribeca accepts short films under 40 minutes, including animation,
  experimental films, and music videos.
- Tribeca NOW is also relevant because it highlights digital storytellers and
  creators across TikTok, Instagram, YouTube, and other platforms.

2026 reference:

- 2026 short-film extended deadline was 2026-02-13.
- 2026 submissions opened 2025-09-25.

Source:

- https://tribecafilm.com/festival/submissions

Action:

- Monitor in September 2026 for 2027 submissions.
- Consider both Short Film and Tribeca NOW depending on final format.

### Cannes / Cannes-Adjacent Route

Why it fits:

- Cannes Official Short Film Competition is extremely selective, but the piece
  could fit if it becomes a truly cinematic short, not just a novelty.
- For 2026, Cannes selected 10 short films from 3,184 productions.
- The AI/cinema conversation around Cannes is active, especially with WAIFF
  running alongside Cannes.

Sources:

- https://www.festival-cannes.com/en/
- https://www.theguardian.com/technology/2026/apr/26/cannes-ai-film-festival-raises-eyebrows-questions-future

Action:

- Treat official Cannes as a moonshot.
- More realistic Cannes-adjacent target: AI/new-media showcases, WAIFF-style
  programs, market screenings, or curated digital-art events.

### Clermont-Ferrand International Short Film Festival

Why it fits:

- One of the strongest short-film targets in the world.
- The festival has international and Lab competitions, which may suit an
  experimental terminal-film version.
- Reported submission window is generally March to October.

Source:

- https://www.clermont-filmfest.org/

Action:

- Monitor 2027 rules and deadlines.
- Submit the 3-6 minute festival cut if public-premiere rules allow.

### Palm Springs International ShortFest

Why it fits:

- Major U.S. short-film festival and market.
- Academy Award qualifying awards include animated short and live-action short.
- Good target after the piece has a clean festival export.

Source:

- https://www.psfilmfest.org/

Action:

- Monitor fall 2026 / winter 2027 call for entries.

### Runway AI Film Festival / Gen:48

Why it fits:

- Highly relevant to AI-assisted filmmaking.
- Good place if we build a version that combines terminal capture with
  AI-generated visual inserts or motion design.
- Runway AIFF has grown rapidly and is a visible AI-film showcase.

Source:

- https://runwayml.com/

Action:

- Monitor 2027 AIFF and Gen:48 calls.
- Keep the human authorship/emotional story central; do not let tools dominate.

## Production Checklist

### Story

- Write a 1-page treatment.
- Cut chapters down to a clean arc:
  1. agent opens the door
  2. concert
  3. room/world of code
  4. code impresses C.
  5. call/silence
  6. CDMX empty
  7. cats
- Remove any line that explains what the image already says.

### Visual

- Add a recording mode with deterministic timing.
- Add stable terminal dimensions for capture.
- Capture 16:9 and 9:16 versions separately.
- Add title cards and transitions.
- Keep ASCII readable on mobile.

### Audio

- Build a fully original theme.
- Keep the 8-bit version, but add a slower piano-like counterline if it helps.
- Avoid commercial melodies.
- Mix to avoid harsh terminal beep energy.

### Legal / Privacy

- No real full names.
- No private screenshots/messages.
- No copyrighted song covers unless properly licensed.
- Make an AI-use statement:
  `AI tools were used as creative instruments; the story, structure, code,
  editing decisions, and emotional authorship are human-led.`

### Submission Materials

- Logline, 35 words:
  `A coder falls in love through an AI-assisted first message, then turns the
  memory into a terminal animation where code, CDMX, and two cats hold what
  words could not.`
- Director statement.
- 3 stills.
- Poster.
- Private screener link.
- Credits.
- AI-use disclosure.
- Privacy note.

## Next Engineering Tasks

1. Add `--record-mode`.
2. Add `--aspect 16:9|9:16`.
3. Add chapter timing config.
4. Add export helper using `asciinema`, `ffmpeg`, or Playwright terminal capture.
5. Add a `festival_cut.py` or config file that trims the live version to 3-6 min.

## Decision Rule

Do not submit because it uses AI.

Submit only when the finished film makes a stranger feel:

- "I understand why this mattered."
- "This could only have been made by this person."
- "The AI is not the soul. The soul is the love."
