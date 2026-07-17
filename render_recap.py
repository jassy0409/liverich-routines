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

messages_gross plus tips_gross must reconcile to gross_total. prev_total is
the previous UTC day's gross total. The change percent, trend colour (green
up, red down, amber flat), and the day over day bars are all derived
automatically from gross_total vs prev_total.
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
BLUE=(90,140,220)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def money(x):
    return f"${x:,.2f}"

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

def fit_font(text, start_size, max_width, bold=True):
    size=start_size
    fn = B if bold else R
    while size>28:
        f=fn(size)
        img=Image.new("RGB",(10,10))
        w=ImageDraw.Draw(img).textlength(text,font=f)
        if w<=max_width: return f,w
        size-=4
    f=fn(size)
    img=Image.new("RGB",(10,10))
    w=ImageDraw.Draw(img).textlength(text,font=f)
    return f,w

def trend(gross_total, prev_total):
    if prev_total>0:
        pct=(gross_total-prev_total)/prev_total*100.0
    elif gross_total>0:
        pct=100.0
    else:
        pct=0.0
    if gross_total>prev_total: return GREEN,"▲",pct
    if gross_total<prev_total: return RED,"▼",pct
    return AMBER,"•",pct

def draw_3d_block(img,cx,cy,label_text,fixed_font,fixed_w,col,scale=1.0):
    bw,bh=int((fixed_w+120)*scale),int(150*scale); depth=int(46*scale)
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
    nf=fixed_font
    nw=d.textlength(label_text,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(30*scale)),label_text,font=nf,fill=WHITE)
    lf=R(int(20*scale)); lw=d.textlength("GROSS",font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),"GROSS",font=lf,fill=shade(WHITE,0.85))

def render(cfg, gross_val, bar_frac, bob=0.0, scale=1.0):
    gross_total=cfg["gross_total"]; prev_total=cfg["prev_total"]
    messages_gross=cfg["messages_gross"]; tips_gross=cfg["tips_gross"]
    col,arrow,pct=trend(gross_total,prev_total)
    fixed_font,fixed_w=fit_font(money(gross_total),72,620)
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,388+int(bob),money(gross_val),fixed_font,fixed_w,col,scale=scale)
    d=ImageDraw.Draw(img)
    chip_txt=f"{arrow} {abs(pct):.1f}% vs prior day"
    cf=B(22); cw=d.textlength(chip_txt,font=cf)
    chip_y=506
    d.rounded_rectangle((cx-cw/2-24,chip_y,cx+cw/2+24,chip_y+44),radius=22,fill=shade(col,0.28))
    center(d,cx,chip_y+9,chip_txt,cf,col)

    py0=574
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+188),radius=22,fill=PANEL)
    d.text((CARD_X0+32,py0+22),"DAY OVER DAY",font=R(15),fill=MUTE)
    bar_area_x0=CARD_X0+32; bar_area_x1=CARD_X1-32
    max_v=max(gross_total,prev_total,1)
    row_y=py0+64
    for lbl,val,c in [("PREV DAY",prev_total,MUTE),("REPORTED DAY",gross_total,col)]:
        d.text((bar_area_x0,row_y),lbl,font=R(15),fill=FAINT)
        vf=B(20); vtxt=money(val)
        d.text((bar_area_x1-d.textlength(vtxt,font=vf),row_y-2),vtxt,font=vf,fill=BODY)
        by=row_y+26
        d.rounded_rectangle((bar_area_x0,by,bar_area_x1,by+14),radius=7,fill=TRACK)
        frac=(val/max_v)*bar_frac
        fillw=(bar_area_x1-bar_area_x0)*frac
        barc = c if c!=MUTE else BLUE
        if fillw>8: d.rounded_rectangle((bar_area_x0,by,bar_area_x0+fillw,by+14),radius=7,fill=barc)
        row_y+=60

    qy0=py0+212
    d.rounded_rectangle((CARD_X0,qy0,CARD_X1,qy0+220),radius=22,fill=PANEL)
    d.text((CARD_X0+32,qy0+22),"GROSS BREAKDOWN",font=R(15),fill=MUTE)
    tot=max(gross_total,0.01)
    msg_pct=messages_gross/tot*100.0
    tip_pct=tips_gross/tot*100.0
    barx0=CARD_X0+32; barx1=CARD_X1-32
    stacked_y=qy0+58
    d.rounded_rectangle((barx0,stacked_y,barx1,stacked_y+28),radius=14,fill=TRACK)
    seg_w=(barx1-barx0)*bar_frac
    msg_w=seg_w*(messages_gross/tot)
    tip_w=seg_w*(tips_gross/tot)
    if msg_w>4:
        d.rounded_rectangle((barx0,stacked_y,barx0+msg_w,stacked_y+28),radius=14,fill=(120,150,235))
    if tip_w>4:
        d.rounded_rectangle((barx0+msg_w,stacked_y,barx0+msg_w+tip_w,stacked_y+28),radius=14,fill=GOLD)
    row2=stacked_y+56
    colw=(barx1-barx0-24)//2
    d.ellipse((barx0,row2+4,barx0+14,row2+18),fill=(120,150,235))
    d.text((barx0+24,row2),"Messages",font=B(18),fill=BODY)
    d.text((barx0+24,row2+26),f"{money(messages_gross)}  ·  {msg_pct:.0f}%",font=R(16),fill=MUTE)
    x2=barx0+colw+24
    d.ellipse((x2,row2+4,x2+14,row2+18),fill=GOLD)
    d.text((x2+24,row2),"Tips",font=B(18),fill=BODY)
    d.text((x2+24,row2+26),f"{money(tips_gross)}  ·  {tip_pct:.0f}%",font=R(16),fill=MUTE)

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
