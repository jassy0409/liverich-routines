#!/usr/bin/env python3
"""LRM Handling Standards Alert renderer (incident dashboard, animated GIF).

Usage:
    python3 render_incident.py <config.json> <out_basepath>

Writes <out_basepath>.gif and <out_basepath>.jpg (preview).

Shares the visual language of render_scorecard.py (dark LRM card, gold accents),
but is an incident / standards report rather than a per-chatter scorecard.

config.json schema:
{
  "title": "HANDLING STANDARDS ALERT",
  "sub": "Karina VIP  ·  Thread: Seve  ·  July 2",
  "severity": "CRITICAL",                       # CRITICAL / HIGH / REVIEW
  "headline": "VIP charged above the mass rate",
  "case": "A VIP was charged 200 for a PPV set that non-VIPs received at 169 ...",
  "violations": ["...", "...", "..."],          # what went wrong
  "rules": ["...", "...", "..."],               # the non-negotiables
  "footer": "LIVERICHMEDIA  ·  HANDLING STANDARDS  ·  JUL 2"
}
"""
import sys, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 840, 1400
F = "/usr/share/fonts/truetype/dejavu/"
def font(p, s): return ImageFont.truetype(F + p, s)
B = lambda s: font("DejaVuSans-Bold.ttf", s)
R = lambda s: font("DejaVuSans.ttf", s)
BG=(23,23,23); PANEL=(32,32,34); WHITE=(245,245,245)
MUTE=(150,150,154); FAINT=(112,112,116); BODY=(224,224,228); GOLD=(208,170,92)
GREEN=(60,200,120); AMBER=(239,159,39); RED=(226,75,74); TRACK=(54,54,58)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

SEV_COL={"CRITICAL":RED,"HIGH":AMBER,"REVIEW":GOLD}

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)

def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(420,(46,28,28),150,120),(360,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_badge(img,cx,cy,sev,scale=1.0,pulse=0.0):
    col=SEV_COL.get(sev,RED)
    rw,rh=int(300*scale),int(66*scale)
    x0,y0=cx-rw//2,cy-rh//2
    glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    a=int(90+80*pulse)
    gd.rounded_rectangle((x0-8,y0-8,x0+rw+8,y0+rh+8),radius=rh//2+8,fill=col+(a,))
    glow=glow.filter(ImageFilter.GaussianBlur(16)); img.alpha_composite(glow)
    d=ImageDraw.Draw(img,"RGBA")
    d.rounded_rectangle((x0,y0,x0+rw,y0+rh),radius=rh//2,fill=shade(col,0.9))
    d.rounded_rectangle((x0,y0,x0+rw,y0+rh),radius=rh//2,outline=shade(col,1.35),width=2)
    lbl=sev+"  SEVERITY"; lf=B(int(26*scale)); lw=d.textlength(lbl,font=lf)
    d.text((cx-lw/2,cy-int(17*scale)),lbl,font=lf,fill=WHITE)

def draw_list(d,x0,y0,x1,title,items,marker_col,title_col):
    d.text((x0,y0),title,font=B(19),fill=title_col)
    yy=y0+40
    for it in items:
        d.ellipse((x0+2,yy+7,x0+12,yy+17),fill=marker_col)
        for i,ln in enumerate(wrap(d,it,R(20),x1-(x0+28))):
            d.text((x0+28,yy+i*28),ln,font=R(20),fill=BODY)
        yy+=28*max(1,len(wrap(d,it,R(20),x1-(x0+28))))+16
    return yy

def render(cfg,reveal=1.0,pulse=0.0):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=72; center(d,cx,y,cfg.get("title","HANDLING STANDARDS ALERT"),B(26),GOLD)
    y+=44; center(d,cx,y,cfg["sub"],R(19),MUTE)
    y+=64; draw_badge(img,cx,y+10,cfg.get("severity","CRITICAL"),pulse=pulse)
    d=ImageDraw.Draw(img,"RGBA")
    y+=70; center(d,cx,y,cfg.get("headline",""),B(24),WHITE)
    # case panel
    y+=52; ph=150
    d.rounded_rectangle((CARD_X0,y,CARD_X1,y+ph),radius=20,fill=PANEL)
    d.text((CARD_X0+34,y+22),"WHAT HAPPENED",font=B(16),fill=GOLD)
    cy=y+54
    for i,ln in enumerate(wrap(d,cfg["case"],R(20),CARD_X1-CARD_X0-68)):
        d.text((CARD_X0+34,cy+i*30),ln,font=R(20),fill=BODY)
    # violations panel
    y+=ph+26; vh=int(360*1)
    n=max(1,len(cfg["violations"]))
    d.rounded_rectangle((CARD_X0,y,CARD_X1,y+vh),radius=20,fill=PANEL)
    end=draw_list(d,CARD_X0+34,y+24,CARD_X1-34,"RULES IGNORED ON THIS THREAD",
                  cfg["violations"],RED,RED)
    # rules panel
    y+=vh+26; rh=int(330)
    d.rounded_rectangle((CARD_X0,y,CARD_X1,y+rh),radius=20,fill=PANEL)
    draw_list(d,CARD_X0+34,y+24,CARD_X1-34,"NON-NEGOTIABLE STANDARD GOING FORWARD",
              cfg["rules"],GREEN,GREEN)
    center(d,cx,CARD_Y1-30,cfg["footer"],B(16),GOLD)
    # reveal wipe from bottom
    if reveal<1.0:
        cut=int(CARD_Y0+(H-80)*reveal)
        ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
        od.rectangle((0,cut,W,H),fill=BG+(255,))
        for i in range(40):
            od.rectangle((0,cut-i,W,cut-i+1),fill=BG+(int(255*(i/40)),))
        img.alpha_composite(ov)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_incident.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    render(cfg,1.0,0.0).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=18
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,reveal=max(0.06,ease),pulse=0.0))
    for k in range(20):
        pulse=0.5+0.5*math.sin(k/20*2*math.pi)
        frames.append(render(cfg,reveal=1.0,pulse=pulse))
    durations=[55]*(steps+1)+[70]*20
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],
                   duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
