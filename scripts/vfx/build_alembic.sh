#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir alembic
cd alembic

if [ ! -f "$DOWNLOADS_DIR/hdf5-${ASWF_HDF5_VERSION}.tar.gz" ]; then
    curl --location "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-${ASWF_HDF5_VERSION}/src/hdf5-${ASWF_HDF5_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/hdf5-${ASWF_HDF5_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/hdf5-${ASWF_HDF5_VERSION}.tar.gz"
cd "hdf5-${ASWF_HDF5_VERSION}"
./configure \
    --prefix="${ASWF_INSTALL_PREFIX}" \
    --enable-threadsafe \
    --disable-hl \
    --with-pthread=/usr/include
make -j$(nproc)
make install

cd ..

if [ ! -f "$DOWNLOADS_DIR/alembic-${ASWF_ALEMBIC_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/alembic/alembic/archive/${ASWF_ALEMBIC_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/alembic-${ASWF_ALEMBIC_VERSION}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/alembic-${ASWF_ALEMBIC_VERSION}.tar.gz"
cd "alembic-${ASWF_ALEMBIC_VERSION}"

# Boost Python3 not found by cmake for PyAlembic as of Alembic 1.7.12
if [[ $ASWF_PYTHON_VERSION == 2.7* ]]; then
    USE_PYALEMBIC=TRUE
else
    USE_PYALEMBIC=FALSE
fi

cmake \
    -D CMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
    -D CMAKE_PREFIX_PATH="${ASWF_INSTALL_PREFIX}" \
    -D BOOST_ROOT="${ASWF_INSTALL_PREFIX}" \
    -D ILMBASE_ROOT="${ASWF_INSTALL_PREFIX}" \
    -D Python_ADDITIONAL_VERSIONS=3 \
    -D USE_PYILMBASE=TRUE \
    -D USE_PYALEMBIC="${USE_PYALEMBIC}" \
    -D USE_ARNOLD=FALSE \
    -D USE_PRMAN=FALSE \
    -D USE_MAYA=FALSE \
    .
make -j$(nproc)
make install

cd ../..
rm -rf alembic
