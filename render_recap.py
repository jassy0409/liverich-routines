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

messages_gross plus tips_gross should reconcile to gross_total. The change
percent, trend colour (green up / red down / amber flat), and the day over
day bars are all derived automatically from gross_total vs prev_total.
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
MSG_COLOR=(94,156,235); TIP_COLOR=(208,170,92)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def money(v):
    v=round(v,2)
    if abs(v-round(v))<0.001:
        return "${:,.0f}".format(v)
    return "${:,.2f}".format(v)
def trend_colour(pct):
    if abs(pct)<0.5: return AMBER
    return GREEN if pct>0 else RED
def ambient():
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(380,(30,46,36),150,120),(340,(40,34,20),W-140,H-180)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def draw_3d_block(img,cx,cy,value,colour,scale=1.0,label="GROSS, DAY"):
    bw,bh=int(300*scale),int(150*scale); depth=int(46*scale)
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
    num=money(value); nf=B(int(64*scale))
    while d.textlength(num,font=nf) > bw-24 and nf.size>28:
        nf=B(nf.size-2)
    nw=d.textlength(num,font=nf)
    d.text((x0+bw/2-nw/2,y0+bh/2-int(40*scale)),num,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lw=d.textlength(label,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),label,font=lf,fill=shade(WHITE,0.85))

def bar_row(d,px,x1,ry,label,val_text,val_col,frac,bar_area_w,row_gap):
    label_f=R(16); val_f=B(18)
    d.text((px,ry),label,font=label_f,fill=MUTE)
    d.text((x1-d.textlength(val_text,font=val_f),ry-2),val_text,font=val_f,fill=val_col)
    by=ry+26
    d.rounded_rectangle((px,by,x1,by+14),radius=7,fill=TRACK)
    fillw=bar_area_w*frac
    if fillw>8:
        d.rounded_rectangle((px,by,px+fillw,by+14),radius=7,fill=val_col)
    return ry+row_gap

def render(cfg, cur_val, bar_frac, pct):
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)

    colour=trend_colour(pct)
    bob=-6*bar_frac; scale=0.9+0.1*bar_frac
    draw_3d_block(img,cx,380+int(bob),cur_val,colour,scale=scale)
    d=ImageDraw.Draw(img)
    center(d,cx,476,"GROSS EARNINGS",R(15),MUTE)

    chip_y=520
    arrow="▲" if pct>0.5 else ("▼" if pct<-0.5 else "▪")
    chip_text="{} {:.1f}% vs yesterday".format(arrow,abs(pct))
    tf=B(22); tw=d.textlength(chip_text,font=tf)
    chip_w=tw+56; chip_x0=cx-chip_w/2
    d.rounded_rectangle((chip_x0,chip_y,chip_x0+chip_w,chip_y+48),radius=24,fill=shade(colour,0.24))
    d.text((chip_x0+28,chip_y+11),chip_text,font=tf,fill=colour)

    py0=592; panel_h=380
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+panel_h),radius=22,fill=PANEL)
    px=CARD_X0+44; x1=CARD_X1-44; bar_area_w=x1-px

    d.text((px,py0+28),"DAY OVER DAY",font=B(18),fill=BODY)
    prev=cfg["prev_total"]; gross=cfg["gross_total"]; maxv=max(prev,gross,1)
    ry=py0+66
    ry=bar_row(d,px,x1,ry,"YESTERDAY",money(prev),FAINT,(prev/maxv)*bar_frac,bar_area_w,62)
    ry=bar_row(d,px,x1,ry,"TODAY",money(gross),colour,(gross/maxv)*bar_frac,bar_area_w,62)

    ry+=14
    d.line((px,ry,x1,ry),fill=TRACK,width=1)
    ry+=24
    d.text((px,ry),"MESSAGES VS TIPS",font=B(18),fill=BODY)
    ry+=38
    total=max(cfg["messages_gross"]+cfg["tips_gross"],1)
    ry=bar_row(d,px,x1,ry,"Messages",money(cfg["messages_gross"]),MSG_COLOR,(cfg["messages_gross"]/total)*bar_frac,bar_area_w,52)
    ry=bar_row(d,px,x1,ry,"Tips",money(cfg["tips_gross"]),TIP_COLOR,(cfg["tips_gross"]/total)*bar_frac,bar_area_w,52)

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gross=cfg["gross_total"]; prev=cfg.get("prev_total",0)
    pct=0.0 if prev==0 else (gross-prev)/prev*100
    render(cfg,gross,1.0,pct).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,gross*ease,ease,pct))
    for k in range(16):
        frames.append(render(cfg,gross,1.0,pct))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
