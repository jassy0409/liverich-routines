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

Trend colour, change percent, and the day-over-day bars are all derived
automatically from gross_total vs prev_total, so callers only supply the raw
figures.
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
    return f"${v:,.0f}"

def trend_colour(cur, prev):
    if prev <= 0: return GREEN if cur > 0 else AMBER
    if cur > prev: return GREEN
    if cur < prev: return RED
    return AMBER

def pct_change(cur, prev):
    if prev <= 0:
        return 0.0 if cur <= 0 else 100.0
    return (cur - prev) / prev * 100.0

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
    num=money(value)
    nf=B(int(58*scale)); nw=d.textlength(num,font=nf)
    while nw > bw-24 and nf.size>18:
        nf=B(nf.size-4); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(30*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lab="GROSS"; lw=d.textlength(lab,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),lab,font=lf,fill=shade(WHITE,0.85))

def render(cfg, cur_val, bar_frac, bob=0.0, scale=1.0):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    prev=cfg["prev_total"]; full=cfg["gross_total"]
    col=trend_colour(full,prev)
    pct=pct_change(full,prev)
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,380+int(bob),cur_val,col,scale=scale)
    d=ImageDraw.Draw(img); center(d,cx,476,"GROSS EARNINGS, TODAY",R(15),MUTE)

    chip_y=530; chip_h=64
    d.rounded_rectangle((CARD_X0,chip_y,CARD_X1,chip_y+chip_h),radius=18,fill=PANEL)
    if prev>0:
        arrow="▲" if full>prev else ("▼" if full<prev else "▪")
        chip_txt=f"{arrow} {abs(pct):.0f}% vs yesterday"
    else:
        chip_txt="first tracked day"
    center(d,cx,chip_y+18,chip_txt,B(22),col)

    bars_y0=chip_y+chip_h+26; bars_h=190
    d.rounded_rectangle((CARD_X0,bars_y0,CARD_X1,bars_y0+bars_h),radius=22,fill=PANEL)
    maxv=max(full,prev,1)
    bar_w=100; gap=70
    base_y=bars_y0+bars_h-34
    top_y=bars_y0+34
    x_prev=cx-gap//2-bar_w
    x_full=cx+gap//2
    ph=(base_y-top_y)*(prev/maxv)
    fh=(base_y-top_y)*(cur_val/maxv)
    d.rounded_rectangle((x_prev,base_y-ph,x_prev+bar_w,base_y),radius=8,fill=shade(MUTE,0.55))
    if fh>0: d.rounded_rectangle((x_full,base_y-fh,x_full+bar_w,base_y),radius=8,fill=col)
    center(d,x_prev+bar_w/2,base_y+10,"YESTERDAY",R(13),MUTE)
    center(d,x_full+bar_w/2,base_y+10,"TODAY",R(13),MUTE)
    center(d,x_prev+bar_w/2,(base_y-ph-24) if ph>20 else (base_y-24),money(prev),B(16),BODY)
    center(d,x_full+bar_w/2,(base_y-fh-24) if fh>20 else (base_y-24),money(cur_val),B(16),WHITE)

    msg=cfg["messages_gross"]; tips=cfg["tips_gross"]; subs=cfg.get("subs_gross",0)
    rows=[("Messages",msg,GOLD),("Tips",tips,shade(GOLD,0.62))]
    if subs: rows.append(("Subs",subs,shade(GOLD,0.4)))
    br_y0=bars_y0+bars_h+22; br_h=34+76*len(rows)+24
    d.rounded_rectangle((CARD_X0,br_y0,CARD_X1,br_y0+br_h),radius=22,fill=PANEL)
    px=CARD_X0+44; bx1=CARD_X1-44
    breakdown_total=max(msg+tips+subs,1)
    yy=br_y0+34
    for label,val,barcol in rows:
        d.text((px,yy),label,font=B(21),fill=BODY)
        vf=B(21); vs=money(val*bar_frac)
        d.text((bx1-d.textlength(vs,font=vf),yy),vs,font=vf,fill=WHITE)
        by=yy+32
        d.rounded_rectangle((px,by,bx1,by+12),radius=6,fill=TRACK)
        fillw=(bx1-px)*(val/breakdown_total)*bar_frac
        if fillw>6: d.rounded_rectangle((px,by,px+fillw,by+12),radius=6,fill=barcol)
        yy+=76

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    full=cfg["gross_total"]
    render(cfg,full,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,full*ease,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,full,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
