#!/usr/bin/env python3
"""
Animacion terminal de una historia de amor con ASCII, ANSI, emojis y musica
sintetizada localmente.

Uso:
  python3 amor_terminal.py
  python3 amor_terminal.py --no-audio
  python3 amor_terminal.py --song waltz
  python3 amor_terminal.py --audio-file "/ruta/a/honeymoon-8bit.mp3"
  python3 amor_terminal.py --speed 0.9
"""

from __future__ import annotations

import argparse
import atexit
import math
import os
import random
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import time
import wave
from dataclasses import dataclass
from typing import Iterable


ESC = "\033["
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"


PALETTE = {
    "rose": "\033[38;5;205m",
    "pink": "\033[38;5;218m",
    "red": "\033[38;5;196m",
    "gold": "\033[38;5;220m",
    "mint": "\033[38;5;121m",
    "cyan": "\033[38;5;117m",
    "blue": "\033[38;5;75m",
    "violet": "\033[38;5;141m",
    "lavender": "\033[38;5;183m",
    "white": "\033[38;5;255m",
    "gray": "\033[38;5;245m",
    "soft": "\033[38;5;253m",
    "shadow": "\033[38;5;238m",
    "green": "\033[38;5;84m",
}


HEART_FRAMES = ["♡", "♥", "💗", "💖", "💘", "💖", "💗", "♥"]
SPARKLES = ["·", "˙", "*", "✦", "✧", "❀", "✶", "♡"]
EMOJI_SPARKLES = ["✨", "💕", "🌙", "🌸", "💻", "🤍", "💫"]


@dataclass
class Terminal:
    width: int
    height: int


def term_size() -> Terminal:
    size = shutil.get_terminal_size((100, 34))
    return Terminal(max(size.columns, 72), max(size.lines, 24))


def write(text: str) -> None:
    sys.stdout.write(text)


def flush() -> None:
    sys.stdout.flush()


def clear() -> None:
    write(f"{ESC}2J{ESC}H")


def move(y: int, x: int) -> str:
    return f"{ESC}{max(1, y)};{max(1, x)}H"


def color(name: str, text: str) -> str:
    return f"{PALETTE[name]}{text}{RESET}"


def strip_ansi_len(text: str) -> int:
    length = 0
    i = 0
    while i < len(text):
        if text[i] == "\033":
            while i < len(text) and text[i] != "m":
                i += 1
            i += 1
        else:
            length += 1
            i += 1
    return length


def visible_len(text: str) -> int:
    # Emojis are treated as width 2 by many terminals. This approximation keeps
    # centering stable enough without external wcwidth dependencies.
    width = 0
    clean = []
    i = 0
    while i < len(text):
        if text[i] == "\033":
            while i < len(text) and text[i] != "m":
                i += 1
            i += 1
        else:
            clean.append(text[i])
            i += 1
    for ch in clean:
        width += 2 if ord(ch) > 0x2E80 else 1
    return width


def print_at(y: int, x: int, text: str) -> None:
    if y < 1:
        return
    write(move(y, x) + text + RESET)


