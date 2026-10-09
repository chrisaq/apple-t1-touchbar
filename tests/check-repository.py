#!/usr/bin/env python3
"""Validate release inputs, shell syntax, and optional built package contents."""
from pathlib import Path
import hashlib
import re
import subprocess
import sys
import tarfile

root = Path(__file__).resolve().parents[1]
recipe = (root / 'PKGBUILD').read_text()
sources = re.findall(r"'([^']+)'", recipe.split('source=(', 1)[1].split(')', 1)[0])
sums = re.findall(r"'([0-9a-f]{64})'", recipe.split('sha256sums=(', 1)[1])
assert len(sources) == len(sums), 'Source/checksum count mismatch'
for name, digest in zip(sources, sums):
    matches = [p for directory in ('driver', 'scripts', 'systemd', 'packaging', '.')
               if (p := root / directory / name).is_file()]
    assert len(matches) == 1, f'Ambiguous or missing input: {name}'
    assert hashlib.sha256(matches[0].read_bytes()).hexdigest() == digest, f'Stale checksum: {name}'
for path in [root / 'PKGBUILD', *sorted((root / 'scripts').iterdir())]:
    if not path.is_file():
        continue
    if path.read_text().startswith('#!/usr/bin/env python3'):
        compile(path.read_text(), str(path), 'exec')
    else:
        subprocess.run(['bash', '-n', str(path)], check=True)
source = (root / 'driver/apple-ibridge.c').read_text()
assert not re.search(r'\bret\s*=\s*usb_set_configuration\s*\(', source), 'Synchronous configuration call returned'
assert 'usb_driver_set_configuration(udev, target_cv)' in source
tb_source = (root / 'driver/apple-ib-tb.c').read_text()
assert '.resume = appletb_reset_resume,' in tb_source, 'Normal/aborted suspend resume callback missing'
assert '.reset_resume = appletb_reset_resume,' in tb_source, 'USB reset resume callback missing'
assert 'KERNELRELEASE=${kernelver}' in (root / 'driver/dkms.conf').read_text()
assert 'KDIR=${kernel_source_dir}' in (root / 'driver/dkms.conf').read_text()
if len(sys.argv) > 1:
    # Python tarfile does not support zstd on every host; decompress with tar.
    import tempfile
    with tempfile.TemporaryDirectory() as directory:
        subprocess.run(['tar', '-xf', sys.argv[1], '-C', directory], check=True)
        package = Path(directory)
        manifest = package / 'usr/share/apple-t1-touchbar/files.sha256'
        for line in manifest.read_text().splitlines():
            digest, relative = line.split('  ', 1)
            path = package / relative
            assert path.is_file(), f'Package file missing: {relative}'
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, f'Package integrity: {relative}'
        assert not list(package.rglob('*.ko')), 'Package should ship source, not modules'
        assert not (package / 'etc/systemd/system/graphical.target.wants/touchbar.service').exists(), 'Package must not enable itself'
print('PASS: release inputs, shell syntax, deferred call path, target-kernel recipe and optional package integrity')
