#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

pypath=$(which python)
if [[ $pypath != /usr/local/bin/python ]]
then
    echo "Wrong python location: $pypath"
    exit 1
fi

pyversion=$(python --version)
if [[ $pyversion != Python\ 3.7* ]]
then
    echo "Wrong python version: $pyversion"
    exit 1
fi

numpyversion=$(python -c "import numpy; print(numpy.__version__)")
if [[ $numpyversion != 1.16* ]]
then
    echo "Wrong numpy version: $numpyversion"
    exit 1
fi
