#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir -p /package

find "${ASWF_INSTALL_PREFIX}" -type l -o -type f -exec realpath {} | cut -c3- > /tmp/new-prefix-files.txt
rsync -av --files-from=/tmp/new-prefix-files.txt --exclude-from=/tmp/previous-prefix-files.txt "${ASWF_INSTALL_PREFIX}" /package/
