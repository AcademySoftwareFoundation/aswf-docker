#!/usr/bin/env bash

set -ex

LOG4CPLUS_MAJOR_MINOR=$(echo "${LOG4CPLUS_VERSION}" | cut -d. -f-2)
LOG4CPLUS_MAJOR=$(echo "${LOG4CPLUS_VERSION}" | cut -d. -f-1)
LOG4CPLUS_MINOR=$(echo "${LOG4CPLUS_MAJOR_MINOR}" | cut -d. -f2-)
LOG4CPLUS_PATCH=$(echo "${LOG4CPLUS_VERSION}" | cut -d. -f3-)

git clone https://github.com/log4cplus/log4cplus.git
cd log4cplus

if [ "$LOG4CPLUS_VERSION" != "latest" ]; then
    git checkout tags/REL_${LOG4CPLUS_MAJOR}_${LOG4CPLUS_MINOR}_${LOG4CPLUS_PATCH} -b ${LOG4CPLUS_VERSION}
fi

mkdir build
cd build
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j4
make install

cd ../..
rm -rf log4cplus
