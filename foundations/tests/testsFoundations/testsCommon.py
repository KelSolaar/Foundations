#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsCommon.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.common` module.

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UniqifyTestCase",
		   "OrderedUniqifyTestCase",
		   "UnpackDefaultTestCase",
		   "PathExistsTestCase",
		   "FilterPathTestCase",
		   "GetFirstItemTestCase",
		   "GetLastItemTestCase",
		   "RepeatTestCase",
		   "DependencyResolverTestCase",
		   "GetHostAddressTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class UniqifyTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.uniqify` definition units tests methods.
	"""

	def testUniqify(self):
		"""
		Tests :func:`foundations.common.uniqify` definition.
		"""

		sequence = ("A", "B", "B", "C")
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), ["A", "B", "C"])
		sequence = ((1, "A"), (2, "B"), (2, "B"), (3, "C"))
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), [(1, "A"), (2, "B"), (3, "C")])
		sequence = ({1: "A"}, {1: "A"}, {2: "B"}, {3: "C"})
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), [{1: "A"}, {2: "B"}, {3: "C"}])

class OrderedUniqifyTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.orderedUniqify` definition units tests methods.
	"""

	def testOrderedUniqify(self):
		"""
		Tests :func:`foundations.common.orderedUniqify` definition.
		"""

		sequence = ("A", "B", "B", "C")
		self.assertListEqual(foundations.common.orderedUniqify(sequence), ["A", "B", "C"])
		sequence = ((1, "A"), (2, "B"), (2, "B"), (3, "C"))
		self.assertListEqual(foundations.common.orderedUniqify(sequence), [(1, "A"), (2, "B"), (3, "C")])

class UnpackDefaultTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.unpackDefault` definition units tests methods.
	"""

	def testUnpackDefault(self):
		"""
		Tests :func:`foundations.common.unpackDefault` definition.
		"""

		self.assertListEqual(list(foundations.common.unpackDefault((1,))), [1, None, None])
		self.assertListEqual(list(foundations.common.unpackDefault((1, 2, 3, 4), length=3)), [1, 2, 3])
		self.assertListEqual(list(foundations.common.unpackDefault((1, 2, 3, 4), length=5, default="Default")),
							 [1, 2, 3, 4, "Default"])

class PathExistsTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.pathExists` definition units tests methods.
	"""

	def testPathExists(self):
		"""
		Tests :func:`foundations.common.pathExists` definition.
		"""

		self.assertEqual(foundations.common.pathExists(None), False)
		self.assertTrue(foundations.common.pathExists(__file__))
		self.assertFalse(foundations.common.pathExists(""))

class FilterPathTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.filterPath` definition units tests methods.
	"""

	def testFilterPath(self):
		"""
		Tests :func:`foundations.common.filterPath` definition.
		"""

		self.assertEqual(foundations.common.filterPath(None), "")
		self.assertEqual(foundations.common.filterPath(__file__), __file__)

class GetFirstItemTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.getFirstItem` definition units tests methods.
	"""

	def testGetFirstItem(self):
		"""
		Tests :func:`foundations.common.getFirstItem` definition.
		"""

		self.assertEqual(foundations.common.getFirstItem(None), None)
		self.assertEqual(foundations.common.getFirstItem([]), None)
		self.assertEqual(foundations.common.getFirstItem([None]), None)
		self.assertEqual(foundations.common.getFirstItem([0]), 0)
		self.assertEqual(foundations.common.getFirstItem(("Nemo",)), "Nemo")
		self.assertEqual(foundations.common.getFirstItem(("Nemo", "John", "Doe")), "Nemo")

class GetLastItemTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.getLastItem` definition units tests methods.
	"""

	def testGetLastItem(self):
		"""
		Tests :func:`foundations.common.getLastItem` definition.
		"""

		self.assertEqual(foundations.common.getLastItem(None), None)
		self.assertEqual(foundations.common.getLastItem([]), None)
		self.assertEqual(foundations.common.getLastItem([None]), None)
		self.assertEqual(foundations.common.getLastItem([0]), 0)
		self.assertEqual(foundations.common.getLastItem(("Nemo",)), "Nemo")
		self.assertEqual(foundations.common.getLastItem(("Nemo", "John", "Doe")), "Doe")

class RepeatTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.repeat` definition units tests methods.
	"""

	def testRepeat(self):
		"""
		Tests :func:`foundations.common.repeat` definition.
		"""

		def foo(bar):
			return bar

		self.assertEqual(len(foundations.common.repeat(lambda: foo(True), 10)), 10)
		self.assertEqual(foundations.common.repeat(lambda: foo(True), 2), [True, True])

class DependencyResolverTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.dependencyResolver` definition units tests methods.
	"""

	def testDependencyResolver(self):
		"""
		Tests :func:`foundations.common.dependencyResolver` definition.
		"""

		dependencies = {"c": ("a", "b"),
						"d": ("c",),
						"f": ("b",)}

		self.assertEquals(foundations.common.dependencyResolver(dependencies),
						  [set(["a", "b"]), set(["c", "f"]), set(["d"])])

class GetHostAddressTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.common.getHostAddress` definition units tests methods.
	"""

	def testGetHostAddress(self):
		"""
		Tests :func:`foundations.common.getHostAddress` definition.
		"""

		self.assertIsInstance(foundations.common.getHostAddress(), unicode)
		self.assertEqual(foundations.common.getHostAddress(-1), foundations.common.DEFAULT_HOST_IP)

if __name__ == "__main__":
	import foundations.tests.utilities

	unittest.main()
