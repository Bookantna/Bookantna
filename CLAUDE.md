# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

GitHub profile README for `Bookantna` (Thanawat Ueasiripracha). Lives at `github.com/Bookantna/Bookantna`. The `README.md` at root renders on the GitHub profile page.

## Owner

- **Name:** Thanawat Ueasiripracha
- **GitHub:** Bookantna
- **Personal email (use for git):** phakamatg@gmail.com
- **Git identity:** `git config user.name "Thanawat Ueasiripracha"` + `git config user.email "phakamatg@gmail.com"`

## Design

Concept: the profile is a hard-drive datasheet (nod to the Seagate internship). Every panel is a hand-written, animated SVG on a dark chassis (`#121211`), one amber accent (`#e2a03f`), paper label (`#ece7dc`), set in Geist / Geist Mono. No emoji, no third-party badge or stats services.

## Structure

- `README.md` — HTML only: stacks the SVG panels, wraps project cards in links
- `src/*.svg` — panel templates (edit these, never `assets/`)
- `assets/*.svg` — build output, committed so GitHub can serve it
- `scripts/build.py` — embeds subset Geist fonts as base64 WOFF2 (`/*FONTS*/`), expands `{{BARCODE}}` and the activity placeholders in `health.svg`
- `scripts/fetch_activity.py` — pulls the last 52 weeks of contributions into `data/activity.json`
- `scripts/fonts/` — Geist variable TTFs + OFL license
- `.github/workflows/activity.yml` — daily: fetch activity, rebuild, commit

## Panels (in README order)

1. `header.svg` — drive label (name, specs, real Code 128 barcode for "BOOKANTNA") + spinning platter with seeking arm
2. `stack.svg` — skills as a partition table
3. `health.svg` — SMART-style status + contribution "sector map" (generated)
4. `tracks.svg` + `track-*.svg` — projects; row widths 59% / 40% keep 708x300 and 480x300 cards the same height
5. `link-*.svg`, `eof.svg` — contact + footer

## Common tasks

```bash
# after editing anything in src/
python scripts/build.py          # needs: pip install fonttools brotli

# refresh contribution data locally
GITHUB_TOKEN=$(gh auth token) python scripts/fetch_activity.py && python scripts/build.py
```

Preview: SVGs animate only when visible; Chrome pauses offscreen `<img>` SVG animations, so full-page screenshots show start states.

## Notes

- `github-readme-stats` and `streak-stats` were dropped (rate limits, off-brand fonts); `health.svg` replaces them.
- Optional `PROFILE_PAT` secret (scope `read:user`) makes the workflow count private contributions.
