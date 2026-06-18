// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: Apache-2.0

#include <libcgroup.h>
#include <stdio.h>

int main(void) {
    int ret = cgroup_init();
    /* cgroup_init may return a non-zero errno-based error code when cgroups
       aren't mounted in the container. That is expected in CI. We just verify
       the library linked and the API is callable. */
    printf("cgroup_init() returned %d (0=mounted, non-zero=not mounted in container — OK)\n", ret);
    printf("libcgroup linked OK\n");
    return 0;
}
