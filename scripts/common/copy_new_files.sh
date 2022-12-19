#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir -p /package

cd "${ASWF_INSTALL_PREFIX}"
find . -type l -o -type f | cut -c3- > /tmp/new-prefix-files.txt
RSYNC_OLD_ARGS=1 rsync -av --trust-sender --files-from=/tmp/new-prefix-files.txt --exclude-from=/tmp/previous-prefix-files.txt . /package/
