#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsCore.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Core tests Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import inspect
import logging
import types
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from foundations.globals.constants import Constants

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
class StandardMessageHookTestCase(unittest.TestCase):
	"""
	This class is the **StandardMessageHookTestCase** class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		hook = core.StandardMessageHook(None)
		requiredAttributes = ("logger",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(hook))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		hook = core.StandardMessageHook(None)
		requiredMethods = ("write",)

		for method in requiredMethods:
			self.assertIn(method, dir(hook))

class SetVerbosityLevelTestCase(unittest.TestCase):
	"""
	This class is the **SetVerbosityLevelTestCase** class.
	"""

	def testSetVerbosityLevel(self):
		"""
		This method tests **setVerbosityLevel** definition.
		"""

		LOGGER = logging.getLogger(Constants.logger)
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.items():
			core.setVerbosityLevel(value)
			self.assertEqual(level, LOGGER.level)

class GetFrameTestCase(unittest.TestCase):
	"""
	This class is the **GetFrameTestCase** class.
	"""

	def testGetFrame(self):
		"""
		This method tests **getFrame** definition.
		"""

		self.assertIsInstance(core.getFrame(0), inspect.currentframe().__class__)

class GetCodeLayerNameTestCase(unittest.TestCase):
	"""
	This class is the **GetCodeLayerNameTestCase** class.
	"""

	def testGetCodeLayerName(self):
		"""
		This method tests **getCodeLayerName** definition.
		"""

		codeLayerName = core.getCodeLayerName()
		self.assertIsInstance(codeLayerName, str)
		self.assertEqual(codeLayerName, inspect.currentframe().f_code.co_name)

class GetModuleTestCase(unittest.TestCase):
	"""
	This class is the **GetCodeLayerNameTestCase** class.
	"""

	def testGetModule(self):
		"""
		This method tests **getModule** definition.
		"""

		self.assertEqual(type(core.getModule(object)), types.ModuleType)
		self.assertEqual(core.getModule(object), inspect.getmodule(object))

class GetObjectNameTestCase(unittest.TestCase):
	"""
	This class is the **GetObjectNameTestCase** class.
	"""

	def testGetObjectName(self):
		"""
		This method tests **getObjectName** definition.
		"""

		objectName = core.getObjectName(object)
		self.assertIsInstance(objectName, str)
		self.assertEqual(objectName, "__builtin__ | testGetObjectName.object()")

if __name__ == "__main__":
	unittest.main()
