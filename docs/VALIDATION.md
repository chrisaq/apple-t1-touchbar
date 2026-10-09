# Validation record

## 2026-10-09

Verified without modifying the working installation:

- `makepkg` built `apple-t1-touchbar-dkms-0.1-3-x86_64.pkg.tar.zst` successfully.
- All fixed local-source SHA-256 checksums passed.
- Package archive was extracted and every integrity-manifest entry matched.
- Package contains source and activation files, no prebuilt kernel modules or
  service-enablement links.
- Isolated DKMS build of all three public-source modules succeeded against
  7.2.5-3-omarchy headers with the revised explicit target-kernel recipe.
- Compiler build log contained no warning/error diagnostics.
- Shell syntax and systemd unit verification passed. The sandbox printed socket
  capability warnings during systemd-analyze; no unit errors were reported.

Local commands:

```bash
./scripts/build-package
python3 tests/check-repository.py build/apple-t1-touchbar-dkms-0.1-3-x86_64.pkg.tar.zst
```

The GitHub workflow checks release inputs and shell syntax with Python and
ShellCheck. CI does not have T1 hardware and cannot validate module loading,
shutdown or suspend. The workflow has not yet run on GitHub.

Runtime validation of the original manual deployment is described in
PROVENANCE.md. The package-managed migration and a real kernel-upgrade transaction
are the remaining deployment checks. The working system was not migrated during
repository preparation.

Revision 0.1-2 adds the boot-integrity helper, a Python dependency, read-only
post-transaction UKI verification on Omarchy, and supported UKI regeneration
following a manual Omarchy DKMS repair. Five boot-integrity tests pass. The same
helper was run on the host: it confirmed a mismatch, rebuilt through Limine and
verified the resulting kernel release and hash. The user subsequently rebooted and confirmed the warning was gone.
The revised package has not been installed on the host.

Revision 0.1-3 registers the normal HID resume callback. All three modules
compiled for 7.2.5-3-omarchy; its package built and passed archive/input integrity
checks. The root manual-repair script and runtime resume remain untested.
