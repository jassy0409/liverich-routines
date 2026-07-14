#!/usr/bin/env python3
"""Build per-model Creative Radar dashboard HTML pages (LRM Look B).

Usage: python3 build_radar_pages.py
Writes karina_dashboard.html and shantal_dashboard.html next to this file.
Edit the KARINA / SHANTAL card lists below for each new week.
"""
import html

CSS = """
  :root{
    --ground:#100E0A; --panel:#18140D; --panel2:#1F1A11;
    --line:#2C2519; --line2:#221D14;
    --ink:#F0E9DA; --soft:#B8AD97; --faint:#8A7F6B;
    --gold:#D9B26A; --gold-deep:#B48F49; --rose:#CD8598;
    --green:#74C08C; --amber:#E0A44A; --red:#DE7676;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    --mono:"SF Mono",ui-monospace,Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{background:var(--ground)}
  body{background:var(--ground);color:var(--ink);font-family:var(--sans);
    font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
  :focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:4px}
  .wrap{max-width:920px;margin:0 auto;padding:0 24px 60px}
  header{position:relative;padding:60px 0 40px;text-align:center;overflow:hidden}
  header::before{content:"";position:absolute;inset:-40% -20% auto;height:150%;pointer-events:none;
    background:radial-gradient(ellipse 60% 55% at 50% 18%,rgba(217,178,106,.14),transparent 70%)}
  .kicker{font-family:var(--mono);font-size:12px;letter-spacing:.26em;text-transform:uppercase;color:var(--gold);position:relative}
  h1{font-family:var(--serif);font-weight:600;position:relative;font-size:clamp(38px,7vw,58px);
    line-height:1.12;letter-spacing:-.01em;margin:14px 0 10px;text-wrap:balance}
  h1 em{font-style:italic;color:var(--gold)}
  .dateline{color:var(--soft);font-size:16px;position:relative}
  .pillrow{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:24px;position:relative}
  .pill{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
    padding:6px 14px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--soft)}
  .pill.gold{border-color:rgba(217,178,106,.45);background:rgba(217,178,106,.10);color:var(--gold)}
  .pill.rose{border-color:rgba(205,133,152,.4);background:rgba(205,133,152,.10);color:var(--rose)}
  .grid{display:grid;gap:16px;margin-top:34px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:24px 26px 22px}
  .card-top{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:4px}
  h3{font-family:var(--serif);font-weight:600;font-size:23px;letter-spacing:-.005em}
  .when{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);white-space:nowrap}
  .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:14px 0 5px}
  .card p{color:var(--soft);font-size:16px;max-width:66ch}
  .flow{margin-top:6px;padding:10px 16px;border-left:3px solid var(--gold);background:var(--panel2);
    border-radius:0 10px 10px 0;font-size:16px;color:var(--ink);max-width:66ch}
  .note{margin-top:14px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
    display:inline-block;padding:5px 12px;border-radius:999px;color:var(--gold);
    border:1px solid rgba(217,178,106,.45);background:rgba(217,178,106,.10)}
  .callout{margin:40px 0 0;padding:22px 26px;border-radius:14px;
    border:1px solid rgba(217,178,106,.35);background:rgba(217,178,106,.08)}
  .callout .lbl{margin-top:0}
  .callout p{color:var(--soft);font-size:16px;max-width:70ch}
  footer{margin-top:52px;padding-top:26px;border-top:1px solid var(--line2);text-align:center;
    font-family:var(--mono);font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--faint)}
"""

def card(title, when, fit, intro, shoot, caption, note=None):
    # fit kept in the data for ordering only — not rendered
    h = [f'<div class="card"><div class="card-top"><h3>{html.escape(title)}</h3>'
         f'<span class="when">{html.escape(when)}</span></div>']
    if intro: h.append(f'<p>{html.escape(intro)}</p>')
    if shoot:
        h.append(f'<div class="lbl">Shoot ideas</div><p>{html.escape(shoot)}</p>')
    if caption:
        h.append(f'<div class="lbl">Caption angle</div><div class="flow">{html.escape(caption)}</div>')
    if note:
        h.append(f'<span class="note">{html.escape(note)}</span>')
    h.append('</div>')
    return "".join(h)

def page(model, voice, lane, pills, cards, callout, footer, dateline="July 14 – 19, 2026 · all times LA"):
    cards_html = "".join(card(*c) for c in cards)
    pills_html = "".join(f'<span class="pill {k}">{html.escape(t)}</span>' for k, t in pills)
    return f"""<!doctype html><html lang="en" data-theme="dark"><head>
<meta charset="utf-8"><title>Creative Radar · {model} · July 2026</title>
<meta name="color-scheme" content="dark">
<script>document.documentElement.setAttribute('data-theme','dark');</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{CSS}</style></head><body>
<div class="wrap">
<header>
  <div class="kicker">LIVERICHMEDIA · CREATIVE RADAR</div>
  <h1>Radar · <em>{model}</em></h1>
  <div class="dateline">{html.escape(dateline)}</div>
  <div class="pillrow"><span class="pill rose">{html.escape(voice)}</span>{pills_html}</div>
  <div class="dateline" style="margin-top:18px;color:var(--faint);font-size:15px">{html.escape(lane)}</div>
</header>
<div class="grid">{cards_html}</div>
<div class="callout"><div class="lbl">Editing board · lock these before the moment</div>
<p>{html.escape(callout)}</p></div>
<footer>{footer}</footer>
</div></body></html>"""

