#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

nvidia_major=`nvidia-smi --query-gpu=driver_version --format=csv,noheader|cut -d. -f1`

# Install nvidia driver DKMS matching current host's driver version for Xorg
sudo yum install -y nvidia-driver-branch-$nvidia_major || echo "OK"

sudo Xorg -config /etc/xpra/xorg.conf :1 vt8 &
export VGL_DISPLAY=:1
export LIBGL_DEBUG=verbose
export VGL_VERBOSE=1

xpra \
    start \
    :100 \
    --daemon=no \
    --terminate-children \
    --exit-with-children=yes \
    --start-child=${ASWF_XPRA_COMMAND}
