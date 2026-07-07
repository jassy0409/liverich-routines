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

Trend colour, change percent, and the day over day bars are all derived
automatically from gross_total vs prev_total, so there is no colour or
percent field for callers to set.
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
def money(v):
    v=round(v)
    return f"${v:,.0f}"
def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def trend_info(total,prev):
    if prev<=0:
        pct=0.0
    else:
        pct=(total-prev)/prev*100.0
    if abs(pct)<0.5:
        return AMBER,pct,"FLAT"
    if pct>0:
        return GREEN,pct,"UP"
    return RED,pct,"DOWN"

def draw_3d_block(img,cx,cy,value,col,scale=1.0):
    bw,bh=int(240*scale),int(150*scale); depth=int(46*scale)
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
    num=money(value); nf=B(int(56*scale)); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(50*scale)),num,font=nf,fill=WHITE)
    lf=R(int(17*scale)); lt="GROSS TODAY"; lw=d.textlength(lt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(32*scale)),lt,font=lf,fill=shade(WHITE,0.85))

def render(cfg,gross_val,bar_frac,bob=0.0,scale=1.0):
    total=cfg["gross_total"]; prev=cfg["prev_total"]
    msg=cfg["messages_gross"]; tips=cfg["tips_gross"]
    col,pct,direction=trend_info(total,prev)
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,378+int(bob),gross_val,col,scale=scale)
    d=ImageDraw.Draw(img,"RGBA")

    chip_y0=546; chip_h=64
    d.rounded_rectangle((CARD_X0,chip_y0,CARD_X1,chip_y0+chip_h),radius=18,fill=PANEL)
    arrow = "▲" if direction=="UP" else ("▼" if direction=="DOWN" else "◆")
    pct_disp=abs(pct)*bar_frac
    chip_txt=f"{arrow} {pct_disp:.1f}%  DAY OVER DAY"
    tf=B(23)
    d.text((CARD_X0+30,chip_y0+chip_h/2-14),chip_txt,font=tf,fill=col)
    prev_txt=f"vs {money(prev)} prior day"
    pf=R(17); pw=d.textlength(prev_txt,font=pf)
    d.text((CARD_X1-30-pw,chip_y0+chip_h/2-10),prev_txt,font=pf,fill=MUTE)

    py0=632; ph=214
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+ph),radius=22,fill=PANEL)
    d.text((CARD_X0+34,py0+24),"DAY OVER DAY GROSS",font=B(18),fill=BODY)
    maxv=max(total,prev,1)
    bar_area_top=py0+64; bar_area_bot=py0+ph-42
    avail_h=bar_area_bot-bar_area_top
    bar_w=100; gap=80
    total_w=bar_w*2+gap
    bx0=cx-total_w/2
    pbh=avail_h*(prev/maxv)*bar_frac
    d.rounded_rectangle((bx0,bar_area_bot-pbh,bx0+bar_w,bar_area_bot),radius=8,fill=shade(MUTE,0.55))
    ptxt=money(prev); pwv=d.textlength(ptxt,font=R(16))
    d.text((bx0+bar_w/2-pwv/2,bar_area_bot-pbh-24),ptxt,font=R(16),fill=MUTE)
    lwv=d.textlength("PRIOR DAY",font=R(13))
    d.text((bx0+bar_w/2-lwv/2,bar_area_bot+10),"PRIOR DAY",font=R(13),fill=FAINT)
    tbx0=bx0+bar_w+gap
    tbh=avail_h*(total/maxv)*bar_frac
    d.rounded_rectangle((tbx0,bar_area_bot-tbh,tbx0+bar_w,bar_area_bot),radius=8,fill=col)
    ttxt=money(total); twv=d.textlength(ttxt,font=B(16))
    d.text((tbx0+bar_w/2-twv/2,bar_area_bot-tbh-24),ttxt,font=B(16),fill=WHITE)
    lwv2=d.textlength("TODAY",font=R(13))
    d.text((tbx0+bar_w/2-lwv2/2,bar_area_bot+10),"TODAY",font=R(13),fill=FAINT)

    by0=py0+ph+20; bh_panel=214
    d.rounded_rectangle((CARD_X0,by0,CARD_X1,by0+bh_panel),radius=22,fill=PANEL)
    d.text((CARD_X0+34,by0+24),"MESSAGES VS TIPS",font=B(18),fill=BODY)
    rows=[("Messages",msg,GOLD),("Tips",tips,shade(GOLD,0.68))]
    ry=by0+66
    rx0=CARD_X0+34; rx1=CARD_X1-34
    for label,val,rc in rows:
        pct_of=(val/total*100) if total>0 else 0
        d.text((rx0,ry),label,font=B(18),fill=BODY)
        vt=f"{money(val)}  ({pct_of:.0f}%)"
        vf=R(16); vw=d.textlength(vt,font=vf)
        d.text((rx1-vw,ry+2),vt,font=vf,fill=MUTE)
        byy=ry+30
        d.rounded_rectangle((rx0,byy,rx1,byy+12),radius=6,fill=TRACK)
        frac=(val/total) if total>0 else 0
        fillw=(rx1-rx0)*frac*bar_frac
        if fillw>6: d.rounded_rectangle((rx0,byy,rx0+fillw,byy+12),radius=6,fill=rc)
        ry+=76

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    total=cfg["gross_total"]
    render(cfg,total,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,total*ease,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,total,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
