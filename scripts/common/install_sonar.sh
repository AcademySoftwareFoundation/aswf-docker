#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir sonar
cd sonar

if [ ! -f "$DOWNLOADS_DIR/sonar-bw.zip" ]; then
    curl --location "https://sonarcloud.io/static/cpp/build-wrapper-linux-x86.zip" -o "$DOWNLOADS_DIR/sonar-bw.zip"
fi
unzip "$DOWNLOADS_DIR/sonar-bw.zip"
mv build-wrapper-linux-x86 /var/opt/.
ln -s /var/opt/build-wrapper-linux-x86/build-wrapper-linux-x86-64 /usr/bin/build-wrapper-linux-x86-64
# Returns with non-zero exit code, catch error with $()
echo $(build-wrapper-linux-x86-64)

if [ ! -f "$DOWNLOADS_DIR/sonar-scanner.zip" ]; then
    curl --location "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${ASWF_SONAR_VERSION}-linux.zip" -o "$DOWNLOADS_DIR/sonar-scanner.zip"
fi
unzip "$DOWNLOADS_DIR/sonar-scanner.zip"
mv "sonar-scanner-${ASWF_SONAR_VERSION}-linux" /var/opt/.
ln -s "/var/opt/sonar-scanner-${ASWF_SONAR_VERSION}-linux/bin/sonar-scanner" /usr/bin/sonar-scanner
sonar-scanner --help

cd ..
rm -rf sonar
