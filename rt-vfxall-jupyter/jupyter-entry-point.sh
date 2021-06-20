# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

export VGL_DISPLAY=:1

vglrun -- /opt/VirtualGL/bin/glxinfo -v
vglrun -- jupyter-lab
