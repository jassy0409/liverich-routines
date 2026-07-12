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

The day over day change percent, trend colour (green up / red down / amber
flat), and the paired trend bars are all derived automatically from
gross_total vs prev_total. messages_gross + tips_gross should reconcile to
gross_total.
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

def money(v):
    return "${:,.0f}".format(v)

def pct_change(gross, prev):
    if prev == 0:
        return 0.0 if gross == 0 else 100.0
    return (gross - prev) / prev * 100.0

def trend_colour(gross, prev):
    pct = pct_change(gross, prev)
    if abs(pct) < 0.5:
        return AMBER
    return GREEN if pct > 0 else RED

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
    num=money(value)
    nf=B(int(64*scale)); nw=d.textlength(num,font=nf)
    while nw > bw-24 and nf.size>28:
        nf=B(nf.size-4); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(46*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lab="GROSS TODAY"; lw=d.textlength(lab,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),lab,font=lf,fill=shade(WHITE,0.85))

def render(cfg,ease,bob=0.0,scale=1.0):
    gross=cfg["gross_total"]; prev=cfg["prev_total"]
    col=trend_colour(gross,prev); pct=pct_change(gross,prev)
    cur_val = gross*ease
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_money_block(img,cx,380+int(bob),cur_val,col,scale=scale)
    d=ImageDraw.Draw(img)

    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+210),radius=22,fill=PANEL)
    d.text((CARD_X0+30,py0+26),"DAY OVER DAY",font=R(15),fill=MUTE)
    if abs(pct) < 0.5:
        chip="FLAT"
    elif pct>0:
        chip="UP {:.1f}%".format(pct)
    else:
        chip="DOWN {:.1f}%".format(abs(pct))
    chip_f=B(26); chip_w=d.textlength(chip,font=chip_f)
    d.rounded_rectangle((CARD_X1-30-chip_w-28,py0+16,CARD_X1-30,py0+16+42),radius=14,fill=shade(col,0.28))
    d.text((CARD_X1-30-chip_w-14,py0+22),chip,font=chip_f,fill=col)

    maxv=max(prev,gross,1)
    bar_top=py0+92; bar_h=54; gap=24
    bw_area=(CARD_X1-CARD_X0-30-gap)//2
    labels=[("YESTERDAY",prev,CARD_X0+30),("TODAY",gross,CARD_X0+30+bw_area+gap)]
    for label,val,bx in labels:
        d.text((bx,bar_top),label,font=R(15),fill=MUTE)
        vf=B(22); vt=money(val)
        d.text((bx,bar_top+22),vt,font=vf,fill=BODY)
        track_y=bar_top+58; track_h=14
        d.rounded_rectangle((bx,track_y,bx+bw_area,track_y+track_h),radius=7,fill=TRACK)
        frac=(val/maxv)*ease
        fillw=bw_area*frac
        if fillw>8:
            barcol = col if val==gross else shade(col,0.6)
            d.rounded_rectangle((bx,track_y,bx+fillw,track_y+track_h),radius=7,fill=barcol)

    py1=py0+210+18
    d.rounded_rectangle((CARD_X0,py1,CARD_X1,py1+210),radius=22,fill=PANEL)
    d.text((CARD_X0+30,py1+26),"MESSAGES VS TIPS",font=R(15),fill=MUTE)
    msg=cfg["messages_gross"]; tips=cfg["tips_gross"]; total=max(msg+tips,1)
    rows=[("MESSAGES",msg,GOLD),("TIPS",tips,shade(GOLD,0.75))]
    ry=py1+70
    for label,val,rc in rows:
        pct_of = val/total*100.0
        d.text((CARD_X0+30,ry),label,font=B(18),fill=BODY)
        vt="{}  ({:.0f}%)".format(money(val),pct_of)
        vw=d.textlength(vt,font=R(16))
        d.text((CARD_X1-30-vw,ry+2),vt,font=R(16),fill=MUTE)
        track_y=ry+30; track_h=12
        d.rounded_rectangle((CARD_X0+30,track_y,CARD_X1-30,track_y+track_h),radius=6,fill=TRACK)
        fillw=(CARD_X1-30-(CARD_X0+30))*(pct_of/100.0)*ease
        if fillw>6:
            d.rounded_rectangle((CARD_X0+30,track_y,CARD_X0+30+fillw,track_y+track_h),radius=6,fill=rc)
        ry+=68

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gm = cfg["messages_gross"]+cfg["tips_gross"]
    if abs(gm - cfg["gross_total"]) > 1:
        print("warning: messages_gross + tips_gross (%s) does not reconcile with gross_total (%s)" % (gm, cfg["gross_total"]))
    render(cfg,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
