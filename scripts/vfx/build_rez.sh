#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Install Rez from the official source release, using the upstream-supported
# installer (install.py) rather than "pip install rez": per
# https://rez.readthedocs.io/en/stable/installation.html pip-installed Rez
# command line tools print an unsupported-installation warning and are not
# guaranteed to work inside resolved environments.
#
# The install lands in its own prefix (/usr/local/rez) because installed Rez
# trees must never be moved after installation (the install carries absolute
# paths); only this final image location is baked in at build time.

set -ex

REZ_VERSION="${ASWF_REZ_VERSION:-3.4.0}"
REZ_INSTALL_DIR="/usr/local/rez"
# sha256 of https://github.com/AcademySoftwareFoundation/rez/releases/download/<version>/<version>.tar.gz
REZ_TARBALL_SHA256="bcef8c8d04c9846d2369b04fad2a22c1e6761c3b5a60ebe13cc42169152c3d1f"

if [[ ! -f "$DOWNLOADS_DIR/rez-${REZ_VERSION}.tar.gz" ]]; then
    curl --location --fail \
        "https://github.com/AcademySoftwareFoundation/rez/releases/download/${REZ_VERSION}/${REZ_VERSION}.tar.gz" \
        -o "$DOWNLOADS_DIR/rez-${REZ_VERSION}.tar.gz"
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

cp "$DOWNLOADS_DIR/rez-${REZ_VERSION}.tar.gz" "$workdir/rez.tar.gz"
echo "${REZ_TARBALL_SHA256}  ${workdir}/rez.tar.gz" | sha256sum -c -

mkdir "${workdir}/src"
tar xf "${workdir}/rez.tar.gz" -C "${workdir}/src" --strip-components 1

cd "${workdir}/src"
python3 ./install.py "${REZ_INSTALL_DIR}"

"${REZ_INSTALL_DIR}"/bin/rez/rez --version
