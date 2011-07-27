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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**testsPkzip.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Pkzip tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import shutil
import tempfile
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from foundations.pkzip import Pkzip

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.zip")
TREE_HIERARCHY = ("level_0", "loremIpsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
					"level_0/standard.ibl", "level_0/level_1",
					"level_0/level_1/loremIpsum.txt", "level_0/level_1/standard.rc", "level_0/level_1/level_2/",
					"level_0/level_1/level_2/standard.sIBLT")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class PkzipTestCase(unittest.TestCase):
	"""
	This class is the PkzipTestCase class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		zipFile = Pkzip(TEST_FILE)
		requiredAttributes = ("archive",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(zipFile))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		zipFile = Pkzip(TEST_FILE)
		requiredMethods = ("extract",)

		for method in requiredMethods:
			self.assertIn(method, dir(zipFile))

	def testRead(self):
		"""
		This method tests the "Pkzip" class "extract" method.
		"""

		zipFile = Pkzip(TEST_FILE)
		tempDirectory = tempfile.mkdtemp()
		extractionSuccess = zipFile.extract(tempDirectory)
		self.assertTrue(extractionSuccess)
		for item in TREE_HIERARCHY:
			self.assertTrue(os.path.exists(os.path.join(tempDirectory, item)))
		shutil.rmtree(tempDirectory)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
