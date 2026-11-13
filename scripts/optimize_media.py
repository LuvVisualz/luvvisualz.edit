#!/usr/bin/env python3
"""Encode the six approved portfolio masters for browser playback.

Originals stay outside Git. Run with --source-dir pointing to the downloaded
Drive folder. This script changes only MP4 outputs in assets/media.
"""
import argparse
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
JOBS = (
    ('INTERSEC 2026.mp4', 'intersec/intersec-1080.mp4', 1080),
    ('INTERSEC 2026.mp4', 'intersec/intersec-720.mp4', 720),
    ('VALLA PORTÁTIL.mp4', 'valla-portatil/valla-1080.mp4', 1080),
    ('VALLA PORTÁTIL.mp4', 'valla-portatil/valla-720.mp4', 720),
    ('01-VIOS - MARRIOTT HOTEL - LA RIOJANA.mp4', 'la-riojana/vios-marriott-la-riojana.mp4', 1080),
    ('02-CLUB DE PLAYA - LA RIOJANA.mp4', 'la-riojana/club-de-playa-la-riojana.mp4', 1080),
    ('SPA 2.mp4', 'lolog-lodge/spa.mp4', 1080),
    ('LOLOG GENERAL.mp4', 'lolog-lodge/hotel-boutique.mp4', 1080),
)

def probe(path):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)

def video_stream(info):
    return next(stream for stream in info['streams'] if stream['codec_type'] == 'video')

def output_size(stream, height):
    width, source_height = int(stream['width']), int(stream['height'])
    max_width, max_height = (height * 16 // 9, height) if width >= source_height else (height, height * 16 // 9)
    scale = min(1, max_width / width, max_height / source_height)
    return max(2, 2 * math.floor(width * scale / 2)), max(2, 2 * math.floor(source_height * scale / 2))

def duration(info):
    return float(info['format']['duration'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    sources = {name: args.source_dir / name for name, _, _ in JOBS}
    missing = [str(path) for path in sources.values() if not path.is_file()]
    if missing:
        parser.error('Missing masters: ' + ', '.join(missing))
    for name, relative, height in JOBS:
        src = sources[name]
        dst = ROOT / 'assets' / 'media' / relative
        if dst.exists() and not args.force:
            print('Already exists:', dst.relative_to(ROOT))
            continue
        original = probe(src)
        stream = video_stream(original)
        width, out_height = output_size(stream, height)
        has_audio = any(s['codec_type'] == 'audio' for s in original['streams'])
        dst.parent.mkdir(parents=True, exist_ok=True)
        temp = dst.with_suffix('.encoding.mp4')
        command = [
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-stats', '-y', '-i', str(src),
            '-map', '0:v:0', '-map', '0:a:0?',
            '-vf', f'scale={width}:{out_height}:flags=lanczos',
            '-c:v', 'libx264', '-preset', 'slow', '-crf', '18' if height == 1080 else '19',
            '-maxrate', '8M' if height == 1080 else '4M',
            '-bufsize', '16M' if height == 1080 else '8M',
            '-pix_fmt', 'yuv420p', '-profile:v', 'high',
            '-c:a', 'aac', '-b:a', '160k',
            '-movflags', '+faststart', str(temp),
        ]
        print(f'Encoding {name} -> {dst.relative_to(ROOT)} ({width}x{out_height})', flush=True)
        try:
            subprocess.run(command, check=True)
            encoded = probe(temp)
            assert video_stream(encoded)['codec_name'] == 'h264'
            assert not has_audio or any(s['codec_type'] == 'audio' and s['codec_name'] == 'aac'
                                        for s in encoded['streams'])
            assert abs(duration(original) - duration(encoded)) < 0.5, 'Duration mismatch'
            assert temp.stat().st_size < 100_000_000, 'File exceeds GitHub 100 MB limit'
            temp.replace(dst)
        finally:
            temp.unlink(missing_ok=True)
        print(f'OK {dst.relative_to(ROOT)}: {dst.stat().st_size / 1_000_000:.1f} MB', flush=True)

if __name__ == '__main__':
    main()
