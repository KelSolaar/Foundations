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

		LOGGER = logging.getLogger(Constants.logger)
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.items():
			core.setVerbosityLevel(value)
			self.assertEqual(level, LOGGER.level)

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

class GetObjectNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.core.getObjectName` definition units tests methods.
	"""

	def testGetObjectName(self):
		"""
		This method tests :func:`foundations.core.getObjectName` definition.
		"""

		objectName = core.getObjectName(object)
		self.assertIsInstance(objectName, str)
		self.assertEqual(objectName, "__builtin__ | testGetObjectName.object()")

class NestedAttributeTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.core.NestedAttribute` class units tests methods.
	"""

	def testNestedAttribute(self):
		"""
		This method tests :class:`foundations.core.NestedAttribute` class.
		"""

		nest = core.NestedAttribute()
		nest.my.deeply.nested.attribute = 64
		self.assertTrue(hasattr(nest, "nest.my.deeply.nested.attribute"))
		self.assertEqual(nest.my.deeply.nested.attribute, 64)

class StructureTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.core.Structure` class units tests methods.
	"""

	def testStructure(self):
		"""
		This method tests :class:`foundations.core.Structure` class.
		"""

		structure = core.Structure(John="Doe", Jane="Doe")
		self.assertIn("John", structure.keys())
		self.assertTrue(hasattr(structure, "John"))

class LookupTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.core.Lookup` class units tests methods.
	"""

	def testGetFirstKeyFromValue(self):
		"""
		This method tests :meth:`foundations.core.Lookup.getFirstKeyFromValue` method.
		"""

		lookup = core.Lookup(firstName="Doe", lastName="John", gender="male")
		self.assertEqual("firstName", lookup.getFirstKeyFromValue("Doe"))

	def testGetKeysFromValue(self):
		"""
		This method tests :meth:`foundations.core.Lookup.getKeysFromValue` method.
		"""

		lookup = core.Lookup(John="Doe", Jane="Doe", Luke="Skywalker")
		self.assertListEqual(["Jane", "John"], lookup.getKeysFromValue("Doe"))

if __name__ == "__main__":
	unittest.main()
