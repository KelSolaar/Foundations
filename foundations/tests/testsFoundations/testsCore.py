#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsCore.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.core` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import types
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["GetFrameTestCase",
		"GetCodeLayerNameTestCase",
		"GetModuleTestCase",
		"GetTraceNameTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GetFrameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.core.getFrame` definition units tests methods.
	"""

	def testGetFrame(self):
		"""
		This method tests :func:`foundations.core.getFrame` definition.
		"""

		self.assertIsInstance(core.getFrame(0), inspect.currentframe().__class__)

class GetCodeLayerNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.core.getCodeLayerName` definition units tests methods.
	"""

	def testGetCodeLayerName(self):
		"""
		This method tests :func:`foundations.core.getCodeLayerName` definition.
		"""

		codeLayerName = core.getCodeLayerName()
		self.assertIsInstance(codeLayerName, str)
		self.assertEqual(codeLayerName, inspect.currentframe().f_code.co_name)

class GetModuleTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.core.getModule` definition units tests methods.
	"""

	def testGetModule(self):
		"""
		This method tests :func:`foundations.core.getModule` definition.
		"""

		self.assertEqual(type(core.getModule(object)), types.ModuleType)
		self.assertEqual(core.getModule(object), inspect.getmodule(object))

class GetTraceNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.core.getTraceName` definition units tests methods.
	"""

	def testGetObjectName(self):
		"""
		This method tests :func:`foundations.core.getTraceName` definition.
		"""

		objectName = core.getTraceName(object)
		self.assertIsInstance(objectName, str)
		self.assertEqual(objectName, "__builtin__ | testGetObjectName.object()")

if __name__ == "__main__":
	unittest.main()
