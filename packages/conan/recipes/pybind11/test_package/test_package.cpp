/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/59cab50aa90f922e61a746eef7c488dd788e4989/recipes/pybind11/all/test_package/test_package.cpp
*/

#include <pybind11/pybind11.h>

static int add(int i, int j) {
    return i + j;
}

static const char *hello() {
    return "Hello from the C++ world!";
}

PYBIND11_MODULE(test_package, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers");
    m.def("msg", &hello, "A function returning a message");
}
