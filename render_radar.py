#!/usr/bin/env python3
"""LRM Creative Radar renderer (generic, config-driven).

A weekly content-planning dashboard card in the same dark LRM visual language
as the chatter scorecard: gold accents, a 3D "peak moment" block, a rounded
panel of tracked moments each with a fit bar, and two summary chips.

Usage:
    python3 render_radar.py <config.json> <out_basepath>

Writes <out_basepath>.gif (deliverable) and <out_basepath>.jpg (preview).

config.json schema:
{
  "name": "Karina",
  "sub": "Week of Jul 13–19  ·  Pacific",
  "hero_label": "PEAK MOMENT",
  "hero_score": 94,
  "hero_caption": "World Cup Final  ·  Sun 12pm PT",
  "events": [
     ["UFC Fight Night", "Ringside glam robe walkout", "SAT 5PM", 95],
     ["World Cup Final", "Jersey fit, couch watch party", "SUN 12PM", 94]
  ],
  "toppick": "UFC + World Cup weekend",
  "window": "Go live ~15 min pre-kickoff",
  "footer": "LIVERICHMEDIA  ·  CREATIVE RADAR  ·  JUL 13–19"
}

Each event is [label, shoot-hook, date-chip, fit 0-100]. The fit bar colour is
derived automatically from the fit score using the same thresholds as the
scorecard (>=80 green, 65-79 amber, <65 red), so callers only supply the score.
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

def colour_for(score):
    return GREEN if score>=80 else (AMBER if score>=65 else RED)
def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def ellipsize(d,t,f,maxw):
    if d.textlength(t,font=f)<=maxw: return t
    while t and d.textlength(t+"…",font=f)>maxw: t=t[:-1]
    return t+"…"
def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(400,(30,46,36),150,120),(360,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img
def draw_3d_block(img,cx,cy,score,scale=1.0):
    col=colour_for(score)
    bw,bh=int(190*scale),int(150*scale); depth=int(46*scale)
    x0,y0=cx-bw//2,cy-bh//2
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    shy=cy+bh//2+depth+int(46*scale); sw=int(bw*0.9)
    sd.ellipse((cx-sw//2,shy-22,cx+sw//2,shy+22),fill=(0,0,0,150))
    sh=sh.filter(ImageFilter.GaussianBlur(18)); img.alpha_composite(sh)
    d=ImageDraw.Draw(img,"RGBA")
    top=shade(col,1.18); front=shade(col,0.82); side=shade(col,0.58)
    d.polygon([(x0,y0),(x0+bw,y0),(x0+bw+depth,y0-depth),(x0+depth,y0-depth)],fill=top)
    d.polygon([(x0+bw,y0),(x0+bw,y0+bh),(x0+bw+depth,y0+bh-depth),(x0+bw+depth,y0-depth)],fill=side)
    d.polygon([(x0,y0),(x0+bw,y0),(x0+bw,y0+bh),(x0,y0+bh)],fill=front)
    d.line([(x0,y0),(x0+bw,y0)],fill=shade(col,1.4),width=2)
    num=str(int(round(score))); nf=B(int(82*scale)); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(56*scale)),num,font=nf,fill=WHITE)
    lf=R(int(20*scale)); lw=d.textlength("fit / 100",font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(30*scale)),"fit / 100",font=lf,fill=shade(WHITE,0.85))

def render(cfg,hero_val,bar_frac,bob=0.0,scale=1.0):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"CREATIVE RADAR",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["name"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,378+int(bob),hero_val,scale=scale)
    d=ImageDraw.Draw(img)
    center(d,cx,470,cfg.get("hero_label","PEAK MOMENT"),R(15),MUTE)
    center(d,cx,494,cfg.get("hero_caption",""),B(20),GOLD)
    # moments panel
    events=cfg["events"]
    row_h=88; pad_top=40; pad_bot=28
    ph=pad_top+row_h*len(events)-16+pad_bot
    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+ph),radius=22,fill=PANEL)
    px=CARD_X0+40; yy=py0+pad_top; bx1=CARD_X1-40
    for label,hook,date,fit in events:
        col=colour_for(fit)
        # date chip on the right
        cf=B(14); cw=d.textlength(date,font=cf)+28; ch=26
        cxr0=bx1-cw; d.rounded_rectangle((cxr0,yy-2,bx1,yy-2+ch),radius=13,fill=(46,46,50))
        d.text((cxr0+14,yy+3),date,font=cf,fill=GOLD)
        # event label + fit value
        vf=B(18); vw=d.textlength(str(fit),font=vf)
        lbl=ellipsize(d,label,B(21),cxr0-px-70)
        d.text((px,yy-2),lbl,font=B(21),fill=WHITE)
        d.text((cxr0-14-vw,yy+30),str(fit),font=vf,fill=col)
        # shoot hook subline
        d.text((px,yy+28),ellipsize(d,hook,R(15),cxr0-px-60),font=R(15),fill=MUTE)
        # fit bar
        by=yy+56
        d.rounded_rectangle((px,by,bx1,by+8),radius=4,fill=TRACK)
        fillw=(bx1-px)*((fit/100.0)*bar_frac)
        if fillw>6: d.rounded_rectangle((px,by,px+fillw,by+8),radius=4,fill=col)
        yy+=row_h
    # summary chips
    cy0=py0+ph+22; chip_h=100; cw=(CARD_X1-CARD_X0-18)//2
    d.rounded_rectangle((CARD_X0,cy0,CARD_X0+cw,cy0+chip_h),radius=18,fill=PANEL)
    d.text((CARD_X0+28,cy0+22),"TOP PICK",font=R(15),fill=MUTE)
    for i,line in enumerate(wrap(d,cfg.get("toppick",""),B(19),cw-52)[:2]):
        d.text((CARD_X0+28,cy0+46+i*24),line,font=B(19),fill=GREEN)
    wx0=CARD_X0+cw+18
    d.rounded_rectangle((wx0,cy0,CARD_X1,cy0+chip_h),radius=18,fill=PANEL)
    d.text((wx0+26,cy0+22),"GO-LIVE WINDOW",font=R(15),fill=MUTE)
    for i,line in enumerate(wrap(d,cfg.get("window",""),B(19),cw-52)[:2]):
        d.text((wx0+26,cy0+46+i*24),line,font=B(19),fill=GOLD)
    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

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

def main():
    if len(sys.argv)<3:
        print("usage: render_radar.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    hv=cfg["hero_score"]
    render(cfg,hv,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,hv*ease,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,hv,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
