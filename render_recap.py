#!/usr/bin/env python3
"""LRM Daily Earnings Recap renderer (generic, config-driven).

Usage:
    python3 render_recap.py <config.json> <out_basepath>

Writes <out_basepath>.gif (deliverable) and <out_basepath>.jpg (preview).

Matches the visual language of render_scorecard.py: dark LRM card, animated
count-up intro and a gentle bob loop. Instead of pillar scores it shows the
day's GROSS earnings, the day-over-day trend, and a messages-vs-tips breakdown.

config.json schema:
{
  "model": "Shantal",
  "sub": "Daily Recap  ·  June 18 2026",
  "gross_total": 1715.00,
  "prev_total": 1520.00,
  "messages_gross": 1310.00,
  "tips_gross": 405.00,
  "footer": "LIVERICHMEDIA  ·  DAILY RECAP  ·  JUN 18 2026"
}

Notes:
- All figures are GROSS dollars. messages_gross + tips_gross should equal
  gross_total (they reconcile); the breakdown bars are drawn from them.
- prev_total is the previous UTC day's gross total; the change chip and the
  day-over-day bars are derived from gross_total vs prev_total.
- change percent is computed automatically (no separate field to get wrong).
"""
import sys, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 840, 1220
F = "/usr/share/fonts/truetype/dejavu/"
def font(p, s): return ImageFont.truetype(F + p, s)
B = lambda s: font("DejaVuSans-Bold.ttf", s)
R = lambda s: font("DejaVuSans.ttf", s)
BG=(23,23,23); PANEL=(32,32,34); WHITE=(245,245,245)
MUTE=(150,150,154); FAINT=(112,112,116); BODY=(224,224,228); GOLD=(208,170,92)
GREEN=(60,200,120); AMBER=(239,159,39); RED=(226,75,74); TRACK=(54,54,58)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def money(v):
    return "$"+format(int(round(v)),",d")
def trend_colour(cur,prev):
    if prev<=0: return GREEN if cur>0 else MUTE
    if cur>prev*1.001: return GREEN
    if cur<prev*0.999: return RED
    return AMBER

def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_money_block(img,cx,cy,value,col,scale=1.0):
    bw,bh=int(300*scale),int(150*scale); depth=int(46*scale)
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
    num=money(value); fs=int(74*scale)
    nf=B(fs)
    while d.textlength(num,font=nf)>bw-40 and fs>28:
        fs-=3; nf=B(fs)
    nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-fs*0.62),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lw=d.textlength("GROSS",font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),"GROSS",font=lf,fill=shade(WHITE,0.85))

def hbar(d,x0,y,x1,frac,col,h=14):
    d.rounded_rectangle((x0,y,x1,y+h),radius=h//2,fill=TRACK)
    w=(x1-x0)*max(0.0,min(1.0,frac))
    if w>h: d.rounded_rectangle((x0,y,x0+w,y+h),radius=h//2,fill=col)

def render(cfg,disp_total,bar_frac,bob=0.0,scale=1.0,show_meta=True):
    gt=float(cfg["gross_total"]); pv=float(cfg.get("prev_total") or 0)
    msg=float(cfg.get("messages_gross") or 0); tip=float(cfg.get("tips_gross") or 0)
    tcol=trend_colour(gt,pv)
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_money_block(img,cx,384+int(bob),disp_total,tcol,scale=scale)
    d=ImageDraw.Draw(img,"RGBA")
    # change chip
    if pv>0:
        pct=(gt-pv)/pv*100.0
        arrow="▲" if pct>0.05 else ("▼" if pct<-0.05 else "▬")
        txt=f"{arrow} {abs(pct):.1f}%  vs day before"
    else:
        txt="new day  ·  no prior baseline"; pct=0
    cf=B(20); tw=d.textlength(txt,font=cf)
    center(d,cx,486,txt,cf,tcol)
    # panel
    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+520),radius=22,fill=PANEL)
    px=CARD_X0+44; bx1=CARD_X1-44
    yy=py0+34
    d.text((px,yy),"EARNINGS BREAKDOWN",font=B(18),fill=GOLD)
    denom=max(gt,msg+tip,1.0)
    yy+=52
    for label,val,col in [("Messages (gross)",msg,GOLD),("Tips (gross)",tip,GREEN)]:
        d.text((px,yy),label,font=B(20),fill=BODY)
        amt=money(val); af=B(20)
        d.text((bx1-d.textlength(amt,font=af),yy-1),amt,font=af,fill=col)
        share=(val/denom*100.0) if denom else 0
        d.text((bx1-d.textlength(f"{share:.0f}%",font=R(15))-0,yy+26),f"{share:.0f}%",font=R(15),fill=FAINT)
        hbar(d,px,yy+30,bx1-46,(val/denom)*bar_frac,col)
        yy+=84
    # divider
    yy+=6
    d.line([(px,yy),(bx1,yy)],fill=TRACK,width=2)
    yy+=22
    d.text((px,yy),"DAY OVER DAY",font=B(18),fill=GOLD)
    yy+=46
    dmax=max(gt,pv,1.0)
    for label,val,col in [("Yesterday",gt,tcol),("Day before",pv,FAINT)]:
        d.text((px,yy),label,font=R(19),fill=BODY)
        amt=money(val); af=B(19)
        d.text((bx1-d.textlength(amt,font=af),yy-1),amt,font=af,fill=col if col is not FAINT else MUTE)
        hbar(d,px,yy+30,bx1,(val/dmax)*bar_frac,col,h=16)
        yy+=76
    if show_meta:
        delta=money(abs(gt-pv)); sign="up" if gt>=pv else "down"
        meta=f"day over day {sign} {delta}  ·  gross before the 20% fee"
        center(d,cx,CARD_Y1-58,meta,R(15),FAINT)
    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gt=float(cfg["gross_total"])
    render(cfg,gt,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,gt*ease,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,gt,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
