#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir -p /package

cd "${ASWF_INSTALL_PREFIX}"
rsync -arv --exclude-from=/tmp/previous-prefix-files.txt --prune-empty-dirs "${ASWF_INSTALL_PREFIX}"/ /package/
