#!/usr/bin/env bash

set -ex

git clone https://github.com/AcademySoftwareFoundation/openvdb 
cd openvdb

git checkout b5af82007f869a29f6fa1af729f14763e99f85be # Known working at that commit...

source ${ASWF_INSTALL_PREFIX}/bin/activate_ccache.sh

ccache --show-stats

ci/build.sh clang++ Release 6 ON

ccache --show-stats
