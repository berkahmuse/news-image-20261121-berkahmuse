# One Day on Earth — 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/berkahmuse/news-image-20261121-berkahmuse/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/berkahmuse/news-image-20261121-berkahmuse/reward.svg)](https://make.fun/c/news-image-20261121)

A program that writes one image summing up the world's news of
**Saturday 21 November 2026**, built for make.fun's
[news-image-20261121](https://make.fun/c/news-image-20261121) competition
("Sum up 21 November's world news in one image", $100 shared by the top 50).

## The image

A newspaper front page, drawn programmatically with Pillow (`render.py`):

- **Lead story — War in Europe:** Russia's biggest strikes of the war on
  Ukraine — 400+ drones and 110 missiles overnight, at least 8 dead in Kyiv —
  and missiles landing in Poland, which Warsaw called a deliberate provocation.
- **Markets:** the AI sell-off — S&P 500 −3.7% into correction, Nasdaq erasing
  its 2026 gains.
- **Europe:** the UK and EU sign their biggest post-Brexit deals (food trade,
  carbon markets, youth mobility for 100,000).
- **Climate:** COP31 talks in Antalya run past deadline, deadlocked over
  fossil fuels.
- **Middle East:** Houthi missiles aimed at Riyadh intercepted — the third
  night running.
- **Also today:** a 6.7 quake shakes central Peru, a pancreatic-cancer pill
  shows hope in trial, and Gen Z protests sweep 25 countries.

Every story was verified as an event of 21 November 2026 from multiple
independent news sources (BBC, Reuters, Al Jazeera, Financial Times,
Guardian). An earlier draft's ICJ Myanmar ruling was dropped after checking:
the ruling was delivered on 19 November, not the 21st.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the pre-rendered
`entry.png` to `/output/entry.png`. It is deterministic — two runs write
byte-identical files — and uses no network. `render.py` regenerates
`entry.png` from scratch (Pillow + DejaVu fonts, local only).

Output: PNG, 1024×1024, ≤ 1 MiB.

## License

MIT — see [LICENSE](LICENSE).
