# Installation

## 1. Confirm the machine and firmware

This release deliberately targets MacBookPro13,2. Other T1 models need their own
validation before removing the model guard.

```bash
cat /sys/class/dmi/id/product_name
uname -r
lsusb -d 05ac:8600
```

Expected model: `MacBookPro13,2`. Expected USB device: `05ac:8600`. Preserve the
original Apple EFI/firmware partition when installing Linux. Full-disk installers
can remove firmware the T1 needs. This repository does not provide a partitioning
or firmware recovery procedure; stop if the T1 is absent or in recovery mode.
A full macOS-to-Linux install is outside this project's scope.

## 2. Install prerequisites

On Omarchy, use the headers for the Omarchy kernel:

```bash
sudo pacman -S --needed base-devel dkms linux-omarchy-headers usbutils zstd
```

On standard Arch with the `linux` kernel, substitute `linux-headers`; for
`linux-lts`, use `linux-lts-headers`. Keep kernel and headers updated together.
Follow Arch's normal full-system upgrade policy if packages are out of sync.
Do not switch kernels merely to install this project.

Confirm the running kernel's headers exist:

```bash
test -d /usr/lib/modules/"$(uname -r)"/build/include
```

If an upgrade removed the running kernel's headers, complete the distribution's
normal upgrade/boot workflow first. A new kernel's successful build does not make
it loadable into the old running kernel.

## 3. Build the package

Copy or clone this repository, enter its root, and build as your normal user:

```bash
./scripts/build-package
```

The output is `build/apple-t1-touchbar-dkms-0.1-3-x86_64.pkg.tar.zst`.
Source checksums are verified. The package contains source, not prebuilt modules;
DKMS compiles on the target machine during installation.

## 4. Install or migrate

The same command handles a fresh install and the earlier manual installation:

```bash
sudo ./scripts/install-package build/apple-t1-touchbar-dkms-0.1-3-x86_64.pkg.tar.zst
```

The script validates model, firmware mode, configuration 1 and current headers;
backs up the previous source and service under `/var/lib/apple-t1-touchbar/backups`;
retains all blacklists; and disables activation while installing the package.
For a manual `appleibridge/0.1` installation, it removes that DKMS registration and
retires the unowned source before pacman installs the managed replacement. Running
modules are not unloaded. Only the named Touch Bar source and activation files
are retired; working audio and keyboard drivers are left alone.

An existing `/etc/systemd/system/touchbar.service` overrides a packaged unit in
`/usr/lib/systemd/system`. The migration script moves the old unowned override
into its backup. If another package owns it, installation stops for review.
The old `/usr/local/sbin/touchbar-enable.sh` is also retired.

Keep the displayed backup path. If installation fails, leave activation disabled
and follow [recovery](UPGRADES.md#recovery). A pacman transaction may complete even
if a DKMS build failed; the final check must pass before you proceed.

```bash
sudo apple-t1-touchbar-check --all
```

For a fresh machine, modules should remain unloaded at this point. Do not put them
in `modules-load.d` or force them into the initramfs. Module signing follows the
host DKMS configuration. Hosts enforcing trusted module signatures also need a
properly trusted DKMS signing key; this installer does not enroll keys or disable
verification.

## 5. Controlled first activation

A driver load can hang in the kernel, and a userspace timeout cannot recover that.
Keep work saved and automatic activation disabled for the first test. Do not
force-unload a module stuck in `coming`.

```bash
sudo apple-t1-touchbar-activate
cat /sys/module/apple_ibridge/initstate
cat /sys/module/apple_ib_tb/initstate
journalctl -k -b -n 60 --no-pager
```

Both states should be `live`. Expect `Touch Bar already in requested mode (cfg=1)`
and `SUCCESS: ... fnmode=0 idle=-1 dim=-1`. Escape and F1–F12 should be visible and
responding. The activator refuses a configuration other than 1 rather than making
a transition. It leaves the ALS module unloaded.

The `MBP14,3` text in driver messages is inherited from upstream; it is not a
hardware model detection result.

## 6. Service and cold boot

After manual activation succeeds:

```bash
sudo systemctl start touchbar.service
journalctl -b -u touchbar.service --no-pager
```

`Type=exec` lets the desktop proceed while activation runs. `Started` alone is
not success: wait for the script's `SUCCESS` line and confirm the keys work.
Then enable the service:

```bash
sudo systemctl enable touchbar.service
```

Shut down normally and power on again. Confirm shutdown was clean, Escape/F-keys
work after login, and this boot's journal contains `SUCCESS`. Verify audio,
keyboard, trackpad and Wi-Fi still work. Suspend/resume needs a separate test;
this release installs no sleep hooks.

## Removing the package

Retain early-boot protection before removing the source:

```bash
sudo apple-t1-touchbar-disable
sudo pacman -R apple-t1-touchbar-dkms
sudo systemctl daemon-reload
```

The recovery blacklist in `/etc/modprobe.d` intentionally survives removal.
Removing the package does not unload the modules currently in memory.
