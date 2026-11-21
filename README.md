# Sum up 21 November's world news in one image

Entry for the make.fun bounty `news-image-20261121`.

## What the entry does

`main.py` (Python standard library only) copies the bundled
`entry.png` to the output directory as `entry.png`. The output is a
byte-for-byte copy, so repeated runs write identical bytes. No network.

- Image: PNG, 1024 × 1024, under 1 MiB

## The image

A newspaper front page, "THE WORLD IN ONE PAGE", dated
**Saturday, November 21, 2026** (in large red text), with four panels
and a bottom strip:

1. **War in Europe** — Russian missiles land in Poland; NATO calls it a
   violation as Russian strikes hit Kyiv again overnight.
2. **Middle East** — Trump weighs new strikes on Iran; Tehran asks for
   diplomacy, Washington calls its terms unacceptable.
3. **Markets** — Stocks slide: S&P 500 falls 3.7%; Anthropic's $2 trillion
   stock-market debut stumbles as AI shares slide.
4. **Tech & Law** — UN opens path to a 'killer robot' pact; negotiators
   in Geneva open the way to global rules by 2028.

Also today: COP31 climate talks go into overtime over fossil fuels;
USDA & FBI breached by hackers; Honda & Toyota recall 1.6 million cars;
Mexico captures a cartel kingpin.

Stories are the day's headlines as reported on 21 November 2026 by
The Japan Times, the South China Morning Post and the New York Times
headline roundups.

## How the image was made

`render.py` draws the page programmatically (Pillow, Liberation fonts):
masthead, a large red date line, four ruled panels with a simple icon
each (missile, target, falling chart, robot), and an "ALSO TODAY" strip.
It is deterministic — fixed layout and fonts, no randomness or clock.
`entry.png` in this directory is its output.
