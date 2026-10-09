# Upgrades and recovery

## What survives upgrades

The package owns `/usr/src/appleibridge-0.1`, the activation commands,
`/usr/lib/systemd/system/touchbar.service`, the vendor modprobe blacklist and a
post-transaction check hook. Local service enablement survives ordinary package
upgrades. The persistent recovery blacklist in `/etc/modprobe.d` also protects
a manual migration and package removal.

Arch DKMS hooks build modules when kernel source/header paths change and when this
package's source is upgraded. The Makefile receives the target `kernelver` and
`kernel_source_dir` explicitly, so a build for a new kernel does not accidentally
use the still-running old kernel. `AUTOINSTALL=yes` supports DKMS autoinstall too.
No custom second rebuild hook is installed.

The final package hook runs `apple-t1-touchbar-check --all` as root. It validates all
installed kernel module trees, matching headers, DKMS installed state, module
kernel metadata, boot blacklists and package-file integrity. It does not load any
module. On an Omarchy installation it also verifies the primary UKI hash (requires sudo).
It does not inspect every boot image or guarantee that a
future kernel has compatible USB/HID behavior.

## Kernel and system upgrades

Use Omarchy's normal upgrade workflow or Arch's normal full-system upgrade.
Keep each installed kernel's matching headers installed. Watch the transaction
output for DKMS failures, then run:

```bash
sudo apple-t1-touchbar-check --all
```

After upgrading, `uname -r` still shows the old running kernel. `--all` deliberately
checks the newly installed kernel before reboot. If a build is missing:

```bash
ls /usr/lib/modules
sudo apple-t1-touchbar-repair <new-kernel-release>
```

Repair rebuilds only `appleibridge/0.1`; it does not reload a live module. For a
`linux-omarchy` target it also backs up, rebuilds and verifies the UKI through
the installed Limine workflow. Other kernels need their own boot-image workflow. If the
source or packaged service was modified, reinstall the package rather than
pretending a rebuild repairs source integrity.

A failing check is a checkpoint to investigate before reboot. If you need to boot
for further diagnosis, disable Touch Bar activation first. A failed post-transaction
hook cannot undo the package transaction and may not make pacman return failure.
Review its output. Keep a known-good kernel/recovery boot option available through
your distribution's normal process.

## Updating this project

Until a package repository is published, updates are explicit:

```bash
# Obtain and review the new source release, then:
./scripts/build-package
sudo pacman -U build/apple-t1-touchbar-dkms-<version>-<release>-x86_64.pkg.tar.zst
sudo systemctl daemon-reload
sudo apple-t1-touchbar-check --all
```

Ordinary package upgrades preserve service enablement and do not restart it.
Changes affect a fresh activation on a later boot. No downloader, scheduled
reinstaller or background module reload is installed.

Reinstall an unchanged release with `pacman -U` to restore package files. The
standard DKMS upgrade hooks remove/rebuild this driver when its source changes.
If the installed build remains stale, use the explicit repair command.

Maintainers must bump `pkgrel` for a package revision and regenerate source
checksums after editing package inputs. Change the DKMS source version and all
references together when making an incompatible driver release. Do not edit
package-owned files in `/usr/src` to maintain a private fix; update the source
repository and rebuild the package.

## Recovery

If activation fails while the machine is usable:

```bash
sudo apple-t1-touchbar-disable
journalctl -b -u touchbar.service --no-pager
journalctl -k -b --no-pager
```

The disable command disables future service activation and writes a persistent
blacklist. It does not stop, kill or unload a possibly stuck module. Inspect
`/sys/module/apple_ibridge/initstate`; a module in `coming` must not be force-unloaded.
An uninterruptible kernel deadlock can still require forced power-off.

If boot hangs, use a known-good recovery boot. Mount the Linux root filesystem,
retain/create `/etc/modprobe.d/apple-t1-touchbar-recovery.conf` with all three
blacklists from `packaging/apple-t1-touchbar.conf`, and remove only the
`graphical.target.wants/touchbar.service` enablement link under that root. Rebuild
an initramfs only if it actually contains the modules or stale boot protection,
using the distribution's supported tooling. Do not edit Apple EFI partitions,
disable Limine hash verification, or force-unload the wedged module.

Backups from migration are under `/var/lib/apple-t1-touchbar/backups`. For a
rollback to a previous package, first disable activation, then use `pacman -U`
with a saved known-good package and recheck builds. Restoring the old manual
source also restores its known deadlock; keep activation disabled. Do not copy
raw DKMS state over an active registration and assume installed modules match it.

Kernel/package transactions can invoke the host's ordinary boot-image hooks.
On MacBookPro13,2 with the recorded Omarchy layout, check or repair explicitly:

```bash
sudo apple-t1-touchbar-boot-integrity
sudo apple-t1-touchbar-boot-integrity --repair
```

The helper delegates rebuilding and entry updates to `limine-mkinitcpio
linux-omarchy`, saves a private UKI/configuration backup under
`/var/lib/macbookpro13-2-omarchy/boot-backups`, then verifies the embedded kernel
release and every matching BLAKE2b hash. It does not reset the boot menu, reboot,
reload modules or deploy the bootloader binary. Host boot hooks still run.
The automatic package check detects a mismatch; it never silently blesses it.
See the [cause, repair and limitations](BOOT-INTEGRITY.md).
Unsupported layouts stop for investigation. Never manually bypass verification.

