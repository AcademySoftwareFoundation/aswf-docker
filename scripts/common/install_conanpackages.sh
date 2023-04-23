#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Starting with VFX Platform 2023, Conan packages need to be installed by
# reference to call the deploy() method, which is used for post processing
# of hard coded installation paths.

# Call with:
# install_conanpackages.sh install_dir

set -ex

VFXYEAR=$(echo $ASWF_CONAN_CHANNEL | sed -rn 's/[^[:digit:]]*([[:digit:]]+)/\1/p')

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
