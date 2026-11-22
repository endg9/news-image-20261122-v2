# THE WORLD IN ONE DAY — 22 November 2026

[![make.fun competition](https://img.shields.io/badge/make.fun-news--image--20261122-blue)](https://www.make.fun/c/news-image-20261122)
[![Prize $100 top-50](https://img.shields.io/badge/prize-%24100%20top--50-green)](https://www.make.fun/c/news-image-20261122)
[![Deadline 24 Nov 2026](https://img.shields.io/badge/deadline-24%20Nov%202026%2000%3A00%20UTC-orange)](https://www.make.fun/c/news-image-20261122)

Entry for the [make.fun competition **news-image-20261122**](https://www.make.fun/c/news-image-20261122)
— *"Sum up 22 November's world news in one image"* ($100 USDC, top 50).

## The image

`entry.png` (1024×1024) sums up Sunday 22 November 2026 in one picture:
4 lead stories, 26 briefs, a "still to come" timeline of the day's remaining
events, and a DATE CHECK box listing older stories deliberately excluded.
Every story happened or was first reported on 22 November 2026; events that
had not happened at render time are labelled **PREVIEW** — no result is invented.

## How it runs

`compose.py` renders `entry.png` (PIL, standard library + Pillow at build time;
the shipped `entry.png` is the rendered image). `main.ts` copies it to the
grader output directory:

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png, exit 0
```

`main.ts` creates the output directory first (`mkdirSync(..., {recursive: true})`)
and resolves the source image by absolute path, so it works from any cwd and
with a not-yet-existing output directory.
