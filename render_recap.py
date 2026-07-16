#!/usr/bin/env python3
"""LRM Daily Earnings Recap renderer (generic, config-driven).

Usage:
    python3 render_recap.py <config.json> <out_basepath>

Writes <out_basepath>.gif (animated deliverable) and <out_basepath>.jpg (static preview).

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

messages_gross + tips_gross should reconcile to gross_total. The change percent,
trend colour (green up / red down / amber flat), and the day over day bars are
all derived automatically from gross_total vs prev_total.
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
MSG_COL=(91,140,238); TIP_COL=(208,170,92)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def dollars(v):
    return "$" + format(int(round(v)), ",")
def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def trend_info(gross_total, prev_total):
    hi = max(gross_total, prev_total, 1)
    if abs(gross_total - prev_total) < 0.005 * hi:
        return "FLAT", 0.0, AMBER
    pct = (gross_total - prev_total) / prev_total * 100.0 if prev_total > 0 else 100.0
    if gross_total > prev_total:
        return "UP", pct, GREEN
    return "DOWN", pct, RED

def fit_font(text, max_w, start_size, min_size=34):
    size = start_size
    while size > min_size:
        f = B(size)
        if ImageDraw.Draw(Image.new("RGB",(1,1))).textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return B(min_size)

def draw_3d_block(img,cx,cy,amount,col,scale=1.0):
    bw,bh=int(220*scale),int(150*scale); depth=int(46*scale)
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
    num=dollars(amount); nf=fit_font(num,bw-int(24*scale),int(70*scale)); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(50*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lt="GROSS TODAY"; lw=d.textlength(lt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),lt,font=lf,fill=shade(WHITE,0.85))

def render(cfg,amount_val,bar_frac,bob=0.0,scale=1.0):
    gross_total=cfg["gross_total"]; prev_total=cfg["prev_total"]
    msg=cfg["messages_gross"]; tips=cfg["tips_gross"]
    label, pct, trend_col = trend_info(gross_total, prev_total)
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,380+int(bob),amount_val,trend_col,scale=scale)
    d=ImageDraw.Draw(img)

    py0=548; ph=190
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+ph),radius=22,fill=PANEL)
    px=CARD_X0+40; pw=CARD_X1-CARD_X0-80
    d.text((px,py0+26),"VS YESTERDAY",font=R(15),fill=MUTE)
    trend_txt = label if label=="FLAT" else f"{label} {abs(pct):.1f}%"
    d.text((px,py0+48),trend_txt,font=B(30),fill=trend_col)
    hi=max(gross_total,prev_total,1)
    bar_y1=py0+108; bar_h=22; bar_w=pw
    d.text((px,bar_y1-20),"TODAY",font=R(14),fill=FAINT)
    d.rounded_rectangle((px,bar_y1,px+bar_w,bar_y1+bar_h),radius=8,fill=TRACK)
    fw1=bar_w*(gross_total/hi)*bar_frac
    if fw1>6: d.rounded_rectangle((px,bar_y1,px+fw1,bar_y1+bar_h),radius=8,fill=trend_col)
    d.text((min(px+fw1+8,CARD_X1-120),bar_y1-1),dollars(gross_total),font=B(16),fill=WHITE)
    bar_y2=bar_y1+44
    d.text((px,bar_y2-20),"YESTERDAY",font=R(14),fill=FAINT)
    d.rounded_rectangle((px,bar_y2,px+bar_w,bar_y2+bar_h),radius=8,fill=TRACK)
    fw2=bar_w*(prev_total/hi)*bar_frac
    if fw2>6: d.rounded_rectangle((px,bar_y2,px+fw2,bar_y2+bar_h),radius=8,fill=shade(MUTE,1.3))
    d.text((min(px+fw2+8,CARD_X1-120),bar_y2-1),dollars(prev_total),font=B(16),fill=BODY)

    qy0=py0+ph+18; qh=190
    d.rounded_rectangle((CARD_X0,qy0,CARD_X1,qy0+qh),radius=22,fill=PANEL)
    d.text((px,qy0+26),"MESSAGES VS TIPS",font=R(15),fill=MUTE)
    tot=max(msg+tips,1)
    mpct=msg/tot*100; tpct=tips/tot*100
    qbar_y1=qy0+70
    d.text((px,qbar_y1-20),f"MESSAGES  {dollars(msg)}  ({mpct:.0f}%)",font=B(17),fill=MSG_COL)
    d.rounded_rectangle((px,qbar_y1,px+pw,qbar_y1+22),radius=8,fill=TRACK)
    mfw=pw*(msg/tot)*bar_frac
    if mfw>6: d.rounded_rectangle((px,qbar_y1,px+mfw,qbar_y1+22),radius=8,fill=MSG_COL)
    qbar_y2=qbar_y1+56
    d.text((px,qbar_y2-20),f"TIPS  {dollars(tips)}  ({tpct:.0f}%)",font=B(17),fill=TIP_COL)
    d.rounded_rectangle((px,qbar_y2,px+pw,qbar_y2+22),radius=8,fill=TRACK)
    tfw=pw*(tips/tot)*bar_frac
    if tfw>6: d.rounded_rectangle((px,qbar_y2,px+tfw,qbar_y2+22),radius=8,fill=TIP_COL)

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
