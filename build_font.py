#!/usr/bin/env python3
"""Build OuchV2.ttf from SVG glyphs using FontForge."""

import os
import fontforge

SVG_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(SVG_DIR, "OuchV2.ttf")

EM = 1000
ADV = 650

GLYPH_MAP = {
    # digits
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    # lowercase
    **{c: c for c in "abcdefghijklmnopqrstuvwxyz"},
    # uppercase
    **{c: c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
    # ASCII punctuation / symbols
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
    # extended / math / arrows
    "lessequal":      "≤",
    "greaterequal":   "≥",
    "notequal":       "≠",
    "tripleequal":    "≡",
    "arrowleft":      "←",
    "arrowright":     "→",
    "longarrowleft":  "⟵",
    "longarrowright": "⟶",
}


def main():
    font = fontforge.font()
    font.familyname = "OuchV2"
    font.fullname   = "OuchV2 Regular"
    font.fontname   = "OuchV2-Regular"
    font.weight     = "Regular"
    font.encoding   = "UnicodeFull"
    font.em         = EM

    font.ascent  = 800
    font.descent = 200

    sp = font.createChar(0x20, "space")
    sp.width = ADV

    for stem, ch in GLYPH_MAP.items():
        svg_file = os.path.join(SVG_DIR, f"{stem}.svg")
        if not os.path.exists(svg_file):
            print(f"  MISSING  {stem}.svg")
            continue

        cp = ord(ch)
        glyph = font.createChar(cp)
        glyph.importOutlines(svg_file)
        glyph.transform((1, 0, 0, 1, -175, 0))
        glyph.width = ADV

        print(f"  {stem!r:20s}  U+{cp:04X}  '{ch}'")

    font.generate(OUT_PATH)
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
