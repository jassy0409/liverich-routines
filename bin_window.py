import json, sys, re
from datetime import datetime
def clean(t):
    t = re.sub(r'<[^>]+>', '', t or '')
    return t.replace('&amp;','&').strip()
MODEL=4669068
def load(path):
    d=json.load(open(path))
    if isinstance(d,list) and d and 'text' in d[0]:
        inner=json.loads(d[0]['text'])['response']['data']
    else:
        inner=d['response']['data']
    return inner
rows=[]
for p in sys.argv[1:]:
    for m in load(p):
        ts=m.get('createdAt','')
        who='chatter' if m.get('fromUser',{}).get('id')==MODEL else 'fan'
        price=m.get('price',0); tip=m.get('isTip'); mc=m.get('mediaCount',0)
        tag=''
        if price and not tip: tag=f'[PPV${price} {mc}media]'
        if tip: tag=f'[TIP]'
        rows.append((ts, who, tag, clean(m.get('text',''))[:90]))
rows=sorted(set(rows))
for ts,who,tag,txt in rows:
    # window: 2026-06-24 07:00 to 15:00 UTC
    if '2026-06-24T07' <= ts[:13] or (ts[:10]=='2026-06-24' and '07:00'<=ts[11:16]<='15:00'):
        inwin = ('2026-06-24T07:00' <= ts[:16] <= '2026-06-24T15:00')
    else:
        inwin=False
    mark='>>' if inwin else '  '
    print(f"{mark} {ts[:16]} | {who:7} | {tag} {txt}")
