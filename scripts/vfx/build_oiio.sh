#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

git clone https://github.com/OpenImageIO/oiio.git
cd oiio

if [ "$OIIO_VERSION" != "latest" ]; then
    git checkout "tags/Release-${OIIO_VERSION}" -b "Release-${OIIO_VERSION}"
fi

PYTHON_MAJOR_MINOR=$(echo "${PYTHON_VERSION}" | cut -d. -f-2)

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DOIIO_BUILD_TOOLS=ON \
      -DOIIO_BUILD_TESTS=OFF \
      -DVERBOSE=ON \
      -DPYTHON_VERSION="${PYTHON_MAJOR_MINOR}" \
      -DBoost_NO_BOOST_CMAKE=ON \
      ../.
make -j$(nproc)
make install

cd ../..
rm -rf oiio
