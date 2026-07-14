# STYLING GUIDE — LiveRichMedia Chatter Playbook design system

Build every page as a self-contained HTML file (or link the shared playbook.css).
Always pin dark mode: right after `<title>`, add
`<meta name="color-scheme" content="dark">` and
`<script>document.documentElement.setAttribute('data-theme','dark');</script>`
Pages must be responsive (mobile-first, max-width wrapper, no horizontal scroll)
and keyboard-accessible (visible `:focus-visible` outline in the accent gold).

THERE ARE TWO LOOKS — pick by page type:

════════════════════════════════════════════════
## LOOK A — "Apple dark" (modules, exams, hubs, manager guides)
════════════════════════════════════════════════

Feel: iOS settings app meets a premium landing page. Frosted glass, soft
depth, pill shapes, SF typography.

Tokens (dark):
- background `#000000`, secondary `#0B0B0D`
- card `#1C1C1E`, card-2 `#2C2C2E`
- separators `rgba(84,84,88,.36)`
- text `#F5F5F7`, soft `#AEAEB2`, faint `#8E8E93`
- accent gold `#E8C170`, deep gold `#D9B26A`, gold wash `rgba(232,193,112,.16)`
- iMessage blue `#1E8CFF` → `#0A74E6` (chat bubbles only)
- semantic: green `#30D158`, amber `#FF9F0A`, red `#FF3B30`

Type: -apple-system / SF Pro stack. H1 700 weight, `clamp(40px,8vw,68px)`,
letter-spacing -0.03em, one word highlighted with a gold gradient
(background-clip:text). Body 17px/1.5. Uppercase gold eyebrows 13px/600.
SF Mono for data labels.

Components:
- Sticky frosted topbar: `blur(20px) saturate(180%)`, brand "LiveRichMedia ·
  Playbook" with gold accent word, a status pill on the right (red pill
  labeled "Managers Only" on manager pages).
- Hero: centered, blurred gold "orb" radial glows behind, stat pills row.
- Cards: 18px radius, 1px separator border, subtle shadow.
- Chat examples as iMessage bubbles: grey incoming (`#3A3A3C`), blue-gradient
  outgoing, red-gradient for "don't do this" examples, 10px uppercase mono
  who-labels, bottom-corner radius 5px on the tail side.
- Optional full iPhone mockups: 44px-radius device frame, Dynamic Island,
  status bar (9:41, signal/battery SVGs), contact header with avatar,
  thread, input bar, "Delivered" tag.
- Numbered/starred rule lists: 24px gold-wash circular badges.
- Callouts: card with emoji + bold title + soft body.
- Radio options as tappable rows: 1.5px border, custom 22px dot, gold
  border + gold-wash fill when selected.
- Buttons: gold gradient pill, dark text (`#2a1e08`), 14px radius; ghost
  variant with card background + border.
- Score ring: SVG circle, stroke-dasharray progress, green if passed /
  amber if not, big number centered.

════════════════════════════════════════════════
## LOOK B — "LRM dark dashboard" (training manual, performance review, scorecard-style pages, gameplan dashboards)
════════════════════════════════════════════════

Feel: the LRM scorecard GIF — luxury dark, champagne gold, editorial serif.

Tokens:
- ground `#100E0A`, panel `#18140D`, panel-2 `#1F1A11`
- lines `#2C2519` / `#221D14`
- text (warm ivory) `#F0E9DA`, soft `#B8AD97`, faint `#8A7F6B`
- champagne gold `#D9B26A`, deep `#B48F49`, rose accent `#CD8598`
- scoring: green `#74C08C`, amber `#E0A44A`, red `#DE7676`
- (score colors follow the house rubric: >=80% green, 65-79% amber, <65% red)

Type: serif display (Iowan Old Style / Palatino stack, Liberation Serif
fallback on Linux render boxes) for H1/H2 at 600 weight, one word italic in
gold; system sans body 17px/1.6; SF Mono (DejaVu Sans Mono fallback) for
kickers with 0.24-0.28em letter-spacing, uppercase, gold.

Components:
- Header with faint gold radial glow, mono kicker line
  ("LIVERICHMEDIA · ..." with real middle dots ·).
- Giant serif score number (80px+) colored by the scoring rubric.
- Thin horizontal score bars (10px, 6px radius) green/red per item.
- Panels: 14px radius on `#18140D` with `#2C2519` border.
- Gold-left-border "flow" quote blocks for example chat lines.
- Status pills: mono 11px, colored border + 10% wash (red "you answered X",
  green "correct Y").
- Include/exclude targeting tags on gameplan dashboards: mono 11px, 8px
  radius, green border+wash for include, red for exclude, gold for lists.
- Gold-wash callouts with mono uppercase titles.
- Mono uppercase footer: "LIVERICHMEDIA · CHATTER PLAYBOOK · ..." with
  middle dots.

════════════════════════════════════════════════
## Shared rules
════════════════════════════════════════════════

- Wrapper max-width 760-920px, 22-24px side padding.
- Sections separated by generous padding (44-60px) and hairline borders.
- Emojis are used as functional icons (🎙 voice, 📘 coaching, 📊 review,
  🔒 managers only) — at line ends or as list badges, never mid-sentence noise.
- Never use the word "tap"; say click/choose. No dashes in fan-facing copy.
- Chat example content must respect house voices (Shantal: proper sentences,
  first names, never "hey", no pet names / Karina VIP: lowercase bratty /
  Karina Free: lowercase softer) and house rules (on-platform only, no
  guilt-tripping, deliver what you promise). No repeated captions across
  gameplans. No "thinking about you" on a mass.

## Rendering to JPG

Use `render_dashboard.js` (Playwright, Chromium at
`/opt/pw-browsers/chromium-*/chrome-linux/chrome` on render boxes):

```
NODE_PATH=/opt/node22/lib/node_modules node render_dashboard.js in.html out.jpg
```

960px viewport, full-page screenshot, JPEG quality 92. Deliver both the JPG
(for Slack drops) and the HTML (source of truth).

`dashboard_template.html` in this repo is the LOOK B gameplan starting point:
hero + stat row, one panel per shift (chatter/shift/time, tone pill, paid
mass with folder + targeting tags, caption quote blocks, bump), numbered
team rules, and the managers-only escalation callout.
