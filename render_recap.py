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

The change percent, the trend colour (green when up, red when down, amber
when flat), and the day over day bars are all derived automatically from
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
BLUE=(108,150,224)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40
BLOCK_COL = GOLD

def trend(gross_total, prev_total):
    if prev_total and prev_total > 0:
        pct = (gross_total - prev_total) / prev_total * 100.0
        if pct > 0.5: return pct, GREEN, "UP"
        if pct < -0.5: return pct, RED, "DOWN"
        return pct, AMBER, "FLAT"
    if gross_total > 0:
        return None, GREEN, "NEW"
    return 0.0, AMBER, "FLAT"

def money(v):
    return "${:,.0f}".format(v)

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def right(d,x,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((x-w,y),t,font=f,fill=fill)

def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(46,40,24),150,120),(340,(24,38,32),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_3d_block(img,cx,cy,value,scale=1.0):
    col=BLOCK_COL
    label=money(value)
    nf_size=int(78*scale)
    nf=B(nf_size)
    max_w=int(300*scale)
    tmp=Image.new("RGB",(4,4)); td=ImageDraw.Draw(tmp)
    while td.textlength(label,font=nf) > max_w and nf_size > 34:
        nf_size -= 4; nf=B(nf_size)
    bw=max(int(220*scale), int(td.textlength(label,font=nf))+int(70*scale))
    bh=int(150*scale); depth=int(46*scale)
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
    nw=d.textlength(label,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(52*scale)),label,font=nf,fill=(20,18,10))
    lf=R(int(19*scale)); ltxt="GROSS TODAY"; lw=d.textlength(ltxt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(30*scale)),ltxt,font=lf,fill=shade((20,18,10),1.6))

def draw_trend_chip(d,cx,y,pct,colour,mode,prev_total,ease=1.0):
    w=380; h=72; x0=cx-w//2
    d.rounded_rectangle((x0,y,x0+w,y+h),radius=18,fill=PANEL,outline=colour,width=2)
    arrow = "▲" if mode=="UP" else ("▼" if mode=="DOWN" else ("▲" if mode=="NEW" else "●"))
    if mode=="NEW":
        main=f"{arrow} NEW"
    elif mode=="FLAT":
        main=f"{arrow} FLAT"
    else:
        main=f"{arrow} {abs(pct)*ease:.1f}%"
    center(d,cx,y+12,main,B(26),colour)
    sub=f"vs {money(prev_total)} yesterday"
    center(d,cx,y+46,sub,R(15),MUTE)

def draw_paired_bars(d,x0,y0,x1,y1,prev_total,gross_total,colour,ease=1.0):
    d.rounded_rectangle((x0,y0,x1,y1),radius=22,fill=PANEL)
    top=y0+74; bottom=y1-56; avail=bottom-top
    denom=max(prev_total,gross_total,1)
    colw=(x1-x0-120)//2
    bx0=x0+60
    ph=int(avail*(prev_total/denom)*ease)
    d.rounded_rectangle((bx0,bottom-ph,bx0+colw,bottom),radius=10,fill=shade(colour,0.55))
    d.text((bx0,bottom-ph-30),money(prev_total),font=B(20),fill=BODY)
    center(d,bx0+colw/2,bottom+14,"YESTERDAY",R(15),MUTE)
    bx1=x1-60-colw
    th=int(avail*(gross_total/denom)*ease)
    d.rounded_rectangle((bx1,bottom-th,bx1+colw,bottom),radius=10,fill=colour)
    d.text((bx1,bottom-th-30),money(gross_total),font=B(20),fill=WHITE)
    center(d,bx1+colw/2,bottom+14,"TODAY",R(15),MUTE)
    center(d,(x0+x1)/2,y0+8,"DAY OVER DAY",R(15),MUTE)

def draw_breakdown(d,x0,y0,x1,y1,messages_gross,tips_gross,ease=1.0):
    d.rounded_rectangle((x0,y0,x1,y1),radius=22,fill=PANEL)
    total=max(messages_gross+tips_gross,1)
    px=x0+44; yy=y0+40
    for label,val,col in [("Messages",messages_gross,GOLD),("Tips",tips_gross,BLUE)]:
        pct=val/total*100
        d.text((px,yy),label,font=B(20),fill=BODY)
        vf=B(22); sf=R(16)
        vtxt=money(val); ptxt=f"  {pct:.0f}%"
        right(d,x1-44-d.textlength(ptxt,font=sf),yy-2,vtxt,vf,col)
        right(d,x1-44,yy+2,ptxt,sf,FAINT)
        by=yy+34; bx1=x1-44
        d.rounded_rectangle((px,by,bx1,by+10),radius=5,fill=TRACK)
        fillw=(bx1-px)*((val/total)*ease)
        if fillw>6: d.rounded_rectangle((px,by,px+fillw,by+10),radius=5,fill=col)
        yy+=78
    center(d,(x0+x1)/2,y0+8,"MESSAGES VS TIPS",R(15),MUTE)

def render(cfg,gross_val,bar_frac,bob=0.0,scale=1.0):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,380+int(bob),gross_val,scale=scale)
    d=ImageDraw.Draw(img)
    pct,colour,mode=trend(cfg["gross_total"],cfg.get("prev_total",0))
    draw_trend_chip(d,cx,478,pct,colour,mode,cfg.get("prev_total",0),ease=bar_frac)
    draw_paired_bars(d,CARD_X0,566,CARD_X1,760,cfg.get("prev_total",0),cfg["gross_total"],colour,ease=bar_frac)
    draw_breakdown(d,CARD_X0,782,CARD_X1,1054,cfg["messages_gross"],cfg["tips_gross"],ease=bar_frac)
    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gt=cfg["gross_total"]
    msg_g=cfg["messages_gross"]; tip_g=cfg["tips_gross"]
    if abs((msg_g+tip_g)-gt) > 0.5:
        print(f"error: messages_gross ({msg_g}) + tips_gross ({tip_g}) = {msg_g+tip_g} does not reconcile to gross_total ({gt})")
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
