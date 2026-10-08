#!/usr/bin/env python3
"""Fetch ONLY publicly accessible originals into this independent project.
Run with internet access on your own machine, then `python build.py`.
Never modifies the original GitHub Pages site or repository.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
import os
import time

ROOT=Path(__file__).resolve().parent
BASE='https://luvvisualz.github.io/'
FILES={
 'brand/luv-visualz-logo.webp':'assets/logo.webp',
 'assets/_vinext_fonts/geist-8ac0455e797f/geist-98bbbccb.woff2':'assets/fonts/geist-latin.woff2',
 'assets/_vinext_fonts/geist-mono-00e989178794/geist-mono-013b2f2f.woff2':'assets/fonts/geist-mono-latin.woff2',
 'work/conoflex/cover.webp':'assets/media/work/conoflex/cover.webp',
 'work/conoflex/videos/poste-vial.mp4':'assets/media/work/conoflex/videos/poste-vial.mp4',
 'work/bienestar/cover.webp':'assets/media/work/bienestar/cover.webp',
 'work/bienestar/videos/silla-e60-hd.mp4':'assets/media/work/bienestar/videos/silla-e60-hd.mp4',
 'work/lupart/cover.webp':'assets/media/work/lupart/cover.webp',
 'work/lupart/videos/mundial-2026-hangcha.mp4':'assets/media/work/lupart/videos/mundial-2026-hangcha.mp4',
 'work/artistic/cover.webp':'assets/media/work/artistic/cover.webp',
 'work/artistic/videos/lost-files-01.mp4':'assets/media/work/artistic/videos/lost-files-01.mp4',
}
for source,target in FILES.items():
 dest=ROOT/target
 if dest.exists() and dest.stat().st_size>0:
  print('Already saved:',target);continue
 dest.parent.mkdir(parents=True,exist_ok=True)
 print('Downloading:',source)
 last=None
 for attempt in range(3):
  try:
   req=Request(BASE+source,headers={'User-Agent':'LuvVisualz-StaticSite-AssetMigration/1.0'})
   with urlopen(req,timeout=60) as response,open(str(dest)+'.part','wb') as out:
    while True:
     chunk=response.read(1024*1024)
     if not chunk:break
     out.write(chunk)
   assert Path(str(dest)+'.part').stat().st_size>0,'Empty file'
   os.replace(str(dest)+'.part',dest)
   print('Saved:',target, f'({dest.stat().st_size} bytes)')
   last=None;break
  except (OSError,URLError,AssertionError) as exc:
   last=exc
   Path(str(dest)+'.part').unlink(missing_ok=True)
   time.sleep(2*(attempt+1))
 if last:raise SystemExit(f'Could not download {source}: {last}')
print('All assets copied locally. Now run: python build.py')
