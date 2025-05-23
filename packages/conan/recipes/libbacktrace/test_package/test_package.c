/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/7abb9ee39e6009e3dbc45043307a1098246d4ad7/recipes/libbacktrace/all/test_package/test_package.c
*/

#include <backtrace-supported.h>
#include <backtrace.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void
error_callback(void* data, const char* msg, int errnum)
{
    fprintf(stderr, "%s", msg);
    if (errnum > 0)
        fprintf(stderr, ": %s", strerror(errnum));
    fprintf(stderr, "\n");
    exit(0);
}

int
simple_callback(void* data, uintptr_t pc)
{
    printf("  0x%016llx\n", pc);
    return 1;
}

int
main(int argc, char** argv)
{
    void* state;

    state = backtrace_create_state(argv[0], BACKTRACE_SUPPORTS_THREADS, error_callback, NULL);
    printf("Top stack frame:\n");
    backtrace_simple(state, 0, simple_callback, error_callback, NULL);
    printf("Done\n");

    return 0;
}
