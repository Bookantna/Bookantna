# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

GitHub profile README for `Bookantna` (Thanawat Ueasiripracha). Lives at `github.com/Bookantna/Bookantna`. The `README.md` at root renders on the GitHub profile page.

## Owner

- **Name:** Thanawat Ueasiripracha
- **GitHub:** Bookantna
- **Personal email (use for git):** phakamatg@gmail.com
- **Git identity:** `git config user.name "Thanawat Ueasiripracha"` + `git config user.email "phakamatg@gmail.com"`

## Structure

- `README.md` — the entire profile page (single file)
- `docs/superpowers/specs/` — design spec
- `docs/superpowers/plans/` — implementation plan

## Sections in README

1. Animated header — `readme-typing-svg.demolab.com`
2. Skills badges — `shields.io` (Languages, ML/Data, Tools, Databases)
3. GitHub Streak card — `streak-stats.demolab.com` (only stats card kept; github-readme-stats.vercel.app was broken)
4. Projects table — Screenie, Flower-Image-Colorization, ticketDorm, Multiprocessing
5. Footer — LinkedIn, email, GitHub badges

## Common tasks

```bash
# Edit and push
git add README.md
git commit -m "..."
git push
```

## Known issues

`github-readme-stats.vercel.app` public instance is rate-limited — stats and top-langs cards removed. Only streak card remains. Fix: deploy own instance of `anuraghazra/github-readme-stats` to Vercel with `PAT_1` env var, then update URLs in README.
