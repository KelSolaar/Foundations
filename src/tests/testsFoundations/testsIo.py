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
**testsIo.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Io Tests Module.

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
import foundations.io
from foundations.io import File

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "loremIpsum.txt")
FILE_CONTENT = ["Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n",
			"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n",
			"Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n",
			"Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"]

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class FileTestCase(unittest.TestCase):
	"""
	This Class Is The FileTestCase Class.
	"""

	def testRequiredAttributes(self):
		"""
		This Method Tests Presence Of Required Attributes.
		"""

		ioFile = File(TEST_FILE)
		requiredAttributes = ("file",
								"content")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(ioFile))

	def testRequiredMethods(self):
		"""
		This Method Tests Presence Of Required Methods.
		"""

		ioFile = File(TEST_FILE)
		requiredMethods = ("read",
							"write",
							"append")

		for method in requiredMethods:
			self.assertIn(method, dir(ioFile))

	def testRead(self):
		"""
		This Method Tests The "File" Class "read" Method.
		"""

		ioFile = File(TEST_FILE)
		self.assertIsInstance(ioFile.content, list)
		readSuccess = ioFile.read()
		self.assertTrue(readSuccess)
		self.assertIsInstance(ioFile.content, list)
		self.assertListEqual(ioFile.content, FILE_CONTENT)

	def testWrite(self):
		"""
		This Method Tests The "File" Class "write" Method.
		"""

		ioFile = File(tempfile.mkstemp()[1])
		self.assertIsInstance(ioFile.content, list)
		ioFile.content = FILE_CONTENT
		writeSuccess = ioFile.write()
		self.assertTrue(writeSuccess)
		ioFile.read()
		self.assertListEqual(ioFile.content, FILE_CONTENT)
		os.remove(ioFile.file)

	def testAppend(self):
		"""
		This Method Tests The "File" Class "append" Method.
		"""

		ioFile = File(tempfile.mkstemp()[1])
		self.assertIsInstance(ioFile.content, list)
		ioFile.content = FILE_CONTENT
		ioFile.write()
		append = ioFile.append()
		self.assertTrue(append)
		ioFile.read()
		self.assertListEqual(ioFile.content, FILE_CONTENT + FILE_CONTENT)
		os.remove(ioFile.file)

class SetLocalDirectoryTestCase(unittest.TestCase):
	"""
	This Class Is The SetLocalDirectoryTestCase Class.
	"""

	def testSetLocalDirectory(self):
		"""
		This Method Tests The "setLocalDirectory" Definition.
		"""

		tempDirectory = tempfile.mkdtemp()
		directoriesTree = "tests/io/setLocalDirectory"
		directory = os.path.join(tempDirectory, directoriesTree)
		foundations.io.setLocalDirectory(directory)
		self.assertTrue(os.path.exists(directory))
		shutil.rmtree(tempDirectory)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
