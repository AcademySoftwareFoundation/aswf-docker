#!/usr/bin/env bash

set -ex

if [ ! -f $DOWNLOADS_DIR/ninja-${NINJA_VERSION}.tar.gz ]; then
    curl --location https://github.com/ninja-build/ninja/archive/v${NINJA_VERSION}.tar.gz -o $DOWNLOADS_DIR/ninja-${NINJA_VERSION}.tar.gz
fi

tar xf $DOWNLOADS_DIR/ninja-${NINJA_VERSION}.tar.gz
cd ninja-${NINJA_VERSION}

./configure.py --bootstrap

sudo cp ninja /usr/local/bin/ninja
