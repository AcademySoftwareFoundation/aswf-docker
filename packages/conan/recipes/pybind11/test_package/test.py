# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/59cab50aa90f922e61a746eef7c488dd788e4989/recipes/pybind11/all/test_package/test.py

import test_package

print("Adding 2 + 3 = {}".format(test_package.add(2, 3)))

print("Message: '{}'".format(test_package.msg()))
