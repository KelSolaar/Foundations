#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**tests_pkzip.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.pkzip` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY", "TEST_FILE", "TREE_HIERARCHY", "PkzipTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.zip")
TREE_HIERARCHY = ("level_0", "lorem_ipsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
					"level_0/standard.ibl", "level_0/level_1",
					"level_0/level_1/lorem_ipsum.txt", "level_0/level_1/standard.rc", "level_0/level_1/level_2/",
					"level_0/level_1/level_2/standard.sIBLT")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PkzipTestCase(unittest.TestCase):
	"""
	Defines :class:`foundations.pkzip.Pkzip` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("archive",)

		for attribute in required_attributes:
			self.assertIn(attribute, dir(Pkzip))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("extract",)

		for method in required_methods:
			self.assertIn(method, dir(Pkzip))

	def test_extract(self):
		"""
		Tests :meth:`foundations.pkzip.Pkzip.extract` method.
		"""

		zip_file = Pkzip(TEST_FILE)
		temp_directory = tempfile.mkdtemp()
		extraction_success = zip_file.extract(temp_directory)
		self.assertTrue(extraction_success)
		for item in TREE_HIERARCHY:
			self.assertTrue(os.path.exists(os.path.join(temp_directory, item)))
		shutil.rmtree(temp_directory)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
