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
import logging
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
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["StandardMessageHookTestCase",
		"SetVerbosityLevelTestCase",
		"GetFrameTestCase",
		"GetCodeLayerNameTestCase",
		"GetModuleTestCase",
		"GetTraceNameTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class StandardMessageHookTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.core.StandardMessageHook` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("logger",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(core.StandardMessageHook))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("write",)

		for method in requiredMethods:
			self.assertIn(method, dir(core.StandardMessageHook))

class SetVerbosityLevelTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.core.setVerbosityLevel` definition units tests methods.
	"""

	def testSetVerbosityLevel(self):
		"""
		This method tests :func:`foundations.core.setVerbosityLevel` definition.
		"""

		logger = logging.getLogger(Constants.logger)
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.iteritems():
			core.setVerbosityLevel(value)
			self.assertEqual(level, logger.level)

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
