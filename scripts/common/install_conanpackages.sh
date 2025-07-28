#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Call with:
#
# install_conanpackages.sh install_dir default_profile exclude_package
#
# where:
#   install_dir: location where Conan packages will installed
#   default_profile: the Conan profile for the year, either ci_commonx or vfx20xx
#   exclude_package: a package to exclude from the install, e.g. oiio if building the ci-oiio image
#                    (but where we want all the dependencies to build oiio)

set -ex

VFXYEAR=$(echo $ASWF_CONAN_CHANNEL | sed -rn 's/[^[:digit:]]*([[:digit:]]+)/\1/p')

if [[ $ASWF_CONAN_CHANNEL == ci_common* ]]; then
    # ci_common images are "year independent", we just care if version 3/2023 or newer
    VFXYEAR=$(( $VFXYEAR + 2020 ))
fi

cd $1
if (( $VFXYEAR < 2023 )); then
    # Install conan packages listed in conanfile.txt in current directory.
    # This won't work with Conan 2
    conan config set general.default_profile=$2
    conan install .
else
    # Escape / or & in install dir for use in regexp
    ESCAPED_PATH=$(printf '%s' "$1" | sed 's/[\/&]/\\&/g')
    # Extract references from conanfile.txt and install them by reference
    for CONANREF in $(awk 'NR == 1, /\[requires\]/ { next } /^[^#]/ { print }' conanfile.txt)
    do
        CONANPACKAGE=$(echo $CONANREF | cut -d\/ -f1)
        # Using the full_deployer gets us all the transitive dependencies, but will require some cleaning up:
        # - header_only libraries have a different installation layout
        # - we don't want to install empty system wrappers
        # - we don't want to install the openfoo package when building ci-openfoo, only its build dependencies
        conan install --requires=$CONANREF --profile:all=${ASWF_CONAN_HOME}/.conan2/profiles_${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} --deployer-folder $1 --deployer=full_deploy
    done

    # The full_deploy generator just copies over generated CMake files which may contain absolute paths pointing inside the Conan cache
    # in the format:
    # /opt/conan_home/d/b/boost64b7fc4516f80/p/...
    # Replace those by our installation prefix.
    find $1/full_deploy -name '*.cmake' -exec sed -i -E 's/\/opt\/conan_home\/d\/b\/[^/]+\/p/'$ESCAPED_PATH'/g' {} \;

    for INSTALLED_PACKAGE in $(find $1/full_deploy/host -mindepth 1 -maxdepth 1 -printf "%f\n"); do
        # Don't relocate the excluded package
        if [[ $INSTALLED_PACKAGE == $3 ]]; then
            continue
        fi

        # Better hope there's only one version of the package
        RELEASE_DIR=""
        INSTALLED_PACKAGE_VERSION=$(find $1/full_deploy/host/${INSTALLED_PACKAGE} -mindepth 1 -maxdepth 1 -printf "%f\n" -quit)
        if [ -d $1/full_deploy/host/${INSTALLED_PACKAGE}/${INSTALLED_PACKAGE_VERSION}/Release ]; then
            # Full packages have extra path component based on Debug/Release and architecture, header-only packages don't
            RELEASE_DIR="Release/x86_64"
        fi

        # Some system wrappers have a version number, but have no subdirectories
        subdir_count=$(find $1/full_deploy/host/${INSTALLED_PACKAGE}/${INSTALLED_PACKAGE_VERSION}/${RELEASE_DIR}/ -mindepth 1 -maxdepth 1 -type d | wc -l)
        if [[ ${INSTALLED_PACKAGE_VERSION} == "system" || $subdir_count -eq 0 ]]; then
            continue
        fi
    
        # Currently cannot build a relocatable CPython package, conan_home paths are hardcoded in sysconfig
        if [[ $INSTALLED_PACKAGE == cpython ]]; then
            find $1/full_deploy/host/cpython -name '_sysconfigdata__linux_x86_64-linux-gnu.py' -exec sed -i -E 's/\/opt\/conan_home\/d\/b\/[^/]+\/p/'$ESCAPED_PATH'/g' {} \;
        fi

        # One off patch for pybind11 : overwrite pybind11Common.cmake with un-modified version
        if [[ $INSTALLED_PACKAGE == pybind11 ]]; then
            mv $1/full_deploy/host/pybind11/${INSTALLED_PACKAGE_VERSION}/lib/cmake/pybind11/pybind11Common.{cmake_NO_CONAN,cmake}
        fi

        rsync --remove-source-files --exclude conaninfo.txt --exclude conanmanifest.txt -a $1/full_deploy/host/${INSTALLED_PACKAGE}/${INSTALLED_PACKAGE_VERSION}/${RELEASE_DIR}/ $1/
    done

    # rsync should have left nothing behind but empty directories (--remove-source-files doesn't remove them),
    # system wrappers and the excluded package
    rm -rf $1/full_deploy
fi
