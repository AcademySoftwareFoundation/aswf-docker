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

# Bypass git-only version detection. Only applies to versions whose
# ci/generate_version_number.py still matches this hunk's context.
case "${ASWF_OPENCUE_VERSION:-1.19.1}" in
    1.19.1|1.13.8)
        cat << 'EOF' | patch -p1
--- a/ci/generate_version_number.py
+++ b/ci/generate_version_number.py
@@ -41,6 +41,7 @@
 This step is already performed automatically within our CI pipelines.
 """

+import os
 import pathlib
 import re
 import subprocess
@@ -101,6 +102,8 @@
     Returns:
         The calculated version string.
     """
+    if "ASWF_OPENCUE_VERSION" in os.environ:
+        return os.environ["ASWF_OPENCUE_VERSION"]
     script_dir = pathlib.Path(__file__).parent.resolve()
     toplevel_dir = script_dir.parent
     version_in_path = toplevel_dir / "VERSION.in"
EOF
        ;;
    1.34.22|1.37.0)
        cat << 'EOF' | patch -p1
--- a/ci/generate_version_number.py
+++ b/ci/generate_version_number.py
@@ -110,6 +111,8 @@
     Returns:
         The calculated version string.
     """
+    if "ASWF_OPENCUE_VERSION" in os.environ:
+        return os.environ["ASWF_OPENCUE_VERSION"]
     script_dir = pathlib.Path(__file__).parent.resolve()
     toplevel_dir = script_dir.parent
     version_in_path = toplevel_dir / "VERSION.in"
EOF
        ;;
esac

# 1. Build Cuebot (Java / Gradle)
# Assuming OpenCue source code is bound or checked out in the workspace
# https://docs.opencue.io/docs/getting-started/deploying-cuebot/#option-4-build-from-source
if [ -d "cuebot" ]; then
    export CI=true
    export GRADLE_OPTS="-Dorg.gradle.daemon=false -Dorg.gradle.console=plain"
    ./cuebot/gradlew -p cuebot build -x :test

    # Create installation directories under ASWF_INSTALL_PREFIX and copy.
    mkdir -p "${ASWF_INSTALL_PREFIX}/lib/opencue"
    mkdir -p "${ASWF_INSTALL_PREFIX}/bin"
    cp cuebot/build/libs/cuebot*.jar "${ASWF_INSTALL_PREFIX}/lib/opencue/cuebot.jar"
    
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
    cargo build --manifest-path rust/Cargo.toml --release -p rqd
    sudo install -m 755 rust/target/release/openrqd /usr/local/bin/
fi

# 3. Build Python packages (pycue, cuesubmit, etc.) via pip/hatch
# --no-build-isolation below means pip expects each package's build backend
# to already be installed rather than fetching it itself.
pip3 install hatchling "grpcio>=1.62.0" "grpcio-tools>=1.62.0"

for pkg in pycue proto rqd cuesubmit cueadmin cuecmd cuenimby; do
    if [ -d "$pkg" ]; then
        pip3 install --no-build-isolation ./$pkg
    fi
done

popd
rm -rf opencue.tar.gz OpenCue-${ASWF_OPENCUE_VERSION:-1.19.1}
