# Apple T1 Touch Bar · Arch & Omarchy

**Escape and F1–F12, restored on the 2016 13-inch MacBook Pro.**

A reproducible DKMS package for **MacBookPro13,2** with late, deliberate Touch Bar
activation. It includes the full driver source, the USB probe deadlock fix,
automatic kernel rebuilds, upgrade checks, and recovery tools.

| Verified on MacBookPro13,2 | Result |
| --- | --- |
| Omarchy Quattro, kernel `7.2.5-3-omarchy` | Working |
| Manual coordinator and Touch Bar loading | Both modules reach `live` |
| Escape and F1–F12 | Visible and responding |
| Normal shutdown and cold boot | Passed |
| Automatic activation after cold boot | Passed |
| Suspend/resume, other models, future kernels | Not yet verified |

The manual installation was verified on 2026-10-09. The package is a reproducible
way to distribute the same fix; package migration still needs a host installation
check. Compilation and packaging checks do not prove compatibility with a future
kernel.

## Start here

1. Read [installation](docs/INSTALL.md) for a fresh machine or migration.
2. Build locally as your normal user: `./scripts/build-package`.
3. Install through `scripts/install-package` in your terminal.
4. Test manually, enable the service, then verify a cold boot.

Keep the Apple firmware/EFI partition intact. This project assumes the T1 already
enumerates as **`05ac:8600`**. A device in recovery mode (`05ac:1281`) needs firmware
recovery before this driver can help. No Apple firmware is distributed here.

## Why it works

The old driver changed USB configuration synchronously from a HID probe. That
removed the device being probed and deadlocked in the kernel device core. Dropping
the driver's own mutex did not solve the device-core lock problem.

This source uses USB core's `usb_driver_set_configuration()` helper. USB core
retains the device reference and queues the change outside the probe task. In the
supported keyboard-mode path, configuration 1 is already active, so the driver
returns without requesting any change.

The service keeps ACPI/HID alias autoload blocked, loads the coordinator explicitly
with `tb_mode_param=keyboard`, discovers the current HID IDs, hands them over from
generic drivers, then loads the Touch Bar subdriver. No hardcoded HID instance
suffix, module reload, or automatic retry is used.

## Upgrades

Pacman owns the source and service files. Arch's DKMS hooks rebuild the driver for
installed kernels with matching headers. A final hook checks source integrity,
blacklists and installed module metadata. Failed checks produce a visible error;
they do not restart the Touch Bar or roll back the package transaction.

```bash
sudo apple-t1-touchbar-check --all
sudo apple-t1-touchbar-repair <kernel-release>
```

See [upgrades and recovery](docs/UPGRADES.md), including how to check the newly
installed kernel **before rebooting**. Upgrading a local package requires building
and installing a newer release; this repository does not provide a remote package
feed or silently download driver updates.

## Repository

| Path | Purpose |
| --- | --- |
| `driver/` | Complete driver source and DKMS recipe |
| `scripts/` | Build, migration, activation, verification and recovery |
| `systemd/` | Activation after the normal system boot target |
| `packaging/` | Boot protections and post-upgrade check hook |
| `docs/` | Installation, upgrades, recovery and technical background |
| `tests/` | Local source, packaging and build checks |

The package touches only this driver and its activation files. It does not install
an audio driver, repartition disks, modify Apple firmware, configure Wi-Fi, or
alter Limine verification. Standard system package hooks may regenerate boot
images during kernel/package transactions; use the distribution's supported boot
entry tooling if that requires synchronization.

GPL-2.0-only. See [LICENSE](LICENSE) and [source attribution](docs/PROVENANCE.md).
