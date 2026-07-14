#!/usr/bin/env python3
"""LRM Daily Earnings Recap renderer (generic, config-driven).

Same dark visual language as render_scorecard.py: a big animated figure in a
3D block that counts up, a day-over-day trend chip + paired trend bars, and
a messages-vs-tips breakdown chart.

Usage:
    python3 render_recap.py <config.json> <out_basepath>

Writes <out_basepath>.gif and <out_basepath>.jpg (preview).

config.json schema:
{
  "model": "Shantal",
  "sub": "July 13 2026",
  "gross_total": 1715,
  "prev_total": 1520,
  "messages_gross": 1310,
  "tips_gross": 405,
  "footer": "LIVERICHMEDIA  ·  DAILY RECAP  ·  JUL 13 2026"
}

The change percent, trend colour (green up / red down / amber flat), and the
day-over-day bars are all derived from gross_total vs prev_total.
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
BLUE=(94,158,214)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def money(v):
    v = round(v, 2)
    if abs(v - round(v)) < 0.005:
        return f"${int(round(v)):,}"
    return f"${v:,.2f}"

def trend_colour(pct):
    if abs(pct) < 0.5: return AMBER
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
    num=money(val); nf=B(int(64*scale)); nw=d.textlength(num,font=nf)
    if nw > bw-24:
        nf=B(int(64*scale*(bw-24)/nw)); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(28*scale)),num,font=nf,fill=WHITE)

def draw_triangle(d,cx,cy,size,col,up=True):
    if up:
        d.polygon([(cx,cy-size),(cx-size,cy+size),(cx+size,cy+size)],fill=col)
    else:
        d.polygon([(cx,cy+size),(cx-size,cy-size),(cx+size,cy-size)],fill=col)

def bar_row(d,px,bx1,yy,label,label_col,val_text,val_col,frac,bar_col,label_font=None,val_font=None):
    lf = label_font or B(20); vf = val_font or B(20)
    d.text((px,yy),label,font=lf,fill=label_col)
    vw=d.textlength(val_text,font=vf)
    d.text((bx1-vw,yy-2),val_text,font=vf,fill=val_col)
    by=yy+34
    d.rounded_rectangle((px,by,bx1,by+14),radius=7,fill=TRACK)
    fillw=(bx1-px)*max(0.0,min(1.0,frac))
    if fillw>8: d.rounded_rectangle((px,by,px+fillw,by+14),radius=7,fill=bar_col)
    return by+14

def render(cfg,gross_val,bar_frac,bob=0.0,scale=1.0):
    gross_total=cfg["gross_total"]; prev_total=cfg["prev_total"]
    messages_gross=cfg["messages_gross"]; tips_gross=cfg["tips_gross"]
    pct = 0.0 if prev_total==0 else (gross_total-prev_total)/prev_total*100.0
    tcol = trend_colour(pct)

    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)

    draw_3d_block(img,cx,378+int(bob),gross_val,tcol,scale=scale)
    d=ImageDraw.Draw(img); center(d,cx,474,"GROSS",R(15),MUTE)

    chip_w=520; chip_h=76; chip_x0=cx-chip_w//2; chip_y0=500
    d.rounded_rectangle((chip_x0,chip_y0,chip_x0+chip_w,chip_y0+chip_h),radius=18,fill=PANEL)
    tri_cx=chip_x0+46; tri_cy=chip_y0+chip_h//2
    if abs(pct) >= 0.5:
        draw_triangle(d,tri_cx,tri_cy,12,tcol,up=(pct>0))
    else:
        d.rounded_rectangle((tri_cx-12,tri_cy-4,tri_cx+12,tri_cy+4),radius=3,fill=tcol)
    pct_text=f"{abs(pct):.1f}%"
    pf=B(30); d.text((tri_cx+26,chip_y0+chip_h//2-20),pct_text,font=pf,fill=tcol)
    sub_text=f"vs {money(prev_total)} day before"
    sf=R(16); d.text((tri_cx+26,chip_y0+chip_h//2+14),sub_text,font=sf,fill=MUTE)

    py0=chip_y0+chip_h+22
    panel_h=176
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+panel_h),radius=22,fill=PANEL)
    px=CARD_X0+40; bx1=CARD_X1-40
    max_pair=max(prev_total,gross_total,1)
    yy=py0+34
    by=bar_row(d,px,bx1,yy,"DAY BEFORE",MUTE,money(prev_total),BODY,
               (prev_total/max_pair)*bar_frac,shade(MUTE,1.3))
    yy=by+30
    bar_row(d,px,bx1,yy,"TODAY",BODY,money(gross_total),tcol,
            (gross_total/max_pair)*bar_frac,tcol)

    py1=py0+panel_h+18
    panel_h2=176
    d.rounded_rectangle((CARD_X0,py1,CARD_X1,py1+panel_h2),radius=22,fill=PANEL)
    yy=py1+34
    mpct = 0 if gross_total==0 else messages_gross/gross_total
    tpct = 0 if gross_total==0 else tips_gross/gross_total
    d.text((px,yy),"MESSAGES",font=B(20),fill=BODY)
    mtxt=f"{money(messages_gross)}  ({mpct*100:.0f}%)"; vf=B(20); vw=d.textlength(mtxt,font=vf)
    d.text((bx1-vw,yy-2),mtxt,font=vf,fill=GOLD)
    by=yy+34
    d.rounded_rectangle((px,by,bx1,by+14),radius=7,fill=TRACK)
    fillw=(bx1-px)*max(0.0,min(1.0,mpct*bar_frac))
    if fillw>8: d.rounded_rectangle((px,by,px+fillw,by+14),radius=7,fill=GOLD)
    yy=by+14+30
    d.text((px,yy),"TIPS",font=B(20),fill=BODY)
    ttxt=f"{money(tips_gross)}  ({tpct*100:.0f}%)"; vw=d.textlength(ttxt,font=vf)
    d.text((bx1-vw,yy-2),ttxt,font=vf,fill=BLUE)
    by=yy+34
    d.rounded_rectangle((px,by,bx1,by+14),radius=7,fill=TRACK)
    fillw=(bx1-px)*max(0.0,min(1.0,tpct*bar_frac))
    if fillw>8: d.rounded_rectangle((px,by,px+fillw,by+14),radius=7,fill=BLUE)

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
