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
    def setUp(self):
        self.index = index.Index()

    def test_iter_images(self):
        packages = list(self.index.iter_images(constants.ImageType.PACKAGE))
        self.assertGreater(len(packages), 15)
        self.assertEqual(packages[0], "clang")

    def test_get_versions(self):
        ciimages = list(self.index.iter_images(constants.ImageType.CI_IMAGE))
        self.assertGreater(len(ciimages), 1)
        self.assertEqual(ciimages[0], "common")
        rtimages = list(self.index.iter_images(constants.ImageType.RT_IMAGE))
        self.assertGreater(len(rtimages), 1)
        self.assertEqual(rtimages[0], "base")
        versions = list(
            self.index.iter_versions(constants.ImageType.CI_IMAGE, ciimages[0])
        )
        self.assertGreaterEqual(len(versions), 1)
        self.assertTrue(versions[0].startswith("1-clang"))

    def test_version_info(self):
        vi = self.index.version_info("2019")
        self.assertTrue(vi)
        self.assertEqual(vi.version, "2019")

    def test_group_from_image(self):
        self.assertEqual(
            self.index.get_group_from_image(constants.ImageType.PACKAGE, "clang"),
            "common",
        )
