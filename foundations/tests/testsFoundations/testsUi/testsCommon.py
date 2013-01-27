#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsCommon.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.ui.common` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest
from PyQt4.QtGui import QWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.ui.common

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY", "UI_TESTS_FILE", "APPLICATION", "QWidgetFactoryTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "../resources/ui")
UI_TESTS_FILE = os.path.join(RESOURCES_DIRECTORY, "Tests_Widget.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class QWidgetFactoryTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.ui.common.QWidgetFactory` definition units tests methods.
	"""

	def testQWidgetFactory(self):
		"""
		This method tests :func:`foundations.ui.common.QWidgetFactory` definition.
		"""

		widget = foundations.ui.common.QWidgetFactory(UI_TESTS_FILE)
		self.assertTrue(hasattr(widget, "uiFile"))
		self.assertEqual(widget.__class__, QWidget.__class__)
		widget = foundations.ui.common.QWidgetFactory()
		self.assertEqual(widget.__class__, QWidget.__class__)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
