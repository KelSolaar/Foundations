#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**testsIo.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.io` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import shutil
import tempfile
import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.io
from foundations.io import File

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
			"TEST_FILE",
			"FILE_CONTENT",
			"FileTestCase",
			"SetDirectoryTestCase",
			"CopyTestCase",
			"RemoveTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
TEST_FILE = os.path.join(RESOURCES_DIRECTORY, "loremIpsum.txt")
FILE_CONTENT = ["Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n",
			"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n",
			"Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n",
			"Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class FileTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.io.File` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("file",
								"content")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(File))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("read",
							"write",
							"append")

		for method in requiredMethods:
			self.assertIn(method, dir(File))

	def testRead(self):
		"""
		This method tests :meth:`foundations.io.File.read` method.
		"""

		ioFile = File(TEST_FILE)
		self.assertIsInstance(ioFile.content, list)
		readSuccess = ioFile.read()
		self.assertTrue(readSuccess)
		self.assertIsInstance(ioFile.content, list)
		self.assertListEqual(ioFile.content, FILE_CONTENT)

	def testWrite(self):
		"""
		This method tests :meth:`foundations.io.File.write` method.
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
		This method tests :meth:`foundations.io.File.append` method.
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

class SetDirectoryTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.io.setDirectory` definition units tests methods.
	"""

	def testSetDirectory(self):
		"""
		This method tests :func:`foundations.io.setDirectory` definition.
		"""

		tempDirectory = tempfile.mkdtemp()
		directoriesTree = "tests/io/setDirectory"
		directory = os.path.join(tempDirectory, directoriesTree)
		foundations.io.setDirectory(directory)
		self.assertTrue(os.path.exists(directory))
		shutil.rmtree(tempDirectory)

class CopyTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.io.copy` definition units tests methods.
	"""

	def testCopy(self):
		"""
		This method tests :func:`foundations.io.copy` definition.
		"""

		tempDirectory = tempfile.mkdtemp()
		destination = os.path.join(tempDirectory, os.path.basename(TEST_FILE))
		foundations.io.copy(TEST_FILE, destination)
		self.assertTrue(os.path.exists(destination))
		shutil.rmtree(tempDirectory)

class RemoveTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.io.remove` definition units tests methods.
	"""

	def testRemove(self):
		"""
		This method tests :func:`foundations.io.remove` definition.
		"""

		tempDirectory = tempfile.mkdtemp()
		destination = os.path.join(tempDirectory, os.path.basename(TEST_FILE))
		foundations.io.copy(TEST_FILE, destination)
		foundations.io.remove(destination)
		self.assertTrue(not os.path.exists(destination))
		shutil.rmtree(tempDirectory)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
