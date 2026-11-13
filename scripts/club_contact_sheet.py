#!/usr/bin/env python3
"""Create nine evenly spaced frames for human review of the Club de Playa master."""
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from PIL import Image, ImageDraw

source, output = map(Path, sys.argv[1:3])
info = json.loads(subprocess.check_output([
    'ffprobe', '-v', 'error', '-show_format', '-of', 'json', str(source)], text=True))
duration = float(info['format']['duration'])
with TemporaryDirectory() as folder:
    canvas = Image.new('RGB', (1440, 900), '#101010')
    draw = ImageDraw.Draw(canvas)
    for i in range(9):
        point = duration * (i + 0.5) / 9
        frame = Path(folder) / f'{i}.jpg'
        subprocess.run([
            'ffmpeg', '-v', 'error', '-ss', str(point), '-i', str(source),
            '-frames:v', '1', '-vf', 'scale=480:270:force_original_aspect_ratio=decrease',
            '-y', str(frame)], check=True)
        image = Image.open(frame).convert('RGB')
        x, y = i % 3 * 480, i // 3 * 300
        canvas.paste(image, (x + (480 - image.width) // 2, y))
        draw.text((x + 8, y + 274), f'{point:.1f}s / {duration:.1f}s', fill='white')
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, quality=88, optimize=True)
