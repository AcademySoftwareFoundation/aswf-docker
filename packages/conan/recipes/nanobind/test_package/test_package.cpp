/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/master/recipes/nanobind/all/test_package/test_package.cpp
*/

#include <nanobind/nanobind.h>

int add(int a, int b) { return a + b; }

NB_MODULE(conan_test_package, m) {
    m.def("add", &add);
}
