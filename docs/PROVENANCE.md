# Source and validation

## Attribution

Driver sources retain their original copyright and GPL notices, including
Ronald Tschalär's iBridge, Touch Bar and ambient light sensor drivers.

Vendored source was copied from
[nohzafk/omarchy-macbookpro-t1](https://github.com/nohzafk/omarchy-macbookpro-t1)
at commit `8e479f0`, `drivers/appleibridge/`, which includes community adaptations
from [F13-Kr1pt0n/macbook-pro-touchbar-driver](https://github.com/F13-Kr1pt0n/macbook-pro-touchbar-driver).
The original community repository includes a compilation-order fix in the Touch
Bar source. Full source is included here; no download from a moving branch is
needed to build this release.

The deferred configuration fix follows the driver change in
[PR #3 by nolith](https://github.com/nohzafk/omarchy-macbookpro-t1/pull/3).
`deferred-configuration.patch` records the initial local change against the
vendored community source. The public source additionally carries its modification
notice and uses an explicit target-kernel Makefile/DKMS recipe.

The activation script, package and operational guides were prepared with Codex
assistance on 2026-10-09. This repository retains upstream author credit; it does
not claim authorship of the inherited drivers.

## References

- [USB core configuration helper](https://github.com/torvalds/linux/blob/master/drivers/usb/core/message.c):
  the asynchronous helper takes a USB device reference and queues USB core work;
  return success means queued, not completed.
- [Arch DKMS package guidelines](https://wiki.archlinux.org/title/DKMS_package_guidelines)
- [Arch DKMS operations](https://wiki.archlinux.org/title/Dynamic_Kernel_Module_Support)
- [PKGBUILD reference](https://man.archlinux.org/man/PKGBUILD.5.en)

## Observed behavior

On MacBookPro13,2 / Omarchy Quattro / kernel 7.2.5-3-omarchy:

1. Original auto-mode probe selected USB configuration 2 and deadlocked in
   `device_del()` beneath synchronous `usb_set_configuration()`.
2. Patched coordinator loaded in explicit keyboard mode and reached `live`.
3. Configuration 1 remained active with no reconfiguration request.
4. Both HID interfaces were bound to apple-ibridge-hid before loading apple_ib_tb.
5. The Touch Bar exposed fnmode=0, idle_timeout=-1 and dim_timeout=-1.
6. User confirmed Escape/F-keys working, clean shutdown and successful cold boot.

The asynchronous display/configuration-transition path was not runtime-tested.
Suspend/resume, trusted-signature enforcement, package migration, kernel upgrades
and other models need their own validation. The package build/check results are
recorded in `VALIDATION.md`.

The source also registers ordinary `resume` using its existing reset-resume
restoration routine. Missing this callback leaves the bar off after ordinary
resume or an aborted suspend. This path is built but not runtime-verified here.
