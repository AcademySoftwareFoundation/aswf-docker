#!/usr/bin/env bash

set -ex

mkdir _sonar
cd _sonar

curl --location https://sonarcloud.io/static/cpp/build-wrapper-linux-x86.zip -o sbw.zip
unzip sbw.zip
mv build-wrapper-linux-x86 /var/opt/.
ln -s /var/opt/build-wrapper-linux-x86/build-wrapper-linux-x86-64 /usr/bin/build-wrapper-linux-x86-64
echo $(build-wrapper-linux-x86-64 --help)

curl --location https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}-linux.zip -o sscli.zip
unzip sscli.zip
mv sonar-scanner-${SONAR_VERSION}-linux /var/opt/.
ln -s /var/opt/sonar-scanner-${SONAR_VERSION}-linux/bin/sonar-scanner /usr/bin/sonar-scanner
echo $(sonar-scanner --help)

cd ..
rm -rf _sonar

