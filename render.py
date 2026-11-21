#!/usr/bin/env python3
"""Draw the one-page world-news summary for Saturday 21 November 2026.

The page imitates a broadsheet front page.  A centred masthead and a
red dateline sit over a two-by-two grid of story cards; each card has
a small hand-drawn pictogram, a bold headline and a short standfirst.
A briefs column along the foot of the page carries four more items.

Everything is placed with fixed coordinates and bundled Liberation
fonts, and nothing here reads the clock or a random source, so two
runs always produce the identical PNG.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
PAGE = 1024
EDGE = 56

COLOURS = {
    "paper": (247, 243, 232),
    "card": (255, 253, 245),
    "black": (24, 22, 20),
    "accent": (158, 24, 36),
    "faded": (96, 90, 82),
    "hairline": (60, 56, 50),
}


def load_font(filename, size):
    """Load one Liberation face at one size."""
    return ImageFont.truetype(str(FONT_DIR / filename), size)


FACES = {
    "masthead": load_font("LiberationSerif-Bold.ttf", 63),
    "dateline": load_font("LiberationSans-Bold.ttf", 40),
    "kicker": load_font("LiberationSans-Bold.ttf", 19),
    "headline": load_font("LiberationSerif-Bold.ttf", 31),
    "body": load_font("LiberationSans-Regular.ttf", 20),
    "briefs": load_font("LiberationSans-Regular.ttf", 19),
    "briefs_head": load_font("LiberationSans-Bold.ttf", 19),
    "folio": load_font("LiberationSans-Regular.ttf", 16),
}


def break_lines(draw, words_text, face, limit):
    """Split text into lines that each fit within ``limit`` pixels."""
    lines = []
    current = ""
    for word in words_text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=face) <= limit:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, y, text, face, colour):
    """Paint one line of text centred on the page at height ``y``."""
    width = draw.textlength(text, font=face)
    draw.text(((PAGE - width) / 2, y), text, font=face, fill=colour)


def paragraph(draw, left, top, text, face, colour, limit, leading):
    """Paint wrapped text from the top-left corner; return end height."""
    y = top
    for line in break_lines(draw, text, face, limit):
        draw.text((left, y), line, font=face, fill=colour)
        y += leading
    return y


# --- pictograms -----------------------------------------------------

def draw_rocket(draw, cx, cy):
    """A simple missile: body, nose cone, two fins and a flame."""
    ink = COLOURS["black"]
    draw.polygon([(cx, cy - 30), (cx + 9, cy - 8), (cx - 9, cy - 8)], fill=ink)
    draw.rectangle([cx - 9, cy - 8, cx + 9, cy + 22], fill=ink)
    draw.polygon([(cx - 9, cy + 8), (cx - 20, cy + 24), (cx - 9, cy + 24)], fill=ink)
    draw.polygon([(cx + 9, cy + 8), (cx + 20, cy + 24), (cx + 9, cy + 24)], fill=ink)
    draw.polygon(
        [(cx - 5, cy + 22), (cx + 5, cy + 22), (cx, cy + 36)],
        fill=COLOURS["accent"],
    )


def draw_target(draw, cx, cy):
    """Concentric rings with a filled centre, like a gunsight."""
    for radius, colour in (
        (26, COLOURS["black"]),
        (19, COLOURS["card"]),
        (12, COLOURS["accent"]),
        (5, COLOURS["black"]),
    ):
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius], fill=colour
        )


def draw_downtrend(draw, cx, cy):
    """A falling line chart with an arrowhead at the low end."""
    ink = COLOURS["black"]
    points = [(cx - 26, cy - 16), (cx - 8, cy - 4), (cx + 6, cy - 10), (cx + 24, cy + 14)]
    draw.line(points, fill=COLOURS["accent"], width=4)
    draw.polygon(
        [(cx + 24, cy + 14), (cx + 12, cy + 12), (cx + 22, cy + 2)], fill=COLOURS["accent"]
    )
    draw.line([cx - 28, cy + 24, cx + 28, cy + 24], fill=ink, width=2)


def draw_robot(draw, cx, cy):
    """A friendly robot head: rounded box, eyes, antenna."""
    ink = COLOURS["black"]
    draw.line([cx, cy - 34, cx, cy - 24], fill=ink, width=3)
    draw.ellipse([cx - 4, cy - 39, cx + 4, cy - 31], fill=COLOURS["accent"])
    draw.rounded_rectangle([cx - 24, cy - 24, cx + 24, cy + 22], radius=8, outline=ink, width=3)
    draw.ellipse([cx - 14, cy - 8, cx - 5, cy + 1], fill=ink)
    draw.ellipse([cx + 5, cy - 8, cx + 14, cy + 1], fill=ink)
    draw.line([cx - 10, cy + 12, cx + 10, cy + 12], fill=ink, width=3)


# --- the page -------------------------------------------------------

STORIES = [
    (
        "WAR IN EUROPE",
        "Russian Missiles Land in Poland",
        "NATO condemned the strike as a violation of its airspace, "
        "while Kyiv was hit by another wave of Russian attacks overnight.",
        draw_rocket,
    ),
    (
        "MIDDLE EAST",
        "Trump Weighs Fresh Strikes on Iran",
        "Tehran says it wants diplomacy; Washington replies that "
        "the terms on offer are unacceptable.",
        draw_target,
    ),
    (
        "MARKETS",
        "Stocks Slide as S&P 500 Drops 3.7%",
        "Anthropic's much-watched $2 trillion market debut stumbled "
        "as AI shares led a broad sell-off.",
        draw_downtrend,
    ),
    (
        "TECH & LAW",
        "UN Opens Path to 'Killer Robot' Pact",
        "Negotiators in Geneva agreed to start work on global rules "
        "for autonomous weapons, aiming for a treaty by 2028.",
        draw_robot,
    ),
]

BRIEFS = (
    "COP31 climate talks run into overtime over fossil fuels  ·  "
    "Hackers breach the USDA and FBI  ·  "
    "Honda and Toyota recall 1.6 million cars  ·  "
    "Mexico captures a cartel kingpin"
)


def paint_card(draw, left, top, story):
    """Paint one story card with its pictogram in the top corner."""
    kicker, headline, body, pictogram = story
    right = left + 444
    bottom = top + 296
    draw.rectangle([left, top, right, bottom], fill=COLOURS["card"])
    draw.rectangle([left, top, right, bottom], outline=COLOURS["hairline"], width=2)
    inner = left + 24
    draw.text((inner, top + 18), kicker, font=FACES["kicker"], fill=COLOURS["accent"])
    pictogram(draw, right - 52, top + 52)
    y = paragraph(
        draw, inner, top + 58, headline, FACES["headline"],
        COLOURS["black"], 348, 38,
    )
    paragraph(draw, inner, y + 12, body, FACES["body"], COLOURS["black"], 396, 27)


def build_page():
    """Assemble the whole front page and return the image."""
    image = Image.new("RGB", (PAGE, PAGE), COLOURS["paper"])
    draw = ImageDraw.Draw(image)

    draw.line([EDGE, 40, PAGE - EDGE, 40], fill=COLOURS["hairline"], width=3)
    centred(draw, 54, "THE WORLD IN ONE PAGE", FACES["masthead"], COLOURS["black"])
    draw.line([EDGE, 138, PAGE - EDGE, 138], fill=COLOURS["hairline"], width=1)
    centred(
        draw, 150, "SATURDAY, NOVEMBER 21, 2026",
        FACES["dateline"], COLOURS["accent"],
    )
    centred(
        draw, 202, "The day's world news, gathered on a single page",
        FACES["folio"], COLOURS["faded"],
    )
    draw.line([EDGE, 232, PAGE - EDGE, 232], fill=COLOURS["hairline"], width=3)

    grid_top = 252
    for index, story in enumerate(STORIES):
        column = index % 2
        row = index // 2
        paint_card(draw, EDGE + column * 468, grid_top + row * 320, story)

    strip_top = grid_top + 2 * 320 + 16
    draw.line([EDGE, strip_top, PAGE - EDGE, strip_top], fill=COLOURS["hairline"], width=3)
    draw.text(
        (EDGE, strip_top + 14), "ALSO TODAY",
        font=FACES["briefs_head"], fill=COLOURS["accent"],
    )
    paragraph(
        draw, EDGE + 150, strip_top + 14, BRIEFS, FACES["briefs"],
        COLOURS["black"], PAGE - 2 * EDGE - 150, 26,
    )
    draw.line([EDGE, PAGE - 44, PAGE - EDGE, PAGE - 44], fill=COLOURS["hairline"], width=1)
    centred(
        draw, PAGE - 36, "Compiled from the day's headlines · One page, one day",
        FACES["folio"], COLOURS["faded"],
    )
    return image


def main():
    """Render the page and store it beside this script as entry.png."""
    target = Path(__file__).resolve().parent / "entry.png"
    build_page().save(target, format="PNG")
    return target


if __name__ == "__main__":
    main()
