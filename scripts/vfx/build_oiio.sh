#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

git clone https://github.com/OpenImageIO/oiio.git
cd oiio

if [[ $ASWF_OIIO_VERSION == 2.0* || $ASWF_OIIO_VERSION == 2.1* || $ASWF_OIIO_VERSION == 2.2*  ]]; then
    OIIO_TAG="Release-${ASWF_OIIO_VERSION}"
else
    OIIO_TAG="v${ASWF_OIIO_VERSION}"
fi

if [ "$ASWF_OIIO_VERSION" != "latest" ]; then
    git checkout "tags/$OIIO_TAG" -b $OIIO_TAG
fi

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DOIIO_BUILD_TOOLS=ON \
      -DOIIO_BUILD_TESTS=OFF \
      -DVERBOSE=ON \
      -DPYTHON_VERSION="${ASWF_PYTHON_MAJOR_MINOR_VERSION}" \
      -DBoost_NO_BOOST_CMAKE=ON \
      -Dpybind11_ROOT="${ASWF_INSTALL_PREFIX}" \
      -DCMAKE_CXX_STANDARD="${ASWF_CXX_STANDARD}" \
      ../.
make -j$(nproc)
make install

cd ../..
rm -rf oiio
