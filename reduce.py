import json, sys, re
from datetime import datetime, timezone, timedelta

MODEL_ID = 4669068  # Shantal
PHT = timezone(timedelta(hours=8))

def clean(t):
    if not t: return ""
    t = re.sub(r'<[^>]+>',' ',t)
    t = t.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&#39;',"'").replace('&quot;','"')
    return re.sub(r'\s+',' ',t).strip()

def load_thread(path):
    d=json.load(open(path))
    inner=json.loads(d[0]['text'])
    return inner['response']['data']

def reduce_msgs(data, model_id=MODEL_ID):
    out=[]
    for m in data:
        if m.get('responseType')!='message': continue
        ca=m.get('createdAt')
        if not ca: continue
        dt=datetime.fromisoformat(ca.replace('Z','+00:00'))
        pht=dt.astimezone(PHT)
        sender='chatter' if m.get('fromUser',{}).get('id')==model_id else 'fan'
        out.append({
            'utc':dt.isoformat(),
            'pht':pht.strftime('%Y-%m-%d %H:%M'),
            'sender':sender,
            'text':clean(m.get('text','')),
            'price':m.get('price',0),
            'isTip':m.get('isTip',False),
            'isFree':m.get('isFree',True),
            'mediaCount':m.get('mediaCount',0),
            'isOpened':m.get('isOpened',None),
        })
    out.sort(key=lambda x:x['utc'])
    return out

if __name__=='__main__':
    data=load_thread(sys.argv[1])
    msgs=reduce_msgs(data)
    for m in msgs:
        tip=f" TIP${m['price']}" if m['isTip'] else ""
        ppv=f" PPV${m['price']}" if (m['price'] and not m['isTip']) else ""
        med=f" [{m['mediaCount']}media]" if m['mediaCount'] else ""
        print(f"{m['pht']} | {m['sender']:7} |{tip}{ppv}{med} {m['text'][:200]}")