KARINA = [
 ("World Cup Semifinal · France vs Spain","TONIGHT · TUE JUL 14 · 12PM LA",96,
  "Kicks off in a few hours at AT&T Stadium. Push it now.",
  "A blue or red game day fit with a quick couch selfie before kickoff. A celebration reaction clip filmed ready to go, hands up or confetti pose the moment a goal drops.",
  "match is on right now, catch me on the couch while spain and france battle it out, today only",
  "push it now · airs in a few hours"),
 ("World Cup Semifinal · England vs Argentina","WED JUL 15 · 12PM LA",92,
  "Second semifinal, huge global audience.",
  "Split fit repping both sides, half England colors half Argentina. Watch party setup on the couch with snacks, biting nails reaction clip for the close moments.",
  "second semifinal today, guess who i'm rooting for, come watch with me, one time only before the final",None),
 ("World Cup Final + Halftime Show","SUN JUL 19 · 12PM LA",98,
  "MetLife Stadium. First ever World Cup halftime show with Madonna, Shakira, Justin Bieber, Burna Boy and BTS. The single biggest sports audience of the year.",
  "Championship walkout entrance in a robe, dropped for a trophy pose fit reveal. Halftime glam look with a dance clip channeling the performers.",
  "final match of the year plus the biggest halftime show ever, tune in with me today, final day only",
  "biggest audience of the year"),
 ("Heartstopper Forever · Netflix","FRI JUL 17",84,
  "Closes out the whole saga. Built in fanbase, huge watch party energy.",
  "Cozy pajama binge setup with tissues nearby for the emotional finale. Pastel or rainbow color coordinated fit tied to the show's look.",
  "the finale is out today, watching it with tissues ready, come binge with me tonight",None),
 ("World Emoji Day","FRI JUL 17",82,
  "Easy and shareable content day, same Friday as the Heartstopper drop.",
  "Dress as your favorite emoji, heart eyes or fire or peach, quick reveal clip. Emoji face reaction challenge, a few faces back to back.",
  "happy world emoji day, guess my emoji fit, playful one day only",None),
]

SHANTAL = [
 ("World Cup Semifinal · France vs Spain","TONIGHT · TUE JUL 14 · 12PM LA",96,
  "Kicks off in a few hours at AT&T Stadium. Push it now.",
  "An elegant blue or red fit, a calm couch moment before kickoff. A genuine celebration reaction filmed ready for the first goal.",
  "The semifinal is on right now, Spain and France battle it out today only, come sit with me while it airs.",
  "push it now · airs in a few hours"),
 ("World Cup Semifinal · England vs Argentina","WED JUL 15 · 12PM LA",92,
  "Second semifinal, huge global audience.",
  "A poised fit in her chosen side's colors, kept refined rather than costume. A quiet snacks setup on the couch, honest reactions in the close moments.",
  "The second semifinal is today and I already chose my side, come watch it with me, one time only before the final.",None),
 ("World Cup Final + Halftime Show","SUN JUL 19 · 12PM LA",98,
  "MetLife Stadium. First ever World Cup halftime show with Madonna, Shakira, Justin Bieber, Burna Boy and BTS. The single biggest sports audience of the year.",
  "An elegant walkout in a robe, opened for a graceful trophy moment fit reveal. Halftime glam look, a soft dance clip in the spirit of the show.",
  "The final is today with the biggest halftime show ever, tune in with me, it is final day only.",
  "biggest audience of the year"),
 ("Heartstopper Forever · Netflix","FRI JUL 17",90,
  "Closes out the whole saga. A natural fit for her cozy one to one lane.",
  "Cozy pajama binge setup with tissues nearby for the emotional finale. Soft pastel fit, unhurried couch framing.",
  "The finale is out today and I have the tissues ready, come binge it with me tonight.",None),
 ("World Emoji Day","FRI JUL 17",68,
  "Light tie in only, keep her Friday focused on the Heartstopper finale.",
  "One subtle playful clip, heart eyes moment to camera. Skip the costume angle, it does not suit the lane.",
  "It is World Emoji Day, can you guess which one I am today.",
  "light tie in · optional"),
]

K_CALLOUT=("France vs Spain fit shoots NOW, before the 12pm kickoff. England vs Argentina split fit tonight "
 "after the match so it is ready for Wednesday noon. Heartstopper and Emoji Day sets in the edit by Thursday Jul 16. "
 "Final walkout robe and halftime glam by Saturday Jul 18. Every go live is timed to kickoff, edits deliver the day before, never day of.")
S_CALLOUT=("France vs Spain fit shoots NOW, before the 12pm kickoff. Wednesday's fit tonight after the match. "
 "Heartstopper set in the edit by Thursday Jul 16, it is her big Friday. Final walkout and halftime glam by "
 "Saturday Jul 18. Every go live is timed to kickoff, edits deliver the day before, never day of.")

open("karina_dashboard.html","w").write(page(
  "Karina","voice · lowercase, playful, bratty",
  "Lane: high energy, teasing, event-native. Semifinal tonight, the Final and halftime show are the week's peak.",
  [("gold","5 moments"),("","Tonight · France vs Spain · 12pm"),("","Peak · Final + halftime show · Sun Jul 19")],
  KARINA,K_CALLOUT,"LIVERICHMEDIA · CREATIVE RADAR · KARINA · JUL 14–19 2026"))
open("shantal_dashboard.html","w").write(page(
  "Shantal","voice · personal, proper sentences, first names",
  "Lane: elegant, one to one, unhurried. Semifinal tonight, Heartstopper Friday is hers, the Final peaks Sunday.",
  [("gold","5 moments"),("","Tonight · France vs Spain · 12pm"),("","Peak · Final + halftime show · Sun Jul 19")],
  SHANTAL,S_CALLOUT,"LIVERICHMEDIA · CREATIVE RADAR · SHANTAL · JUL 14–19 2026"))
print("wrote karina_dashboard.html, shantal_dashboard.html")
