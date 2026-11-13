"""Prepublication checks for the approved ten-video ES/EN layout.

Run with --require-media after the MP4 files have been integrated.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRE_MEDIA = '--require-media' in sys.argv[1:]

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.videos = []
        self.assets = []
        self.quality_sources = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'html':
            self.lang = data.get('lang')
        if 'id' in data:
            self.ids.add(data['id'])
        if tag == 'a' and 'href' in data:
            self.links.append(data['href'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'video':
            self.videos.append((data.get('src'), data.get('poster')))
        if tag == 'link' and data.get('rel') == 'stylesheet':
            self.assets.append(data.get('href'))
        if tag == 'script' and data.get('src'):
            self.assets.append(data['src'])
        if tag == 'option' and data.get('data-src'):
            self.quality_sources.append(data['data-src'])

def local_path(page, url):
    if not url or urlparse(url).scheme or url.startswith('//'):
        return None
    return (page.parent / url).resolve()

pages = []
missing_media = set()
for lang, page in [('es', ROOT / 'index.html'), ('en', ROOT / 'en/index.html')]:
    parser = SiteParser()
    html = page.read_text(encoding='utf-8')
    parser.feed(html)
    assert parser.lang == lang and parser.h1 == 1, f'{lang}: language or H1'
    assert len(parser.videos) == 10, f'{lang}: expected ten videos'
    assert all(link[1:] in parser.ids for link in parser.links if link.startswith('#')), f'{lang}: broken anchor'
    assert sum('wa.me/' in link for link in parser.links) >= 2, f'{lang}: contact links'
    assert all(local_path(page, asset).is_file() for asset in parser.assets), f'{lang}: CSS or JS missing'
    assert all(local_path(page, poster) and local_path(page, poster).is_file()
               for _, poster in parser.videos), f'{lang}: cover missing'
    for src, _ in parser.videos:
        path = local_path(page, src)
        if path and not path.is_file():
            missing_media.add(path.relative_to(ROOT))
    pages.append((parser, page))
    print(f'PASS {lang}: ten videos, ten covers, assets, anchors and contact links')

es, es_page = pages[0]
en, en_page = pages[1]
def media_references(parser, page):
    return [(
        str(local_path(page, src)) if local_path(page, src) else src,
        str(local_path(page, poster))
    ) for src, poster in parser.videos]

assert media_references(es, es_page) == media_references(en, en_page), 'ES/EN media references differ'
assert 'prefers-reduced-motion' in (ROOT / 'assets/style-v7.css').read_text()
result = subprocess.run(['node', '--check', str(ROOT / 'assets/app.js')], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
print('PASS ES/EN media parity, JavaScript syntax and reduced motion')
if missing_media:
    print('Local MP4 still needed:')
    for path in sorted(missing_media):
        print(f'  {path}')
    if REQUIRE_MEDIA:
        raise SystemExit(1)
