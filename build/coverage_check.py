import re, html, json, sys
f = sys.argv[1] if len(sys.argv)>1 else 'out/心理学12_一根线串起整讲.html'
src = open(f, encoding='utf-8').read()
src = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', '', src)
src = re.sub(r'<script.*?</script>','',src,flags=re.S)
txt = html.unescape(re.sub(r'<[^>]+>', '', src))
txt = re.sub(r'\s+', '', txt)
L=[]
for p in ['a','b','c','q']: L += json.load(open(f'build/ledger_{p}.json',encoding='utf-8'))
norm = lambda s: re.sub(r'\s+','',s)
miss=[]; ok=0
for cat,desc,srcs,kws in L:
    bad=[k for k in kws if norm(k) not in txt]
    if bad: miss.append((cat,desc,bad))
    else: ok+=1
nq=sum(1 for x in L if x[0]=='真题')
print(f'[{f}] 条目总数 {len(L)}（知识点 {len(L)-nq} + 真题 {nq}）  已覆盖 {ok}  未覆盖 {len(miss)}')
for m in miss: print('  MISS',m)
