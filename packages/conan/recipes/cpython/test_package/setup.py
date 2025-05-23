# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/cpython/all/test_package/setup.py

import os

# Hack to work around Python 3.8+ secure dll loading:
# see https://docs.python.org/3/whatsnew/3.8.html#bpo-36085-whatsnew
if hasattr(os, "add_dll_directory"):
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        if os.path.isdir(directory):
            os.add_dll_directory(directory)

from setuptools import setup, Extension

script_dir = os.path.dirname(os.path.realpath(__file__))

setup(
    name="test_package",
    version="1.0",
    ext_modules=[
        Extension("spam", [os.path.join(script_dir, "test_module.c")]),
    ],
)
