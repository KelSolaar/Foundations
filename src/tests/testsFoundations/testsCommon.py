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

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class GetSystemApplicationDatasDirectoryTestCase(unittest.TestCase):
	"""
	This class is the :func:`foundations.common.getSystemApplicationDatasDirectory` test case class.
	"""

	def testGetSystemApplicationDatasDirectory(self):
		"""
		This method tests :func:`foundations.common.getSystemApplicationDatasDirectory` definition.
		"""

		path = foundations.common.getSystemApplicationDatasDirectory()
		self.assertIsInstance(path, str)
		self.assertTrue(os.path.exists(path))

class GetUserApplicationDatasDirectoryTestCase(unittest.TestCase):
	"""
	This class is the :func:`foundations.common.getUserApplicationDatasDirectory` test case class.
	"""

	def testGetUserApplicationDatasDirectory(self):
		"""
		This method tests :func:`foundations.common.getUserApplicationDatasDirectory` definition.
		"""

		path = foundations.common.getUserApplicationDatasDirectory()
		self.assertIsInstance(path, str)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
