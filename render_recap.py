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
gross_total vs prev_total.
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
FLAT_EPS = 1.0  # percent band treated as "flat"

def money(v):
    if abs(v - round(v)) < 0.005:
        return "${:,.0f}".format(round(v))
    return "${:,.2f}".format(v)

def trend(gross_total, prev_total):
    if prev_total > 0:
        pct = (gross_total - prev_total) / prev_total * 100.0
    elif gross_total > 0:
        pct = 100.0
    else:
        pct = 0.0
    if abs(pct) < FLAT_EPS:
        col = AMBER; arrow = "→"
    elif pct > 0:
        col = GREEN; arrow = "↑"
    else:
        col = RED; arrow = "↓"
    return pct, col, arrow

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

def draw_3d_block(img,cx,cy,value,col,scale=1.0):
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
    num=money(value); nf=B(int(58*scale)); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(48*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lt="GROSS TODAY"; lw=d.textlength(lt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),lt,font=lf,fill=shade(WHITE,0.85))

def render(cfg,value_val,bar_frac,bob=0.0,scale=1.0):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    gross=cfg["gross_total"]; prev=cfg["prev_total"]
    pct,col,arrow = trend(gross,prev)
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,378+int(bob),value_val,col,scale=scale)
    d=ImageDraw.Draw(img)

    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+150),radius=22,fill=PANEL)
    center(d,cx,py0+22,"DAY OVER DAY",R(15),MUTE)
    chip_txt=f"{arrow} {abs(pct):.1f}%"
    center(d,cx,py0+48,chip_txt,B(34),col)
    bx0=CARD_X0+44; bx1=CARD_X1-44; by=py0+112
    maxv=max(gross,prev,1)
    bar_w=(bx1-bx0-16)//2
    prev_h=int(24*(prev/maxv))*bar_frac if maxv else 0
    curr_h=int(24*(gross/maxv))*bar_frac if maxv else 0
    d.rounded_rectangle((bx0,by,bx0+bar_w,by+24),radius=6,fill=TRACK)
    if prev_h>4: d.rounded_rectangle((bx0,by+24-prev_h,bx0+bar_w,by+24),radius=6,fill=shade(MUTE,1.0))
    d.rounded_rectangle((bx0+bar_w+16,by,bx1,by+24),radius=6,fill=TRACK)
    if curr_h>4: d.rounded_rectangle((bx0+bar_w+16,by+24-curr_h,bx1,by+24),radius=6,fill=col)
    d.text((bx0,by-24),f"YESTERDAY  {money(prev)}",font=R(14),fill=FAINT)
    d.text((bx0+bar_w+16,by-24),f"TODAY  {money(gross)}",font=R(14),fill=FAINT)

    py1=py0+150+18
    msg=cfg["messages_gross"]; tips=cfg["tips_gross"]
    total=max(msg+tips,1)
    d.rounded_rectangle((CARD_X0,py1,CARD_X1,py1+220),radius=22,fill=PANEL)
    center(d,cx,py1+24,"MESSAGES VS TIPS",R(15),MUTE)
    barx0=CARD_X0+44; barx1=CARD_X1-44; bary=py1+70; barh=28
    msg_frac=(msg/total)*bar_frac
    tips_frac=(tips/total)*bar_frac
    d.rounded_rectangle((barx0,bary,barx1,bary+barh),radius=10,fill=TRACK)
    msg_w=(barx1-barx0)*msg_frac
    tips_w=(barx1-barx0)*tips_frac
    if msg_w>4:
        d.rounded_rectangle((barx0,bary,barx0+msg_w,bary+barh),radius=10,fill=GOLD)
    if tips_w>4:
        d.rounded_rectangle((barx0+msg_w,bary,barx0+msg_w+tips_w,bary+barh),radius=10,fill=(94,150,214))
    ly=bary+barh+28
    d.ellipse((barx0,ly,barx0+14,ly+14),fill=GOLD)
    d.text((barx0+22,ly-3),f"Messages  {money(msg)}",font=B(19),fill=BODY)
    ly2=ly+40
    d.ellipse((barx0,ly2,barx0+14,ly2+14),fill=(94,150,214))
    d.text((barx0+22,ly2-3),f"Tips  {money(tips)}",font=B(19),fill=BODY)

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gross=cfg["gross_total"]
    msg_check = cfg["messages_gross"] + cfg["tips_gross"]
    if abs(msg_check - gross) > 0.5:
        print(f"WARNING: messages_gross + tips_gross ({msg_check}) does not reconcile with gross_total ({gross})")
    render(cfg,gross,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,gross*ease,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,gross,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
