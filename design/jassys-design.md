# JASSY'S DESIGN

Jassy's personal design system: Apple's design language — Liquid Glass,
concentric corners, typography-first hierarchy, measured Apple.com specs —
reimagined in a soft, feminine, girly style. Blush pinks, lavender, rose
gold, and creamy off-whites replace Apple's grays and blues, while every
structural rule of the Apple system stays intact. Give this to any designer
or AI assistant and ask for work "in Jassy's Design."

**The vibe in one line:** an Apple keynote page that grew up on rose gold —
clean, luxurious, airy, and unmistakably feminine, never cluttered or cutesy.

How to use it: read Part 1 for the why, Part 2 for the hard rules, Parts 3–8
for the system detail, Part 9 for Apple.com-style marketing pages, and Part 10
as a final checklist before shipping any screen.

---

## Part 1 — The eight design principles (the WHY layer)

Design is making something with intention. Every feature asks for someone's
time, attention, and trust — choosing what to build is often deciding what NOT
to include. Principles can pull against each other; judgment picks the path.

**1. Purpose.** Before a sketch or a line of code, ask whether the thing has
purpose. Focus on what matters most to the person so you build something they
truly value.

**2. Agency (and forgiveness).** Put people in control. Offer choices; never
force a predetermined path. Freedom means mistakes, so offer forgiveness: easy
undo for anything, double-check destructive actions. Interrupt carefully, and
only when someone is about to make a big mistake.

**3. Responsibility.** Privacy is a human right: ask for personal data at the
right moment, only what's necessary, and say what it's for. Never wall the app
off behind launch-time permission prompts. For every feature ask: how could
this be misused, who could be harmed, how do I prevent it? For AI features,
anticipate wrong or unexpected output — add previews, confirmations,
disclaimers, and remove the feature entirely if the risk outweighs the value.

**4. Familiarity.** Build on what people already know. Metaphors must be
neither too literal nor too abstract — a good one lets people PREDICT what it
does. Trash means delete; never bend a known symbol to a new meaning. Things
that look the same must behave the same, in the same placement across screens
and devices.

**5. Flexibility.** People use your design in contexts as unique as they are.
Each device deserves its strengths: phone is quick touch interactions; desktop
is deep workflows and precise pointer control. Cater to the range of abilities
— age, language, novice vs pro, accessibility needs. When no single layout
fits everyone, let people personalize.

**6. Simplicity.** Simple is NOT minimal. Burying functionality in one place
looks minimal but isn't simple. Simple = frictionless. Concise: plain
language, no jargon, fewer steps. Clear: hierarchy from order, spacing, and
contrast — the most important item on screen is always the most OBVIOUS one.
Answer three questions: what do I pay attention to, what can I interact with,
how do I interact. Sometimes simpler means ADDING context.

**7. Craft.** Craft is the detail that tells people you care. Laggy buttons,
jittery scroll, misaligned icons, and layouts that break on rotate make people
doubt the RESULTS your product gives them. Quality materials: beautiful fonts,
colors that adapt to light and dark, clear iconography, fluid animation.

**8. Delight.** Not confetti, not flourishes tacked on at the end. Pick the
EMOTION you want people to feel and reinforce it through the design. Delight
is the sum of getting all the other principles right.

---

## Part 2 — The ten rules that matter most

1. **Liquid Glass is a functional layer floating ABOVE content. Never apply it
   to content itself.** Controls, bars, and overlays get glass; photos, text
   documents, video, and feeds never do.

2. **Apply the material directly to the control, and layer text and controls
   above the glass** — otherwise the lensing distorts them.

3. **Hierarchy comes from layout and grouping, not decoration.** The UI should
   feel spatial yet grounded.

4. **Menus and dialogs spring from the action that triggered them**, not from
   a detached screen edge. Confirmations appear at the button you tapped.

5. **Interrupting task = glass + dimming layer. Parallel task = glass alone.**
   If the user must stop and decide, dim behind the surface. If they keep
   working alongside it, glass separation alone keeps things clear.

6. **Concentric corners everywhere.** Nested shapes share a center; inner
   radius = outer radius minus inset. Capsules are naturally concentric. If a
   corner feels pinched or flared, the radii don't share a center.

7. **Clean up your bars.** Group actions by function. One symbol introduces a
   group, text does the rest. Never repeat or tweak icons. Never group a
   symbol button and a text button in the same container. Primary action stays
   separate and tinted. Secondary actions go in a More menu.

8. **Define a shared anatomy and reuse it.** Selection indicator, icon, label,
   accessory — the same pieces in familiar placements across sidebars, tab
   bars, menus, and tables, scaling across devices rather than being rebuilt.

9. **Scroll edge effects are functional, not decorative.** They replace hard
   dividers with a subtle blur that keeps bars legible. Content scrolls
   beneath bars and behind sidebars by default.

