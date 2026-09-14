#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Install Rez from the official source release, using the upstream-supported
# installer (install.py) rather than "pip install rez": per
# https://rez.readthedocs.io/en/stable/installation.html pip-installed Rez
# command line tools print an unsupported-installation warning and are not
# guaranteed to work inside resolved environments.
#
# The install lands in its own prefix (${ASWF_INSTALL_PREFIX}/rez) because
# installed Rez trees must never be moved after installation (the install
# carries absolute paths); only this final image location is baked in at
# build time.
#
# The release source tarball is downloaded from the AcademySoftwareFoundation
# rez GitHub releases (the filtered "rez-<version>.tar.gz" artifact produced
# by the release process, not the full repository archive).

set -ex

REZ_VERSION="${ASWF_REZ_VERSION:?ASWF_REZ_VERSION must be set (per-year VFX Platform version)}"
REZ_INSTALL_DIR="${ASWF_INSTALL_PREFIX:-/usr/local}/rez"

if [[ ! -f "$DOWNLOADS_DIR/rez-${REZ_VERSION}.tar.gz" ]]; then
    curl --location --fail \
        "https://github.com/AcademySoftwareFoundation/rez/releases/download/${REZ_VERSION}/rez-${REZ_VERSION}.tar.gz" \
        -o "$DOWNLOADS_DIR/rez-${REZ_VERSION}.tar.gz"
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

cp "$DOWNLOADS_DIR/rez-${REZ_VERSION}.tar.gz" "$workdir/rez.tar.gz"

mkdir "${workdir}/src"
tar xf "${workdir}/rez.tar.gz" -C "${workdir}/src" --strip-components 1

cd "${workdir}/src"
python3 ./install.py "${REZ_INSTALL_DIR}"

"${REZ_INSTALL_DIR}"/bin/rez/rez --version
