#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_rotating_backup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.rotating_backup` module.

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
from foundations.rotating_backup import RotatingBackup

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY", "TEST_FILE", "TEST_DIRECTORY", "TestRotatingBackup"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ibl")
TEST_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "standard")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TestRotatingBackup(unittest.TestCase):
	"""
	Defines :class:`foundations.rotating_backup.RotatingBackup` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("source",
							"destination",
							"count")

		for attribute in required_attributes:
			self.assertIn(attribute, dir(RotatingBackup))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("backup",)

		for method in required_methods:
			self.assertIn(method, dir(RotatingBackup))

	def test_backup(self):
		"""
		Tests :meth:`foundations.rotating_backup.RotatingBackup.backup` method.
		"""

		temp_directory = tempfile.mkdtemp()
		rotating_backup = RotatingBackup(TEST_FILE, temp_directory, 3)
		rotating_backup.backup()
		self.assertTrue(os.path.exists(os.path.join(temp_directory, os.path.basename(TEST_FILE))))
		for i in range(1, 4):
			rotating_backup.backup()
			self.assertTrue(os.path.exists(os.path.join(temp_directory, os.path.basename("{0}.{1}".format(TEST_FILE, i)))))
		rotating_backup.backup()
		self.assertFalse(os.path.exists(os.path.join(temp_directory, os.path.basename("{0}.4".format(TEST_FILE)))))
		shutil.rmtree(temp_directory)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
