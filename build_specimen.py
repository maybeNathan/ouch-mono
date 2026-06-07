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
    "70": "0", "71": "1", "72": "2", "73": "3", "74": "4",
    "75": "5", "76": "6", "77": "7", "78": "8", "79": "9",
    **{c: c for c in "abcdefghijklmnopqrstuvwxyz"},
    **{c: c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
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
    "sc-less-than-or-equal-to":    "≤",
    "sc-greater-than-or-equal-to": "≥",
    "scnot":                       "≠",
    "scthree_equal":               "≡",
    "scleft_arrow":                "←",
    "scright_arrow":               "→",
    "scleft_arrow_long":           "⟵",
    "scright_arrow_long":          "⟶",
}

ORDER = [
    "70","71","72","73","74","75","76","77","78","79",
    *list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    *list("abcdefghijklmnopqrstuvwxyz"),
    "sc!","sc_double quot","sc#","sc$","sc_percent","sc_amper","sc_apostraphe",
    "sc_paren_left","sc_paren_right","sc_ast","sc_plus","sc-comma",
    "sc_minus","sc-period","sc-forward-slash","sc-colon","sc_semi-colon",
    "sc-less-than","sc_equal","sc-greater-than","sc-question","sc@",
    "sc_bracket_left","sc-back-slash","sc_bracket_right","sc_bump","sc_under",
    "sc-grave","sc_curly_left","sc-pipe","sc_curly_right","sc-tilde",
    "sc-less-than-or-equal-to","sc-greater-than-or-equal-to","scnot","scthree_equal",
    "scleft_arrow","scright_arrow","scleft_arrow_long","scright_arrow_long",
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
