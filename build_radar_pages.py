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

def page(model, voice, lane, pills, cards, callout, footer):
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
  <div class="dateline">July 13 – 31, 2026 · all times Pacific</div>
  <div class="pillrow"><span class="pill rose">{html.escape(voice)}</span>{pills_html}</div>
  <div class="dateline" style="margin-top:18px;color:var(--faint);font-size:15px">{html.escape(lane)}</div>
</header>
<div class="grid">{cards_html}</div>
<div class="callout"><div class="lbl">Editing board · lock these before the moment</div>
<p>{html.escape(callout)}</p></div>
<footer>{footer}</footer>
</div></body></html>"""

KARINA = [
 ("World Cup Final","SUN JUL 19 · 12PM",96,
  "The championship match, the single biggest audience moment of the month.",
  "Bratty game day jersey tied at the waist, quick teasing mirror clip before kickoff. Couch watch party with popcorn and a playful championship pick sign held to camera, cheeky bet with me energy.",
  "one team takes it all today and so do i, watch the final with me before kickoff, today only",None),
 ("UFC Fight Night · Du Plessis vs Usman","SAT JUL 18 · 5PM",94,None,
  "Ringside glam with a robe entrance, fighter walkout attitude. Post fight celebration clip, arms up like she just took the belt.",
  "fight night, live only while the card is on, come watch me take the belt tonight",
  "her strongest fit of the week"),
 ("Christmas in July","SAT JUL 25",93,
  "The biggest sales moment of the back half of the month. Frame the drop as a gift, one night only.",
  "Red bow and ribbon styling, gift wrap tease with a slow unwrap clip. Santa hat and stockings by a fake tree, naughty list sign held to camera.",
  "christmas came early and so did your gift, unwrap me tonight only",
  "vip gift drop · pair with a bundle"),
 ("National Ice Cream Day","SUN JUL 19",92,None,
  "Cone or sundae taste test, playful lick and bite reaction, messy on purpose. Spoon lick cleanup moment by the couch. Same day as the Final, run it as the morning warm up post.",
  "ice cream day and i am being messy on purpose, sweet content today only, don't miss it",None),
 ("World Cup Semifinals","TUE JUL 14 + WED JUL 15 · 12PM",88,None,
  "Team colors robe walkout reveal, tunnel entrance strut with a drop on the reveal. Loud couch reaction clip, big gasp and cheer during the match.",
  "only two teams left and i already picked my winner, tune in with me while it airs tonight",None),
 ("National Tequila Day","FRI JUL 24",86,None,
  "Going out cocktail look, lime and salt play, a wink over the shoulder shot glass clip. Body shot setup implied, kept playful.",
  "it's tequila day, take a shot with me and see where the night goes",None),
 ("MLB All Star Game","TUE JUL 14 · EVENING",85,None,
  "Ballpark chic cap and tiny shorts posed like heading out to the game. Hot dog and soda flat lay with a messy playful bite reaction clip.",
  "all star night, baseball is on and i wore the cap just for you, hang out with me for the game tonight",None),
 ("Comic-Con weekend","THU JUL 23 – SUN JUL 26",83,None,
  "Cosplay costume reveal tease, spin transition from casual to full costume. Poll the fans on which character she suits up as next.",
  "suited up for con weekend, guess who i came as, full reveal in your dms",None),
 ("National Hot Dog Day","WED JUL 22",74,None,
  "Quick playful food clip, natural follow on from the All Star hot dog flat lay. Low lift filler day, one post max.",
  "apparently it's hot dog day, i had to, don't judge me just watch",
  "filler · keep it light"),
]

SHANTAL = [
 ("World Cup Final","SUN JUL 19 · 12PM",96,
  "The championship match, the single biggest audience moment of the month.",
  "Elegant team colors fit, a calm mirror moment before kickoff. Tidy couch watch party setup, a quiet pick your team with me note held to camera.",
  "The final is today and only one team lifts the trophy, come watch it with me before kickoff, just for today.",None),
 ("National Ice Cream Day","SUN JUL 19",90,None,
  "Sundae taste test at home, a soft genuine reaction. An unhurried sweet moment on the couch, morning post before the Final takes over.",
  "It is National Ice Cream Day, I made myself a treat and saved a spot for you, come share something sweet with me today.",None),
 ("World Cup Semifinals","TUE JUL 14 + WED JUL 15 · 12PM",88,None,
  "Refined team color entrance, poised rather than costume. An honest reaction moment on the couch during the match.",
  "Only two teams remain tonight, tune in with me while the semifinal airs, I kept you a place on the couch.",None),
 ("Christmas in July","SAT JUL 25",88,None,
  "Cosy at home styling, soft lighting, a wrapped gift on her lap opened slowly to camera. Keep it intimate rather than costume.",
  "A little Christmas in July, just for you. I put something together and it is ready whenever you are.",
  "gift framed ppv drop"),
 ("The Open · golf major","THU JUL 16 – SUN JUL 19",82,None,
  "Country club chic, pleated skirt and polo, posed like heading to the course. A quiet afternoon of watching together framing.",
  "The Open is on this week and I dressed for the occasion, spend a slow afternoon watching with me.",None),
 ("National Tequila Day","FRI JUL 24",76,None,
  "One elegant cocktail at home, evening dress, a single toast to camera. Refined rather than party energy.",
  "It is Tequila Day and I made us a drink, join me for one tonight, I saved you the seat next to me.",None),
 ("MLB All Star Game","TUE JUL 14 · EVENING",72,None,
  "Ballpark chic, cap and shorts, posed and clean like heading out to the game. A simple hot dog and soda flat lay.",
  "It is All Star night and the game is on, come watch it with me tonight, I even found my cap.",None),
 ("UFC Fight Night","SAT JUL 18 · 5PM",64,None,
  "Off lane. If she wants it, a soft ringside glam look with the robe kept elegant. Otherwise a quiet at home evening post and let the other lane own fight night.",
  "Fight night is on tonight, if you are watching the card come watch it with me while it is live.",
  "off lane · optional"),
 ("Comic-Con weekend","THU JUL 23 – SUN JUL 26",58,None,
  "Soft pass. Costume energy does not suit the lane, keep the weekend for an elegant summer evening set instead.",
  None,"skip · protect the lane"),
]

K_CALLOUT=("Semifinal fits by Mon Jul 13 evening. All Star fit Tue morning. UFC glam by Fri Jul 17. "
 "Final plus Ice Cream Day shot Sat Jul 18 so both post Sunday morning. Tequila, Comic-Con and "
 "Christmas in July sets in the edit by Wed Jul 22. Every go live is timed to kickoff, edits deliver the day before, never day of.")
S_CALLOUT=("Semifinal fits by Mon Jul 13 evening. All Star fit Tue morning. The Open look by Wed Jul 15. "
 "Final plus Ice Cream Day shot Sat Jul 18 so both post Sunday morning. Tequila and Christmas in July "
 "sets in the edit by Wed Jul 22. Every go live is timed to kickoff, edits deliver the day before, never day of.")

open("karina_dashboard.html","w").write(page(
  "Karina","voice · lowercase, playful, bratty",
  "Lane: high energy, teasing, event-native. Fight night and the Final are hers this month.",
  [("gold","9 moments"),("","Peak · World Cup Final · Sun Jul 19"),("","Sale window · Christmas in July · Jul 25")],
  KARINA,K_CALLOUT,"LIVERICHMEDIA · CREATIVE RADAR · KARINA · JUL 13–31 2026"))
open("shantal_dashboard.html","w").write(page(
  "Shantal","voice · personal, proper sentences, first names",
  "Lane: elegant, one to one, unhurried. She wins the Final and the sweet moments, skip the fight card.",
  [("gold","9 moments"),("","Peak · World Cup Final · Sun Jul 19"),("","Sale window · Christmas in July · Jul 25")],
  SHANTAL,S_CALLOUT,"LIVERICHMEDIA · CREATIVE RADAR · SHANTAL · JUL 13–31 2026"))
print("wrote karina_dashboard.html, shantal_dashboard.html")
