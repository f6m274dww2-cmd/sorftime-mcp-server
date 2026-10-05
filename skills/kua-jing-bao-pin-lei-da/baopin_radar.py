# -*- coding: utf-8 -*-
"""爆品雷达：1688 专供扫描 → HTML 日报（精简版，每日跑）。依赖本机 sorftime-seller-agent bridge。"""
import argparse, datetime, json, os, pathlib, subprocess
SKROOT=os.environ.get('SORFTIME_SKILL') or str(pathlib.Path(__file__).resolve().parent.parent / 'sorftime-seller-agent')
ZHUANG=['跨境专供','亚马逊专供','外贸','跨境','出口','亚马逊','Amazon']
def call(tool,args):
    r=subprocess.run(['python3.12','scripts/sorftime_bridge.py','--one-shot',tool,json.dumps(args,ensure_ascii=False)],
                     capture_output=True,text=True,env=dict(os.environ),timeout=90,cwd=SKROOT)
    try: return json.loads(r.stdout)
    except Exception: return {}
def items(resp):
    if not isinstance(resp,dict): return []
    d=resp.get('data',resp)
    if isinstance(d,dict):
        for v in d.values():
            if isinstance(v,list): return v
        return []
    return d if isinstance(d,list) else []
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--kw',default='keywords.txt'); ap.add_argument('--out',default='爆品雷达日报.html'); a=ap.parse_args()
    kws=[l.strip() for l in pathlib.Path(a.kw).read_text(encoding='utf-8').splitlines() if l.strip()]
    hits=[]
    for kw in kws:
        for it in items(call('ali1688_similar_product',{'search_name':kw})):
            t=str(it.get('title') or '')
            if any(x in t for x in ZHUANG): hits.append({'kw':kw,'title':t,'price':it.get('price'),'pid':it.get('product_id'),'store':it.get('store_name'),'sales':it.get('sales_of_30d')})
    seen=set(); out=[]
    for h in hits:
        if h['pid'] in seen: continue
        seen.add(h['pid']); out.append(h)
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    rows=''.join(f'<tr><td>{h["kw"]}</td><td>{h["title"][:44]}</td><td>{h["price"]}</td><td>{h["sales"]}</td><td>{h["store"]}</td></tr>' for h in out[:200])
    html=f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>爆品雷达日报</title><style>body{{font-family:-apple-system,"PingFang SC",sans-serif;margin:0;background:#eef2fb;color:#0f1b38}}.w{{max-width:1000px;margin:auto;padding:20px}}.h{{background:linear-gradient(120deg,#0d1830,#2c2150);color:#fff;border-radius:16px;padding:22px}}table{{width:100%;border-collapse:collapse;background:#fff;font-size:13px}}th{{background:#172554;color:#fff;padding:8px;text-align:left}}td{{padding:8px;border-bottom:1px solid #e4e9f5}}</style></head><body><div class="w"><div class="h"><h1>📡 爆品雷达日报</h1><p>{now} · 扫描 {len(kws)} 词 · 专供候选 {len(out)} 条（估算列由下钻补全）</p></div><table><tr><th>类目词</th><th>产品</th><th>价格¥</th><th>30天销量</th><th>店铺</th></tr>{rows}</table></div></body></html>'
    pathlib.Path(a.out).write_text(html,encoding='utf-8'); print('OK',a.out,len(out))
if __name__=='__main__': main()
