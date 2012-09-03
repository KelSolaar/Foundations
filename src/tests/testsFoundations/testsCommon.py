#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsCommon.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.common` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform
import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common

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
		"LIBRARY",
		"TEXT_FILE",
		"UniqifyTestCase",
		"OrderedUniqifyTestCase",
		"PathExistsTestCase",
		"getFirstItemTestCase",
		"IsBinaryFileTestCase",
		"RepeatTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
LIBRARIES_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "libraries")
if platform.system() == "Windows" or platform.system() == "Microsoft":
	LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/FreeImage.dll")
elif platform.system() == "Darwin":
	LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/libfreeimage.dylib")
elif platform.system() == "Linux":
	LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/libfreeimage.so")
TEXT_FILE = os.path.join(RESOURCES_DIRECTORY, "loremIpsum.txt")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class UniqifyTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.uniqify` definition units tests methods.
	"""

	def testUniqify(self):
		"""
		This method tests :func:`foundations.common.uniqify` definition.
		"""

		sequence = ("A", "B", "B", "C")
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), ["A", "B", "C"])
		sequence = ((1, "A"), (2, "B"), (2, "B"), (3, "C"))
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), [(1, "A"), (2, "B"), (3, "C")])
		sequence = ({1 : "A"}, {1 : "A"}, {2 : "B"}, {3 : "C"})
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), [{1 : "A"}, {2 : "B"}, {3 : "C"}])


class OrderedUniqifyTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.orderedUniqify` definition units tests methods.
	"""

	def testOrderedUniqify(self):
		"""
		This method tests :func:`foundations.common.orderedUniqify` definition.
		"""

		sequence = ("A", "B", "B", "C")
		self.assertListEqual(foundations.common.orderedUniqify(sequence), ["A", "B", "C"])
		sequence = ((1, "A"), (2, "B"), (2, "B"), (3, "C"))
		self.assertListEqual(foundations.common.orderedUniqify(sequence), [(1, "A"), (2, "B"), (3, "C")])

class PathExistsTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.pathExists` definition units tests methods.
	"""

	def testPathExists(self):
		"""
		This method tests :func:`foundations.common.pathExists` definition.
		"""

		self.assertEqual(foundations.common.pathExists(None), False)
		self.assertTrue(foundations.common.pathExists(__file__))
		self.assertFalse(foundations.common.pathExists(unicode()))

class getFirstItemTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.getFirstItem` definition units tests methods.
	"""

	def testGetFirstItem(self):
		"""
		This method tests :func:`foundations.common.getFirstItem` definition.
		"""

		self.assertEqual(foundations.common.getFirstItem(None), None)
		self.assertEqual(foundations.common.getFirstItem([]), None)
		self.assertEqual(foundations.common.getFirstItem([None]), None)
		self.assertEqual(foundations.common.getFirstItem([0]), 0)
		self.assertEqual(foundations.common.getFirstItem(("Nemo",)), "Nemo")

class IsBinaryFileTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.isBinaryFile` definition units tests methods.
	"""

	def testPathExists(self):
		"""
		This method tests :func:`foundations.common.isBinaryFile` definition.
		"""

		self.assertTrue(foundations.common.isBinaryFile(LIBRARY))
		self.assertFalse(foundations.common.isBinaryFile(TEXT_FILE))

class RepeatTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.isBinaryFile` definition units tests methods.
	"""

	def testRepeat(self):
		"""
		This method tests :func:`foundations.common.repeat` definition.
		"""

		def foo(bar):
			return bar

		self.assertEqual(len(foundations.common.repeat(lambda: foo(True), 10)), 10)
		self.assertEqual(foundations.common.repeat(lambda: foo(True), 2), [True, True])

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
