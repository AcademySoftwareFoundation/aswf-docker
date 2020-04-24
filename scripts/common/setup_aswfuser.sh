#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

# Grant user 'aswfuser' SUDO privilege and allow it run any command without authentication.
# 1001 is used by Azure Pipelines user so we use 1002
useradd -m -u 1002 aswfuser
groupadd aswfgroup
usermod -a -G aswfgroup aswfuser
su -c "echo '%aswfgroup ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers"
