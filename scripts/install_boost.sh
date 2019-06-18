#!/usr/bin/env bash

set -ex

BOOST_VERSION="$1"
BOOST_MAJOR_MINOR=$(echo "${BOOST_VERSION}" | cut -d. -f-2)
BOOST_MAJOR=$(echo "${BOOST_VERSION}" | cut -d. -f-1)
BOOST_MINOR=$(echo "${BOOST_MAJOR_MINOR}" | cut -d. -f2-)
BOOST_PATCH=$(echo "${BOOST_VERSION}" | cut -d. -f3-)
BOOST_VERSION_U="${BOOST_MAJOR}_${BOOST_MINOR}_${BOOST_PATCH}"

mkdir _boost
cd _boost

wget -q https://sourceforge.net/projects/boost/files/boost/${BOOST_VERSION}/boost_${BOOST_VERSION_U}.tar.gz
tar -xzf boost_${BOOST_VERSION_U}.tar.gz

cd boost_${BOOST_VERSION_U}
sh bootstrap.sh
./b2 install -j4 variant=release toolset=gcc \
    --with-atomic \
    --with-chrono \
    --with-container \
    --with-context \
    --with-coroutine \
    --with-date_time \
    --with-exception \
    --with-fiber \
    --with-filesystem \
    --with-graph \
    --with-graph_parallel \
    --with-iostreams \
    --with-locale \
    --with-log \
    --with-math \
    --with-mpi \
    --with-program_options \
    --with-python \
    --with-random \
    --with-regex \
    --with-serialization \
    --with-signals \
    --with-stacktrace \
    --with-system \
    --with-test \
    --with-thread \
    --with-timer \
    --with-type_erasure \
    --with-wave \
    --prefix=/usr/local

cd ../..
rm -rf _boost
