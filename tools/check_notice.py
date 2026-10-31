import sys, json, re, html
from html.parser import HTMLParser
page, adf, lang = sys.argv[1], sys.argv[2], sys.argv[3]
class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.inn=0; s.cur=None; s.out=[]
    def handle_starttag(s,t,a):
        if t=='div' and ('id','notice') in a: s.inn=1
        elif s.inn and t=='p': s.cur=''
    def handle_endtag(s,t):
        if s.inn and t=='p': s.out.append(s.cur); s.cur=None
        elif t=='div': s.inn=0
    def handle_data(s,d):
        if s.cur is not None: s.cur+=d
p=P(); p.feed(open(page,encoding='utf-8').read())
open(f'{sys.argv[4]}/{lang}-from-html.txt','w',encoding='utf-8').write('\n'.join(p.out))
for para in json.load(open(adf,encoding='utf-8')):
    t=''.join(n['text'] for n in para['content'])
    if t.startswith(lang.upper()):
        open(f'{sys.argv[4]}/{lang}-from-adf.txt','w',encoding='utf-8').write('\n'.join(t.split('\n')[1:]))
