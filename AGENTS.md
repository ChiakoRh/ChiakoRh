# AGENTS.md

## What this repo is

- GitHub profile README for user **ChiakoRh** (`ChiakoRh/ChiakoRh`). `README.md` renders on https://github.com/ChiakoRh.
- No build, no tests, no lockfile. Verification = open the SVGs in a browser locally, or push and check the profile page.
- The user communicates in Persian (RTL); code, paths, and English terms stay LTR.

## Gotchas

- README uses raw HTML blocks (`<p align>`, `<table>`) inside Markdown. GitHub strips `<script>`, CSS `style` attributes and some tags — don't rely on them.
- Visuals come from external SVG services (readme-typing-svg.demolab.com, github-readme-stats.vercel.app, capsule-render.vercel.app, shields.io, komarev). A broken image is usually the service flaking, not the repo.
- `github-readme-streak-stats.herokuapp.com` is dead — the live host is `streak-stats.demolab.com`.
- `api.github.com` is unreliable from Iran. `scripts/generate-cards.py` falls back to the cached `scripts/repos.json` locally; GitHub Actions runners always have API access and refresh the cache.

## Profile design (agreed decisions)

Style reference: https://github.com/yappologistic/yappologistic (hand-made SVG assets + CI-generated cards).

- **Theme (user's choice):** the yappologistic monochrome theme — bg `#121212`, surface `#181818`, border `#2b2b2b`, fg `#f2f2f2`, text2 `#b4b4b4`, text3 `#8c8c8c`, accents red `#e0525b` and gold `#e8c46a`. Dark-only. (A Tokyo Night palette was tried first and replaced.)
- `assets/` = hand-written SVGs (hero, CTA buttons, section headers, footer). SVGs are plain text — edit them as files, no image generator needed.
- `scripts/generate-cards.py` regenerates `output/card-*.svg` (featured, big) and `output/mini-*.svg` from repo metadata. Generated SVGs are committed to `main`; don't treat them as dirty-file noise after a workflow run.
- `.github/workflows/snake.yml` (Platane/snk) publishes the contribution snake to the `output` branch.
- Featured big cards: **WSK**, **BPB-Scan**. Mini cards: RemGodCatcher, KKDA, KHP, KAL.
- **Never display fork repos on the profile.** Forks excluded: BPB-Wizard, BPB-Worker-Panel, persiterm, Scheme-Size_V158, Unlimited-Armament-Works, v2ray-config-modifier.
