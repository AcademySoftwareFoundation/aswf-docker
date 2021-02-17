#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

LOG4CPLUS_MAJOR_MINOR=$(echo "${ASWF_LOG4CPLUS_VERSION}" | cut -d. -f-2)
LOG4CPLUS_MAJOR=$(echo "${ASWF_LOG4CPLUS_VERSION}" | cut -d. -f-1)
LOG4CPLUS_MINOR=$(echo "${LOG4CPLUS_MAJOR_MINOR}" | cut -d. -f2-)
LOG4CPLUS_PATCH=$(echo "${ASWF_LOG4CPLUS_VERSION}" | cut -d. -f3-)

git clone https://github.com/log4cplus/log4cplus.git
cd log4cplus

if [ "$ASWF_LOG4CPLUS_VERSION" != "latest" ]; then
    git checkout "tags/REL_${LOG4CPLUS_MAJOR}_${LOG4CPLUS_MINOR}_${LOG4CPLUS_PATCH}" -b "${ASWF_LOG4CPLUS_VERSION}"
fi

mkdir build
cd build
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" ..
make -j$(nproc)
make install

cd ../..
rm -rf log4cplus
