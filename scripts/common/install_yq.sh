#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# Install the yq command line tool for processing yaml files.
# Since it is written in Golang, and no RPM is currently in EPEL,
# we just install a binary.

set -ex

curl --output /usr/local/bin/yq -L https://github.com/mikefarah/yq/releases/download/v${ASWF_YQ_VERSION}/yq_linux_amd64
chmod +x /usr/local/bin/yq
