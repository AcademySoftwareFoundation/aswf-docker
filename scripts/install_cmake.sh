#!/usr/bin/env bash

set -ex

CMAKE_VERSION="$1"
CMAKE_MAJOR_MINOR=$(echo "${CMAKE_VERSION}" | cut -d. -f-2)
CMAKE_MAJOR=$(echo "${CMAKE_VERSION}" | cut -d. -f-1)
CMAKE_MINOR=$(echo "${CMAKE_MAJOR_MINOR}" | cut -d. -f2-)
CMAKE_PATCH=$(echo "${CMAKE_VERSION}" | cut -d. -f3-)

curl --location "https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.sh" -o "cmake.sh" &&\
sh cmake.sh --skip-license
rm cmake.sh
