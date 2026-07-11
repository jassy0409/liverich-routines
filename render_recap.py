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
  "other_gross": 0,
  "footer": "LIVERICHMEDIA  ·  DAILY RECAP  ·  JUN 18 2026"
}

messages_gross + tips_gross + other_gross must reconcile to gross_total
("other_gross" defaults to 0 and only needs to be set when a page has
revenue outside messages/tips, e.g. subscriptions; the chart then shows a
third segment so nothing is hidden). Trend colour, change percent, and the
day over day bars are all derived automatically from gross_total vs
prev_total.
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
TEAL=(74,175,196)
CARD_X0,CARD_Y0,CARD_X1,CARD_Y1 = 40,40,W-40,H-40

def money(v):
    if abs(v-round(v))<0.005:
        return f"${int(round(v)):,}"
    return f"${v:,.2f}"

def trend(gross_total,prev_total):
    if prev_total<=0:
        pct = 100.0 if gross_total>0 else 0.0
    else:
        pct = (gross_total-prev_total)/prev_total*100
    if pct>0.5: return GREEN,pct,"▲"
    if pct<-0.5: return RED,pct,"▼"
    return AMBER,pct,"◆"

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

def draw_3d_block(img,cx,cy,value,col,scale=1.0):
    label=money(value)
    nf=B(int(72*scale))
    tmp=ImageDraw.Draw(Image.new("RGB",(1,1)))
    nw=tmp.textlength(label,font=nf)
    bw=int(max(240,nw+80)*scale/scale); bw=int(max(240*scale,nw+80))
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
    d.text((x0+bw/2-nw/2,y0+bh/2-int(50*scale)),label,font=nf,fill=WHITE)
    lf=R(int(18*scale)); lt="GROSS"; lw=d.textlength(lt,font=lf)
    d.text((x0+bw/2-lw/2,y0+bh/2+int(34*scale)),lt,font=lf,fill=shade(WHITE,0.85))

def render(cfg,value,bar_frac,bob=0.0,scale=1.0):
    gross_total=cfg["gross_total"]; prev_total=cfg["prev_total"]
    msg_g=cfg["messages_gross"]; tip_g=cfg["tips_gross"]; oth_g=cfg.get("other_gross",0)
    col,pct,arrow = trend(gross_total,prev_total)
    img=ambient().convert("RGBA"); d=ImageDraw.Draw(img); cx=W//2
    y=76; center(d,cx,y,"DAILY RECAP",B(20),GOLD)
    y+=36; center(d,cx,y,cfg["model"],B(40),WHITE)
    y+=58; center(d,cx,y,cfg["sub"],R(20),MUTE)
    draw_3d_block(img,cx,378+int(bob),value,col,scale=scale)
    d=ImageDraw.Draw(img); center(d,cx,474,"GROSS TOTAL",R(15),MUTE)

    py0=546
    chip_h=90
    d.rounded_rectangle((CARD_X0,py0,CARD_X1,py0+chip_h),radius=18,fill=PANEL)
    at=f"{arrow} {abs(pct):.1f}%"
    d.text((CARD_X0+30,py0+18),"DAY OVER DAY",font=R(15),fill=MUTE)
    d.text((CARD_X0+30,py0+40),at,font=B(30),fill=col)
    trailing=f"{money(prev_total)}  →  {money(gross_total)}"
    tw=d.textlength(trailing,font=R(18))
    d.text((CARD_X1-30-tw,py0+38),trailing,font=R(18),fill=BODY)

    by0=py0+chip_h+18; bh_panel=150
    d.rounded_rectangle((CARD_X0,by0,CARD_X1,by0+bh_panel),radius=22,fill=PANEL)
    maxval=max(prev_total,gross_total,1)
    bx0=CARD_X0+140; bx1=CARD_X1-44
    rows=[("YESTERDAY",prev_total,MUTE),("TODAY",gross_total,col)]
    ry=by0+30
    for label,val,c in rows:
        d.text((CARD_X0+30,ry+2),label,font=B(16),fill=BODY)
        d.rounded_rectangle((bx0,ry,bx1,ry+22),radius=11,fill=TRACK)
        frac=(val/maxval)*bar_frac
        fw=(bx1-bx0)*frac
        if fw>10: d.rounded_rectangle((bx0,ry,bx0+fw,ry+22),radius=11,fill=c)
        vtxt=money(val)
        d.text((bx0+8,ry+2),"",font=R(14),fill=WHITE)
        vw=d.textlength(vtxt,font=B(15))
        vx = bx0+fw+10 if fw>10 else bx0+10
        if vx+vw>bx1-4: vx=bx1-vw-8
        d.text((vx,ry+3),vtxt,font=B(15),fill=WHITE)
        ry+=58

    sy0=by0+bh_panel+18; sh_panel=170
    d.rounded_rectangle((CARD_X0,sy0,CARD_X1,sy0+sh_panel),radius=22,fill=PANEL)
    d.text((CARD_X0+30,sy0+22),"MESSAGES VS TIPS",font=R(15),fill=MUTE)
    segs=[("Messages",msg_g,GOLD),("Tips",tip_g,TEAL)]
    if oth_g>0.005: segs.append(("Subs",oth_g,(150,120,200)))
    total=max(sum(v for _,v,_ in segs),0.01)
    bx0=CARD_X0+30; bx1=CARD_X1-30; byy=sy0+56; bhh=26
    d.rounded_rectangle((bx0,byy,bx1,byy+bhh),radius=13,fill=TRACK)
    frac_total=bar_frac
    xcur=bx0
    for _,v,c in segs:
        seglen=(bx1-bx0)*(v/total)*frac_total
        if seglen>1:
            d.rounded_rectangle((xcur,byy,min(xcur+seglen,bx1),byy+bhh),radius=13,fill=c)
        xcur+=seglen
    ly=byy+bhh+22
    lx=bx0
    for label,v,c in segs:
        d.ellipse((lx,ly+4,lx+14,ly+18),fill=c)
        txt=f"{label}  {money(v)}"
        d.text((lx+22,ly),txt,font=R(17),fill=BODY)
        lx+=22+d.textlength(txt,font=R(17))+34

    center(d,cx,CARD_Y1-32,cfg["footer"],B(16),GOLD)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_recap.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    gross_total=cfg["gross_total"]
    recon = cfg["messages_gross"]+cfg["tips_gross"]+cfg.get("other_gross",0)
    if abs(recon-gross_total)>0.5:
        print(f"ERROR: messages_gross+tips_gross+other_gross ({recon}) does not reconcile to gross_total ({gross_total})")
        sys.exit(1)
    render(cfg,gross_total,1.0,bob=-6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=24
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,gross_total*ease,ease,bob=-10*ease,scale=0.9+0.1*ease))
    for k in range(16):
        bob=-6+6*math.sin(k/16*2*math.pi)
        frames.append(render(cfg,gross_total,1.0,bob=bob,scale=1.0))
    durations=[65]*(steps+1)+[80]*16
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif")

if __name__=="__main__": main()
