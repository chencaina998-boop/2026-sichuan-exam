import json, re, os
parts = ['p0_head.html','p1_intro_ausubel.html','p2_gagne.html','p3_schools_watson.html','p4_thorndike.html','p5_pavlov.html','p6_end.html']
html = ''.join(open('build/'+p, encoding='utf-8').read() for p in parts)
imgs = json.load(open('build/img/imgs.json'))
def rep(m):
    k = m.group(1)
    if k not in imgs: raise SystemExit('missing img '+k)
    return imgs[k]
html = re.sub(r'\{\{IMG:(S\d{3})\}\}', rep, html)
assert '{{IMG' not in html
out = 'out/心理学12_一根线串起整讲.html'
open(out,'w',encoding='utf-8').write(html)
print(out, len(html)//1024, 'KB')
