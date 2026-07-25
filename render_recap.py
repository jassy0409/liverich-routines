#!/usr/bin/env python3
"""LRM Daily Earnings Recap renderer (generic, config-driven).

Usage:
    python3 render_recap.py <config.json> <out_basepath>

Writes <out_basepath>.gif and <out_basepath>.jpg (preview).

config.json schema:
{
  "model": "Shantal",
  "sub": "June 18 2026",
  "gross_total": 1715,
  "prev_total": 1520,
  "messages_gross": 1310,
  "tips_gross": 405,
  "footer": "LIVERICHMEDIA  ·  DAILY RECAP  ·  JUN 18 2026"
}

messages_gross + tips_gross should reconcile to gross_total. The day over day
change percent, trend colour (green up / red down / amber flat), and the
paired trend bars are all derived automatically from gross_total vs
prev_total.
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
BLUE=(90,150,230); PINK=(224,110,160)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def money(v):
    return "${:,.2f}".format(v)

def money_short(v):
    return "${:,.0f}".format(v)

def trend_colour(cur,prev):
    if abs(cur-prev)<0.005: return AMBER
    return GREEN if cur>prev else RED

def pct_change(cur,prev):
    if prev<=0.005:
        return None
    return (cur-prev)/prev*100.0

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_3d_block(img,cx,cy,val,col,scale=1.0):
    bw,bh=int(280*scale),int(150*scale); depth=int(46*scale)
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
    num=money_short(val); nf=B(int(66*scale))
    nw=d.textlength(num,font=nf)
    while nw>bw-24 and nf.size>28:
        nf=B(nf.size-4); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(30*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lt="GROSS TODAY"; lw=d.textlength(lt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(38*scale)),lt,font=lf,fill=shade(WHITE,0.85))

def render(cfg,gross_val,bar_frac,bob=0.0,scale=1.0,show_meta=True):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    prev=cfg["prev_total"]; total=cfg["gross_total"]
    col=trend_colour(total,prev)
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,380+int(bob),gross_val,col,scale=scale)
    d=ImageDraw.Draw(img); center(d,cx,476,"GROSS EARNINGS",R(15),MUTE)

    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+180),radius=22,fill=PANEL)
    px=CARD_X0+44; yy=py0+34
    d.text((px,yy),"DAY OVER DAY",font=B(18),fill=BODY)
    pct=pct_change(total,prev)
    if pct is None:
        chip_txt = "NEW" if total>0.005 else "FLAT"
        chip_col = GREEN if total>0.005 else AMBER
    else:
        arrow = "▲" if total>prev else ("▼" if total<prev else "▬")
        chip_txt=f"{arrow} {abs(pct):.1f}%"
        chip_col = col
    cf=B(22); cw=d.textlength(chip_txt,font=cf)
    d.rounded_rectangle((CARD_X1-44-cw-28,yy-8,CARD_X1-44,yy-8+38),radius=19,fill=shade(chip_col,0.22))
    d.text((CARD_X1-44-cw-14,yy),chip_txt,font=cf,fill=chip_col)

    by=yy+56; bh_max=64; bar_gap=18
    bar_w=(CARD_X1-CARD_X0-88-bar_gap)//2
    maxv=max(prev,total,0.01)
    prev_h=int(bh_max*(prev/maxv)*bar_frac)
    cur_h=int(bh_max*(total/maxv)*bar_frac)
    bx0=px
    d.rounded_rectangle((bx0,by+bh_max-prev_h,bx0+bar_w,by+bh_max),radius=8,fill=shade(MUTE,0.9))
    d.text((bx0,by+bh_max+8),"YESTERDAY",font=R(14),fill=FAINT)
    d.text((bx0,by+bh_max-prev_h-24 if prev_h>20 else by+bh_max-prev_h-24),money_short(prev),font=B(16),fill=MUTE)
    bx1=bx0+bar_w+bar_gap
    d.rounded_rectangle((bx1,by+bh_max-cur_h,bx1+bar_w,by+bh_max),radius=8,fill=col)
    d.text((bx1,by+bh_max+8),"TODAY",font=R(14),fill=FAINT)
    d.text((bx1,by+bh_max-cur_h-24 if cur_h>20 else by+bh_max-cur_h-24),money_short(total),font=B(16),fill=col)

    my0=py0+210; mh=200
    d.rounded_rectangle((CARD_X0,my0,CARD_X1,my0+mh),radius=22,fill=PANEL)
    d.text((px,my0+30),"MESSAGES VS TIPS",font=B(18),fill=BODY)
    msg=cfg["messages_gross"]; tips=cfg["tips_gross"]; tot=max(msg+tips,0.01)
    rowy=my0+74
    for label,val,barcol in [("Messages",msg,BLUE),("Tips",tips,PINK)]:
        pct_of=val/tot*100.0
        d.text((px,rowy),label,font=R(18),fill=BODY)
        vf=B(20); vt=money(val); vw=d.textlength(vt,font=vf)
        d.text((CARD_X1-44-vw,rowy-2),vt,font=vf,fill=WHITE)
        by2=rowy+30; bx1b=CARD_X1-44
        d.rounded_rectangle((px,by2,bx1b,by2+12),radius=6,fill=TRACK)
        fillw=(bx1b-px)*((pct_of/100.0)*bar_frac)
        if fillw>6: d.rounded_rectangle((px,by2,px+fillw,by2+12),radius=6,fill=barcol)
        d.text((px,by2+18),f"{pct_of:.0f}% of gross",font=R(13),fill=FAINT)
        rowy+=68

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    total=cfg["gross_total"]
    render(cfg,total,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,total*ease,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,total,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
