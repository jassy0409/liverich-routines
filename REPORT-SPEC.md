# LiveRichMedia Model Report Spec — CANONICAL

This is the required format for ALL model report dashboards (mid-month and
end-of-month, every model). The reference implementations are:

- `outputs/shantal-monique_end-of-month_2026-06-30_v3.html` (end-of-month deep dive)
- `outputs/shantal-monique_mid-month_2026-07-15.html` (mid-month + Content Playbook)

Reproduce their look, depth, and behavior. Jassy approved this format on 2026-07-14.

## Non-negotiables

1. **ANIMATED — always.** Every report must animate:
   - Hero stat pills and KPI numbers count up (~1.7s, ease-out cubic).
   - Every canvas chart draws in via requestAnimationFrame with
     `e = 1 - (1-p)^3` easing (~1.1s). Charts re-animate on every tab switch.
   - Flow nodes and funnel steps stagger in (CSS `rise` / `grow` keyframes,
     ~0.12s delay per item).
2. **Deep dive, not surface.** OnlyFans Statistics / Creator Reports depth:
   every category (Messages, Tips, Posts, Streams, Subscriptions) gets its own
   section with real numbers, counts, averages, and vs-prior-period deltas.
   Include the statement table (category / gross / share / delta), top spenders,
   subscriber composition, geography, best-days analysis.
3. **"💡 The logic" box under every chart.** Explains in plain language what the
   visual means, what drives it, and what moves it. The models must be able to
   understand the WHY, not just see a pretty chart.
4. **Content Playbook is the closing analytical section** on every report:
   - Hero card: best go-live day + time window, derived from the account's own
     weekday-earnings pattern + audience geography (US evening prime).
   - 5–6 ranked recommendation cards. EVERY card ends with a
     `Source: <metric>` line citing the exact data it came from.
   - Chips: `urgent` (red) for decayed metrics, `working` (green) for
     momentum to protect.
5. **GROSS only.** All money displayed is gross. `getEarningsOverview` /
   statement data returns NET → gross = net ÷ 0.8. `getEarnings` `gross` field
   is authoritative. Never show net.
6. **Real API data only.** Pull fresh from the OnlyFans MCP each run. No
   placeholder series — if a daily breakdown chart is shown, the daily numbers
   must come from the API (e.g. `getSubscriberStatistics` for daily subs).
   Partial "today" bars render at 50% opacity and are labeled partial.
7. **Status pill** top-right: AHEAD / ON PACE / BEHIND vs the monthly goal
   pace (goal × days-elapsed ÷ days-in-month). Green ≥100% of pace,
   amber 90–99%, red <90%. BEHIND reports get an action-plan emphasis;
   AHEAD keeps a light verdict.

## Design system — "Apple dark, girly mode"

- Base tokens: bg `#000`, cards `#1C1C1E` / `#2C2C2E`, separators
  `rgba(84,84,88,.36)`, text `#F5F5F7` / `#AEAEB2` / `#8E8E93`.
- Accents: rose `#FF6FA5`/`#F0518A`, lavender `#C9A0FF`/`#9B6EF0`,
  mint `#2FD9C3`/`#0AA592`, gold `#E8C170`/`#B0802C`.
  Hero gradient `linear-gradient(135deg,#FF6FA5,#C9A0FF)`.
- Chart categorical palette (CVD-validated, keep order):
  `#F0518A, #9B6EF0, #0AA592, #B0802C`.
- Frosted sticky topbar (blur 20px sat 180%), blurred rose/lavender orbs
  behind the hero, gradient-highlighted word in the H1, pill nav (sticky),
  20px-radius cards, 100px pill buttons, SF/-apple-system type,
  SF Mono for footers/labels.
- Semantic: green `#30D158`, amber `#FF9F0A`, red `#FF3B30` — reserved for
  status/deltas, never used as series colors.
- Pin dark mode: `<meta name="color-scheme" content="dark">` +
  `data-theme="dark"` on `<html>`. Responsive (grids collapse ≤680px),
  no horizontal scroll, `:focus-visible` gold outline.
- Hover tooltips on every canvas chart (crosshair value readout).
- Charts: rounded bar tops (4px), gradient fills, glow (shadowBlur) on
  hero lines, 2px surface gaps between donut segments, dashed gold pace line.
- Footer: mono uppercase `LiveRichMedia · <Model> · <Report> · <Period> ·
  gross figures (net ÷ 0.8)`.

## Section order

End-of-month: Overview · Earnings · Messages · Tips · Fans & Subs · Reach ·
Top Spenders · Content · Revenue Engine · Content Playbook · Verdict.

Mid-month: Overview · Earnings · <biggest-mover alert tab> · Reach & Fans ·
Best Days · Content Playbook · Verdict.

Karina reports: same structure with VIP / Free split pills throughout and a
combined view; BEHIND months render the action plan as flowchart steps.

## Copy rules

No word "tap" (use click/choose). No dashes in fan-facing copy. Emojis at line
ends or as list badges only. Top-spender names: first name + VIP tag +
location only — strip internal chatter notes. Never reproduce explicit thread
content.

## Delivery per run

1. Save to `/mnt/user-data/outputs/` and `outputs/` (repo), named
   `<model>_<report-type>_<YYYY-MM-DD>.html`.
2. Verify by rendering (Playwright screenshot every tab; zero console errors)
   before sending.
3. Commit + push to the designated branch.
4. Slack text summary to the model's team channel; PushNotification to Jassy.
