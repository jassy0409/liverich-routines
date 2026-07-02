#!/usr/bin/env python3
"""LRM Red Alert / Account Rules notice renderer (animated GIF).

Usage:
    python3 render_incident.py <config.json> <out_basepath>

Writes <out_basepath>.gif and <out_basepath>.jpg (preview).

Shares the LRM dark card look. Title is a big bold RED alert flanked by drawn
warning triangles (vector, so no missing-emoji boxes). Canvas height is computed
from the content so nothing clips.

config.json schema:
{
  "title": "SHANTAL TEAM  -  FINAL WARNING",
  "sub": "Account Rules Update  ·  Seve thread  ·  July 1",
  "severity": "CRITICAL",
  "headline": "Escalate. You do not make these calls.",
  "case": "one-paragraph what-triggered-this",
  "sections": [
     {"title": "HARD RULES - NON NEGOTIABLE", "color": "red",   "items": ["...","..."]},
     {"title": "CONSEQUENCES",                "color": "amber", "items": ["...","..."]}
  ],
  "ack": "Every chatter replies in-thread with full acknowledgement. No reply = not working the account.",
  "footer": "LIVERICHMEDIA  ·  ACCOUNT RULES UPDATE  ·  JUL 1"
}
"""
import sys, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = 860
F = "/usr/share/fonts/truetype/dejavu/"
def font(p, s): return ImageFont.truetype(F + p, s)
B = lambda s: font("DejaVuSans-Bold.ttf", s)
R = lambda s: font("DejaVuSans.ttf", s)
BG=(23,23,23); PANEL=(32,32,34); WHITE=(245,245,245)
MUTE=(150,150,154); FAINT=(112,112,116); BODY=(226,226,230); GOLD=(208,170,92)
GREEN=(60,200,120); AMBER=(239,159,39); RED=(226,75,74); TRACK=(54,54,58)
REDX=(255,74,74)
MX=40
COLS={"red":RED,"amber":AMBER,"green":GREEN,"gold":GOLD}

def shade(c,f): return tuple(max(0,min(255,int(v*f))) for v in c)
def lerp(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def center(d,cx,y,t,f,fill):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=fill)
def fit(d,text,maxw,start,minsz=22):
    s=start
    while s>minsz and d.textlength(text,font=B(s))>maxw: s-=1
    return B(s)
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines or [""]

def warn_tri(d,cx,cy,s,col):
    """Draw a filled warning triangle with an exclamation, centred at (cx,cy)."""
    h=s; w=s*1.15
    p=[(cx,cy-h/2),(cx-w/2,cy+h/2),(cx+w/2,cy+h/2)]
    d.polygon(p,fill=col,outline=shade(col,1.3))
    # exclamation
    ew=max(2,int(s*0.07))
    d.rounded_rectangle((cx-ew,cy-h*0.12,cx+ew,cy+h*0.20),radius=ew,fill=(20,20,20))
    d.ellipse((cx-ew,cy+h*0.27,cx+ew,cy+h*0.27+2*ew),fill=(20,20,20))

# ---- layout: measure content, then render at computed height ----
def layout(cfg):
    dummy=ImageDraw.Draw(Image.new("RGB",(W,10)))
    plan=[]; y=52
    tf=fit(dummy,cfg["title"],W-230,52)   # leave room for triangles
    plan.append(("title",y,tf)); y+=tf.size+22
    plan.append(("sub",y,None)); y+=40
    plan.append(("badge",y,None)); y+=92
    hl=wrap(dummy,cfg.get("headline",""),B(25),W-2*MX)
    plan.append(("headline",y,hl)); y+=len(hl)*32+18
    # case panel
    cl=wrap(dummy,cfg["case"],R(20),W-2*MX-68)
    ph=40+len(cl)*30+26
    plan.append(("case",y,(cl,ph))); y+=ph+22
    # sections
    for sec in cfg["sections"]:
        rows=[]; ih=0
        for it in sec["items"]:
            wl=wrap(dummy,it,R(20),W-2*MX-58)
            rows.append(wl); ih+=len(wl)*28+15
        sh=54+ih+14
        plan.append(("section",y,(sec,rows,sh))); y+=sh+22
    # ack banner
    al=wrap(dummy,cfg["ack"],B(21),W-2*MX-56)
    ah=34+len(al)*30+22
    plan.append(("ack",y,(al,ah))); y+=ah+20
    plan.append(("footer",y,None)); y+=40
    return plan,y+30

def ambient(H):
    img=Image.new("RGB",(W,H),BG); gd=ImageDraw.Draw(img)
    for r,col,cx,cy in [(460,(52,26,26),140,110),(380,(40,34,20),W-130,H-160)]:
        for i in range(r,0,-6):
            gd.ellipse((cx-i,cy-i,cx+i,cy+i),fill=lerp(col,BG,i/r))
    return img