10. **Typography is bolder now, and left-aligned in key moments** like alerts
    and onboarding. Weight carries hierarchy, not color.

### Common mistakes to scan for before shipping

- **Chips.** Status pills, tag chips, filter pills, metric badges — text
  fragments in tiny rounded containers pretending to be data, settings, or
  buttons. Apple's system contains none: data gets typographic weight and
  color ON the words ("M3 Ultra" as gradient text, never a spec badge);
  contained content gets a real card with real imagery and one clear capsule
  button. Metrics are plain text, settings are dropdowns, actions are buttons,
  statuses are colored plain text.
- **Fake glass.** A flat gray translucent rectangle is not Liquid Glass. Glass
  is backdrop blur of REAL CONTENT behind it. If nothing sits behind the
  panel, restructure so content flows underneath (scroll behind bars,
  background extension).
- **Ignoring typography.** The system is typography first: weight and size
  carry hierarchy, gradients go ON hero words, menus can be plain text rows.
  If the design's personality isn't coming from the type scale, it's
  decoration — start over from the type.
- **Starving the content.** The canvas (timeline, feed, video) gets the room;
  controls consolidate into ONE panel on one side. Never shrink the content
  area to fit more control containers.

---

## Part 3 — Liquid Glass

**What it is.** A functional layer in the UI, floating above content, bringing
structure and clarity without stealing focus. It lenses: it bends and refracts
what is behind it in real time, with specular highlights and adaptive shadows.

**Where it goes:** toolbars, tab bars, navigation bars, floating controls,
sheets, menus, alerts, sliders, toggles, buttons in the control layer.
**Where it never goes:** content. Photos, video, documents, feeds, artwork,
reading surfaces.

**Applying it correctly.** Apply the material directly to the control. Layer
text and controls ABOVE the glass. Glass lifts controls off the background —
use that as permission to remove borders and boxes you were using to fake
separation.

**Interruption vs parallel.** A task that interrupts the main flow (a
confirmation, a destructive decision) pairs glass with a dimming layer. A task
that happens in parallel (a half-height panel over a map) uses glass alone.

**Focus shifts.** When focus deepens — the user drags a sheet upward — glass
subtly recedes: more opaque, gently larger. Depth of engagement is
communicated by the material, not by new chrome.

**Menus spring from the action.** Define the action SOURCE (the button) and
the action PRESENTATION (the menu or dialog) so the system animates one from
the other. Confirmations belong at the point of action.

**Sizing.** On desktop, mini/small/medium controls keep rounded rectangles;
large and extra-large controls use glass for emphasis in spacious areas. Glass
buttons are best for standout actions, not sprayed across every control.

---

## Part 4 — Shapes and concentricity

Corner geometry is a system, not a per-element choice.

**Three shape types:**
1. **Fixed** — a set corner radius that never changes.
2. **Capsule** — fully rounded ends; naturally concentric; the system leans on
   it for buttons, tabs, segments, and bars.
3. **Concentric** — the radius is DERIVED from the container: inner radius =
   outer radius minus the inset, so both curves share a center.

**Rules:**
- Nested shapes must share a center: a card inside a screen, artwork inside a
  card, a button inside a bar.
- Use a concentric shape WITH A FALLBACK radius for components that sometimes
  stand alone.
- Pinched = inner radius too small for its inset. Flared = inner radius too
  large. Fix the relationship, don't eyeball a new number.
- Near device edges, give components extra margin.

**Web/CSS translation:** inner radius = outer radius − padding between the two
boxes; clamp at a sane fallback (e.g. 12px) standalone. Never give a child a
LARGER radius than its parent minus the inset. Capsule = border-radius: 999px.

---

## Part 5 — Bars, symbols, and navigation

- If a bar feels crowded, cut. Group actions BY FUNCTION — related actions
  share one glass container; unrelated actions get their own.
- Secondary actions go in a More menu (ellipsis).
- The PRIMARY action (Done, Continue) stays separate and tinted.
- Use a symbol ONCE to introduce a group; let text do the rest. Never repeat
  or tweak icons. Never mix symbol buttons and text buttons in one container.
- When there's no clear pictorial shorthand (Select, Edit), a TEXT LABEL is
  the better choice.
- Tab bars support persistent features via accessory views (a mini player
  riding above the bar). Persistent only — never screen-specific actions.
- Bars are glass: content scrolls beneath them and stays subtly visible.
  Legibility comes from scroll edge effects, not opaque bars or divider lines.

---

## Part 6 — Components and continuity across devices

- **Shared anatomy:** a selection indicator, an icon/accessory, a title, a
  disclosure indicator. The same pieces in familiar placements across
  sidebars, tab bars, menus, and tables.
- **Structure components to scale.** The SAME component adapts across phone,
  tablet, and desktop. Tabs become a sidebar; a segmented control and a tab
  bar express the same selection with the same capsule language.
