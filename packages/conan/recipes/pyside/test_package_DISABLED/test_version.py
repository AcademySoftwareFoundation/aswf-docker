import common

import sys

expected_version = sys.argv[1]

import PySide6

assert (
    PySide6.__version__ == expected_version
), "expected version {} got version {}".format(expected_version, PySide6.__version__)

import shiboken6

assert (
    shiboken6.__version__ == expected_version
), "expected version {} got version {}".format(expected_version, shiboken6.__version__)
