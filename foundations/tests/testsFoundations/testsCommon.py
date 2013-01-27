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
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
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
		"GetFirstItemTestCase",
		"GetLastItemTestCase",
		"IsBinaryFileTestCase",
		"RepeatTestCase",
		"DependencyResolverTestCase",
		"GetHostAddressTestCase"]

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

class UnpackDefaultTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.unpackDefault` definition units tests methods.
	"""

	def testUnpackDefault(self):
		"""
		This method tests :func:`foundations.common.unpackDefault` definition.
		"""

		self.assertListEqual(list(foundations.common.unpackDefault((1,))), [1, None, None])
		self.assertListEqual(list(foundations.common.unpackDefault((1, 2, 3, 4), length=3)), [1, 2, 3])
		self.assertListEqual(list(foundations.common.unpackDefault((1, 2, 3, 4), length=5, default="Default")),
							[1, 2, 3, 4, "Default"])

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

class GetFirstItemTestCase(unittest.TestCase):
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
		self.assertEqual(foundations.common.getFirstItem(("Nemo", "John", "Doe")), "Nemo")

class GetLastItemTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.getLastItem` definition units tests methods.
	"""

	def testGetLastItem(self):
		"""
		This method tests :func:`foundations.common.getLastItem` definition.
		"""

		self.assertEqual(foundations.common.getLastItem(None), None)
		self.assertEqual(foundations.common.getLastItem([]), None)
		self.assertEqual(foundations.common.getLastItem([None]), None)
		self.assertEqual(foundations.common.getLastItem([0]), 0)
		self.assertEqual(foundations.common.getLastItem(("Nemo",)), "Nemo")
		self.assertEqual(foundations.common.getLastItem(("Nemo", "John", "Doe")), "Doe")

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

class DependencyResolverTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.dependencyResolver` definition units tests methods.
	"""

	def testDependencyResolver(self):
		"""
		This method tests :func:`foundations.common.dependencyResolver` definition.
		"""

		dependencies = {"c" : ("a", "b"),
						"d" : ("c",),
						"f" : ("b",)}

		self.assertEquals(foundations.common.dependencyResolver(dependencies),
						[set(["a", "b"]), set(["c", "f"]), set(["d"])])

class GetHostAddressTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.getHostAddress` definition units tests methods.
	"""

	def testGetHostAddress(self):
		"""
		This method tests :func:`foundations.common.getHostAddress` definition.
		"""

		self.assertIsInstance(foundations.common.getHostAddress(), str)
		self.assertEqual(foundations.common.getHostAddress("Nemo, John Doe!"), foundations.common.DEFAULT_HOST_IP)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
