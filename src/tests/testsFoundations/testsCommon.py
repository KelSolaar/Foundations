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

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.common

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["GetSystemApplicationDataDirectoryTestCase", "GetUserApplicationDataDirectoryTestCase"]

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class GetSystemApplicationDataDirectoryTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.getSystemApplicationDataDirectory` definition units tests methods.
	"""

	def testGetSystemApplicationDataDirectory(self):
		"""
		This method tests :func:`foundations.common.getSystemApplicationDataDirectory` definition.
		"""

		path = foundations.common.getSystemApplicationDataDirectory()
		self.assertIsInstance(path, str)
		self.assertTrue(os.path.exists(path))

class GetUserApplicationDataDirectoryTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.getUserApplicationDataDirectory` definition units tests methods.
	"""

	def testGetUserApplicationDataDirectory(self):
		"""
		This method tests :func:`foundations.common.getUserApplicationDataDirectory` definition.
		"""

		path = foundations.common.getUserApplicationDataDirectory()
		self.assertIsInstance(path, str)

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

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
