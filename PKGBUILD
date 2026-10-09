# SPDX-License-Identifier: GPL-2.0-only
pkgname=apple-t1-touchbar-dkms
pkgver=0.1
pkgrel=2
pkgdesc='Apple T1 Touch Bar keyboard mode with deferred USB configuration and late activation'
arch=('x86_64')
license=('GPL-2.0-only')
depends=('dkms' 'bash' 'systemd' 'kmod' 'util-linux' 'zstd' 'python')
makedepends=('coreutils')
optdepends=('linux-omarchy-headers: build against the Omarchy kernel'
            'linux-headers: build against the Arch kernel'
            'linux-lts-headers: build against the Arch LTS kernel')
conflicts=('appleibridge-dkms')
options=('!strip')
source=(
    'apple-ibridge.c'
    'apple-ibridge.h'
    'apple-ib-tb.c'
    'apple-ib-als.c'
    'Makefile'
    'dkms.conf'
    'activate'
    'check'
    'repair'
    'disable'
    'boot-integrity'
    'touchbar.service'
    'apple-t1-touchbar.conf'
    '99-apple-t1-touchbar-check.hook'
    'LICENSE'
)
package() {
    install -d "$pkgdir/usr/src/appleibridge-0.1"
    install -m 644 "$srcdir/"*.c "$srcdir/apple-ibridge.h" "$srcdir/Makefile" "$srcdir/dkms.conf" "$pkgdir/usr/src/appleibridge-0.1/"
    for command in activate check repair disable boot-integrity; do
        install -Dm755 "$srcdir/$command" "$pkgdir/usr/bin/apple-t1-touchbar-$command"
    done
    install -Dm644 "$srcdir/touchbar.service" "$pkgdir/usr/lib/systemd/system/touchbar.service"
    install -Dm644 "$srcdir/apple-t1-touchbar.conf" "$pkgdir/usr/lib/modprobe.d/apple-t1-touchbar.conf"
    install -Dm644 "$srcdir/99-apple-t1-touchbar-check.hook" "$pkgdir/usr/share/libalpm/hooks/99-apple-t1-touchbar-check.hook"
    install -Dm644 "$srcdir/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    install -d "$pkgdir/usr/share/apple-t1-touchbar"
    (cd "$pkgdir"; find usr/src/appleibridge-0.1 usr/bin/apple-t1-touchbar-* \
        usr/lib/systemd/system/touchbar.service usr/lib/modprobe.d/apple-t1-touchbar.conf \
        usr/share/libalpm/hooks/99-apple-t1-touchbar-check.hook -type f -print0 | \
        sort -z | xargs -0 sha256sum) > "$pkgdir/usr/share/apple-t1-touchbar/files.sha256"
}

sha256sums=(
    '8a1cdaaf0c4312857833ef0a859ab8989b3d2724b8a225bd1e8acad3459d7cb9'
    '0b95701c3ec490b3e158ced93c2a4233551d21ce945d99d436fee3684f850150'
    '5cfc8a9c27aa91eb6e4a1f39411427c08c8fd6de4ec9226c65128ed0c5fda6d1'
    '3b0a13160e5091420cff507ccc87f6b1e7127932a5c120ee345365d0870477ef'
    'df27e95a65577fe7f42ff9feb4b6865d824ec2edaf03ef3f904285d233070265'
    '1b8c4d5d0078c13e4cea7e05f30166f9fb3ebde1bf25bf42f3b73e96d775ed2f'
    'd602483f40c54fe7cca86c0b5c3aca44b4d1927427379780754f771f6c27a212'
    'fcffacf318ea120a3de70e790f4f11407442833273c14552741ab33808f02deb'
    '2535f6f892626cc09683671340fdb0e907dd422c0e713c6522d9ae5cbea7a551'
    '1ab3307687320672e47e9b18251b43b6b323c88863533e489df208bb872958e5'
    'e807bd92174fa14ee91f2116f6ca4bbb64e1443e3334619c826a1c858a3cdb50'
    '379cbee879ae4661b600290c98034ebe12afa633adcb8b2b9e6c6fb7a3351500'
    '3dfdd08113ab8df1f84c6aaa5507f5149b62f84eb7e75b0c533c8637d7fc7923'
    '013dd8b88f4b8ccd44f4f24b3aa7f41dfba7834ba691818404aa296748b01428'
    'db296f2f7f35bca3a174efb0eb392b3b17bd94b341851429a3dff411b1c2fc73'
)