- **Support core interactions everywhere:** select, activate, drag, context
  menu — on touch, pointer, and keyboard. Never remove an interaction people
  already rely on when restyling.
- **Control sizes:** capsules for touch-friendly layouts; in dense desktop
  environments reserve them for standout actions.
- **Typography:** bolder, left-aligned in key moments (alerts, onboarding).
  Headlines semibold or bolder; never thin weights for large titles. Weight
  carries hierarchy, not color.
- **Color:** if your palette fights the glass material, adjust the palette,
  not the glass.

---

## Part 7 — Structure, scroll edge effects, and sidebars

Structure has four jobs: depict relationships, reflect navigation focus,
elevate controls, organize for legibility.

- **Depict relationships.** Surfaces show where they came from: a dialog
  springs from its button, a sheet rises over its context. Nothing teleports
  in from an unrelated edge.
- **Scroll edge effects** are the subtle blur/fade where content meets a bar,
  replacing hard dividers. Two styles — soft (default) and hard (mostly
  desktop, for pinned headers needing extra clarity). Never mix or stack them.
  One per scroll region; in split views each pane gets its own, kept
  consistent in height.
- **Sidebars are glass; content flows behind them.** Use the background
  extension effect so hero content reads full-bleed without hiding information
  under glass. Don't inset a scroll view to dodge the sidebar.
- **Layout skeleton:** background extension regions (top/bottom heroes) +
  scroll view(s) + a floating glass control layer. Content owns the full
  canvas; controls float.

---

## Part 8 — Search patterns

**The field's anatomy is sacred:** leading magnifying glass (never a brand
glyph), placeholder, clear button once text is entered, Cancel while focused.

**Two questions decide placement:** how do people navigate the app, and what
is the SCOPE? Placement sets the expectation of what's being searched.

**Phone placements:** bottom toolbar preferred (ergonomic; the field animates
up over the keyboard); top toolbar when the bottom is occupied; a Search tab
for tabbed apps (standard = landing page with suggestions; prominent = keyboard
instantly); inline under a section title for scoped search.

**Tablet/desktop:** toolbar trailing for split-view apps; sidebar top when
search filters the sidebar's own list; a dedicated search section for rich
multi-section apps.

**Best practices:** recent searches on focus (allow removal); predictive
suggestions with the typed part visually distinct; start broad and let people
narrow with a scope bar; search tokens live INSIDE the field as highlighted
query text and never replace visible filter UI; never a blank screen on zero
results — symbol, title, subtitle, and echo the search text so people catch
their own typos.

---

## Part 9 — Apple.com-style marketing pages (measured specs)

Captured from live Apple.com pages (home, iPhone Pro, Mac, iPad, Vision Pro,
TV & Home).

### Typography (the single most important rule)
Font: SF Pro Display (≥20px) / SF Pro Text (<20px), falling back to
-apple-system, "Helvetica Neue", Inter, Arial. Headlines are ALWAYS semibold
(600) on marketing pages, or bold (700) for immersive text-over-media
sections. Never thin or regular for big headlines. Large type uses NEGATIVE
letter-spacing; small type slightly positive.

**Jassy's accent type:** one elegant serif-italic word is allowed inside a
hero headline (New York italic, falling back to "Playfair Display", Georgia
italic) — e.g. "Made *beautifully* simple." Maximum one per section, hero
and closing sections only. Everything else stays SF Pro. No script or
handwriting fonts anywhere.

| Role | px | weight | line-height | tracking |
|---|---|---|---|---|
| Page-landing hero | 80 | 600 | 84 | −1.2 |
| Closing/feature headline | 64 | 700 | ~1.05 | −0.576 |
| Product hero | 56 | 600 | 60 | −0.28 |
| "Explore the lineup" | 48 | 600 | 52 | −0.144 |
| Section headline | 40 | 600 | 44 | normal |
| Immersive over-media | 36 | 700 | ~1.1 | normal |
| Sub-headline | 32 | 600 | 40 | +0.13 |
| Eyebrow / category label | 24 | 600 | 28 | +0.22 |
| Hero subhead | 28 | 400 | 32 | +0.20 |
| Card title | 28 | 600 | 32 | +0.20 |
| Body | 17–21 | 400 | ~1.4 | small+ |
| Caption / legal | 14 | 400–500 | 20 | normal |

### Color — Jassy's palette
- Light backgrounds: creamy white #FFFBFC and the signature blush
  #FBF3F6 (alternate sections, replacing Apple's #F5F5F7). Optional soft
  lavender section #F7F4FB for variety — never two tinted sections in a row.
