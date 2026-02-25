# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/75b9e9922496dc0acc2499df76f8f10601042b60/recipes/nanobind/all/test_package/test_package.py

import conan_test_package

assert conan_test_package.add(2, 3) == 5
print("Test passed: conan_test_package.add(2, 3) == 5")
