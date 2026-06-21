> **⚠️ Project archived — no longer maintained**
>
> The live site at debateclock.org has been taken offline.
>
> **Traffic before closing:** 69 clicks, 3.6K impressions. Real timer sessions in 41 countries. ChatGPT referrals were growing weekly.
>
> This code is MIT licensed. Feel free to fork, self-host, or continue development. No permission needed.

# DebateClock

Free browser-based debate timer with prep pool tracking, two-device sync, and support for all major competitive debate formats.

## What it was

A single-page debate timer used in competitive rounds and practice sessions across 41+ countries. Vanilla HTML/CSS/JS — no build step, no framework, no backend.

**Features:**
- 9 debate formats preloaded: Lincoln-Douglas, Policy (CX), Public Forum, Parliamentary, World Schools (WSDC), British Parliamentary, Asian Parliamentary, Canadian Parliamentary (CUSID), plus a custom format option
- Independent prep pools per debater with shared-pool tracking
- Two-device udge controls a phone, debaters watch a clean full-screen countdown on a laptop
- POI window indicators for parliamentary formats (1:00–6:00 for BP/Asian/CUSID, 1:00–7:00 for WSDC)
- Practice tools: motion timer, random motion generator (150+ motions), extemp prep room, practice round logger with CSV export, flow timer, tournament schedule countdown
- Format reference guides, long-form blog content, judge paradigm setup guide

## Stack

- Vanilla HTML, CSS, JavaScript — no build pipeline
- Hosted on Vercel with automatic deploy on push to main
- Fully static site, no backend, no database
- Optional Umami analytics integration (self-hosted)

## Self-hosting

```bash
git clone https://github.com/metriclogic26/debateclock.git
cd debateclock

# Serve locally — any static server works
python3 -m http.server 8000
# or
npx serve
```

For production, connect this repo to any static host: Vercel, Netlify, Cloudflare Pages, GitHub Pages, S3 + CloudFront, Nginx, Caddy. No special configuration required.

If youmi analytics, replace the `data-website-id` value in each HTML file's `<script defer src="https://cloud.umami.is/script.js" ...>` tag with your own site ID, or remove the script entirely.

## Project structure
/

├── index.html              # Homepage

├── app/                    # Two-device timer (the main tool)

├── timer/                  # Per-format informational + entry pages

├── formats/                # Format reference guides

├── practice/               # Practice tools (motion, flow, round logger, etc.)

├── blog/                   # Long-form content

├── setup/                  # Tabroom paradigm setup guide

├── terms/                  # Privacy policy and terms

├── assets/                 # Shared CSS, fonts

└── sitemap.xml

## License

MIT. Use it however you want.

## Acknowledgements

Built 2024–2026. Used in real competitive debate rounds across 41+ countries by debaters, judges, and coaches who needed a free timer that jus

If you fork this and continue the project, that would be wonderful — no obligation, just a hope that someone in the debate community picks it up.
