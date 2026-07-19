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

messages_gross + tips_gross must reconcile to gross_total. prev_total is the
previous UTC day's gross total. The day over day change percent, trend
colour (green up / red down / amber flat), and the paired trend bars are all
derived automatically from gross_total vs prev_total.
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

def trend(gross_total, prev_total):
    if prev_total and prev_total > 0:
        pct = (gross_total - prev_total) / prev_total * 100
    else:
        pct = 100.0 if gross_total > 0 else 0.0
    if pct > 0.5: return pct, GREEN, "UP"
    if pct < -0.5: return pct, RED, "DOWN"
    return pct, AMBER, "FLAT"

def money(v):
    return "${:,.2f}".format(v)

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def right(d,x,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((x-w,y),t,font=f,fill=fill)
def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_3d_block(img,cx,cy,amount_val,col,scale=1.0):
    label=money(amount_val)
    bf=B(int(78*scale)); tmp=ImageDraw.Draw(Image.new("RGB",(1,1)))
    lw=tmp.textlength(label,font=bf)
    bw=int(max(230,lw+70)*scale); bh=int(150*scale); depth=int(46*scale)
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
    nw=d.textlength(label,font=bf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(52*scale)),label,font=bf,fill=WHITE)
    lf=R(int(18*scale)); ltxt="GROSS TODAY"; lw2=d.textlength(ltxt,font=lf)
    d.text((x0+bw/2-lw2/2,y0+bh/2+int(32*scale)),ltxt,font=lf,fill=shade(WHITE,0.85))

def render(cfg,amount_val,bar_frac,bob=0.0,scale=1.0):
    gross_total=cfg["gross_total"]; prev_total=cfg["prev_total"]
    messages_gross=cfg["messages_gross"]; tips_gross=cfg["tips_gross"]
    pct,tcol,_=trend(gross_total,prev_total)
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,380+int(bob),amount_val,tcol,scale=scale)
    d=ImageDraw.Draw(img)

    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+340),radius=22,fill=PANEL)
    px=CARD_X0+44; bx1=CARD_X1-44; yy=py0+38

    d.text((px,yy),"DAY OVER DAY",font=B(20),fill=BODY)
    arrow = "▲" if pct>0.5 else ("▼" if pct<-0.5 else "→")
    pct_txt=f"{arrow} {abs(pct):.1f}%"
    right(d,bx1,yy-2,pct_txt,B(22),tcol)
    yy+=42
    maxv=max(prev_total,gross_total,1)
    bar_h=26; gap=14
    for lbl,val,base_col in [("YESTERDAY",prev_total,FAINT),("TODAY",gross_total,tcol)]:
        d.text((px,yy),lbl,font=R(16),fill=MUTE)
        vtxt=money(val)
        right(d,bx1,yy-2,vtxt,R(18),BODY)
        by=yy+22
        d.rounded_rectangle((px,by,bx1,by+bar_h),radius=8,fill=TRACK)
        fillw=(bx1-px)*((val/maxv)*bar_frac)
        col = base_col if lbl=="YESTERDAY" else tcol
        if fillw>6: d.rounded_rectangle((px,by,px+fillw,by+bar_h),radius=8,fill=col)
        yy=by+bar_h+gap+8

    yy+=6
    d.text((px,yy),"MESSAGES VS TIPS",font=B(20),fill=BODY); yy+=34
    seg_h=30
    mfrac = (messages_gross/gross_total) if gross_total>0 else 0.0
    tfrac = (tips_gross/gross_total) if gross_total>0 else 0.0
    seg_w=(bx1-px)*bar_frac
    d.rounded_rectangle((px,yy,bx1,yy+seg_h),radius=10,fill=TRACK)
    mw = seg_w*mfrac
    if mw>4: d.rounded_rectangle((px,yy,px+mw,yy+seg_h),radius=10,fill=GOLD)
    tw = seg_w*tfrac
    if tw>4: d.rounded_rectangle((px+mw,yy,px+mw+tw,yy+seg_h),radius=10,fill=shade(GOLD,0.55))
    yy+=seg_h+18
    half=(bx1-px-18)/2
    d.text((px,yy),"MESSAGES",font=R(15),fill=MUTE)
    d.text((px,yy+22),money(messages_gross),font=B(22),fill=GOLD)
    d.text((px+half+18,yy),"TIPS",font=R(15),fill=MUTE)
    d.text((px+half+18,yy+22),money(tips_gross),font=B(22),fill=shade(GOLD,0.7))

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gt=cfg["gross_total"]
    reconciled = round(cfg["messages_gross"]+cfg["tips_gross"],2)
    if abs(reconciled-round(gt,2))>0.02:
        print(f"ERROR: messages_gross+tips_gross ({reconciled}) does not reconcile to gross_total ({gt})")
        sys.exit(1)
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
