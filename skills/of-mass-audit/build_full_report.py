#!/usr/bin/env python3
# Build LRM dark-mode HTML report from lucy_mass.json
import json, html
from collections import defaultdict
from datetime import datetime

msgs = json.load(open("/sessions/modest-great-ptolemy/mnt/outputs/lucy_mass.json"))
OUT = "/sessions/modest-great-ptolemy/mnt/Downloads/lucymochi-mass-message-audit-2026-06-03.html"

MONTH_NAMES = {"2025-01":"January 2025","2025-02":"February 2025","2025-03":"March 2025",
               "2025-04":"April 2025","2025-05":"May 2025","2025-06":"June 2025","2025-07":"July 2025",
               "2025-08":"August 2025","2025-09":"September 2025","2025-10":"October 2025",
               "2025-11":"November 2025","2025-12":"December 2025",
               "2026-01":"January 2026","2026-02":"February 2026",
               "2026-03":"March 2026","2026-04":"April 2026","2026-05":"May 2026","2026-06":"June 2026 (3 days)"}

AV=[("#CECBF6","#26215C"),("#B5D4F4","#042C53"),("#F4C0D1","#4B1528"),("#FAC775","#412402"),
    ("#C0DD97","#173404"),("#9FE1CB","#04342C"),("#F7C1C1","#501313"),("#B4B2A9","#2C2C2A"),
    ("#F0997B","#4A1B0C"),("#EF9F27","#412402")]
def esc(s): return html.escape(s).replace("\n","<br>")

months = defaultdict(lambda: dict(n=0,paid=0,free=0,rev=0.0,purch=0,views=[]))
for m in msgs:
    M = months[m["month"]]
    M["n"]+=1; M["paid" if m["paid"] else "free"]+=1
    M["rev"]+=m["revenue"]; M["purch"]+=m["purchases"] or 0
    if m["viewed"] is not None and (m["sent"] or 0)>10000: M["views"].append(m["viewed"])

