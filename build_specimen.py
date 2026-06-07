#!/usr/bin/env python3
"""Build glyphs.svg — all OuchV2 glyphs in a single specimen SVG."""

import os
import re
import math
import html

SVG_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(SVG_DIR, "glyphs.svg")

COLS = 13
CELL_W = 90
CELL_H = 100
GLYPH_SZ = 70
PAD = 14
HEADER_H = 52

GLYPH_MAP = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    **{c: c for c in "abcdefghijklmnopqrstuvwxyz"},
    **{c: c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
    "exclam":       "!",
    "quotedbl":     '"',
    "numbersign":   "#",
    "dollar":       "$",
    "percent":      "%",
    "ampersand":    "&",
    "quotesingle":  "'",
    "parenleft":    "(",
    "parenright":   ")",
    "asterisk":     "*",
    "plus":         "+",
    "comma":        ",",
    "hyphen":       "-",
    "period":       ".",
    "slash":        "/",
    "colon":        ":",
    "semicolon":    ";",
    "less":         "<",
    "equal":        "=",
    "greater":      ">",
    "question":     "?",
    "at":           "@",
    "bracketleft":  "[",
    "backslash":    "\\",
    "bracketright": "]",
    "asciicircum":  "^",
    "underscore":   "_",
    "grave":        "`",
    "braceleft":    "{",
    "bar":          "|",
    "braceright":   "}",
    "asciitilde":   "~",
    "lessequal":      "≤",
    "greaterequal":   "≥",
    "notequal":       "≠",
    "tripleequal":    "≡",
    "arrowleft":      "←",
    "arrowright":     "→",
    "longarrowleft":  "⟵",
    "longarrowright": "⟶",
}

ORDER = [
    "zero","one","two","three","four","five","six","seven","eight","nine",
    *list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    *list("abcdefghijklmnopqrstuvwxyz"),
    "exclam","quotedbl","numbersign","dollar","percent","ampersand","quotesingle",
    "parenleft","parenright","asterisk","plus","comma","hyphen","period","slash",
    "colon","semicolon","less","equal","greater","question","at",
    "bracketleft","backslash","bracketright","asciicircum","underscore","grave",
    "braceleft","bar","braceright","asciitilde",
    "lessequal","greaterequal","notequal","tripleequal",
    "arrowleft","arrowright","longarrowleft","longarrowright",
]


def get_inner(svg_path):
    with open(svg_path) as f:
        content = f.read()
    inner = re.sub(r"<svg[^>]*>", "", content, count=1)
    inner = re.sub(r"</svg>\s*$", "", inner)
    return inner.strip()


def main():
    rows = math.ceil(len(ORDER) / COLS)
    W = COLS * CELL_W + PAD * 2
    H = rows * CELL_H + PAD * 2 + HEADER_H

    out = []
    out.append(
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )
    out.append(f'<rect width="{W}" height="{H}" fill="#f4f4f4"/>')
    out.append(
        f'<text x="{W // 2}" y="34" font-family="monospace" font-size="24" '
        f'font-weight="bold" text-anchor="middle" fill="#111">Ouch Mono</text>'
    )

    for i, stem in enumerate(ORDER):
        ch = GLYPH_MAP.get(stem, "?")
        row = i // COLS
        col = i % COLS
        cx = PAD + col * CELL_W
        cy = PAD + HEADER_H + row * CELL_H

        svg_file = os.path.join(SVG_DIR, f"{stem}.svg")
        if not os.path.exists(svg_file):
            print(f"  MISSING  {stem}.svg")
            continue

        inner = get_inner(svg_file)
        gx = cx + (CELL_W - GLYPH_SZ) // 2
        gy = cy + 4

        out.append(
            f'<rect x="{cx + 1}" y="{cy + 1}" width="{CELL_W - 3}" '
            f'height="{CELL_H - 3}" fill="white" stroke="#ddd" stroke-width="1" rx="4"/>'
        )
        out.append(
            f'<svg x="{gx}" y="{gy}" width="{GLYPH_SZ}" height="{GLYPH_SZ}" '
            f'viewBox="0 0 1000 1000">'
        )
        out.append(inner)
        out.append("</svg>")

        label = html.escape(ch)
        out.append(
            f'<text x="{cx + CELL_W // 2}" y="{cy + GLYPH_SZ + 20}" '
            f'font-family="monospace" font-size="12" text-anchor="middle" '
            f'fill="#555">{label}</text>'
        )

    out.append("</svg>")

    with open(OUT_PATH, "w") as f:
        f.write("\n".join(out))
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