def center(y: int, text: str, width: int | None = None) -> None:
    if width is None:
        width = term_size().width
    x = max(1, (width - visible_len(text)) // 2)
    print_at(y, x, text)


def box(y: int, x: int, w: int, h: int, title: str = "", hue: str = "soft") -> None:
    w = max(8, w)
    h = max(4, h)
    c = PALETTE[hue]
    print_at(y, x, c + "╭" + "─" * (w - 2) + "╮")
    for row in range(1, h - 1):
        print_at(y + row, x, c + "│" + RESET + " " * (w - 2) + c + "│")
    print_at(y + h - 1, x, c + "╰" + "─" * (w - 2) + "╯")
    if title:
        title_text = f" {title} "
        print_at(y, x + 2, c + title_text[: max(0, w - 4)])


def wrapped_lines(text: str, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        proposed = word if not current else f"{current} {word}"
        if visible_len(proposed) <= max_width:
            current = proposed
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def typewrite(
    y: int,
    text: str,
    *,
    hue: str = "soft",
    delay: float = 0.018,
    width: int | None = None,
    center_text: bool = True,
) -> None:
    t = term_size()
    max_width = min(width or t.width - 8, t.width - 8)
    lines = wrapped_lines(text, max_width)
    for idx, line in enumerate(lines):
        prefix = PALETTE[hue]
        if center_text:
            x = max(1, (t.width - visible_len(line)) // 2)
        else:
            x = 4
        print_at(y + idx, x, prefix)
        for ch in line:
            write(ch)
            flush()
            time.sleep(delay)
        write(RESET)
    flush()


def sleep_scaled(seconds: float, speed: float) -> None:
    time.sleep(max(0.01, seconds / speed))


def note_to_freq(note: str) -> float:
    if note == "R":
        return 0.0
    names = {
        "C": -9,
        "C#": -8,
        "Db": -8,
        "D": -7,
        "D#": -6,
        "Eb": -6,
        "E": -5,
        "F": -4,
        "F#": -3,
        "Gb": -3,
        "G": -2,
        "G#": -1,
        "Ab": -1,
        "A": 0,
        "A#": 1,
        "Bb": 1,
        "B": 2,
    }
    if len(note) == 2:
        name, octave_text = note[0], note[1]
    else:
        name, octave_text = note[:-1], note[-1]
    semitone = names[name] + (int(octave_text) - 4) * 12
    return 440.0 * (2 ** (semitone / 12))


def square(freq: float, t: float, duty: float = 0.5) -> float:
    if freq <= 0:
        return 0.0
    return 1.0 if (t * freq) % 1.0 < duty else -1.0


def soft_key(freq: float, t: float) -> float:
    if freq <= 0:
        return 0.0
    fundamental = math.sin(2 * math.pi * freq * t)
    warm_harmonic = math.sin(2 * math.pi * freq * 2 * t) * 0.32
    glass_harmonic = math.sin(2 * math.pi * freq * 3 * t) * 0.12
    return fundamental + warm_harmonic + glass_harmonic


def semitone(freq: float, steps: int) -> float:
    if freq <= 0:
        return 0.0
    return freq * (2 ** (steps / 12))


def synth_wave(path: str, song: str, sample_rate: int = 22050) -> None:
    random.seed(42)
    if song == "waltz":
        bpm = 112
        melody = [
            ("E5", 1), ("G5", 1), ("C6", 1), ("B5", 1), ("A5", 1), ("G5", 1),
            ("E5", 1), ("G5", 1), ("C6", 1), ("D6", 1), ("C6", 1), ("B5", 1),
            ("A5", 1), ("C6", 1), ("F6", 1), ("E6", 1), ("D6", 1), ("C6", 1),
            ("G5", 1), ("B5", 1), ("E6", 1), ("D6", 1), ("C6", 1), ("B5", 1),
        ]
        bass = [("C3", 1), ("G3", 1), ("E4", 1), ("G2", 1), ("D3", 1), ("B3", 1)]
        arp_steps = [0, 7, 12, 7]
        volume = 0.17
    else:
        # Original "honeymoon" 8-bit mood. Same cute chiptune character as the
        # earlier version, slowed down to fit the more romantic pacing.
        # It is intentionally not a cover of any commercial song.
        bpm = 78
        melody = [
            ("A4", 1), ("C5", 1), ("E5", 2), ("D5", 1), ("C5", 1), ("A4", 2),
            ("G4", 1), ("A4", 1), ("C5", 2), ("E5", 2), ("R", 1), ("E5", 1),
            ("F5", 2), ("E5", 1), ("D5", 1), ("C5", 2), ("A4", 2),
            ("C5", 1), ("D5", 1), ("E5", 2), ("G5", 2), ("E5", 2),
        ]
        bass = [("A2", 2), ("E3", 2), ("F2", 2), ("C3", 2), ("D3", 2), ("E3", 2)]
        arp_steps = [0, 4, 7, 12]
        volume = 0.19

    beat = 60.0 / bpm
    frames: list[int] = []
    bass_index = 0
    melody_index = 0
    total_beats = 192 if song == "waltz" else 160
    beat_cursor = 0.0

    while beat_cursor < total_beats:
        note, dur = melody[melody_index % len(melody)]
        bass_note, bass_dur = bass[bass_index % len(bass)]
        melody_index += 1
        if melody_index % 3 == 0:
            bass_index += 1
        dur_seconds = dur * beat
        samples = int(sample_rate * dur_seconds)
        f1 = note_to_freq(note)
        f2 = note_to_freq(bass_note)
        tick = max(1, int(sample_rate * beat / (3 if song == "waltz" else 4)))
        for i in range(samples):
            t = i / sample_rate
            envelope = min(1.0, i / (sample_rate * 0.006)) * min(1.0, (samples - i) / (sample_rate * 0.04))
            arp_freq = semitone(f1, arp_steps[(i // tick) % len(arp_steps)])
            if song == "waltz":
                lead = square(arp_freq, t, 0.36)
                harmony = square(semitone(f1, -12), t, 0.25) * 0.18 if f1 else 0.0
                bass_wave = square(f2, t, 0.50) * 0.34
                noise_decay = max(0.0, 1.0 - i / max(1, int(sample_rate * 0.035)))
                noise = (random.random() * 2.0 - 1.0) * noise_decay * 0.05
                sample = (lead * 0.68 + harmony + bass_wave + noise) * envelope * volume
                sample = round(sample * 12) / 12
            else:
                lead = square(arp_freq, t, 0.34)
                harmony = square(semitone(f1, -12), t, 0.25) * 0.22 if f1 else 0.0
                bass_wave = square(f2, t, 0.50) * 0.42
                noise_decay = max(0.0, 1.0 - i / max(1, int(sample_rate * 0.035)))
                noise = (random.random() * 2.0 - 1.0) * noise_decay * 0.08
                sample = (lead * 0.78 + harmony + bass_wave + noise) * envelope * volume
                sample = round(sample * 10) / 10
            frames.append(int(max(-1.0, min(1.0, sample)) * 32767))
        beat_cursor += dur

    with wave.open(path, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"".join(struct.pack("<h", sample) for sample in frames))


def find_player(prefer_ffplay: bool = False) -> list[str] | None:
    candidates = ("ffplay", "paplay", "aplay") if prefer_ffplay else ("aplay", "paplay", "ffplay")
    for candidate in candidates:
        found = shutil.which(candidate)
        if not found:
            continue
        if candidate == "ffplay":
            return [found, "-nodisp", "-autoexit", "-loglevel", "quiet"]
        return [found]
    return None


class Audio:
    def __init__(self, enabled: bool, song: str, audio_file: str | None = None) -> None:
        self.enabled = enabled
        self.song = song
        self.audio_file = audio_file
        self.tmpdir: str | None = None
        self.processes: list[subprocess.Popen] = []

    def start(self) -> None:
        if not self.enabled:
            return
        if self.audio_file:
            player = find_player(prefer_ffplay=True)
            if not player:
                return
            if not os.path.exists(self.audio_file):
                print_at(1, 1, PALETTE["red"] + f"No encontre el audio: {self.audio_file}")
                flush()
                time.sleep(2)
                return
            try:
                self.processes.append(
                    subprocess.Popen(player + [self.audio_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                )
            except OSError:
                pass
            return

        player = find_player()
        if not player:
            return
        self.tmpdir = tempfile.mkdtemp(prefix="amor-terminal-")
        songs = ["honeymoon", "waltz"] if self.song == "both" else [self.song]
        for idx, song in enumerate(songs):
            path = os.path.join(self.tmpdir, f"{song}.wav")
            synth_wave(path, song)
            cmd = player + [path]
            try:
                if idx == 0:
                    self.processes.append(subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                else:
                    # Start the second piece later so the slower show changes
                    # from intimate glow to flower-waltz movement.
                    self.processes.append(
                        subprocess.Popen(
                            [sys.executable, "-c", "import subprocess,time,sys; time.sleep(54); subprocess.run(sys.argv[1:])", *cmd],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                    )
            except OSError:
                pass

    def stop(self) -> None:
        for proc in self.processes:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=0.4)
                except subprocess.TimeoutExpired:
                    proc.kill()
        if self.tmpdir:
            try:
                for name in os.listdir(self.tmpdir):
                    os.unlink(os.path.join(self.tmpdir, name))
                os.rmdir(self.tmpdir)
            except OSError:
                pass


class Show:
    def __init__(self, speed: float) -> None:
        self.speed = speed
        self.frame = 0
        self.t = term_size()
        self.stars = self.make_stars(88)

    def refresh_size(self) -> None:
        self.t = term_size()

    def make_stars(self, amount: int) -> list[tuple[float, float, float, str]]:
        random.seed(7)
        return [
            (
                random.random(),
                random.random(),
                random.uniform(0.2, 1.0),
                random.choice(SPARKLES),
            )
            for _ in range(amount)
        ]

    def cute_face_lines(self, who: str, mood: str, frame: int) -> list[str]:
        faces = {
            "J.": {
                "happy": [["  .-^-.", " ( •‿•)", " /づ💻づ"], ["  .-^-.", " ( ^‿^)", " /づ✨づ"]],
                "love": [["  .-^-.", " (♡‿♡)", " /づ♡づ"], ["  .-^-.", " (♥‿♥)", " /づ💕づ"]],
                "wow": [["  .-^-.", " ( •̀ᴗ•́)", " /づ⚡づ"], ["  .-^-.", " (⌐■_■)", " /づ💻づ"]],
                "cook": [["  .-^-.", " ( ^‿^)", " /づ🍜づ"], ["  .-^-.", " ( •‿•)", " /づ🍞づ"]],
                "sleep": [["  .-^-.", " ( -.-)", " /づ♡づ"], ["  .-^-.", " ( u.u)", " /づ☾づ"]],
                "sad": [["  .-^-.", " (._. )", " /づ  づ"], ["  .-^-.", " (;_;) ", " /づ♡づ"]],
                "call": [["  .-^-.", " ( •_•)", " /づ☎づ"], ["  .-^-.", " (._. )", " /づ☎づ"]],
            },
            "C.": {
                "happy": [["  .-^-.", " (◕‿◕✿)", " /づ🌙づ"], ["  .-^-.", " (づ^‿^)づ", "   ✨♡"]],
                "love": [["  .-^-.", " (♡‿♡✿)", " /づ♡づ"], ["  .-^-.", " (♥‿♥✿)", " /づ💕づ"]],
                "wow": [["  .-^-.", " (✿ ♥‿♥)", " /づ💻づ"], ["  .-^-.", " (◕o◕✿)", " /づ✨づ"]],
                "cook": [["  .-^-.", " (◕‿◕✿)", " /づ♡づ"], ["  .-^-.", " (✿^‿^)", " /づ🍓づ"]],
                "sleep": [["  .-^-.", " ( u.u✿)", " /づ☾づ"], ["  .-^-.", " ( -.-✿)", " /づ♡づ"]],
                "sad": [["  .-^-.", " (._.✿)", " /づ  づ"], ["  .-^-.", " (;_;✿)", " /づ♡づ"]],
                "call": [["  .-^-.", " ( •_•✿)", " /づ☎づ"], ["  .-^-.", " (._.✿)", " /づ☎づ"]],
            },
        }
        options = faces.get(who, faces["J."]).get(mood, faces.get(who, faces["J."])["happy"])
        return options[(frame // 10) % len(options)]

    def draw_face(self, y: int, x: int, who: str, mood: str, hue: str, frame: int, label: bool = True) -> None:
        if label:
            print_at(y - 1, x + 3, PALETTE[hue] + who)
        for idx, line in enumerate(self.cute_face_lines(who, mood, frame)):
            print_at(y + idx, x, PALETTE[hue] + line)

    def background(self, mood: str = "night") -> None:
        self.refresh_size()
        clear()
        hue_cycle = ["shadow", "gray", "lavender", "cyan", "rose"]
        for sx, sy, depth, char in self.stars:
            x = int(2 + sx * (self.t.width - 4))
            y = int(2 + sy * (self.t.height - 4))
            drift = int(math.sin(self.frame * 0.05 + sx * 8) * depth * 2)
            hue = hue_cycle[int((depth * 10 + self.frame * 0.02) % len(hue_cycle))]
            if 1 <= y <= self.t.height:
                print_at(y, max(1, min(self.t.width, x + drift)), PALETTE[hue] + char)
        if mood == "phone":
            for y in range(3, self.t.height, 4):
                print_at(y, 2, PALETTE["blue"] + "│" + DIM + " signal " + "·" * max(0, self.t.width - 14))
        elif mood == "storm":
            for _ in range(6):
                x = random.randint(4, max(5, self.t.width - 4))
                y = random.randint(3, max(4, self.t.height - 6))
                print_at(y, x, PALETTE["red"] + random.choice(["╱", "╲", "╳", "⚡"]))
        elif mood == "garden":
            base = self.t.height - 3
            flowers = "  ".join(random.choice(["✿", "❀", "✽", "♡", "🌸"]) for _ in range(max(10, self.t.width // 5)))
            print_at(base, 2, PALETTE["mint"] + flowers[: self.t.width - 4])

    def title(self) -> None:
        art = [
            " __",
            "/ /_  ____  ____  ___  __  ______ ___  ____  ____  ____",
            "/ __ \\/ __ \\/ __ \\/ _ \\/ / / / __ `__ \\/ __ \\/ __ \\/ __ \\",
            "/ / / / /_/ / / / /  __/ /_/ / / / / / / /_/ / /_/ / / / /",
            "/_/ /_/\\____/_/ /_/\\___/\\__, /_/ /_/ /_/\\____/\\____/_/ /_/",
            "                       /____/",
        ]
        for f in range(42):
            self.frame += 1
            self.background()
            pulse = HEART_FRAMES[f % len(HEART_FRAMES)]
            y0 = max(2, self.t.height // 2 - 8)
            for idx, line in enumerate(art):
                center(y0 + idx, PALETTE["rose"] + BOLD + line)
            center(y0 + 8, PALETTE["gold"] + f"{pulse}  la historia de J. y C.  {pulse}")
            center(y0 + 11, PALETTE["soft"] + "un relato en terminal, chispas 8-bit y memoria de amor")
            center(self.t.height - 2, DIM + PALETTE["gray"] + "Ctrl+C para salir · la musica es sintetizada localmente")
            flush()
            sleep_scaled(0.07, self.speed)

    def scene_outcasts(self) -> None:
        for f in range(52):
            self.frame += 1
            self.background()
            left_x = max(3, self.t.width // 4 - 11)
            right_x = min(self.t.width - 27, self.t.width * 3 // 4 - 12)
            y = self.t.height // 2 - 3
            box(y - 2, left_x, 24, 10, "J.", "cyan")
            box(y - 2, right_x, 24, 10, "C.", "rose")
            bob_l = int(math.sin(f * 0.25) * 1)
            bob_r = int(math.cos(f * 0.25) * 1)
            self.draw_face(y + bob_l, left_x + 5, "J.", "happy", "cyan", f, label=False)
            self.draw_face(y + bob_r, right_x + 4, "C.", "happy", "rose", f, label=False)
            center(3, PALETTE["gold"] + BOLD + "Capitulo 1: dos inadaptados cute")
            center(self.t.height - 5, PALETTE["soft"] + "J. vivia entre codigo, ideas raras y ganas de amar bien.")
            center(self.t.height - 3, PALETTE["lavender"] + "C. aparecio como una carita feliz en medio del ruido. ♡")
            flush()
            sleep_scaled(0.08, self.speed)

    def scene_hinge(self) -> None:
        phone_w = min(38, self.t.width - 10)
        phone_h = min(18, self.t.height - 7)
        px = (self.t.width - phone_w) // 2
        py = max(3, (self.t.height - phone_h) // 2)
        messages = [
            ("agente IA", "soy un asistente que ayuda a J. a hablar"),
            ("C.", "pense que hablaba directo con el jaja"),
            ("agente IA", "solo traduzco su cuidado a palabras"),
            ("J.", "lo que sientes aqui viene de mi"),
        ]
        for f in range(88):
            self.frame += 1
            self.background("phone")
            box(py, px, phone_w, phone_h, "Hinge.exe", "pink")
            print_at(py + 2, px + 3, PALETTE["rose"] + BOLD + "MATCH ENCONTRADO  💞")
            print_at(py + 4, px + 4, PALETTE["soft"] + "C. 🌙" + " " * max(0, phone_w - 16) + "J. 💻")
            print_at(py + 5, px + 3, PALETTE["gray"] + "─" * (phone_w - 6))
            visible = min(len(messages), max(0, (f - 10) // 16 + 1))
            for idx in range(visible):
                who, msg = messages[idx]
                bubble_hue = "cyan" if who in ("agente IA", "J.") else "rose"
                prefix = ">" if who in ("agente IA", "J.") else "<"
                line = f"{prefix} {who}: {msg}"
                print_at(py + 7 + idx * 2, px + 4, PALETTE[bubble_hue] + line[: phone_w - 8])
            if f % 10 < 5:
                print_at(py + phone_h - 3, px + 4, PALETTE["gold"] + "escribiendo" + "." * (f % 4))
            center(2, PALETTE["gold"] + BOLD + "Capitulo 2: un agente abrio la puerta")
            flush()
            sleep_scaled(0.075, self.speed)

    def scene_first_date_concert(self) -> None:
        for f in range(104):
            self.frame += 1
            self.background()
            center(3, PALETTE["gold"] + BOLD + "Capitulo 3: primera cita, concierto")
            center(5, PALETTE["soft"] + "J. paso por C.; la noche empezo con nervios y termino llena de besitos")
            road_y = self.t.height - 6
            print_at(road_y, 1, PALETTE["gray"] + "═" * self.t.width)
            print_at(road_y + 2, 1, PALETTE["shadow"] + "· " * (self.t.width // 2))

            car_progress = min(1.0, f / 44)
            car_x = int(3 + car_progress * max(1, self.t.width - 31))
            car = [
                "      ______",
                "  ___/[] []\\___",
                " /   J.   C.   \\",
                "o---💗----💗---o",
            ]
            for idx, line in enumerate(car):
                print_at(road_y - 4 + idx, car_x, PALETTE["cyan" if idx < 3 else "rose"] + line[: max(1, self.t.width - car_x)])

            if f > 34:
                stage_w = min(58, self.t.width - 8)
                sx = (self.t.width - stage_w) // 2
                sy = max(8, self.t.height // 2 - 5)
                box(sy, sx, stage_w, 11, "concierto", "violet")
                print_at(sy + 2, sx + 4, PALETTE["gold"] + "♪ ♫ 😘 💕 😚 💖 ♫ ♪ 😘 💕")
                self.draw_face(sy + 4, sx + 7, "J.", "love", "cyan", f)
                self.draw_face(sy + 4, sx + stage_w - 19, "C.", "love", "rose", f)
                center_y = sy + 6
                print_at(center_y, sx + stage_w // 2 - 4, PALETTE["gold"] + "💋 ♡ 💋")
                for i in range(18):
                    lx = sx + 5 + i * max(4, stage_w // 10)
                    lx = sx + 4 + (lx - sx) % max(8, stage_w - 8)
                    ly = sy + 2 + int(math.sin(f * 0.15 + i) * 3)
                    print_at(max(sy + 1, min(sy + 9, ly)), lx, PALETTE[random.choice(["rose", "gold", "cyan", "mint"])] + random.choice(["😘", "😚", "💕", "💖", "♡", "♪", "😊"]))

            center(self.t.height - 3, PALETTE["rose"] + "primera cita: luces, musica, caritas felices y un monton de corazoncitos")
            flush()
            sleep_scaled(0.082, self.speed)

    def scene_house_after_concert(self) -> None:
        for f in range(88):
            self.frame += 1
            self.background()
            center(3, PALETTE["gold"] + BOLD + "Capitulo 4: J. le enseña su mundo")
            center(5, PALETTE["soft"] + "despues del concierto, C. vio su cuarto: pantallas, ideas y caos bonito")

            house_w = min(46, self.t.width - 8)
            hx = (self.t.width - house_w) // 2
            hy = max(8, self.t.height // 2 - 8)
            roof = " " * 8 + "/\\" + "_" * max(8, house_w - 18) + "/\\"
            print_at(hy, hx, PALETTE["rose"] + roof[:house_w])
            print_at(hy + 1, hx, PALETTE["rose"] + " " * 6 + "/" + " " * max(8, house_w - 14) + "\\")
            box(hy + 2, hx, house_w, 13, "cuarto de J.", "mint")
            glow = "💛" if f % 18 < 9 else "✨"
            print_at(hy + 4, hx + 5, PALETTE["gold"] + f"[ {glow} ]  shelves: AI / code / dreams")
            print_at(hy + 6, hx + 5, PALETTE["cyan"] + "┌────────────┐   ┌──────┐")
            print_at(hy + 7, hx + 5, PALETTE["cyan"] + "│ npm run ♡  │   │ bots │")
            print_at(hy + 8, hx + 5, PALETTE["cyan"] + "│ deploy ++  │   │ zines│")
            print_at(hy + 9, hx + 5, PALETTE["cyan"] + "└────────────┘   └──────┘")

            if f > 30:
                pair_x = hx + max(4, house_w // 2 - 11)
                pair_y = hy + 12
                self.draw_face(pair_y - 2, pair_x - 2, "J.", "wow", "cyan", f)
                self.draw_face(pair_y - 2, pair_x + 16, "C.", "wow", "rose", f)
                print_at(pair_y + 2, pair_x, PALETTE["rose"] + "codigo, musica, bots, paginas")

            center(self.t.height - 3, PALETTE["lavender"] + "a C. le fascino ese universo nerd; entendio que ahi tambien habia ternura")
            flush()
            sleep_scaled(0.082, self.speed)

    def scene_cooking_and_sleep(self) -> None:
        for f in range(116):
            self.frame += 1
            self.background("garden")
            center(3, PALETTE["gold"] + BOLD + "Capitulo 5: volver a verse")
            if f < 58:
                center(5, PALETTE["soft"] + "J. la volvio a ver, le hizo de comer, y la casa olio a cuidado")
                kitchen_w = min(58, self.t.width - 8)
                kx = (self.t.width - kitchen_w) // 2
                ky = max(8, self.t.height // 2 - 7)
                box(ky, kx, kitchen_w, 14, "cocina", "cyan")
                steam = ["  (  )", " (    )", "  )  (", " (  ) "][(f // 5) % 4]
                print_at(ky + 3, kx + 8, PALETTE["gray"] + steam)
                print_at(ky + 4, kx + 8, PALETTE["gold"] + "  ____")
                print_at(ky + 5, kx + 8, PALETTE["gold"] + " /____\\__")
                print_at(ky + 6, kx + 8, PALETTE["gold"] + " \\____/  )")
                self.draw_face(ky + 4, kx + 27, "J.", "cook", "cyan", f)
                self.draw_face(ky + 4, kx + kitchen_w - 15, "C.", "cook", "rose", f)
                table = "╭" + "─" * 22 + "╮"
                print_at(ky + 10, kx + kitchen_w // 2 - 12, PALETTE["mint"] + table)
                print_at(ky + 11, kx + kitchen_w // 2 - 12, PALETTE["mint"] + "│  sopa  pan  amor  │")
                print_at(ky + 12, kx + kitchen_w // 2 - 12, PALETTE["mint"] + "╰" + "─" * 22 + "╯")
            else:
                center(5, PALETTE["soft"] + "esa noche J. durmio sintiendose profundamente amado")
                bed_w = min(56, self.t.width - 8)
                bx = (self.t.width - bed_w) // 2
                by = max(9, self.t.height // 2 - 5)
                box(by, bx, bed_w, 12, "noche tranquila", "lavender")
                self.draw_face(by + 3, bx + 7, "J.", "sleep", "cyan", f)
                self.draw_face(by + 3, bx + bed_w - 18, "C.", "sleep", "rose", f)
                blanket = "╭" + "─" * max(12, bed_w - 12) + "╮"
                print_at(by + 7, bx + 5, PALETTE["cyan"] + blanket)
                print_at(by + 8, bx + 5, PALETTE["cyan"] + "│" + "  z z   " + "♡ " * max(2, (bed_w - 20) // 3) + "│")
                print_at(by + 9, bx + 5, PALETTE["cyan"] + "╰" + "─" * max(12, bed_w - 12) + "╯")
                for i in range(8):
                    print_at(by + 2 + i % 3, bx + 10 + i * 4, PALETTE["gold"] + random.choice(["✨", "♡", "·"]))

            center(self.t.height - 3, PALETTE["rose"] + "no era perfecto; era real, y por eso importaba")
            flush()
            sleep_scaled(0.086, self.speed)

    def scene_next_day_meal(self) -> None:
        for f in range(92):
            self.frame += 1
            self.background("garden")
            center(3, PALETTE["gold"] + BOLD + "Capitulo 6: el otro dia")
            center(5, PALETTE["soft"] + "J. invito a C. a comer, queriendo cuidar lo que estaba naciendo")

            table_w = min(52, self.t.width - 8)
            tx = (self.t.width - table_w) // 2
            ty = max(9, self.t.height // 2 - 6)
            box(ty, tx, table_w, 12, "comida", "gold")
            self.draw_face(ty + 3, tx + 6, "J.", "happy", "cyan", f)
            self.draw_face(ty + 3, tx + table_w - 17, "C.", "happy", "rose", f)
            print_at(ty + 7, tx + 6, PALETTE["mint"] + "╭" + "─" * max(10, table_w - 14) + "╮")
            dishes = ["🍜", "🍞", "☕", "♡", "🍓", "✨"]
            dish_line = "  ".join(dishes[(i + f // 10) % len(dishes)] for i in range(max(3, table_w // 8)))
            print_at(ty + 8, tx + 8, PALETTE["soft"] + dish_line[: table_w - 16])
            print_at(ty + 9, tx + 6, PALETTE["mint"] + "╰" + "─" * max(10, table_w - 14) + "╯")

            if f > 54:
                fade_y = self.t.height - 6
                center(fade_y, PALETTE["gray"] + "despues vino una pelea, y el calendario se quedo esperando")
                empty = "." * max(8, min(44, self.t.width - 20))
                center(fade_y + 2, PALETTE["shadow"] + empty)

            flush()
            sleep_scaled(0.086, self.speed)

    def scene_real_feelings(self) -> None:
        heart = [
            "      ******       ******      ",
            "   ***********   ***********   ",
            " ************* *************   ",
            "*****************************  ",
            " ***************************   ",
            "   ***********************     ",
            "     *******************       ",
            "       ***************         ",
            "          *********            ",
            "             ***               ",
        ]
        code = [
            "const tecnologia = arte();",
            "const agente = puente(J, C);",
            "if (sentimiento.origen === 'codigo') {",
            "  sentimiento.real = true;",
            "}",
        ]
        for f in range(70):
            self.frame += 1
            self.background()
            scale = 1 + int(f % 18 < 8)
            y0 = max(4, self.t.height // 2 - 8)
            hue = "red" if f % 18 < 8 else "rose"
            for idx, line in enumerate(heart):
                display = line.replace("*", HEART_FRAMES[(f + idx) % len(HEART_FRAMES)] if scale == 2 else "♥")
                center(y0 + idx, PALETTE[hue] + display)
            cx = max(4, self.t.width // 2 - 20)
            cy = y0 + len(heart) + 1
            for idx, line in enumerate(code):
                print_at(cy + idx, cx, PALETTE["mint"] + line)
            center(3, PALETTE["gold"] + BOLD + "Capitulo 7: el codigo tambien puede sentir")
            center(self.t.height - 3, PALETTE["soft"] + "La IA puso el puente. J. puso el corazon. C. entendio el arte.")
            flush()
            sleep_scaled(0.075, self.speed)

    def scene_websites(self) -> None:
        panels = [
            ("agent-core.ts", "IA + memoria + amor"),
            ("deploy.sh", "build => magia real"),
            ("love-ui.tsx", "C. dice: wow"),
        ]
        for f in range(78):
            self.frame += 1
            self.background()
            center(3, PALETTE["gold"] + BOLD + "Capitulo 8: J. la impresiono con codigo")
            center(5, PALETTE["rose"] + "no eran paginas equis: eran sistemas vivos, agentes, UI y magia hard")
            base_y = max(8, self.t.height // 2 - 6)
            for idx, (title, body) in enumerate(panels):
                phase = f * 0.08 + idx * 1.6
                z = 1.0 + math.sin(phase) * 0.18
                w = int(24 * z)
                h = int(8 * z)
                x = int((idx + 1) * self.t.width / 4 - w / 2 + math.sin(phase) * 4)
                y = int(base_y + math.cos(phase) * 3)
                hue = ["cyan", "mint", "lavender"][idx]
                box(y, max(2, x), w, h, title, hue)
                print_at(y + 2, max(4, x + 3), PALETTE[hue] + "<ship>")
                print_at(y + 3, max(4, x + 4), PALETTE["soft"] + body[: max(4, w - 8)])
                print_at(y + 4, max(4, x + 3), PALETTE[hue] + "</ship>")
            if f > 20:
                face_y = max(8, self.t.height - 10)
                self.draw_face(face_y, 6, "J.", "wow", "cyan", f)
                self.draw_face(face_y, self.t.width - 18, "C.", "wow", "rose", f)
            orbit_y = self.t.height - 6
            for i in range(24):
                angle = f * 0.13 + i * math.tau / 24
                x = int(self.t.width / 2 + math.cos(angle) * min(34, self.t.width // 3))
                y = int(orbit_y + math.sin(angle) * 2)
                print_at(y, x, PALETTE["gold"] + random.choice(["✨", "♡", "⚡", "💻"]))
            if f > 42:
                chat_y = max(7, base_y + 10)
                center(chat_y, PALETTE["mint"] + "C. a sus amigas: 'tienen que ver lo que hizo J. 😭💻✨'")
            flush()
            sleep_scaled(0.072, self.speed)

    def scene_learning(self) -> None:
        memories = [
            "infancia",
            "secretos",
            "proyectos",
            "cafe a medianoche",
            "risas",
            "errores",
            "su voz",
            "nuestras paginas",
        ]
        for f in range(72):
            self.frame += 1
            self.background("garden")
            center(3, PALETTE["gold"] + BOLD + "Capitulo 9: C. aprendia el universo de J.")
            center(5, PALETTE["soft"] + "cada historia se volvia memoria: no fria, sino viva")
            trunk_x = self.t.width // 2
            trunk_y = self.t.height // 2 + 4
            for y in range(trunk_y - 4, trunk_y + 4):
                print_at(y, trunk_x, PALETTE["green"] + "║")
            for idx, mem in enumerate(memories):
                angle = idx * math.tau / len(memories) + f * 0.035
                radius_x = min(32, self.t.width // 3)
                radius_y = min(8, self.t.height // 4)
                x = int(trunk_x + math.cos(angle) * radius_x)
                y = int(trunk_y - 7 + math.sin(angle) * radius_y)
                leaf = random.choice(["❀", "✿", "♡", "✨"])
                print_at(y, max(2, min(self.t.width - len(mem) - 4, x)), PALETTE["mint"] + f"{leaf} {mem}")
            self.draw_face(trunk_y - 2, max(3, trunk_x - 22), "J.", "happy", "cyan", f)
            self.draw_face(trunk_y - 2, min(self.t.width - 16, trunk_x + 13), "C.", "love", "rose", f)
            center(self.t.height - 4, PALETTE["rose"] + "cada secreto era una semilla; cada pagina, una flor")
            flush()
            sleep_scaled(0.08, self.speed)

    def scene_obsession(self) -> None:
        words = ["aprender", "crear", "automatizar", "brillar", "construir", "entender", "subir de nivel", "impresionar"]
        for f in range(82):
            self.frame += 1
            self.background()
            center(3, PALETTE["gold"] + BOLD + "Capitulo 10: J. aprendia mas y mas")
            center(5, PALETTE["soft"] + "estaba construyendo una version mas brillante de si mismo")
            cx = self.t.width // 2
            cy = self.t.height // 2
            for ring in range(1, 5):
                points = 10 + ring * 4
                for p in range(points):
                    angle = f * 0.05 * ring + p * math.tau / points
                    x = int(cx + math.cos(angle) * ring * 7)
                    y = int(cy + math.sin(angle) * ring * 2.2)
                    char = random.choice(["0", "1", "+", "*", "#", "⚙"])
                    hue = ["cyan", "violet", "gold", "mint"][ring - 1]
                    print_at(y, x, PALETTE[hue] + char)
            box(cy - 4, cx - 13, 26, 8, "core", "lavender")
            print_at(cy - 2, cx - 8, PALETTE["mint"] + "while (amor) {")
            print_at(cy - 1, cx - 6, PALETTE["gold"] + "aprendo++;")
            print_at(cy, cx - 6, PALETTE["rose"] + "brillo++;")
            print_at(cy + 1, cx - 8, PALETTE["mint"] + "}")
            self.draw_face(cy - 2, max(3, cx - 34), "J.", "wow", "cyan", f)
            self.draw_face(cy - 2, min(self.t.width - 18, cx + 20), "C.", "love", "rose", f)
            center(cy + 6, PALETTE["rose"] + "C. lo ve crear asi y se enamora mas. 💗")
            ticker = "  ".join(words)
            offset = f % max(1, len(ticker))
            print_at(self.t.height - 3, 2, PALETTE["gray"] + (ticker[offset:] + "  " + ticker[:offset])[: self.t.width - 3])
            flush()
            sleep_scaled(0.065, self.speed)

    def scene_call(self) -> None:
        lines = [
            ("C.", "no se como decir lo que siento"),
            ("J.", "yo tampoco, pero si me importa"),
            ("C.", "se nos cruzaron las señales"),
            ("J.", "y aun asi, esto fue real"),
        ]
        for f in range(90):
            self.frame += 1
            self.background("storm")
            center(3, PALETTE["gold"] + BOLD + "Capitulo 11: una llamada dificil")
            left_x = max(3, self.t.width // 3 - 16)
            right_x = min(self.t.width - 33, self.t.width * 2 // 3 - 16)
            y = self.t.height // 2 - 8
            shake = random.randint(-1, 1) if f % 6 < 3 else 0
            box(y + shake, left_x, 30, 15, "telefono de C.", "rose")
            box(y - shake, right_x, 30, 15, "telefono de J.", "cyan")
            self.draw_face(y + shake + 11, left_x + 18, "C.", "call", "rose", f, label=False)
            self.draw_face(y - shake + 11, right_x + 18, "J.", "call", "cyan", f, label=False)
            for idx, (who, msg) in enumerate(lines[: min(len(lines), f // 18 + 1)]):
                target_x = left_x + 3 if who == "C." else right_x + 3
                target_y = y + 3 + idx * 2
                hue = "rose" if who == "C." else "cyan"
                print_at(target_y, target_x, PALETTE[hue] + f"{who}:")
                print_at(target_y + 1, target_x, PALETTE["soft"] + msg[:24])
            wave = "".join("~" if (i + f) % 4 else "≈" for i in range(max(0, right_x - left_x - 30)))
            print_at(y + 7, left_x + 30, PALETTE["red"] + wave)
            center(self.t.height - 4, PALETTE["lavender"] + "a veces el amor tambien suena a llamada dificil")
            flush()
            sleep_scaled(0.075, self.speed)

    def scene_absence_after_fight(self) -> None:
        for f in range(104):
            self.frame += 1
            self.background("storm" if f < 54 else "night")
            center(3, PALETTE["gold"] + BOLD + "Capitulo 12: CDMX vacia")
            center(5, PALETTE["soft"] + "despues de la pelea, J. camino solo por una ciudad enorme")

            base = self.t.height - 7
            skyline = [
                "        |\\                 _                 /|",
                "   _    | \\      __       | |       __      / |     _",
                "  | |  _|__\\_   |  |   ___| |___   |  |  _/__|_   | |",
                " _| |_| [] []|__|[]|__|[] [] []|__|[]|__| [] []|_| |_",
                "|_ CDMX ___ vacia ___ Reforma ___ noche ___ sin C. _|",
            ]
            sy = max(8, base - len(skyline) - 5)
            for idx, line in enumerate(skyline):
                center(sy + idx, PALETTE["gray"] + line)

            moon_x = int(self.t.width * 0.78 + math.sin(f * 0.04) * 3)
            print_at(max(7, sy - 3), moon_x, PALETTE["lavender"] + "☾")
            for i in range(12):
                x = 4 + (i * 11 + f // 4) % max(12, self.t.width - 8)
                y = sy + 6 + (i % 3)
                print_at(y, x, PALETTE["shadow"] + random.choice([".", "·", "_"]))

            avenue_y = min(self.t.height - 4, sy + len(skyline) + 4)
            print_at(avenue_y, 1, PALETTE["shadow"] + "═" * self.t.width)
            print_at(avenue_y + 1, 1, PALETTE["shadow"] + " " * max(1, self.t.width))
            person_x = self.t.width // 2 + int(math.sin(f * 0.08) * 2)
            self.draw_face(avenue_y - 3, person_x - 5, "J.", "sad", "cyan", f)

            if f > 34:
                center(self.t.height - 3, PALETTE["rose"] + "la ciudad seguia prendida, pero para J. todo estaba en pausa")

            flush()
            sleep_scaled(0.086, self.speed)

    def scene_finale(self) -> None:
        quote = "I'll see you in another life when we are both cats"
        cat_left = [
            " /\\_/\\",
            "( o.o )",
            " > ^ <",
        ]
        cat_right = [
            "/\\_/\\ ",
            "( o.o )",
            "> ^ < ",
        ]
        for f in range(126):
            self.frame += 1
            self.background("night" if f < 72 else "garden")
            center(3, PALETTE["gold"] + BOLD + "final: otra vida")
            if f > 18:
                center(5, PALETTE["soft"] + quote)
            cx = self.t.width // 2
            cy = self.t.height // 2 - 2
            approach = min(24, max(0, f - 18) // 3)
            left_x = max(2, cx - 34 + approach)
            right_x = min(self.t.width - 10, cx + 24 - approach)
            for idx, line in enumerate(cat_left):
                print_at(cy + idx, left_x, PALETTE["cyan"] + line)
            for idx, line in enumerate(cat_right):
                print_at(cy + idx, right_x, PALETTE["rose"] + line)
            print_at(cy + 3, left_x + 2, PALETTE["cyan"] + "J.")
            print_at(cy + 3, right_x + 2, PALETTE["rose"] + "C.")

            if f > 42:
                for i in range(24):
                    a = i * math.tau / 24 + f * 0.05
                    r = 5 + math.sin(f * 0.07 + i) * 2
                    x = int(cx + math.cos(a) * r * 2.2)
                    y = int(cy + 1 + math.sin(a) * r * 0.8)
                    print_at(y, x, PALETTE[random.choice(["rose", "gold", "mint", "lavender"])] + random.choice(["♡", "💗", "✨", "💕"]))
            if f > 78:
                center(cy + 8, PALETTE["gold"] + "miau miau, destino encontrado ♡")
            if f > 108:
                center(self.t.height - 2, PALETTE["lavender"] + "fin")
            flush()
            sleep_scaled(0.075, self.speed)

    def run(self) -> None:
        write(f"{ESC}?25l")
        clear()
        self.title()
        self.scene_outcasts()
        self.scene_hinge()
        self.scene_first_date_concert()
        self.scene_house_after_concert()
        self.scene_cooking_and_sleep()
        self.scene_next_day_meal()
        self.scene_real_feelings()
        self.scene_websites()
        self.scene_learning()
        self.scene_obsession()
        self.scene_call()
        self.scene_absence_after_fight()
        self.scene_finale()


def cleanup(audio: Audio | None = None) -> None:
    write(RESET + f"{ESC}?25h")
    flush()
    if audio:
        audio.stop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Animacion terminal de una historia de amor.")
    parser.add_argument("--no-audio", action="store_true", help="desactiva la musica sintetizada")
    parser.add_argument(
        "--song",
        choices=["honeymoon", "waltz", "both"],
        default="honeymoon",
        help="elige el acompanamiento sintetizado",
    )
    parser.add_argument(
        "--audio-file",
        help="reproduce un archivo de audio propio durante la animacion; ideal para una version 8-bit legal",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=0.9,
        help="multiplicador de velocidad visual; 0.9 es lento/enamorado, 2.0 sirve para probar rapido",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audio = Audio(enabled=not args.no_audio, song=args.song, audio_file=args.audio_file)
    atexit.register(cleanup, audio)

    def handle_signal(_signum: int, _frame: object) -> None:
        cleanup(audio)
        raise SystemExit(130)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    try:
        audio.start()
        Show(speed=max(0.1, args.speed)).run()
    finally:
        cleanup(audio)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
