# Contributing

Keep changes small and report the exact hardware model, kernel, headers, DKMS
version and boot state. Share relevant logs with personal information removed.
Do not attach firmware, signing keys, full machine backups or raw disk images.

For source or packaging changes:

```bash
python3 tests/update-checksums.py
python3 tests/check-repository.py
./scripts/build-package
python3 tests/check-repository.py build/apple-t1-touchbar-dkms-0.1-1-x86_64.pkg.tar.zst
```

Bump `pkgrel` for a revised package. Keep the DKMS version consistent in the source
recipe, package paths and operational scripts. Test a non-running target kernel's
build as well as the current one when kernel build behavior changes.

Runtime tests must proceed through manual activation, service idempotence, clean
shutdown and cold boot. Test suspend/resume separately. A userspace timeout does
not make a kernel module-load test safe. Never force-unload a stuck module or
silently enable activation during installation.

For another hardware model, validate configuration descriptors and HID ownership
before changing the guard. Document successes and limitations with evidence.
