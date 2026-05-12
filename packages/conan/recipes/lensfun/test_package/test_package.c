/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
*/

#include <lensfun/lensfun.h>

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    lfDatabase *db = lf_db_new();
    if (!db) {
        fprintf(stderr, "Failed to allocate lensfun database\n");
        return EXIT_FAILURE;
    }

    printf("Lensfun version macro: %d\n", LF_VERSION);
    lf_db_destroy(db);
    return EXIT_SUCCESS;
}
