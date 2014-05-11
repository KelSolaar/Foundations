#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_common.py**

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

__all__ = ["TestUniqify",
		   "TestOrderedUniqify",
		   "TestUnpackDefault",
		   "TestPathExists",
		   "TestFilterPath",
		   "TestGetFirstItem",
		   "TestGetLastItem",
		   "TestRepeat",
		   "TestDependencyResolver",
		   "TestGetHostAddress"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TestUniqify(unittest.TestCase):
	"""
	Defines :func:`foundations.common.uniqify` definition units tests methods.
	"""

	def test_uniqify(self):
		"""
		Tests :func:`foundations.common.uniqify` definition.
		"""

		sequence = ("A", "B", "B", "C")
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), ["A", "B", "C"])
		sequence = ((1, "A"), (2, "B"), (2, "B"), (3, "C"))
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), [(1, "A"), (2, "B"), (3, "C")])
		sequence = ({1: "A"}, {1: "A"}, {2: "B"}, {3: "C"})
		self.assertListEqual(sorted(foundations.common.uniqify(sequence)), [{1: "A"}, {2: "B"}, {3: "C"}])

class TestOrderedUniqify(unittest.TestCase):
	"""
	Defines :func:`foundations.common.ordered_uniqify` definition units tests methods.
	"""

	def test_ordered_uniqify(self):
		"""
		Tests :func:`foundations.common.ordered_uniqify` definition.
		"""

		sequence = ("A", "B", "B", "C")
		self.assertListEqual(foundations.common.ordered_uniqify(sequence), ["A", "B", "C"])
		sequence = ((1, "A"), (2, "B"), (2, "B"), (3, "C"))
		self.assertListEqual(foundations.common.ordered_uniqify(sequence), [(1, "A"), (2, "B"), (3, "C")])

class TestUnpackDefault(unittest.TestCase):
	"""
	Defines :func:`foundations.common.unpack_default` definition units tests methods.
	"""

	def test_unpack_default(self):
		"""
		Tests :func:`foundations.common.unpack_default` definition.
		"""

		self.assertListEqual(list(foundations.common.unpack_default((1,))), [1, None, None])
		self.assertListEqual(list(foundations.common.unpack_default((1, 2, 3, 4), length=3)), [1, 2, 3])
		self.assertListEqual(list(foundations.common.unpack_default((1, 2, 3, 4), length=5, default="Default")),
							 [1, 2, 3, 4, "Default"])

class TestPathExists(unittest.TestCase):
	"""
	Defines :func:`foundations.common.path_exists` definition units tests methods.
	"""

	def test_path_exists(self):
		"""
		Tests :func:`foundations.common.path_exists` definition.
		"""

		self.assertEqual(foundations.common.path_exists(None), False)
		self.assertTrue(foundations.common.path_exists(__file__))
		self.assertFalse(foundations.common.path_exists(""))

class TestFilterPath(unittest.TestCase):
	"""
	Defines :func:`foundations.common.filter_path` definition units tests methods.
	"""

	def test_filter_path(self):
		"""
		Tests :func:`foundations.common.filter_path` definition.
		"""

		self.assertEqual(foundations.common.filter_path(None), "")
		self.assertEqual(foundations.common.filter_path(__file__), __file__)

class TestGetFirstItem(unittest.TestCase):
	"""
	Defines :func:`foundations.common.get_first_item` definition units tests methods.
	"""

	def test_get_first_item(self):
		"""
		Tests :func:`foundations.common.get_first_item` definition.
		"""

		self.assertEqual(foundations.common.get_first_item(None), None)
		self.assertEqual(foundations.common.get_first_item([]), None)
		self.assertEqual(foundations.common.get_first_item([None]), None)
		self.assertEqual(foundations.common.get_first_item([0]), 0)
		self.assertEqual(foundations.common.get_first_item(("Nemo",)), "Nemo")
		self.assertEqual(foundations.common.get_first_item(("Nemo", "John", "Doe")), "Nemo")

class TestGetLastItem(unittest.TestCase):
	"""
	Defines :func:`foundations.common.get_last_item` definition units tests methods.
	"""

	def test_get_last_item(self):
		"""
		Tests :func:`foundations.common.get_last_item` definition.
		"""

		self.assertEqual(foundations.common.get_last_item(None), None)
		self.assertEqual(foundations.common.get_last_item([]), None)
		self.assertEqual(foundations.common.get_last_item([None]), None)
		self.assertEqual(foundations.common.get_last_item([0]), 0)
		self.assertEqual(foundations.common.get_last_item(("Nemo",)), "Nemo")
		self.assertEqual(foundations.common.get_last_item(("Nemo", "John", "Doe")), "Doe")

class TestRepeat(unittest.TestCase):
	"""
	Defines :func:`foundations.common.repeat` definition units tests methods.
	"""

	def test_repeat(self):
		"""
		Tests :func:`foundations.common.repeat` definition.
		"""

		def foo(bar):
			return bar

		self.assertEqual(len(foundations.common.repeat(lambda: foo(True), 10)), 10)
		self.assertEqual(foundations.common.repeat(lambda: foo(True), 2), [True, True])

class TestDependencyResolver(unittest.TestCase):
	"""
	Defines :func:`foundations.common.dependency_resolver` definition units tests methods.
	"""

	def test_dependency_resolver(self):
		"""
		Tests :func:`foundations.common.dependency_resolver` definition.
		"""

		dependencies = {"c": ("a", "b"),
						"d": ("c",),
						"f": ("b",)}

		self.assertEquals(foundations.common.dependency_resolver(dependencies),
						  [set(["a", "b"]), set(["c", "f"]), set(["d"])])

class TestGetHostAddress(unittest.TestCase):
	"""
	Defines :func:`foundations.common.get_host_address` definition units tests methods.
	"""

	def test_get_host_address(self):
		"""
		Tests :func:`foundations.common.get_host_address` definition.
		"""

		self.assertIsInstance(foundations.common.get_host_address(), unicode)
		self.assertEqual(foundations.common.get_host_address(-1), foundations.common.DEFAULT_HOST_IP)

if __name__ == "__main__":
	import foundations.tests.utilities

	unittest.main()
