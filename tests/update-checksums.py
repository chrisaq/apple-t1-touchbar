#!/usr/bin/env python3
"""Refresh the fixed local-source hashes after reviewing a source change."""
from pathlib import Path
import hashlib
import re
root = Path(__file__).resolve().parents[1]
p = root / 'PKGBUILD'
recipe = p.read_text()
names = re.findall(r"'([^']+)'", recipe.split('source=(', 1)[1].split(')', 1)[0])
hashes = []
for name in names:
    matches = [path for folder in ('driver', 'scripts', 'systemd', 'packaging', '.')
               if (path := root / folder / name).is_file()]
    if len(matches) != 1:
        raise SystemExit(f'Missing or ambiguous source: {name}')
    hashes.append(hashlib.sha256(matches[0].read_bytes()).hexdigest())
p.write_text(recipe.split('sha256sums=(', 1)[0] + 'sha256sums=(\n' +
             ''.join(f"    '{value}'\n" for value in hashes) + ')\n')
