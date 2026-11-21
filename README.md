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

- **Lead story — Markets:** Bitcoin crashes below $60,000 — down 10% in a
  day, its lowest since September 2024, with nearly $2.4B in leveraged
  bets wiped out.
- **Sport:** Formula 1 under the lights in Las Vegas — Verstappen on pole
  for the night's 50-lap race on the Strip (a race-night preview; the
  race had not run yet).
- **United Nations:** the Geneva "killer robot" talks end in a weak deal —
  rules on autonomous weapons pushed to 2028, no binding ban.
- **Climate:** COP31 talks in Antalya run past deadline, deadlocked over
  fossil fuels.
- **Middle East:** Houthi missiles aimed at Riyadh intercepted — the third
  night running.
- **Also today:** a 6.7 quake shakes central Peru, and a fire at the
  Hartha power station in Basra kills at least 4.

## Date verification

Each story was checked against independent reporting before rendering;
the event date below is the date of the event / first report, per the
competition rule (an event of 21 November 2026 in any time zone):

| Story | Event date | Evidence |
|---|---|---|
| Bitcoin below $60,000 | Sat 21 Nov 2026 | CoinGecko 06:06 UTC 21 Nov: $55,684, −9.96%/24h, lowest since Sept 2024; liquidations $1.76B (BeInCrypto) to ~$2.4B (CryptoPotato, The Defiant) — bitcoinfoundation.org, trustscrypto.com |
| F1 Las Vegas GP | Race night Sat 21 Nov 2026 | Race Sat 21 Nov 20:00 PST, 50 laps, Las Vegas Strip Circuit; Verstappen pole after Antonelli's 5-place grid penalty — Reuters 21 Nov, formula1.com |
| UN "killer robots" | Sat 21 Nov 2026 | CCW talks in Geneva end ~03:00 GMT Sat in a non-binding deal; two-year mandate to elaborate rules by 2028 — Reuters 21 Nov |
| COP31 overtime | Sat 21 Nov 2026 | Closing plenary suspended Fri 22:29 local; third draft and talks continue Saturday — AP / TBS News, The Climate Watch |
| Houthi missiles at Riyadh | Early Sat 21 Nov 2026 | Saudi-led coalition intercepts 3 ballistic missiles, third night running — Reuters 21 Nov |
| Peru quake (ticker) | 00:09 GMT Sat 21 Nov 2026 | M6.7, central Peru; 19:09 Fri local = 00:09 GMT Sat — AP, China Daily |
| Basra fire (ticker) | Sat 21 Nov 2026 | Fire at Hartha power station kills at least 4, injures 30 — Reuters, dateline Basra, Nov 21 |

## Fix note

The first build of this entry failed independent verification on
21 Nov 2026 (~15:25 WIB): 5 of its 8 stories (the Russia-strikes lead,
the S&P 500 rout, the UK–EU deals, the pancreatic-cancer pill ticker
item and the Gen Z protests ticker item) were events of **20 November**,
not the 21st. All 5 were replaced with the verified 21 November stories
above; the COP31, Houthi and Peru stories passed verification and were
kept. An even earlier draft's ICJ Myanmar ruling had already been
dropped for the same reason: it was delivered on 19 November.

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