def med(v): v=sorted(v); return v[len(v)//2] if v else 0
mk = sorted(months)
rev_series=[round(months[k]["rev"]) for k in mk]
view_series=[med(months[k]["views"]) for k in mk]
labels=[MONTH_NAMES[k].split(" (")[0].replace(" 20"," '") for k in mk]

# ---- pure-CSS bar charts (no external JS — always renders) ----
def css_bars(vals, fmt, labs=None, mx=None, avg=None):
    labs = labs if labs is not None else labels
    avg = avg if avg is not None else sum(vals)/len(vals)
    def col(v):
        if v >= 2*avg: return "#97C459"
        if v >= avg: return "#C0DD97"
        if v >= avg*0.5: return "#FAC775"
        return "#85B7EB" if v > 0 else "#444441"
    mx = (mx if mx is not None else max(vals)) or 1
    out = '<div class="bars">'
    for v, lab in zip(vals, labs):
        h = max(round(v/mx*160), 3)
        out += (f'<div class="barcol"><div class="barval">{fmt(v)}</div>'
                f'<div class="bar" style="height:{h}px;background:{col(v)};"></div>'
                f'<div class="barlab">{lab}</div></div>')
    return out + "</div>"

# split into one row per year so 18 months never crowd the labels
fmt_money = lambda v: f"${v/1000:.1f}k" if v >= 1000 else f"${v:,.0f}"
fmt_count = lambda v: f"{v/1000:.1f}k" if v >= 1000 else f"{v:,}"
ABBR = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun",
        "07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
mk25 = [k for k in mk if k.startswith("2025")]
mk26 = [k for k in mk if k.startswith("2026")]
def short_labs(keys):
    return [ABBR[k[5:]] + (" 1–3" if k == "2026-06" else "") for k in keys]
def year_split_chart(series_by_key, fmt):
    allv = [series_by_key[k] for k in mk]
    gmx, gavg = max(allv), sum(allv)/len(allv)
    out = ""
    for yr, keys in (("2025", mk25), ("2026", mk26)):
        vals = [series_by_key[k] for k in keys]
        out += (f'<p class="label" style="margin:6px 0 8px;">{yr}</p>'
                + css_bars(vals, fmt, short_labs(keys), mx=gmx, avg=gavg))
        if yr == "2025":
            out += '<div style="height:14px;"></div>'
    return out
rev_by_key = {k: round(months[k]["rev"]) for k in mk}
view_by_key = {k: med(months[k]["views"]) for k in mk}
rev_chart = year_split_chart(rev_by_key, fmt_money)
view_chart = year_split_chart(view_by_key, fmt_count)

# ---- YoY same window: Jan 1 – Jun 3 of each year ----
def window(ms, y):
    return [m for m in ms if m["date"] >= f"{y}-01-01" and m["date"] <= f"{y}-06-03T23:59:59"]
w25, w26 = window(msgs, 2025), window(msgs, 2026)
def agg(ms):
    v = sorted(x["viewed"] for x in ms if x["viewed"] is not None and (x["sent"] or 0) > 10000)
    return dict(rev=sum(x["revenue"] for x in ms), buys=sum(x["purchases"] or 0 for x in ms),
                n=len(ms), paid=sum(1 for x in ms if x["paid"]),
                med=v[len(v)//2] if v else 0)
A25, A26 = agg(w25), agg(w26)
may25 = months["2025-05"]; may26 = months["2026-05"]
yoy_delta = (A26["rev"]-A25["rev"])/A25["rev"]*100
may_delta = (may26["rev"]-may25["rev"])/may25["rev"]*100
yoy_chart = css_bars([round(A25["rev"]), round(A26["rev"])],
                     lambda v: f"${v/1000:.1f}k", ["Jan 1–Jun 3, 2025", "Jan 1–Jun 3, 2026"])

# ---- Lucy cadence / vitals facts (computed) ----
y25 = [m for m in msgs if m["month"].startswith("2025")]
y26 = [m for m in msgs if m["month"].startswith("2026")]
y25_paid = sum(1 for m in y25 if m["paid"]); y25_free = len(y25)-y25_paid
y26_paid = sum(1 for m in y26 if m["paid"]); y26_free = len(y26)-y26_paid
y25_rev = sum(m["revenue"] for m in y25); y26_rev = sum(m["revenue"] for m in y26)
days25, days26 = 365, 154  # Jan 1 2025–Dec 31 2025 / Jan 1 2026–Jun 3 2026
free_day_25 = y25_free/days25; free_day_26 = y26_free/days26
paid_wk_25 = y25_paid/days25*7; paid_wk_26 = y26_paid/days26*7
import statistics
medprice25 = statistics.median(m["price"] for m in y25 if m["paid"])
medprice26 = statistics.median(m["price"] for m in y26 if m["paid"])
jun26 = months["2026-06"]
free_drop = (free_day_26-free_day_25)/free_day_25*100

# ---- duplicates / re-sends that sold again ----
import unicodedata
def normcap(c):
    c = c.lower()
    c = "".join(ch for ch in c if ch.isalnum() or ch == " ")
    return " ".join(c.split())[:45]
groups = defaultdict(list)
for m in msgs:
    if m["paid"] and m["caption"]:
        groups[normcap(m["caption"])].append(m)
dups = [(k, v) for k, v in groups.items()
        if len(v) >= 2 and sum(x["revenue"] for x in v) > 0
        and len({x["day"] for x in v}) >= 2]
dups.sort(key=lambda kv: -sum(x["revenue"] for x in kv[1]))
dups = dups[:20]

dup_rows = ""
for i, (k, v) in enumerate(dups):
    bg, fg = AV[i % 10]
    v = sorted(v, key=lambda x: x["date"])
    tot = sum(x["revenue"] for x in v)
    sells = " · ".join(f'{datetime.fromisoformat(x["date"]).strftime("%b %d %y").replace(" 20"," ʼ")} ${x["price"]:.0f}×{x["purchases"] or 0}' for x in v)
    cap = v[0]["caption"].split("\n")[0][:64]
    dup_rows += f'''<div class="domain-row"><div class="domain-rank">{i+1}</div>
<div class="domain-avatar" style="background:{bg};color:{fg};">{len(v)}</div>
<div class="domain-info"><div class="domain-name">{esc(cap)}</div>
<div class="domain-meta">{len(v)} sends — {esc(sells)}</div></div>
<div class="domain-count">${tot:,.0f}</div></div>\n'''

# ---- day of week / time of day (paid masses only) ----
DOW = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
dow_rev = {d: 0.0 for d in DOW}; dow_n = {d: 0 for d in DOW}
for m in msgs:
    if m["paid"]:
        dow_rev[m["dow"]] += m["revenue"]; dow_n[m["dow"]] += 1
dow_per = [round(dow_rev[d]/dow_n[d]) if dow_n[d] else 0 for d in DOW]
dow_chart = css_bars(dow_per, lambda v: f"${v}", DOW)

BUCKETS = [("Late 12–6a", 0, 6), ("Morning 6–11a", 6, 11), ("Midday 11a–4p", 11, 16),
           ("Evening 4–9p", 16, 21), ("Night 9p–12a", 21, 24)]
buck = []
for name, lo, hi in BUCKETS:
    sel = [m for m in msgs if m["paid"] and lo <= m["hour"] < hi]
    r = sum(m["revenue"] for m in sel)
    buck.append((name, len(sel), r, round(r/len(sel)) if sel else 0))
hour_chart = css_bars([b[3] for b in buck], lambda v: f"${v}", [b[0].split()[0] for b in buck])

# ---- price bands ----
BANDS = [("Under $10", 0, 10), ("$10–14.99", 10, 15), ("$15–19.99", 15, 20),
         ("$20–29.99", 20, 30), ("$30–49.99", 30, 50), ("$50–99.99", 50, 100), ("$100+", 100, 10**6)]
band_rows = ""
band_max = 0; band_data = []
for name, lo, hi in BANDS:
    sel = [m for m in msgs if m["paid"] and lo <= m["price"] < hi]
    r = sum(m["revenue"] for m in sel); b = sum(m["purchases"] or 0 for m in sel)
    rps = r/len(sel) if sel else 0
    band_data.append((name, len(sel), b, b/len(sel) if sel else 0, r, rps))
    band_max = max(band_max, rps)
for i, (name, n, b, bps, r, rps) in enumerate(band_data):
    bg, fg = AV[i % 10]
    band_rows += f'''<div class="domain-row"><div class="domain-rank">{i+1}</div>
<div class="domain-avatar" style="background:{bg};color:{fg};">$</div>
<div class="domain-info"><div class="domain-name">{name}</div>
<div class="domain-meta">{n} sends · {b} buys · {bps:.1f} buys/send</div></div>
<div class="domain-bar-wrap"><div class="domain-bar" style="width:{rps/band_max*100:.0f}%;"></div></div>
<div class="domain-count">${rps:,.0f}/send</div></div>\n'''

top = sorted(msgs,key=lambda x:-x["revenue"])[:10]
maxrev = top[0]["revenue"]

top_rows=""
for i,m in enumerate(top):
    bg,fg=AV[i%10]
    d=datetime.fromisoformat(m["date"]).strftime("%b %d")
    cap=m["caption"].split("\n")[0]
    cap=cap[:80]+("…" if len(cap)>80 else "")
    top_rows+=f'''<div class="domain-row"><div class="domain-rank">{i+1}</div>
<div class="domain-avatar" style="background:{bg};color:{fg};">{d.split()[0][0]}</div>
<div class="domain-info"><div class="domain-name">{esc(cap)}</div>
<div class="domain-meta">{d} · ${m["price"]:.2f} × {m["purchases"]} buys</div></div>
<div class="domain-bar-wrap"><div class="domain-bar" style="width:{m["revenue"]/maxrev*100:.0f}%;"></div></div>
<div class="domain-count">${m["revenue"]:,.0f}</div></div>\n'''

table_rows=""
for k in mk:
    M=months[k]
    cls=' style="color:var(--success-text);"' if k in("2025-12","2026-03") else (' style="color:var(--amber-text);"' if k in("2025-11","2026-05","2026-06") else "")
    table_rows+=f'''<tr{cls}><td>{MONTH_NAMES[k]}</td><td>{M["n"]}</td><td>{M["paid"]}</td><td>{M["free"]}</td><td>${M["rev"]:,.0f}</td><td>{M["purch"]}</td><td>{med(M["views"]):,}</td></tr>\n'''

# full log grouped by month, newest first
log=""
for k in sorted(mk,reverse=True):
    log+=f'<h3 class="log-month">{MONTH_NAMES[k]} — ${months[k]["rev"]:,.0f} est · {months[k]["paid"]} paid / {months[k]["free"]} free</h3>\n'
    mm=[m for m in msgs if m["month"]==k]
    mm.sort(key=lambda x:x["date"],reverse=True)
    for m in mm:
        d=datetime.fromisoformat(m["date"]).strftime("%b %d, %I:%M %p").replace(" 0"," ")
        if m["paid"]:
            rev=m["revenue"]
            cls="msg paid"+(" hot" if rev>=500 else "")
            meta=f'${m["price"]:.2f} · {m["purchases"] or 0} buys · ${rev:,.0f}'
        else:
            cls="msg"; meta="free"
        views=f'{m["viewed"]:,} viewed' if m["viewed"] is not None else ""
        log+=f'''<div class="{cls}"><div class="msg-head"><span class="msg-date">{d}</span><span class="msg-views">{views}</span><span class="msg-meta">{meta}</span></div><div class="msg-cap">{esc(m["caption"]) or "<i>(no caption)</i>"}</div></div>\n'''

html_doc=f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lucy · Mass Message Audit · Jan 2025 → Jun 2026</title>
<style>
:root{{--bg:#1a1a1a;--bg-card:#232323;--bg-card-soft:#2a2a2a;--text:#f5f5f4;--text-secondary:#a8a8a4;
--border:rgba(255,255,255,0.10);--success-border:#97C459;--success-text:#C0DD97;--success-bg-soft:#1f2e1a;
--info-border:#85B7EB;--info-text:#B5D4F4;--purple-border:#7F77DD;--purple-text:#CECBF6;
--amber-text:#FAC775;--pink-text:#F4C0D1;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:14px;line-height:1.55;padding:32px 20px;}}
.container{{max-width:720px;margin:0 auto;}}
.header-top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:24px;}}
.brand{{background:linear-gradient(90deg,#CECBF6 0%,#F4C0D1 50%,#85B7EB 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-weight:600;font-size:22px;}}
.header-meta{{font-size:11px;color:var(--text-secondary);text-align:right;}}
h1{{font-size:26px;font-weight:500;letter-spacing:-0.01em;}}
.subtitle{{font-size:13px;color:var(--text-secondary);margin:4px 0 24px;}}
h2{{font-size:16px;font-weight:500;margin:28px 0 12px;}}
.stat-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}}
.stat-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:16px 18px;}}
.stat-card.success{{border-top:2px solid var(--success-border);}}
.stat-card.info{{border-top:2px solid var(--info-border);}}
.stat-card.purple{{border-top:2px solid var(--purple-border);}}
.stat-card.amber{{border-top:2px solid var(--amber-text);}}
.label{{font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:var(--text-secondary);}}
.big{{font-size:28px;font-weight:500;letter-spacing:-0.02em;margin-top:4px;}}
.sub{{font-size:12px;margin-top:4px;color:var(--text-secondary);}}
.delta.down{{color:#f87171;}}.delta.up{{color:#4ade80;}}
.callout-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;}}
.callout{{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:14px 18px;}}
.callout.purple{{border-left:3px solid var(--purple-border);}}
.callout.pink{{border-left:3px solid var(--pink-text);}}
.callout .ll{{font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:var(--text-secondary);}}
.callout .vv{{font-size:19px;font-weight:500;margin:3px 0;}}
.callout .ss{{font-size:12px;color:var(--text-secondary);}}
.card{{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:16px 18px;}}
.bars{{display:flex;align-items:flex-end;gap:10px;height:215px;padding-top:4px;}}
.barcol{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;min-width:0;}}
.bar{{width:100%;max-width:72px;border-radius:6px 6px 2px 2px;}}
.barval{{font-size:10px;color:var(--text);margin-bottom:4px;font-variant-numeric:tabular-nums;white-space:nowrap;}}
.barlab{{font-size:10px;color:var(--text-secondary);margin-top:6px;white-space:nowrap;}}
.domain-row{{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,0.06);}}
.domain-row:last-child{{border-bottom:none;}}
.domain-rank{{width:22px;font-size:12px;color:var(--text-secondary);text-align:center;flex-shrink:0;}}
.domain-avatar{{width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:14px;flex-shrink:0;}}
.domain-info{{flex:1;min-width:0;}}
.domain-name{{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.domain-meta{{font-size:11px;color:var(--text-secondary);}}
.domain-bar-wrap{{width:110px;height:6px;background:rgba(255,255,255,0.06);border-radius:3px;flex-shrink:0;}}
.domain-bar{{height:6px;background:#85B7EB;border-radius:3px;}}
.domain-count{{width:70px;text-align:right;font-size:13px;font-variant-numeric:tabular-nums;flex-shrink:0;}}
table{{width:100%;border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums;}}
th{{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:var(--text-secondary);font-weight:500;padding:6px 8px;border-bottom:1px solid var(--border);}}
td{{padding:8px;border-bottom:1px solid rgba(255,255,255,0.06);}}
tr:last-child td{{border-bottom:none;}}
.compare-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
.compare{{background:var(--bg-card);border:1px solid var(--border);border-radius:14px;padding:16px 18px;font-size:13px;}}
.compare.win{{border-top:2px solid var(--success-border);}}
.compare.lose{{border-top:2px solid var(--amber-text);}}
.compare h4{{font-size:13px;margin-bottom:8px;}}
.compare ul{{margin:0 0 0 16px;color:var(--text-secondary);}}
.compare li{{margin-bottom:6px;}}
.compare b{{color:var(--text);font-weight:500;}}
.summary-box{{background:var(--success-bg-soft);border-left:3px solid var(--success-border);border-radius:12px;padding:16px 20px;margin-top:12px;font-size:13px;color:var(--success-text);}}
.summary-box b{{color:var(--text);}}
.warn-box{{background:#2e2412;border-left:3px solid var(--amber-text);border-radius:12px;padding:16px 20px;margin-top:12px;font-size:13px;color:#f0d9a8;}}
.warn-box b{{color:var(--text);}}
.log-wrap{{max-height:560px;overflow-y:auto;padding-right:6px;}}
.log-month{{font-size:13px;font-weight:600;color:var(--purple-text);margin:18px 0 8px;position:sticky;top:0;background:var(--bg-card);padding:6px 0;}}
.msg{{border-left:2px solid rgba(255,255,255,0.12);padding:8px 0 8px 12px;margin-bottom:10px;}}
.msg.paid{{border-left-color:var(--info-border);}}
.msg.paid.hot{{border-left-color:var(--success-border);}}
.msg-head{{display:flex;gap:12px;font-size:11px;color:var(--text-secondary);margin-bottom:3px;flex-wrap:wrap;}}
.msg-date{{font-weight:600;color:var(--text);}}
.msg.paid .msg-meta{{color:var(--info-text);}}
.msg.paid.hot .msg-meta{{color:var(--success-text);}}
.msg-cap{{font-size:12.5px;color:var(--text-secondary);word-break:break-word;}}
.legend{{font-size:11px;color:var(--text-secondary);margin-bottom:10px;}}
.legend span{{display:inline-block;margin-right:14px;}}
.dot{{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:5px;vertical-align:middle;}}
.footer{{text-align:center;margin-top:32px;padding-top:20px;border-top:1px solid var(--border);font-size:12px;color:var(--text-secondary);}}
@media (max-width:880px){{.stat-grid{{grid-template-columns:1fr 1fr;}}}}
@media (max-width:640px){{
body{{padding:20px 14px;font-size:13px;}}
.header-top{{flex-direction:column;align-items:flex-start;gap:6px;}}
.header-meta{{text-align:left;}}
h1{{font-size:22px;}}
.stat-grid{{grid-template-columns:1fr;gap:10px;}}
.stat-card .big{{font-size:24px;}}
.callout-grid,.compare-grid{{grid-template-columns:1fr;gap:10px;}}
.card{{padding:14px 16px;}}
.domain-bar-wrap{{width:50px;}}
.bars{{gap:5px;height:185px;}}
.barval{{font-size:9px;}}
.barlab{{font-size:9px;}}
.mtable{{overflow-x:auto;}}
}}
</style></head><body><div class="container">

<div class="header-top">
<div class="brand">LiveRichMedia</div>
<div class="header-meta">Mass message audit · pulled Jun 3, 2026<br>@lucymochi · Jan 2025 → Jun 2026</div>
</div>

<h1>Lucy — Mass Message Audit</h1>
<p class="subtitle">Jan 1, 2025 → Jun 3, 2026 · 6,846 masses captured via API</p>

<h2 style="margin-top:8px;">The bottom line first — total revenue, Jan 1 → Jun 3 each year (OF-reported, gross)</h2>
<div class="stat-grid">
<div class="stat-card success"><p class="label">@lucymochi · 2025</p><p class="big">$1,068,358</p><p class="sub">subs $239,378 + msgs $672,361 + tips $156,619</p></div>
<div class="stat-card amber"><p class="label">@lucymochi · 2026</p><p class="big">$943,520</p><p class="sub"><span class="delta down">−$124,838 · −11.7% YoY</span></p></div>
<div class="stat-card info"><p class="label">Messages</p><p class="big">−3.7%</p><p class="sub">$672.4k → $647.4k <span class="delta down">−$25,009</span></p></div>
<div class="stat-card amber"><p class="label">Subs + Tips</p><p class="big">−25.2%</p><p class="sub">$396.0k → $296.2k <span class="delta down">−$99,829</span></p></div>
</div>
<div class="callout-grid">
<div class="callout purple"><p class="ll">Mass-window est. revenue (price × buys)</p><p class="vv">${A25["rev"]/1000:,.1f}k → ${A26["rev"]/1000:,.1f}k</p><p class="ss">Jan 1–Jun 3 each year · <b>{yoy_delta:+.1f}%</b>. The mass machine itself is flat YoY — {A25["buys"]:,} buys ({A25["paid"]} paid sends) vs {A26["buys"]:,} buys ({A26["paid"]} paid sends).</p></div>
<div class="callout pink"><p class="ll">The cadence shift — paid up, free gutted</p><p class="vv">{free_day_25:.1f} → {free_day_26:.1f} free/day</p><p class="ss">Free/engagement masses fell {free_drop:.0f}% ({y25_free:,} in 2025 → {y26_free:,} in 154 days of 2026) while paid sends rose {paid_wk_25:.1f} → {paid_wk_26:.1f}/wk. The feed got more salesy and less social.</p></div>
</div>
<div class="warn-box"><b>The −11.7% YoY drop is NOT a mass-message problem — masses are holding flat (est. ${A25["rev"]:,.0f} → ${A26["rev"]:,.0f}, {yoy_delta:+.1f}%) and OF-reported message revenue is only down −3.7%.</b> The leak is subs + tips: −$99,829 (−25.2%), which is 80% of the total decline. The data shows what changed: free/engagement masses were cut in half ({free_day_25:.1f}/day in 2025 → {free_day_26:.1f}/day in 2026) while paid sends were pushed up ({paid_wk_25:.1f} → {paid_wk_26:.1f}/wk) and the median paid price climbed ${medprice25:.0f} → ${medprice26:.0f}. Squeezing harder on PPV while halving the free touchpoints that keep fans subscribed and tipping is exactly the pattern that produces flat message money on a shrinking, less-engaged base — and buys per window already slipped {A25["buys"]:,} → {A26["buys"]:,} (−21%).</div>

<h2>Mass message vitals</h2>
<div class="stat-grid">
<div class="stat-card success"><p class="label">2025 est. monthly avg</p><p class="big">${y25_rev/12:,.0f}</p><p class="sub">${y25_rev/1000:,.1f}k ÷ 12 · {y25_paid} paid / {y25_free:,} free</p></div>
<div class="stat-card amber"><p class="label">May 2026</p><p class="big">${may26["rev"]:,.0f}</p><p class="sub"><span class="delta down">{(may26["rev"]-y25_rev/12)/(y25_rev/12)*100:.0f}% vs 2025 avg</span> · {may26["n"]} masses (fewest of any month)</p></div>
<div class="stat-card info"><p class="label">Median paid price</p><p class="big">${medprice25:.0f} → ${medprice26:.0f}</p><p class="sub">2025 vs 2026 · pricing drifted up</p></div>
<div class="stat-card amber"><p class="label">June so far (3 days)</p><p class="big">${jun26["rev"]:,.0f}</p><p class="sub">{jun26["purch"]} buys · {jun26["paid"]} paid / {jun26["free"]} free sends</p></div>
</div>

<div class="callout-grid">
<div class="callout purple"><p class="ll">Buys per month</p><p class="vv">{months["2025-12"]["purch"]:,} → {may26["purch"]:,}</p><p class="ss">Dec '25 vs May '26 · −69%. Send list still ~160–175k fans on full-list sends all period.</p></div>
<div class="callout pink"><p class="ll">Volume collapse</p><p class="vv">699 → 130 masses/mo</p><p class="ss">Jan '25 vs May '26 · −81%. Free masses went 632 → 70 in the same comparison.</p></div>
</div>

<h2>Monthly revenue from masses (est. price × purchases)</h2>
<div class="card">{rev_chart}</div>

<h2>Median views per full-list send</h2>
<div class="card">{view_chart}</div>

<h2>Month by month</h2>
<div class="card mtable"><table>
<thead><tr><th>Month</th><th>Masses</th><th>Paid</th><th>Free</th><th>Est. rev</th><th>Buys</th><th>Median views</th></tr></thead>
<tbody>{table_rows}</tbody></table></div>

<h2>Top 10 earning masses (Jan '25 → Jun '26)</h2>
<div class="card">{top_rows}</div>

<h2>Same window, year over year — Jan 1 → Jun 3</h2>
<div class="stat-grid">
<div class="stat-card success"><p class="label">2025 · Jan 1–Jun 3</p><p class="big">${A25["rev"]:,.0f}</p><p class="sub">{A25["buys"]:,} buys · {A25["paid"]} paid masses</p></div>
<div class="stat-card amber"><p class="label">2026 · Jan 1–Jun 3</p><p class="big">${A26["rev"]:,.0f}</p><p class="sub"><span class="delta down">{yoy_delta:.0f}% YoY</span> · {A26["buys"]} buys · {A26["paid"]} paid</p></div>
<div class="stat-card info"><p class="label">May 2025</p><p class="big">${may25["rev"]:,.0f}</p><p class="sub">{may25["purch"]} buys · {may25["paid"]} paid masses</p></div>
<div class="stat-card amber"><p class="label">May 2026</p><p class="big">${may26["rev"]:,.0f}</p><p class="sub"><span class="delta down">{may_delta:.0f}% vs May '25</span> · {may26["purch"]} buys</p></div>
</div>
<div class="card" style="margin-top:12px;">{yoy_chart}</div>

<h2>Proof re-sends print money — 20 captions that sold again and again</h2>
<div class="card">{dup_rows}</div>
<div class="summary-box"><b>This is the cheapest revenue in the account.</b> These 20 recycled captions alone produced the totals on the right with zero new content — same caption, re-priced, re-sent weeks or months apart, and fans bought every time. The #1 group ("$2.50 A SCENE?!") earned $30,840 across 4 sends spanning Dec 31 '25 → Feb 12 '26, and its Memorial Day re-run on May 25 '26 still did $5,920. Any manager can be handed this list today.</div>

<h2>When paid masses actually sell — est. $ per paid send</h2>
<div class="callout-grid">
<div class="card"><p class="label" style="margin-bottom:8px;">By day of week</p>{dow_chart}</div>
<div class="card"><p class="label" style="margin-bottom:8px;">By time of day (PT)</p>{hour_chart}</div>
</div>

<h2>Price points that sell — revenue per paid send</h2>
<div class="card">{band_rows}</div>

<h2>2025 playbook vs. 2026 playbook</h2>
<div class="compare-grid">
<div class="compare win"><h4 style="color:var(--success-text);">What was working (2025)</h4><ul>
<li><b>Cheap volume bundles printed:</b> 53 sends under $10 did 18,019 buys and ~$94.1k est. — "SIX FOR $6 Monday Deal" alone did $5,922 in one send ($15,390 across 3 re-sends).</li>
<li><b>Event bundles were the heroes:</b> "$2.50 A SCENE?! 16 FULL scenes" at $40 did 529 buys / $21,160 on Dec 31; "BEST OF 2024 BUNDLE" $22 × 341 = $7,502 on Jan 1; "Besties Bundle 50% OFF Woman's Day" $20 × 297 = $5,940.</li>
<li><b>Heavy free engagement:</b> {free_day_25:.1f} free masses/day (4,688 in 2025) kept the list warm between paid drops — Jan '25 alone ran 632 free sends.</li>
<li><b>Median paid price ${medprice25:.0f},</b> only 4 sends all year priced $100+. Volume over long-shots.</li></ul></div>
<div class="compare lose"><h4 style="color:var(--amber-text);">What it drifted to (2026)</h4><ul>
<li><b>Volume drops nearly vanished:</b> under-$10 sends fell 53 → 16 (2,477 buys vs 18,019) while $100+ long-shots jumped 4 → 22 sends. Median paid price climbed to ${medprice26:.0f}.</li>
<li><b>Free cadence halved:</b> {free_day_25:.1f} → {free_day_26:.1f} free/day; May '26 ran only 70 free masses vs 514 in May '25. Total masses 130 vs 578.</li>
<li><b>More paid pressure on fewer touches:</b> paid sends up {paid_wk_25:.1f} → {paid_wk_26:.1f}/wk — paid share of all masses went 14% → 28%.</li>
<li><b>The winners that still work are recycled 2025 bundles:</b> the top 3 sends of 2026 are "$2.50 A SCENE" re-runs and "TOP HITS" flash sales ($8.6k–$9.1k each) — proof the old formula still converts when it's actually run.</li></ul></div>
</div>

<h2>Full mass message log — Jan 2025 → Jun 2026, newest first</h2>
<div class="card">
<div class="legend"><span><span class="dot" style="background:#97C459;"></span>Paid · $500+ earned</span><span><span class="dot" style="background:#85B7EB;"></span>Paid</span><span><span class="dot" style="background:rgba(255,255,255,0.25);"></span>Free / engagement</span></div>
<div class="log-wrap">
{log}
</div></div>

<h2>Why revenue is down despite flat mass money — for the manager/CFO conversation</h2>
<div class="warn-box"><b>The masses are holding the line; the relationship layer is not.</b> Mass-window est. revenue is {yoy_delta:+.1f}% YoY (${A25["rev"]:,.0f} → ${A26["rev"]:,.0f}) and OF-reported message revenue is only −3.7% — but subs + tips fell −$99,829 (−25.2%), which is 80% of Lucy's total −$124,838 decline. What changed in the data: free/engagement masses were cut from {free_day_25:.1f}/day to {free_day_26:.1f}/day (5,706 free sends total, but May '26 ran just 70), paid pressure rose to {paid_wk_26:.1f} sends/wk, median PPV price climbed ${medprice25:.0f} → ${medprice26:.0f}, and the cheap volume bundles that did 18,019 buys in 2025 were run only 16 times in 2026. Fans are getting asked for money more often and talked to less — that erodes subs and tips first, then buys ({A25["buys"]:,} → {A26["buys"]:,} in the same window, −21%).</div>

<h2>Read on the situation</h2>
<div class="warn-box"><b>Lucy's mass machine is not broken — but it's being run hotter on a cooling base.</b> March 2026 was actually the third-best est. month of the whole window ($88,667 on 100 paid sends, behind only Dec '25 $92,356 and Jan '25 $91,934) and the recycled 2025 bundles still print ($30,840 from one caption re-sent 4×). But total mass volume collapsed 699/mo (Jan '25) → 130/mo (May '26), buys per window fell −21%, and the −25.2% subs+tips bleed says the audience is disengaging. The fix isn't more PPV — it's restoring the free-touch cadence and the under-$10 volume drops that kept 18k buyers/window active in 2025.</div>
<div class="summary-box"><b>Where the money actually came from:</b> the biggest sends across the whole window were cheap, high-volume event bundles — "$2.50 A SCENE?!" $40 × 529 = $21,160 (Dec 31), "24 HOUR FLASH SALE OF MY TOP HITS" $40 × 228 = $9,118, "BEST OF 2024 BUNDLE" $22 × 341 = $7,502, "SIX FOR $6 Monday Deal" $6 × 987 = $5,922 — not the $100+ long-shots (22 sends in 2026 averaged just $462 each). The 2025 machine ran ~{free_day_25:.0f} free touches/day, priced at a ${medprice25:.0f} median, and re-sent proven winners on holidays. Estimated figures are price × recorded buys (OF nets out discounts/refunds), so treat month-level numbers as directional.</div>

<div class="footer">Your reputation matters · we keep the data honest so the work stays the focus</div>
</div>
</body></html>'''

open(OUT,"w",encoding="utf-8").write(html_doc)
print("written", OUT, len(html_doc), "bytes")
