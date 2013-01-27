#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**testsPkzip.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.pkzip` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import shutil
import tempfile
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from foundations.pkzip import Pkzip

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY", "TEST_FILE", "TREE_HIERARCHY", "PkzipTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.zip")
TREE_HIERARCHY = ("level_0", "loremIpsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
					"level_0/standard.ibl", "level_0/level_1",
					"level_0/level_1/loremIpsum.txt", "level_0/level_1/standard.rc", "level_0/level_1/level_2/",
					"level_0/level_1/level_2/standard.sIBLT")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PkzipTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.pkzip.Pkzip` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("archive",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(Pkzip))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("extract",)

		for method in requiredMethods:
			self.assertIn(method, dir(Pkzip))

	def testExtract(self):
		"""
		This method tests :meth:`foundations.pkzip.Pkzip.extract` method.
		"""

		zipFile = Pkzip(TEST_FILE)
		tempDirectory = tempfile.mkdtemp()
		extractionSuccess = zipFile.extract(tempDirectory)
		self.assertTrue(extractionSuccess)
		for item in TREE_HIERARCHY:
			self.assertTrue(os.path.exists(os.path.join(tempDirectory, item)))
		shutil.rmtree(tempDirectory)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
