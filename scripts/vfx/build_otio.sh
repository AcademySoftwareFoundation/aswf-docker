#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

git clone https://github.com/PixarAnimationStudios/OpenTimelineIO.git
cd OpenTimelineIO

if [ "$ASWF_OTIO_VERSION" != "latest" ]; then
    git checkout "tags/v${ASWF_OTIO_VERSION}" -b "v${ASWF_OTIO_VERSION}"
fi

pip install --prefix="${ASWF_INSTALL_PREFIX}" .

cd ..
rm -rf OpenTimelineIO
