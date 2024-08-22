#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

BASEOS_MAJORVERSION=$(sed -n  's/^.* release \([0-9]*\)\..*$/\1/p' /etc/redhat-release)

if [ "$BASEOS_MAJORVERSION" -gt "7" ]; then
    python -m ensurepip --upgrade

    # There is a package called python3-html5lib through yum/dnf but it install it
    # for the system Python - which is not the same one that it used by downstream projects.
    python -m pip install html5lib
fi