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

The day over day change percent, the trend colour (green up / red down /
amber flat), and the paired trend + breakdown bars are all derived
automatically from gross_total vs prev_total and messages_gross vs
tips_gross, so callers only supply raw dollar figures.
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

def fmt_money(x):
    if abs(x-round(x))<0.005:
        return "${:,.0f}".format(round(x))
    return "${:,.2f}".format(x)

def trend(gross_total,prev_total):
    if prev_total>0:
        pct=(gross_total-prev_total)/prev_total*100.0
    elif gross_total>0:
        pct=100.0
    else:
        pct=0.0
    if pct>0.5: col=GREEN; arrow="▲"
    elif pct<-0.5: col=RED; arrow="▼"
    else: col=AMBER; arrow="▪"
    return pct,col,arrow

def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_3d_block(img,cx,cy,dollar_val,block_col,scale=1.0):
    txt=fmt_money(dollar_val)
    nf=B(int(72*scale))
    tmp=ImageDraw.Draw(img)
    tw=tmp.textlength(txt,font=nf)
    bw=max(int(260*scale),int(tw+80*scale)); bh=int(150*scale); depth=int(46*scale)
    x0,y0=cx-bw//2,cy-bh//2
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    shy=cy+bh//2+depth+int(46*scale); sw=int(bw*0.9)
    sd.ellipse((cx-sw//2,shy-22,cx+sw//2,shy+22),fill=(0,0,0,150))
    sh=sh.filter(ImageFilter.GaussianBlur(18)); img.alpha_composite(sh)
    d=ImageDraw.Draw(img,"RGBA")
    top=shade(block_col,1.18); front=shade(block_col,0.82); side=shade(block_col,0.58)
    d.polygon([(x0,y0),(x0+bw,y0),(x0+bw+depth,y0-depth),(x0+depth,y0-depth)],fill=top)
    d.polygon([(x0+bw,y0),(x0+bw,y0+bh),(x0+bw+depth,y0+bh-depth),(x0+bw+depth,y0-depth)],fill=side)
    d.polygon([(x0,y0),(x0+bw,y0),(x0+bw,y0+bh),(x0,y0+bh)],fill=front)
    d.line([(x0,y0),(x0+bw,y0)],fill=shade(block_col,1.4),width=2)
    d.text((cx-tw/2,y0+bh/2-int(48*scale)),txt,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lab="GROSS"; lw=d.textlength(lab,font=lf)
    d.text((cx-lw/2,y0+bh/2+int(34*scale)),lab,font=lf,fill=shade(WHITE,0.85))

def render(cfg,gross_val,bar_frac,bob=0.0,scale=1.0):
    gross_total=cfg["gross_total"]; prev_total=cfg["prev_total"]
    messages_gross=cfg["messages_gross"]; tips_gross=cfg["tips_gross"]
    pct,tcol,arrow=trend(gross_total,prev_total)
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,380+int(bob),gross_val,tcol,scale=scale)
    d=ImageDraw.Draw(img); center(d,cx,476,"GROSS TODAY",R(15),MUTE)

    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+340),radius=22,fill=PANEL)
    px=CARD_X0+44; bx1=CARD_X1-44; yy=py0+34

    # day over day chip
    chip_txt=f"{arrow}  {abs(pct):.1f}%  DAY OVER DAY"
    d.text((px,yy),"DAY OVER DAY",font=B(20),fill=BODY)
    pf=B(22); ptxt=f"{arrow} {abs(pct):.1f}%"
    pw=d.textlength(ptxt,font=pf)
    d.text((bx1-pw,yy-2),ptxt,font=pf,fill=tcol)
    yy+=44

    # paired trend bars: yesterday vs today
    maxv=max(gross_total,prev_total,1)
    bar_h=26; gap=14
    labels=[("YESTERDAY",prev_total),("TODAY",gross_total)]
    for lab,val in labels:
        d.text((px,yy),lab,font=R(15),fill=MUTE)
        vtxt=fmt_money(val)
        d.text((bx1-d.textlength(vtxt,font=R(15)),yy),vtxt,font=R(15),fill=FAINT)
        by=yy+22
        d.rounded_rectangle((px,by,bx1,by+bar_h),radius=13,fill=TRACK)
        fillw=(bx1-px)*((val/maxv)*bar_frac)
        col=tcol if lab=="TODAY" else FAINT
        if fillw>6: d.rounded_rectangle((px,by,px+fillw,by+bar_h),radius=13,fill=col)
        yy+=bar_h+gap+26

    yy+=10
    d.line([(px,yy),(bx1,yy)],fill=TRACK,width=1)
    yy+=26

    # messages vs tips breakdown
    d.text((px,yy),"MESSAGES vs TIPS",font=B(20),fill=BODY)
    yy+=34
    total=max(messages_gross+tips_gross,0.01)
    msg_pct=messages_gross/total*100.0; tip_pct=tips_gross/total*100.0
    seg_h=30
    bw_full=bx1-px
    msg_w=bw_full*(msg_pct/100.0)*bar_frac
    tip_w=bw_full*(tip_pct/100.0)*bar_frac
    d.rounded_rectangle((px,yy,bx1,yy+seg_h),radius=15,fill=TRACK)
    if msg_w>4:
        d.rounded_rectangle((px,yy,px+msg_w,yy+seg_h),radius=15,fill=GOLD)
    if tip_w>4:
        d.rounded_rectangle((bx1-tip_w,yy,bx1,yy+seg_h),radius=15,fill=(90,150,220))
    yy+=seg_h+18
    mtxt=f"Messages ({msg_pct:.0f}%)"
    ttxt=f"Tips ({tip_pct:.0f}%)"
    d.text((px,yy),mtxt,font=R(16),fill=GOLD)
    twd=d.textlength(ttxt,font=R(16))
    d.text((bx1-twd,yy),ttxt,font=R(16),fill=(120,170,230))

    cy0=py0+372; chip_h=96; cw=(CARD_X1-CARD_X0-18)//2
    d.rounded_rectangle((CARD_X0,cy0,CARD_X0+cw,cy0+chip_h),radius=18,fill=PANEL)
    d.text((CARD_X0+30,cy0+22),"MESSAGES GROSS",font=R(15),fill=MUTE)
    d.text((CARD_X0+30,cy0+46),fmt_money(messages_gross),font=B(30),fill=GOLD)
    wx0=CARD_X0+cw+18
    d.rounded_rectangle((wx0,cy0,CARD_X1,cy0+chip_h),radius=18,fill=PANEL)
    d.text((wx0+28,cy0+22),"TIPS GROSS",font=R(15),fill=MUTE)
    d.text((wx0+28,cy0+46),fmt_money(tips_gross),font=B(30),fill=(120,170,230))

    center(d,cx,CARD_Y1-58,"8am PHT to 8am PHT  ·  UTC calendar day",R(15),FAINT)
    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gt=cfg["gross_total"]
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
