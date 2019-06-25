#!/usr/bin/env bash

set -ex

curl --location https://github.com/ninja-build/ninja/releases/download/v${NINJA_VERSION}/ninja-linux.zip -o /tmp/ninja.zip

unzip /tmp/ninja.zip -d /usr/bin
chmod a+x /usr/bin/ninja

rm /tmp/ninja.zip