def render(cfg,plan,H,reveal=1.0,pulse=0.0):
    img=ambient(H).convert("RGBA"); cx=W//2
    for kind,y,extra in plan:
        d=ImageDraw.Draw(img,"RGBA")
        if kind=="title":
            tf=extra; tw=d.textlength(cfg["title"],font=tf)
            # red glow
            glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
            a=int(80+95*pulse)
            gd.text((cx-tw/2,y),cfg["title"],font=tf,fill=RED+(a,))
            glow=glow.filter(ImageFilter.GaussianBlur(15)); img.alpha_composite(glow)
            d=ImageDraw.Draw(img,"RGBA")
            d.text((cx-tw/2,y),cfg["title"],font=tf,fill=REDX)
            ts=tf.size*0.92; tcy=y+tf.size*0.5
            tcol=shade(AMBER,1.0)
            warn_tri(d,cx-tw/2-ts*0.85,tcy,ts,tcol)
            warn_tri(d,cx+tw/2+ts*0.85,tcy,ts,tcol)
        elif kind=="sub":
            center(d,cx,y,cfg["sub"],R(19),MUTE)
        elif kind=="badge":
            sev=cfg.get("severity","CRITICAL")
            rw,rh=330,60; x0=cx-rw//2
            glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
            gd.rounded_rectangle((x0-8,y-8,x0+rw+8,y+rh+8),radius=rh//2+8,
                                 fill=RED+(int(80+80*pulse),))
            glow=glow.filter(ImageFilter.GaussianBlur(16)); img.alpha_composite(glow)
            d=ImageDraw.Draw(img,"RGBA")
            d.rounded_rectangle((x0,y,x0+rw,y+rh),radius=rh//2,fill=shade(RED,0.9),
                                outline=shade(RED,1.4),width=2)
            lbl=sev+"  ALERT"; lf=B(26); lw=d.textlength(lbl,font=lf)
            d.text((cx-lw/2,y+15),lbl,font=lf,fill=WHITE)
        elif kind=="headline":
            yy=y
            for ln in extra:
                center(d,cx,yy,ln,B(25),WHITE); yy+=32
        elif kind=="case":
            cl,ph=extra
            d.rounded_rectangle((MX,y,W-MX,y+ph),radius=20,fill=PANEL)
            d.text((MX+30,y+20),"WHAT TRIGGERED THIS",font=B(16),fill=GOLD)
            yy=y+52
            for ln in cl: d.text((MX+30,yy),ln,font=R(20),fill=BODY); yy+=30
        elif kind=="section":
            sec,rows,sh=extra; col=COLS.get(sec.get("color","red"),RED)
            d.rounded_rectangle((MX,y,W-MX,y+sh),radius=20,fill=PANEL)
            d.text((MX+30,y+22),sec["title"],font=B(18),fill=col)
            yy=y+54
            for wl in rows:
                d.ellipse((MX+30,yy+7,MX+40,yy+17),fill=col)
                for i,ln in enumerate(wl):
                    d.text((MX+56,yy+i*28),ln,font=R(20),fill=BODY)
                yy+=len(wl)*28+15
        elif kind=="ack":
            al,ah=extra
            d.rounded_rectangle((MX,y,W-MX,y+ah),radius=18,
                                fill=shade(RED,0.32),outline=REDX,width=2)
            d.text((MX+28,y+16),"RESPONSE REQUIRED",font=B(15),fill=REDX)
            yy=y+40
            for ln in al: d.text((MX+28,yy),ln,font=B(21),fill=WHITE); yy+=30
        elif kind=="footer":
            center(d,cx,y,cfg["footer"],B(16),GOLD)
    if reveal<1.0:
        cut=int(40+(H-40)*reveal)
        ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
        od.rectangle((0,cut,W,H),fill=BG+(255,))
        for i in range(46):
            od.rectangle((0,cut-i,W,cut-i+1),fill=BG+(int(255*(i/46)),))
        img.alpha_composite(ov)
    return img.convert("RGB")

def main():
    if len(sys.argv)<3:
        print("usage: render_incident.py <config.json> <out_basepath>"); sys.exit(1)
    cfg=json.load(open(sys.argv[1])); out=sys.argv[2]
    plan,H=layout(cfg)
    render(cfg,plan,H,1.0,0.6).save(out+".jpg","JPEG",quality=94)
    frames=[]; steps=16
    for s in range(steps+1):
        t=s/steps; ease=1-(1-t)*(1-t)
        frames.append(render(cfg,plan,H,reveal=max(0.05,ease),pulse=0.0))
    for k in range(22):
        pulse=0.5+0.5*math.sin(k/22*2*math.pi)
        frames.append(render(cfg,plan,H,reveal=1.0,pulse=pulse))
    durations=[55]*(steps+1)+[70]*22
    frames[0].save(out+".gif",save_all=True,append_images=frames[1:],
                   duration=durations,loop=0,optimize=True)
    print("wrote",out+".gif","H=",H)

if __name__=="__main__": main()
