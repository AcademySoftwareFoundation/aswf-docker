#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir openrv
cd openrv
git clone --recursive https://github.com/AcademySoftwareFoundation/OpenRV.git .


# Take latest from main for now.

# Qt files are under /tmp/qttemp because OpenRV compiles it own PySide2 and it
# causes issues during the build when Qt is within system folder (e.g. /usr/local)
export QT_HOME=/tmp/qttemp

# Expand aliases.
shopt -s expand_aliases

# Setup environments for OpenRV.
source rvcmds.sh

# Execute the rvsetup command to install Python dependencies.
rvsetup

# There are decrepencies between Qt6 from Conan and Qt6 from the online installer regardings some directories location:
# - libexec directory is in the bin directory
# - translations is under res/datadir
# - resources is under res/datadir

# Copy those folder to the same locations as the official online installer because OpenRV expected them to be there.
mkdir /tmp/qttemp/libexec
mkdir /tmp/qttemp/translations
mkdir /tmp/qttemp/resources
cp -R /tmp/qttemp/bin/* /tmp/qttemp/libexec
cp -R /tmp/qttemp/res/datadir/translations/* /tmp/qttemp/translations
cp -R /tmp/qttemp/res/datadir/resources/* /tmp/qttemp/resources

# Configure setp.
cmake -B _build \
      -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DRV_DEPS_QT6_LOCATION=/tmp/qttemp \
      -DRV_VFX_PLATFORM=CY2024

# Build dependencies.
cmake --build _build \
      --target dependencies \
      --parallel=1 \
      -v

# Build main executable.
cmake --build _build \
      --target main_executable \
      --parallel \
      -v

# Install step.
cmake --install _build --prefix ~/openrv_install

cd ../..
rm -rf openrv
