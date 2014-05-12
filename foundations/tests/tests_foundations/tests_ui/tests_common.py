#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_common.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.ui.common` module.

**Others:**

"""

from __future__ import unicode_literals

import os
import sys

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest
from PyQt4.QtGui import QWidget

import foundations.ui.common

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY", "UI_TESTS_FILE", "APPLICATION", "TestQWidget_factory"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources/ui")
UI_TESTS_FILE = os.path.join(RESOURCES_DIRECTORY, "Tests_Widget.ui")


class TestQWidget_factory(unittest.TestCase):
    """
    Defines :func:`foundations.ui.common.QWidget_factory` definition units tests methods.
    """

    def test_qwidget_factory(self):
        """
        Tests :func:`foundations.ui.common.QWidget_factory` definition.
        """

        widget = foundations.ui.common.QWidget_factory(UI_TESTS_FILE)
        self.assertTrue(hasattr(widget, "ui_file"))
        self.assertEqual(widget.__class__, QWidget.__class__)
        widget = foundations.ui.common.QWidget_factory()
        self.assertEqual(widget.__class__, QWidget.__class__)


if __name__ == "__main__":
    import foundations.tests.utilities

    unittest.main()
