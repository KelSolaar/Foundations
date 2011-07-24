#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**testsRotatingBackup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	RotatingBackup Tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import os
import shutil
import tempfile
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from foundations.rotatingBackup import RotatingBackup

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ibl")
TEST_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "standard")

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class RotatingBackupTestCase(unittest.TestCase):
	"""
	This Class Is The RotatingBackupTestCase Class.
	"""

	def testRequiredAttributes(self):
		"""
		This Method Tests Presence Of Required Attributes.
		"""

		rotatingBackup = RotatingBackup()
		requiredAttributes = ("source",
							"destination",
							"count")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(rotatingBackup))

	def testRequiredMethods(self):
		"""
		This Method Tests Presence Of Required Methods.
		"""

		rotatingBackup = RotatingBackup()
		requiredMethods = ("backup", "copy", "delete")

		for method in requiredMethods:
			self.assertIn(method, dir(rotatingBackup))

	def testBackup(self):
		"""
		This Method Tests The "RotatingBackup" Class "backup" Method.
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

	def testCopy(self):
		"""
		This Method Tests The "RotatingBackup" Class "copy" Method.
		"""

		tempDirectory = tempfile.mkdtemp()
		rotatingBackup = RotatingBackup(TEST_FILE, tempDirectory, 3)
		for element in (TEST_FILE, TEST_DIRECTORY):
			destination = os.path.join(tempDirectory, os.path.basename(element))
			rotatingBackup.copy(element, destination)
			self.assertTrue(os.path.exists(destination))
		shutil.rmtree(tempDirectory)

	def testDelete(self):
		"""
		This Method Tests The "RotatingBackup" Class "delete" Method.
		"""

		tempDirectory = tempfile.mkdtemp()
		rotatingBackup = RotatingBackup(TEST_FILE, tempDirectory, 3)
		for element in (TEST_FILE, TEST_DIRECTORY):
			destination = os.path.join(tempDirectory, os.path.basename(element))
			rotatingBackup.copy(element, destination)
			rotatingBackup.delete(destination)
			self.assertTrue(not os.path.exists(destination))
		shutil.rmtree(tempDirectory)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
