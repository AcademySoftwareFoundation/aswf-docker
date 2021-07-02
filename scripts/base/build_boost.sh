#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

BOOST_MAJOR_MINOR=$(echo "${ASWF_BOOST_VERSION}" | cut -d. -f-2)
BOOST_MAJOR=$(echo "${ASWF_BOOST_VERSION}" | cut -d. -f-1)
BOOST_MINOR=$(echo "${BOOST_MAJOR_MINOR}" | cut -d. -f2-)
BOOST_PATCH=$(echo "${ASWF_BOOST_VERSION}" | cut -d. -f3-)
BOOST_VERSION_U="${BOOST_MAJOR}_${BOOST_MINOR}_${BOOST_PATCH}"

if [[ $ASWF_BOOST_VERSION != 1.61* ]]; then
    BOOST_EXTRA_ARGS="cxxstd=14"
else
    BOOST_EXTRA_ARGS=""
fi

BOOTSTRAP_ARGS="--with-python=${ASWF_INSTALL_PREFIX}/bin/python${ASWF_PYTHON_MAJOR_MINOR_VERSION} --with-python-version=${ASWF_PYTHON_MAJOR_MINOR_VERSION} --with-python-root=${ASWF_INSTALL_PREFIX}/lib/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}"
if [[ $ASWF_PYTHON_MAJOR_MINOR_VERSION == 3.7* ]]; then
    # The unfortunate trick is the "m" in the python include path...
    echo "using python : ${ASWF_PYTHON_MAJOR_MINOR_VERSION} : ${ASWF_INSTALL_PREFIX}/bin/python${ASWF_PYTHON_MAJOR_MINOR_VERSION} : ${ASWF_INSTALL_PREFIX}/include/python${ASWF_PYTHON_MAJOR_MINOR_VERSION}m : ${ASWF_INSTALL_PREFIX}/lib ;" > ~/user-config.jam
else
    echo "using python : ${ASWF_PYTHON_MAJOR_MINOR_VERSION} : ${ASWF_INSTALL_PREFIX}/bin/python${ASWF_PYTHON_MAJOR_MINOR_VERSION} : ${ASWF_INSTALL_PREFIX}/include/python${ASWF_PYTHON_MAJOR_MINOR_VERSION} : ${ASWF_INSTALL_PREFIX}/lib ;" > ~/user-config.jam
fi

mkdir boost
cd boost

if [ ! -f "$DOWNLOADS_DIR/boost-${ASWF_BOOST_VERSION}.tar.gz" ]; then
    curl --location "https://sourceforge.net/projects/boost/files/boost/${ASWF_BOOST_VERSION}/boost_${BOOST_VERSION_U}.tar.gz" -o "$DOWNLOADS_DIR/boost-${ASWF_BOOST_VERSION}.tar.gz"
fi

tar -xzf "$DOWNLOADS_DIR/boost-${ASWF_BOOST_VERSION}.tar.gz"

cd "boost_${BOOST_VERSION_U}"
sh bootstrap.sh ${BOOTSTRAP_ARGS}
./b2 install -j2 variant=release toolset=gcc link=shared \
    --with-atomic \
    --with-chrono \
    --with-container \
    --with-context \
    --with-coroutine \
    --with-date_time \
    --with-exception \
    --with-filesystem \
    --with-graph \
    --with-graph_parallel \
    --with-iostreams \
    --with-locale \
    --with-log \
    --with-math \
    --with-mpi \
    --with-program_options \
    --with-random \
    --with-regex \
    --with-serialization \
    --with-system \
    --with-test \
    --with-thread \
    --with-timer \
    --with-type_erasure \
    --with-wave \
    --prefix="${ASWF_INSTALL_PREFIX}" \
    --with-python \
    ${BOOST_EXTRA_ARGS}

cd ../..
rm -rf boost
