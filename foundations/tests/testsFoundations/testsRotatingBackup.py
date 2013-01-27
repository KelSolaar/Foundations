#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsRotatingBackup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.rotatingBackup` module.

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
from foundations.rotatingBackup import RotatingBackup

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY", "TEST_FILE", "TEST_DIRECTORY", "RotatingBackupTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ibl")
TEST_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "standard")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RotatingBackupTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.rotatingBackup.RotatingBackup` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("source",
							"destination",
							"count")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(RotatingBackup))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("backup",)

		for method in requiredMethods:
			self.assertIn(method, dir(RotatingBackup))

	def testBackup(self):
		"""
		This method tests :meth:`foundations.rotatingBackup.RotatingBackup.backup` method.
		"""

		tempDirectory = tempfile.mkdtemp()
		rotatingBackup = RotatingBackup(TEST_FILE, tempDirectory, 3)
		rotatingBackup.backup()
		self.assertTrue(os.path.exists(os.path.join(tempDirectory, os.path.basename(TEST_FILE))))
		for i in range(1, 4):
			rotatingBackup.backup()
			self.assertTrue(os.path.exists(os.path.join(tempDirectory, os.path.basename("{0}.{1}".format(TEST_FILE, i)))))
		rotatingBackup.backup()
		self.assertFalse(os.path.exists(os.path.join(tempDirectory, os.path.basename("{0}.4".format(TEST_FILE)))))
		shutil.rmtree(tempDirectory)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
