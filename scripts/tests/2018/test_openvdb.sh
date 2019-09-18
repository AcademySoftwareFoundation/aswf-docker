#!/usr/bin/env bash

set -ex

git clone https://github.com/AcademySoftwareFoundation/openvdb 
cd openvdb

git checkout b5af82007f869a29f6fa1af729f14763e99f85be # Known working at that commit...

ci/build.sh clang++ Release 6 ON
