#!/usr/bin/env bash

set -ex

NINJA_VERSION="$1"

wget https://github.com/ninja-build/ninja/releases/download/v${NINJA_VERSION}/ninja-linux.zip -O /tmp/ninja.zip

unzip /tmp/ninja.zip -d /usr/bin
chmod a+x /usr/bin/ninja

rm /tmp/ninja.zip
