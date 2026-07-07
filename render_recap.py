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
automatically from gross_total vs prev_total, so callers only supply the
raw dollar figures.
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
TEAL=(64,170,185)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def money(v):
    return "${:,.0f}".format(v)

def trend_colour(delta_pct):
    if delta_pct > 0.5: return GREEN
    if delta_pct < -0.5: return RED
    return AMBER

def trend_arrow(delta_pct):
    if delta_pct > 0.5: return "▲"
    if delta_pct < -0.5: return "▼"
    return "●"

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

def draw_money_block(img,cx,cy,amount,col,scale=1.0):
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
    num=money(amount)
    size=int(58*scale)
    nf=B(size); nw=d.textlength(num,font=nf)
    while nw > bw-24 and size > 22:
        size-=2; nf=B(size); nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(50*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lw=d.textlength("GROSS TODAY",font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(32*scale)),"GROSS TODAY",font=lf,fill=shade(WHITE,0.85))

def render(cfg,gross_val,bar_frac,bob=0.0,scale=1.0):
    prev=cfg["prev_total"]; final_gross=cfg["gross_total"]
    delta_pct = ((final_gross-prev)/prev*100) if prev else 0.0
    col = trend_colour(delta_pct)
    msg_g=cfg["messages_gross"]; tip_g=cfg["tips_gross"]
    total=msg_g+tip_g if (msg_g+tip_g)>0 else 1
    msg_pct=msg_g/total*100; tip_pct=tip_g/total*100

    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_money_block(img,cx,380+int(bob),gross_val,col,scale=scale)
    d=ImageDraw.Draw(img)

    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+340),radius=22,fill=PANEL)
    px=CARD_X0+44; bx1=CARD_X1-44
    yy=py0+34
    d.text((px,yy),"DAY OVER DAY",font=R(16),fill=MUTE)
    yy+=26
    chg_txt=f"{trend_arrow(delta_pct)} {abs(delta_pct):.1f}%"
    d.text((px,yy),chg_txt,font=B(34),fill=col)
    sub_txt=f"vs {money(prev)} yesterday"
    sw=d.textlength(sub_txt,font=R(18))
    d.text((bx1-sw,yy+8),sub_txt,font=R(18),fill=MUTE)

    bars_top=yy+70; bars_h=100
    bar_w=90; gap=60
    bx_center=cx
    y_bar_x0=bx_center-gap//2-bar_w
    t_bar_x0=bx_center+gap//2
    max_val=max(prev,final_gross,1)
    y_h=int(bars_h*(prev/max_val)*bar_frac)
    t_h=int(bars_h*(final_gross/max_val)*bar_frac)
    y_base=bars_top+bars_h
    d.rounded_rectangle((y_bar_x0,y_base-y_h,y_bar_x0+bar_w,y_base),radius=8,fill=shade(WHITE,0.4))
    d.rounded_rectangle((t_bar_x0,y_base-t_h,t_bar_x0+bar_w,y_base),radius=8,fill=col)
    yv=money(prev); yv_w=d.textlength(yv,font=B(16))
    d.text((y_bar_x0+bar_w/2-yv_w/2,y_base-y_h-22),yv,font=B(16),fill=BODY)
    tv=money(final_gross); tv_w=d.textlength(tv,font=B(16))
    d.text((t_bar_x0+bar_w/2-tv_w/2,y_base-t_h-22),tv,font=B(16),fill=BODY)
    center(d,y_bar_x0+bar_w/2,y_base+10,"YESTERDAY",R(13),FAINT)
    center(d,t_bar_x0+bar_w/2,y_base+10,"TODAY",R(13),FAINT)

    stack_y=y_base+46; stack_h=22
    msg_w=(bx1-px)*(msg_pct/100.0)*bar_frac
    tip_w=(bx1-px)*(tip_pct/100.0)*bar_frac
    d.rounded_rectangle((px,stack_y,bx1,stack_y+stack_h),radius=10,fill=TRACK)
    if msg_w>4:
        d.rounded_rectangle((px,stack_y,px+msg_w,stack_y+stack_h),radius=10,fill=GOLD)
    if tip_w>4:
        d.rounded_rectangle((bx1-tip_w,stack_y,bx1,stack_y+stack_h),radius=10,fill=TEAL)

    leg_y=stack_y+34
    d.rectangle((px,leg_y+4,px+14,leg_y+18),fill=GOLD)
    d.text((px+22,leg_y),f"Messages {money(msg_g)} ({msg_pct:.0f}%)",font=R(16),fill=BODY)
    tip_lbl=f"Tips {money(tip_g)} ({tip_pct:.0f}%)"
    tip_lbl_w=d.textlength(tip_lbl,font=R(16))
    d.rectangle((bx1-tip_lbl_w-22,leg_y+4,bx1-tip_lbl_w-8,leg_y+18),fill=TEAL)
    d.text((bx1-tip_lbl_w,leg_y),tip_lbl,font=R(16),fill=BODY)

    cy0=py0+372; chip_h=96; cw=(CARD_X1-CARD_X0-18)//2
    d.rounded_rectangle((CARD_X0,cy0,CARD_X0+cw,cy0+chip_h),radius=18,fill=PANEL)
    d.text((CARD_X0+30,cy0+22),"MESSAGES GROSS",font=R(15),fill=MUTE)
    d.text((CARD_X0+30,cy0+46),money(msg_g),font=B(30),fill=GOLD)
    wx0=CARD_X0+cw+18
    d.rounded_rectangle((wx0,cy0,CARD_X1,cy0+chip_h),radius=18,fill=PANEL)
    d.text((wx0+28,cy0+22),"TIPS GROSS",font=R(15),fill=MUTE)
    d.text((wx0+28,cy0+46),money(tip_g),font=B(30),fill=TEAL)

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
