#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Starting with VFX Platform 2023, Conan packages need to be installed by
# reference to call the deploy() method, which is used for post processing
# of hard coded installation paths.

# Call with:
#
# install_conanpackages.sh install_dir default_profile
#
# where:
#   install_dir: location where Conan packages will installed
#   default_profile: the Conan profile for the year, either ci_commonx or vfx20xx

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
        conan install --requires=$CONANREF --profile:all=${ASWF_CONAN_HOME}/.conan2/profiles_${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL} --deployer-folder $1 --deployer=direct_deploy
        # The direct_deploy generator just copies over generated CMake files which may contain absolute paths pointing inside the Conan cache
        # in the format:
        # /opt/conan_home/d/b/boost64b7fc4516f80/p/...
        # Replace those by our installation prefix.
        find $1/direct_deploy/${CONANPACKAGE} -name '*.cmake' -exec sed -i -E 's/\/opt\/conan_home\/d\/b\/[^/]+\/p/'$ESCAPED_PATH'/g' {} \;
        # Currently cannot build a relocatable CPython package, conan_home paths are hardcoded in sysconfig
        if [[ $CONANPACKAGE == cpython* ]]; then
            find $1/direct_deploy/${CONANPACKAGE} -name '_sysconfigdata__linux_x86_64-linux-gnu.py' -exec sed -i -E 's/\/opt\/conan_home\/d\/b\/[^/]+\/p/'$ESCAPED_PATH'/g' {} \;
        fi
        # No way to tell Conan 2 to flatten the deployment destination, we move the files after the fact
        rsync --remove-source-files -a $1/direct_deploy/${CONANPACKAGE}/ $1/
    done
    # One off patch for pybind11 : overwrite pybind11Common.cmake with un-modified version
    if test -f $1/lib64/cmake/pybind11/pybind11Common.cmake_NO_CONAN; then
        mv $1/lib64/cmake/pybind11/pybind11Common.{cmake_NO_CONAN,cmake}
    fi
    rm -rf $1/direct_deploy
fi
