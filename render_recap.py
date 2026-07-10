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

messages_gross + tips_gross should reconcile to gross_total. The trend
colour, change percent, and day over day bars are all derived from
gross_total vs prev_total, so there is no colour/percent field to set.
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
BLUE=(120,165,225)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def right(d,x1,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((x1-w,y),t,font=f,fill=fill)
def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img
def money(v):
    return "${:,.0f}".format(v)

def trend_info(cur, prev):
    if prev <= 0:
        if cur <= 0: return AMBER, 0.0, "●"
        return GREEN, 100.0, "▲"
    pct = (cur - prev) / prev * 100.0
    if abs(pct) < 0.5: return AMBER, pct, "●"
    if pct > 0: return GREEN, pct, "▲"
    return RED, pct, "▼"

def draw_3d_money_block(img,cx,cy,amount,colour,scale=1.0):
    txt=money(amount)
    d0=ImageDraw.Draw(img,"RGBA")
    nf=B(int(78*scale))
    tw=d0.textlength(txt,font=nf)
    bw=max(int(230*scale),int(tw+90*scale)); bh=int(150*scale); depth=int(46*scale)
    x0,y0=cx-bw//2,cy-bh//2
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    shy=cy+bh//2+depth+int(46*scale); sw=int(bw*0.9)
    sd.ellipse((cx-sw//2,shy-22,cx+sw//2,shy+22),fill=(0,0,0,150))
    sh=sh.filter(ImageFilter.GaussianBlur(18)); img.alpha_composite(sh)
    d=ImageDraw.Draw(img,"RGBA")
    top=shade(colour,1.18); front=shade(colour,0.82); side=shade(colour,0.58)
    d.polygon([(x0,y0),(x0+bw,y0),(x0+bw+depth,y0-depth),(x0+depth,y0-depth)],fill=top)
    d.polygon([(x0+bw,y0),(x0+bw,y0+bh),(x0+bw+depth,y0+bh-depth),(x0+bw+depth,y0-depth)],fill=side)
    d.polygon([(x0,y0),(x0+bw,y0),(x0+bw,y0+bh),(x0,y0+bh)],fill=front)
    d.line([(x0,y0),(x0+bw,y0)],fill=shade(colour,1.4),width=2)
    d.text((x0+bw/2-tw/2,y0+bh/2-int(56*scale)),txt,font=nf,fill=WHITE)
    lf=R(int(20*scale)); lt="GROSS TODAY"; lw=d.textlength(lt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(30*scale)),lt,font=lf,fill=shade(WHITE,0.85))

def draw_bar_row(d,px,bx1,yy,label,val,total,colour,bar_frac,show_pct=True):
    d.text((px,yy),label,font=B(20),fill=BODY)
    amt=money(val)
    vf=B(22)
    right(d,bx1,yy-2,amt,vf,colour)
    if show_pct:
        pct = (val/total*100.0) if total>0 else 0.0
        pf=R(15); pt=f"{pct:.0f}% of gross"
        right(d,bx1,yy+26,pt,pf,FAINT)
        by=yy+52
    else:
        by=yy+30
    bx0=px; d.rounded_rectangle((bx0,by,bx1,by+10),radius=5,fill=TRACK)
    m=max(total,1)
    fillw=(bx1-bx0)*min(1.0,(val/m))*bar_frac
    if fillw>6: d.rounded_rectangle((bx0,by,bx0+fillw,by+10),radius=5,fill=colour)

def render(cfg,trend_col,pct_final,arrow,pct_shown,bar_frac,gross_shown,bob=0.0,scale=1.0):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_money_block(img,cx,380+int(bob),gross_shown,trend_col,scale=scale)
    d=ImageDraw.Draw(img,"RGBA")

    py0=548
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+458),radius=22,fill=PANEL)
    px=CARD_X0+44; bx1=CARD_X1-44

    # trend chip
    chip_y0=py0+28; chip_h=92
    d.rounded_rectangle((px-4,chip_y0,bx1+4,chip_y0+chip_h),radius=18,fill=shade(trend_col,0.18))
    at=f"{arrow} {abs(pct_shown):.1f}%"
    d.text((px+18,chip_y0+18),at,font=B(34),fill=trend_col)
    right(d,bx1-18,chip_y0+20,"day over day",R(15),MUTE)
    right(d,bx1-18,chip_y0+46,f"vs {money(cfg['prev_total'])} yesterday",R(15),BODY)

    yy=chip_y0+chip_h+34
    center(d,cx,yy-24,"YESTERDAY VS TODAY",R(15),MUTE)
    draw_bar_row(d,px,bx1,yy,"Yesterday",cfg["prev_total"],max(cfg["prev_total"],cfg["gross_total"]),FAINT,bar_frac,show_pct=False)
    yy+=70
    draw_bar_row(d,px,bx1,yy,"Today",cfg["gross_total"],max(cfg["prev_total"],cfg["gross_total"]),trend_col,bar_frac,show_pct=False)

    yy+=96
    center(d,cx,yy-24,"MESSAGES VS TIPS",R(15),MUTE)
    draw_bar_row(d,px,bx1,yy,"Messages",cfg["messages_gross"],cfg["gross_total"],BLUE,bar_frac)
    yy+=78
    draw_bar_row(d,px,bx1,yy,"Tips",cfg["tips_gross"],cfg["gross_total"],GOLD,bar_frac)

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gt=cfg["gross_total"]; pt=cfg["prev_total"]
    recon = cfg["messages_gross"] + cfg["tips_gross"]
    if abs(recon - gt) > 1.0:
        print(f"warning: messages_gross + tips_gross ({recon}) does not reconcile to gross_total ({gt})")
    trend_col,pct_final,arrow = trend_info(gt,pt)

    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,trend_col,pct_final,arrow,pct_final*ease,ease,gt*ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,trend_col,pct_final,arrow,pct_final,1.0,gt,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16

    frames[-1].save(out+".jpg","JPEG",quality=94)
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
