#!/usr/bin/env python3
"""Download and size-check the six public Drive masters for the media workflow."""
import argparse
from pathlib import Path
import gdown

MASTERS = (
    ('1Wm20YNll7Yxtvabu0Qed-Fbk5ByxoYm5', 'INTERSEC 2026.mp4', 228196616),
    ('1elEisTlFEqSoYijxZG-fS8SuysOMDniA', 'VALLA PORTÁTIL.mp4', 234656968),
    ('1RR4dz6KfotsRt2nEqZlScR9C7H_9LXQ8', '01-VIOS - MARRIOTT HOTEL - LA RIOJANA.mp4', 93214559),
    ('1UCPN-u7bnQqFrXh6IZ0tEQb0jfGxBHpu', '02-CLUB DE PLAYA - LA RIOJANA.mp4', 72083793),
    ('1vnXJcSUv89zyo71pTBy3w3RYASW2VKvD', 'SPA 2.mp4', 40046824),
    ('143wejxOo3C4xq7YI_u6ipLRCcDw48_8_', 'LOLOG GENERAL.mp4', 30382525),
)

parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
args.output_dir.mkdir(parents=True, exist_ok=True)
for file_id, name, expected_size in MASTERS:
    target = args.output_dir / name
    if target.is_file() and target.stat().st_size == expected_size:
        print('Already downloaded:', name, flush=True)
        continue
    target.unlink(missing_ok=True)
    result = gdown.download(id=file_id, output=str(target), quiet=False)
    if not result or not target.is_file() or target.stat().st_size != expected_size:
        raise SystemExit(f'Drive download failed or size mismatch for {name}')
    print(f'OK {name}: {expected_size} bytes', flush=True)
