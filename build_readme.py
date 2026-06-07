#!/usr/bin/env python3
"""Build README.pdf — font specimen using OuchV2.ttf."""

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(DIR, "OuchV2.ttf")
OUT_PATH = os.path.join(DIR, "README.pdf")

pdfmetrics.registerFont(TTFont("OuchV2", FONT_PATH))

W, H = A4
MARGIN = 48


def rule(c, y):
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(0.5)
    c.line(MARGIN, y, W - MARGIN, y)


def heading(c, text, y):
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.45, 0.45, 0.45)
    c.drawString(MARGIN, y, text.upper())
    c.setFillColorRGB(0, 0, 0)


def main():
    c = canvas.Canvas(OUT_PATH, pagesize=A4)
    y = H - MARGIN

    # Title
    c.setFont("OuchV2", 52)
    c.setFillColorRGB(0.05, 0.05, 0.05)
    c.drawString(MARGIN, y - 52, "Ouch Mono")
    y -= 68

    # Subtitle
    c.setFont("OuchV2", 14)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(MARGIN, y, "A handcrafted monospace typeface")
    y -= 24
    rule(c, y)
    y -= 20

    # Full character set
    heading(c, "Full character set", y)
    y -= 18
    char_rows = [
        '! " # $ % & \' ( ) * + , - . / 0 1 2 3 4 5 6 7',
        '8 9 : ; < = > ? @ A B C D E F G H I J K L M N O',
        'P Q R S T U V W X Y Z [ \\ ] ^ _ ` a b c d e f g',
        'h i j k l m n o p q r s t u v w x y z { | } ~',
    ]
    c.setFillColorRGB(0, 0, 0)
    for row in char_rows:
        c.setFont("OuchV2", 18)
        c.drawString(MARGIN, y, row)
        y -= 26
    y -= 6

    heading(c, "Extended", y)
    y -= 18
    c.setFont("OuchV2", 18)
    c.drawString(MARGIN, y, "≤ ≥ ≠ ≡ ← → ⟵ ⟶")
    y -= 32

    rule(c, y)
    y -= 20

    # Size specimens
    heading(c, "Size specimens", y)
    y -= 4
    for sz in [36, 24, 18, 14, 11]:
        y -= sz + 6
        c.setFont("OuchV2", sz)
        c.drawString(MARGIN, y, "the quick brown fox")
    y -= 20

    rule(c, y)
    y -= 20

    # Pangrams
    heading(c, "Pangrams", y)
    y -= 18
    c.setFont("OuchV2", 13)
    for p in [
        "the quick brown fox jumps over the lazy dog",
        "pack my box with five dozen liquor jugs",
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
    ]:
        c.drawString(MARGIN, y, p)
        y -= 18
    y -= 10

    rule(c, y)
    y -= 20

    # Code sample
    heading(c, "Code sample", y)
    y -= 18
    c.setFont("OuchV2", 11)
    c.setFillColorRGB(0.1, 0.1, 0.1)
    for line in [
        "fn greet(name: &str) -> String {",
        '    format!("hello, {}!", name)',
        "}",
        "",
        "if x >= 0 && x <= 100 {",
        '    println!("in range: {}", x);',
        "}",
        "",
        "let result = match op {",
        '    "add" => a + b,',
        '    "sub" => a - b,',
        "    _     => 0,",
        "};",
    ]:
        c.drawString(MARGIN, y, line)
        y -= 15

    c.save()
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
