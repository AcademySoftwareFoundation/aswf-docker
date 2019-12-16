#!/usr/bin/env bash

set -ex

mkdir -p /package

cd ${ASWF_INSTALL_PREFIX}
find . -type l -o -type f | cut -c3- > /tmp/new-prefix-files.txt
rsync -av --files-from=/tmp/new-prefix-files.txt --exclude-from=/tmp/previous-prefix-files.txt . /package/
