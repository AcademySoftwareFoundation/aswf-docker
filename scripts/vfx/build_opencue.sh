#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java-17-openjdk}"
export PATH="$JAVA_HOME/bin:$PATH"

# Download and extract the OpenCue source archive for the specified version
curl -L -s https://github.com/AcademySoftwareFoundation/OpenCue/archive/refs/tags/v${ASWF_OPENCUE_VERSION:-1.19.1}.tar.gz -o opencue.tar.gz
tar -xzf opencue.tar.gz
pushd OpenCue-${ASWF_OPENCUE_VERSION:-1.19.1}

# 1. Build Cuebot (Java / Gradle)
# Assuming OpenCue source code is bound or checked out in the workspace
# https://docs.opencue.io/docs/getting-started/deploying-cuebot/#option-4-build-from-source
if [ -d "cuebot" ]; then
    pushd cuebot
    ./gradlew build -x test
    popd
fi

# 2. Build RQD & Rust components (Cargo)
# https://github.com/AcademySoftwareFoundation/OpenCue/tree/master/rust#build-instructions
if [ -d "rust" ]; then
    pushd rust
    cargo build --release -p rqd
    popd
fi

# 3. Build Python packages (pycue, cuesubmit, etc.) via pip/hatch
for pkg in pycue proto rqd cuesubmit cueadmin cuecmd cuenimby; do
    if [ -d "$pkg" ]; then
        pip install --no-build-isolation -e ./$pkg
    fi
done

popd
rm -rf opencue.tar.gz OpenCue-${ASWF_OPENCUE_VERSION:-1.19.1}