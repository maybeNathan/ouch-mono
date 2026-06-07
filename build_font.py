#!/usr/bin/env python3
"""Build OuchV2.ttf from SVG glyphs using FontForge."""

import os
import fontforge

SVG_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(SVG_DIR, "OuchV2.ttf")

EM = 1000
ADV = 650

# Map filename stem -> unicode character
GLYPH_MAP = {
    # digits: "7X" prefix is serialization noise, X is the digit
    "70": "0", "71": "1", "72": "2", "73": "3", "74": "4",
    "75": "5", "76": "6", "77": "7", "78": "8", "79": "9",
    # lowercase
    **{c: c for c in "abcdefghijklmnopqrstuvwxyz"},
    # uppercase
    **{c: c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
    # punctuation / special (ASCII)
    "sc!":              "!",
    "sc_double quot":   '"',
    "sc#":              "#",
    "sc$":              "$",
    "sc_percent":       "%",
    "sc_amper":         "&",
    "sc_apostraphe":    "'",
    "sc_paren_left":    "(",
    "sc_paren_right":   ")",
    "sc_ast":           "*",
    "sc_plus":          "+",
    "sc-comma":         ",",
    "sc_minus":         "-",
    "sc-period":        ".",
    "sc-forward-slash": "/",
    "sc-colon":         ":",
    "sc_semi-colon":    ";",
    "sc-less-than":     "<",
    "sc_equal":         "=",
    "sc-greater-than":  ">",
    "sc-question":      "?",
    "sc@":              "@",
    "sc_bracket_left":  "[",
    "sc-back-slash":    "\\",
    "sc_bracket_right": "]",
    "sc_bump":          "^",
    "sc_under":         "_",
    "sc-grave":         "`",
    "sc_curly_left":    "{",
    "sc-pipe":          "|",
    "sc_curly_right":   "}",
    "sc-tilde":         "~",
    # extended / math / arrows (Unicode)
    "sc-less-than-or-equal-to":    "≤",  # ≤
    "sc-greater-than-or-equal-to": "≥",  # ≥
    "scnot":                       "≠",  # ≠
    "scthree_equal":               "≡",  # ≡
    "scleft_arrow":                "←",  # ←
    "scright_arrow":               "→",  # →
    "scleft_arrow_long":           "⟵",  # ⟵
    "scright_arrow_long":          "⟶",  # ⟶
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

        print(f"  {stem!r:35s}  U+{cp:04X}  '{ch}'")

    font.generate(OUT_PATH)
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
