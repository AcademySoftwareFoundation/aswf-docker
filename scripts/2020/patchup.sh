#!/usr/bin/env bash

set -ex

echo "Updating to newer cmake to enable python-3"

export CMAKE_VERSION=3.14.5
/tmp/install_cmake.sh
