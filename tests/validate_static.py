from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import subprocess

base=Path(__file__).resolve().parents[1]
class SiteParser(HTMLParser):
 def __init__(self): super().__init__(); self.ids=set(); self.links=[]; self.lang=None; self.h1=0; self.video_count=0; self.styles=[]; self.scripts=[]
 def handle_starttag(self, tag, attrs):
  d=dict(attrs)
  if tag=='html': self.lang=d.get('lang')
  if 'id' in d: self.ids.add(d['id'])
  if tag=='a' and 'href' in d: self.links.append(d['href'])
  if tag=='h1': self.h1+=1
  if tag=='video': self.video_count+=1
  if tag=='link' and d.get('rel')=='stylesheet': self.styles.append(d.get('href'))
  if tag=='script' and d.get('src'): self.scripts.append(d.get('src'))

for lang, path in [('es', base/'index.html'),('en',base/'en'/'index.html')]:
 p=SiteParser();html=path.read_text(encoding='utf-8');p.feed(html)
 assert p.lang==lang and p.h1==1 and p.video_count==1, (lang,p.lang,p.h1,p.video_count)
 assert all(x[1:] in p.ids for x in p.links if x.startswith('#')), f'Broken anchors in {lang}'
 assert sum('wa.me/' in x for x in p.links)>=2
 assert 'https://luvvisualz.github.io/' not in ''.join(p.links), 'Original portfolio linked as navigation'
 for asset in p.styles+p.scripts: assert (path.parent/asset).is_file(), asset
 assert 'data-video-url=' in html and html.count('data-video-url=')==4
 assert '<meta name="description"' in html
 print(f'PASS {lang}: one H1, four real media cards, valid local assets, anchors and WhatsApp links')
assert 'prefers-reduced-motion' in (base/'assets/style.css').read_text()
res=subprocess.run(['node','--check',str(base/'assets/app.js')],capture_output=True,text=True)
assert res.returncode==0, res.stderr
print('PASS JS syntax and reduced-motion CSS')
