#!/usr/bin/env bash

set -ex

rm -rf /package

cd ${ASWF_INSTALL_PREFIX}
find . -type f -o -type l | cut -c3- > /tmp/previous-prefix-files.txt
