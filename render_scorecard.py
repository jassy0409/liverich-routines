#!/usr/bin/env python3
"""LRM Chatter Scorecard renderer (generic, config-driven).

Usage:
    python3 render_scorecard.py <config.json> <out_basepath>

Writes <out_basepath>.gif and <out_basepath>.jpg (preview).

config.json schema:
{
  "name": "Alyzha",
  "sub": "Karina  \u00b7  Afternoon  \u00b7  June 24",
  "pillars": [
     ["Relationship building", 18],
     ["Value setting", 18],
     ["VIP funnel", 19],
     ["Avoids dead ends", 16]
  ],
  "overall": 71,
  "restricted": 0,
  "weakest": "Avoids dead ends",
  "threads": "threads read: TW \u00b7 VIP john  \u00b7  attribution by shift window",
  "footer": "LIVERICHMEDIA  \u00b7  CHATTER SCORECARD  \u00b7  JUN 24 AFTERNOON"
}

Pillar bar colour is derived automatically from each pillar's score using the
same thresholds as the overall block, so callers only supply label+score.
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

def colour_for(score):
    return GREEN if score>=80 else (AMBER if score>=65 else RED)
def pillar_colour(val):
    # pillar scored out of 25; scale to /100 equivalent for the same thresholds
    pct = val*4
    return GREEN if pct>=80 else (AMBER if pct>=65 else RED)
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
    lf=R(int(20*scale)); lw=d.textlength("/ 100",font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(30*scale)),"/ 100",font=lf,fill=shade(WHITE,0.85))

def render(cfg,score_val,bar_frac,restricted_val,bob=0.0,scale=1.0,show_meta=True):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"CHATTER SCORECARD",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["name"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,380+int(bob),score_val,scale=scale)
    d=ImageDraw.Draw(img); center(d,cx,476,"OVERALL",R(15),MUTE)
    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+340),radius=22,fill=PANEL)
    px=CARD_X0+44; yy=py0+40
    for label,val in cfg["pillars"]:
        col=pillar_colour(val)
        d.text((px,yy),label,font=B(20),fill=BODY)
        vf=B(22); sf=R(16)
        d.text((CARD_X1-44-d.textlength(str(val),font=vf)-d.textlength(" /25",font=sf),yy-2),str(val),font=vf,fill=col)
        d.text((CARD_X1-44-d.textlength(" /25",font=sf),yy+2)," /25",font=sf,fill=FAINT)
        by=yy+34; bx1=CARD_X1-44
        d.rounded_rectangle((px,by,bx1,by+10),radius=5,fill=TRACK)
        fillw=(bx1-px)*((val/25.0)*bar_frac)
        if fillw>6: d.rounded_rectangle((px,by,px+fillw,by+10),radius=5,fill=col)
        yy+=78
    cy0=py0+372; chip_h=96; cw=(CARD_X1-CARD_X0-18)//2
    d.rounded_rectangle((CARD_X0,cy0,CARD_X0+cw,cy0+chip_h),radius=18,fill=PANEL)
    d.text((CARD_X0+30,cy0+22),"RESTRICTED WORDS",font=R(15),fill=MUTE)
    d.text((CARD_X0+30,cy0+46),str(int(restricted_val)),font=B(34),fill=GREEN if restricted_val==0 else RED)
    wx0=CARD_X0+cw+18
    d.rounded_rectangle((wx0,cy0,CARD_X1,cy0+chip_h),radius=18,fill=PANEL)
    d.text((wx0+28,cy0+22),"WEAKEST LINK",font=R(15),fill=MUTE)
    d.text((wx0+28,cy0+48),cfg["weakest"],font=B(24),fill=RED)
    if show_meta:
        center(d,cx,CARD_Y1-58,cfg["threads"],R(15),FAINT)
    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_scorecard.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    ov=cfg["overall"]; rs=cfg["restricted"]
    render(cfg,ov,1.0,rs,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,ov*ease,ease,rs,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,ov,1.0,rs,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
