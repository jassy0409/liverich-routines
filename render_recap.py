#!/usr/bin/env python3
"""LRM Daily Earnings Recap renderer (generic, config-driven).

Usage:
    python3 render_recap.py <config.json> <out_basepath>

Writes <out_basepath>.gif and <out_basepath>.jpg (preview).

config.json schema:
{
  "model": "Shantal",
  "sub": "July 17 2026",
  "gross_total": 2258.94,
  "prev_total": 1333.94,
  "messages_gross": 1793.94,
  "tips_gross": 465.00,
  "footer": "LIVERICHMEDIA  ·  DAILY RECAP  ·  JUL 17 2026"
}

Trend colour (green up / red down / amber flat), change percent, and the
day over day bar heights are all derived from gross_total vs prev_total,
so callers only supply the raw dollar figures.
"""
import sys, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 840, 1100
F = "/usr/share/fonts/truetype/dejavu/"
def font(p, s): return ImageFont.truetype(F + p, s)
B = lambda s: font("DejaVuSans-Bold.ttf", s)
R = lambda s: font("DejaVuSans.ttf", s)
BG=(23,23,23); PANEL=(32,32,34); WHITE=(245,245,245)
MUTE=(150,150,154); FAINT=(112,112,116); BODY=(224,224,228); GOLD=(208,170,92)
GREEN=(60,200,120); AMBER=(239,159,39); RED=(226,75,74); TRACK=(54,54,58)
BLUE=(90,150,230); PINK=(214,110,170)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def trend_colour(pct):
    if pct > 0.5: return GREEN
    if pct < -0.5: return RED
    return AMBER
def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def money(v, cents=False):
    v = round(v, 2)
    if cents:
        s = f"{abs(v):,.2f}"
    else:
        s = f"{abs(int(round(v))):,}"
    return ("-$" if v < 0 else "$") + s

def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_3d_block(img,cx,cy,value,col,scale=1.0):
    bw,bh=int(230*scale),int(150*scale); depth=int(46*scale)
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
    num=money(value); fs=int(64*scale) if len(num)<=7 else int(52*scale)
    nf=B(fs); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(52*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lt="GROSS TODAY"; lw=d.textlength(lt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(32*scale)),lt,font=lf,fill=shade(WHITE,0.85))

def render(cfg,val,ease,bob=0.0,scale=1.0):
    gross=cfg["gross_total"]; prev=cfg["prev_total"]
    pct = 0.0 if prev==0 else (gross-prev)/prev*100.0
    col = trend_colour(pct)
    msg_g=cfg["messages_gross"]; tip_g=cfg["tips_gross"]
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,382+int(bob),val,col,scale=scale)
    d=ImageDraw.Draw(img)
    arrow = "▲" if pct>0.5 else ("▼" if pct<-0.5 else "▸")
    chip_txt=f"{arrow} {abs(pct):.1f}% day over day"
    cf=B(22); ctw=d.textlength(chip_txt,font=cf)
    chip_w=ctw+64; chip_h=48; chip_x0=cx-chip_w/2; chip_y0=486
    d.rounded_rectangle((chip_x0,chip_y0,chip_x0+chip_w,chip_y0+chip_h),radius=chip_h/2,fill=shade(col,0.24))
    center(d,cx,chip_y0+11,chip_txt,cf,col)

    py0=560
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+220),radius=22,fill=PANEL)
    d.text((CARD_X0+30,py0+24),"DAY OVER DAY",font=R(15),fill=MUTE)
    bar_area_y0=py0+64; bar_area_y1=py0+190; bar_max=bar_area_y1-bar_area_y0
    labels=[("YESTERDAY",prev,FAINT),("TODAY",gross,col)]
    bw=140; gap=90
    total_w=bw*2+gap; start_x=cx-total_w/2
    hi=max(gross,prev,1)
    for i,(lab,v,c) in enumerate(labels):
        bx0=start_x+i*(bw+gap); bx1=bx0+bw
        h=bar_max*ease*(v/hi if hi>0 else 0)
        by1=bar_area_y1; by0=by1-h
        d.rounded_rectangle((bx0,bar_area_y0,bx1,bar_area_y1),radius=10,fill=TRACK)
        if h>6: d.rounded_rectangle((bx0,by0,bx1,by1),radius=10,fill=c)
        vf=B(20); vt=money(v); vw=d.textlength(vt,font=vf)
        d.text((bx0+bw/2-vw/2,by0-30 if h>30 else bar_area_y0-30),vt,font=vf,fill=WHITE)
        lf=R(14); lw=d.textlength(lab,font=lf)
        d.text((bx0+bw/2-lw/2,bar_area_y1+10),lab,font=lf,fill=MUTE)

    qy0=py0+244; qh=200
    d.rounded_rectangle((CARD_X0,qy0,CARD_X1,qy0+qh),radius=22,fill=PANEL)
    d.text((CARD_X0+30,qy0+24),"MESSAGES VS TIPS",font=R(15),fill=MUTE)
    rows=[("Messages",msg_g,BLUE),("Tips",tip_g,PINK)]
    ry=qy0+64; track_x0=CARD_X0+30; track_x1=CARD_X1-30
    denom = max(gross,0.01)
    for lab,v,c in rows:
        d.text((track_x0,ry),lab,font=B(18),fill=BODY)
        vt=money(v,cents=True); vf=B(18); vw=d.textlength(vt,font=vf)
        d.text((track_x1-vw,ry),vt,font=vf,fill=c)
        by=ry+30
        d.rounded_rectangle((track_x0,by,track_x1,by+12),radius=6,fill=TRACK)
        frac=min(1.0,(v/denom))*ease
        fw=(track_x1-track_x0)*frac
        if fw>6: d.rounded_rectangle((track_x0,by,track_x0+fw,by+12),radius=6,fill=c)
        ry+=64

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gross=cfg["gross_total"]
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