- Dark backgrounds: deep plum-black #1A1418 or mauve-charcoal #241C22
  (replacing #000000 / #1D1D1F). Dark mode stays warm, never cold gray.
- Text on light: primary #2B2228 (warm near-black), secondary #8E7F88
  (mauve-gray).
- Text on dark: headlines #FBF3F6 (blush off-white, NOT pure white for large
  type), secondary #D9CCD4, emphasis rgba(255,240,246,0.92).
- Accents: link/CTA pink #E0407B (#FF8AB8 on dark). One accent eyebrow per
  section, used sparingly.
- Hero gradients (for gradient text ON key words only): rose gold
  #E8A87C → #E0407B, or pink-to-lavender #FF8AB8 → #A78BDB. Never gradient
  backgrounds behind body text.
- Rule of restraint: pink is the ACCENT, not the wallpaper. Most of the page
  is creamy white / blush; saturated pink appears only on CTAs, links,
  eyebrows, and hero gradient words.

### Spacing & layout
- Major sections: padding-top ~160px, padding-bottom ~216px; tighter sections
  ~114/160. Asymmetric (more bottom) is intentional.
- Text container max-width ~980px; full-bleed media wider (~1440px).
- Everything centered; group with whitespace, not borders or drop shadows.

### Components
- **Hero:** full-bleed product image; centered headline + one-line subhead;
  CTA pair (filled blue "Learn more" + outline "Buy"). Text in the top third.
- **Card:** rounded rect 28–32px radius; surface-color hierarchy (blush
  #FBF3F6 / soft lavender #F7F4FB / elevated dark plum / full-bleed photo)
  instead of borders; full-bleed image clipped by the corners; two-tone
  caption (blush-white key phrase + mauve-gray remainder). An optional
  1px inner highlight rgba(255,255,255,0.6) on light cards gives a pearly,
  soft-glow finish — never a hard drop shadow.
- **Buttons:** pill, border-radius 980px. Primary = filled pink #E0407B,
  white text (on dark: #FF8AB8 fill with #2B1220 text). Secondary = pink text
  + thin pink outline, transparent fill. Optional soft variant: blush
  #FBE4EE fill with #E0407B text for gentle tertiary actions.
- **Horizontal carousel:** scroll-snap-type: x mandatory on the track;
  scroll-snap-align: start per card; prev/next arrows + optional dots.
- **Sticky gallery:** a pinned section whose inner track scrolls horizontally
  as the user scrolls vertically.

### Motion
- Reveal on scroll: opacity 0→1 + translateY 30px→0, staggered ~80ms.
- Media hover: scale 1.0→1.05 over ~400ms, clipped to corners.
- Easing: cubic-bezier(0.28, 0.11, 0.32, 1).
- Jassy's touch: motion stays soft and dreamy — slightly longer fades are
  fine, but NO bounces, sparkles, floating hearts, or particle effects.
  Elegance over cuteness, always.

### Per-template variants
- Category landing (Mac, iPad): 80px hero → "Explore the lineup" 48px →
  horizontal product carousel with arrows and color swatches.
- Product page (iPhone): 56px hero, dark scheme, accent eyebrows, long
  scroll-snap feature carousels.
- Immersive (Vision Pro): 700-weight white headlines over full-bleed media.
- TV & Home: light + #F5F5F7 panels, 700-weight headlines, no carousels.

---

## Part 10 — Review checklist for any screen

1. Is anything glass sitting ON content instead of above it?
2. Do all nested corners share centers (no pinch, no flare)?
3. Could any hard divider become a scroll edge effect?
4. Do menus and dialogs spring from their triggering action?
5. Are bar items grouped by function, symbols not repeated, the primary
   action separate and tinted?
6. Does each sheet/panel choose correctly between dimming (interrupt) and
   plain glass (parallel)?
7. Does content extend behind bars and sidebars rather than stopping short?
8. Zero chips: no text fragments in tiny rounded containers posing as data,
   settings, or buttons.
9. Is hierarchy carried by the type scale (weight and size), not decoration?
10. Marketing pages: SF Pro stack, headlines ≥600 weight, negative tracking
    on big type, correct light/dark text colors, pill buttons, generous
    asymmetric section padding, reveal-on-scroll and hover-scale motion.
11. Jassy's palette check: backgrounds creamy white/blush (never gray),
    dark mode warm plum (never cold black), pink #E0407B only on accents
    and CTAs, at most one serif-italic accent word per hero, rose-gold or
    pink-lavender gradients on hero words only.
12. Girly ≠ cluttered: no sparkles, hearts, glitter, or script fonts. The
    femininity comes from the palette, the pearly surfaces, and the soft
    motion — the structure stays pure Apple.

### Official design resources
Everything lives at developer.apple.com/design/resources: platform UI kits for
Figma and Sketch, hardware bezels for framing screenshots, Icon Composer, and
SF Symbols. Use the kits WITH the Human Interface Guidelines: the kits show
what components look like; the HIG says where, when, and why.
