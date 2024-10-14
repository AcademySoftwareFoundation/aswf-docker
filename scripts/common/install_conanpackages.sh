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
    # Extract references from conanfile.txt and install them by reference
    for CONANREF in $(awk 'NR == 1, /\[requires\]/ { next } /^[^#]/ { print }' conanfile.txt)
    do
        CONANPACKAGE=$(echo $CONANREF | cut -d\/ -f1)
        conan install --requires=$CONANREF --profile:all=${CONAN_USER_HOME}/.conan2/profiles/${ASWF_CONAN_CHANNEL} --deployer-folder $1 --deployer=direct_deploy
        # No way to tell Conan 2 to flatten the deployment destination, we move the files after the fact
        rsync --remove-source-files -a $1/direct_deploy/${CONANPACKAGE}/ $1/
    done
    rm -rf $1/direct_deploy
fi
