#!/usr/bin/env bash

set -ex

NINJA_VERSION="$1"
NINJA_MAJOR_MINOR=$(echo "${NINJA_VERSION}" | cut -d. -f-2)
NINJA_MAJOR=$(echo "${NINJA_VERSION}" | cut -d. -f-1)
NINJA_MINOR=$(echo "${NINJA_MAJOR_MINOR}" | cut -d. -f2-)
NINJA_PATCH=$(echo "${NINJA_VERSION}" | cut -d. -f3-)

wget https://github.com/ninja-build/ninja/releases/download/v${NINJA_VERSION}/ninja-linux.zip -O /tmp/ninja.zip

unzip /tmp/ninja.zip -d /usr/bin
chmod a+x /usr/bin/ninja

rm /tmp/ninja.zip
