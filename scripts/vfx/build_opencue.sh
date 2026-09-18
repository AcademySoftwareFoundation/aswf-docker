#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java-17-openjdk}"
export PATH="$JAVA_HOME/bin:$PATH"

# Download and extract the OpenCue source archive for the specified version
if [[ ! -f "$DOWNLOADS_DIR/opencue-${ASWF_OPENCUE_VERSION:-1.19.1}.tar.gz" ]]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenCue/archive/refs/tags/v${ASWF_OPENCUE_VERSION:-1.19.1}.tar.gz" -o "$DOWNLOADS_DIR/opencue-${ASWF_OPENCUE_VERSION:-1.19.1}.tar.gz"
fi
tar -zxf "$DOWNLOADS_DIR/opencue-${ASWF_OPENCUE_VERSION:-1.19.1}.tar.gz"

pushd OpenCue-${ASWF_OPENCUE_VERSION:-1.19.1}

# 1. Build Cuebot (Java / Gradle)
# Assuming OpenCue source code is bound or checked out in the workspace
# https://docs.opencue.io/docs/getting-started/deploying-cuebot/#option-4-build-from-source
if [ -d "cuebot" ]; then
    ./cuebot/gradlew -p cuebot build -x 

    # Create installation directories under ASWF_INSTALL_PREFIX and copy.
    mkdir -p "${ASWF_INSTALL_PREFIX}/lib/opencue"
    mkdir -p "${ASWF_INSTALL_PREFIX}/bin"
    cp cuebot/build/libs/cuebot-*.jar "${ASWF_INSTALL_PREFIX}/lib/opencue/cuebot.jar"
    
    # Create a wrapper script to run Cuebot via Java
    cat << 'EOF' > "${ASWF_INSTALL_PREFIX}/bin/cuebot"
#!/usr/bin/env bash
exec java -jar /usr/local/lib/opencue/cuebot.jar "$@"
EOF
    chmod +x "${ASWF_INSTALL_PREFIX}/bin/cuebot"

fi

# 2. Build RQD & Rust components (Cargo)
# https://github.com/AcademySoftwareFoundation/OpenCue/tree/master/rust#build-instructions
if [ -d "rust" ]; then
    cargo build --manifest-path rust/Cargo.toml --release -p rqd --target-dir="${ASWF_INSTALL_PREFIX}/bin"
fi

# 3. Build Python packages (pycue, cuesubmit, etc.) via pip/hatch
for pkg in pycue proto rqd cuesubmit cueadmin cuecmd cuenimby; do
    if [ -d "$pkg" ]; then
        pip3 install --no-build-isolation -e ./$pkg
    fi
done

popd
rm -rf opencue.tar.gz OpenCue-${ASWF_OPENCUE_VERSION:-1.19.1}