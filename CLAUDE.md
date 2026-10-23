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

Concept: the profile is a comic book, "The Amazing BOOKANTNA, Season 2 #01". Season 1 was the Seagate internship (ended Oct 2026); the retired hard drive is now the hero's sidekick. Every panel is a hand-inked, animated SVG: newsprint paper (`#f4ecd6` / `#fffaf0`), ink (`#1d1a16`), and two process colors only, red (`#e4432d`) and yellow (`#f7c548`). Halftone dot patterns for shading, thick ink outlines, Bangers for titles/SFX, Comic Neue for lettering, Geist Mono for nerdy data labels. No emoji, no third-party badge or stats services.

## Structure

- `README.md` — HTML only: stacks the SVG panels, wraps episode cards in links
- `src/*.svg` — panel templates (edit these, never `assets/`)
- `assets/*.svg` — build output, committed so GitHub can serve it
- `scripts/build.py` — embeds subset fonts as base64 WOFF2 (`/*FONTS*/`; only families named in the file's `<style>`), expands `{{BARCODE}}`, `{{BURST cx cy rIn rOut points seed}}` (comic starburst path), `{{RAYS cx cy rIn rOut count seed}}` (speed lines) and the activity placeholders in `health.svg`
- `scripts/fetch_activity.py` — pulls the last 52 weeks of contributions into `data/activity.json`
- `scripts/fonts/` — Bangers, Comic Neue, Geist, Geist Mono + OFL licenses
- `.github/workflows/activity.yml` — daily: fetch activity, rebuild, commit

## Panels (in README order)

1. `header.svg` — comic cover: masthead, masked hero in glasses, HDD sidekick, real Code 128 barcode for "BOOKANTNA", "Seagate arc complete" burst
2. `origin.svg` — "Previously on..." four-panel origin strip (KKU at 2 a.m., Seagate arc, arc complete, Season 2)
3. `stack.svg` — trading card + "Powers & gadgets" skill chips
4. `health.svg` — current quest + "training montage" halftone contribution map (generated)
5. `tracks.svg` + `track-*.svg` — projects as episodes; row widths 59% / 40% keep 708x320 and 480x320 cards the same height
6. `link-*.svg`, `eof.svg` — "letters page" contact + "The end?" footer

## Common tasks

```bash
# after editing anything in src/
python scripts/build.py          # needs: pip install fonttools brotli

# refresh contribution data locally
GITHUB_TOKEN=$(gh auth token) python scripts/fetch_activity.py && python scripts/build.py
```

Preview: open `preview.html` (copy of README in a GitHub-like shell). SVGs animate only when visible; Chrome pauses offscreen `<img>` SVG animations, so full-page screenshots show start states.

## Notes

- `github-readme-stats` and `streak-stats` were dropped (rate limits, off-brand fonts); `health.svg` replaces them.
- Optional `PROFILE_PAT` secret (scope `read:user`) makes the workflow count private contributions.
