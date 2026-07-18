# Project instructions

## Gameplan dashboards — publishing rules (MANDATORY)

Every gameplan / dashboard / team board built for a model MUST be published
as a public GitHub Pages file, never as a claude.ai artifact link (org
settings block "anyone with link" sharing on artifacts, so those links
require access and the chatters can't open them).

How to publish:
1. Build the dashboard as a self-contained HTML file (dark ops-hub style,
   sidebar sections — match the existing gameplan-*.html files).
2. Commit it to the branch `claude/onlyfans-chat-guide-070tsw` named
   `gameplan-<model>-<topic>.html` (this branch auto-deploys to GitHub
   Pages via .github/workflows/pages.yml).
3. Share the public URL:
   `https://jassy0409.github.io/liverich-routines/gameplan-<model>-<topic>.html`
   — this link opens for anyone, no login.
4. Also send the HTML file to Jassy as a downloadable attachment.

⚠️ WARNING: pages.yml also triggers on pushes to `main` and deploys the
entire checkout — pushing to `main` (which has no HTML files) would WIPE
the live Pages site. Never push to `main` while that trigger exists.

## Design system — JASSY'S DESIGN

All UI, web pages, and visual work in this project must follow Jassy's
Design in `design/jassys-design.md` — Apple's design language restyled in a
soft, feminine, girly aesthetic. Read that file before doing any design
work. Key points:

- Typography first: SF Pro stack, headlines semibold (600) or bolder,
  negative letter-spacing on large type. One serif-italic accent word
  allowed per hero headline.
- Colors: creamy white #FFFBFC / blush #FBF3F6 / soft lavender #F7F4FB
  backgrounds; warm plum dark mode #1A1418 / #241C22; text #2B2228 /
  #8E7F88 (light) and #FBF3F6 / #D9CCD4 (dark); accent pink #E0407B
  (#FF8AB8 on dark).
- Rose-gold (#E8A87C → #E0407B) or pink-lavender (#FF8AB8 → #A78BDB)
  gradients on hero words only.
- Pill buttons (border-radius 980px, pink primary), cards with 28–32px
  radius and pearly surfaces, concentric nested corners.
- No chips/badges, no sparkles/hearts/glitter/script fonts; hierarchy from
  type weight and size, not decoration. Pink is the accent, not the
  wallpaper.
- Generous asymmetric section padding, soft reveal-on-scroll and
  hover-scale motion.

Before shipping any screen, run the review checklist in Part 10 of
`design/jassys-design.md`.
