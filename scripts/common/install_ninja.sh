#!/usr/bin/env bash

set -ex

if [ ! -f $DOWNLOADS_DIR/ninja-${NINJA_VERSION}.zip ]; then
    curl --location https://github.com/ninja-build/ninja/releases/download/v${NINJA_VERSION}/ninja-linux.zip -o $DOWNLOADS_DIR/ninja-${NINJA_VERSION}.zip
fi
unzip $DOWNLOADS_DIR/ninja-${NINJA_VERSION}.zip -d /usr/local/bin
chmod a+x /usr/local/bin/ninja
