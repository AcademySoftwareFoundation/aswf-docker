# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for user settings
"""

import unittest
import tempfile
import os
import logging

from aswfdocker import constants, index


class TestIndex(unittest.TestCase):
    def test_iter_images(self):
        i = index.Index()
        packages = list(i.iter_images(constants.ImageType.PACKAGE))
        self.assertGreater(len(packages), 15)
        self.assertEqual(packages[0], "clang")

    def test_get_versions(self):
        i = index.Index()
        images = list(i.iter_images(constants.ImageType.IMAGE))
        self.assertGreater(len(images), 1)
        self.assertEqual(images[0], "common")
        versions = list(i.iter_versions(constants.ImageType.IMAGE, images[0]))
        self.assertGreaterEqual(len(versions), 1)
        self.assertTrue(versions[0].startswith("1."))
