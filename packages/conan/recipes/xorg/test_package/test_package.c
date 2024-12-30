/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/4622ac85d1cec8cb7a2fcc8a1796d4b73bff285e/recipes/xorg/all/test_package/test_package.c
*/

#include <X11/Xlib.h>
#include <X11/Xutil.h>

#include <X11/Xauth.h>

#include <X11/SM/SMlib.h>

#include <stdio.h>

int main() {
    Display *display = XOpenDisplay(NULL);

    if (!display) {
        printf("XOpenDisplay failed\n");
        return 0;
    }

    {
        char *xau_file_name = XauFileName();
        if (xau_file_name)
            printf("XauFileName: %s\n", xau_file_name);
    }

    XCloseDisplay(display);
    SmcSetErrorHandler(NULL);
}