#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

rm -rf /package

find "${ASWF_INSTALL_PREFIX}" -type f -o -type l -exec realpath {} | cut -c3- > /tmp/previous-prefix-files.txt
