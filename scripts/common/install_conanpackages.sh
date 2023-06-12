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

conan config set general.default_profile=$2

cd $1
if (( $VFXYEAR < 2023 )); then
    # Install conan packages listed in conanfile.txt in current directory
    conan install .
else
    # Extract references from conanfile.txt and install them by reference
    for CONANREF in $(awk 'NR == 1, /\[requires\]/ { next } /^[^#]/ { print }' conanfile.txt)
    do
        conan install $CONANREF --install-folder $1
    done
fi
