#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsEnvironment.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.environment` module.

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
import foundations.environment
from foundations.environment import Environment

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["EnvironmentTestCase",
		"GetSystemApplicationDataDirectoryTestCase",
		"GetUserApplicationDataDirectoryTestCase", ]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EnvironmentTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.environment.Environment` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("variables",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(Environment))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("getValues",
						"setValues",
						"getValue",
						"setValue")

		for method in requiredMethods:
			self.assertIn(method, dir(Environment))

	def testGetValues(self):
		"""
		This method tests :meth:`foundations.environment.Environment.getValues` method.
		"""

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			variable = "APPDATA"
		elif platform.system() == "Darwin":
			variable = "HOME"
		elif platform.system() == "Linux":
			variable = "HOME"

		environment = Environment(variable)
		self.assertIsInstance(environment.getValues(), dict)
		self.assertIsInstance(environment.getValues(variable), dict)

		self.assertIsInstance(environment.getValues().get(variable), str)
		self.assertEqual(environment.getValues()[variable], os.environ[variable])
		environment.getValues("JOHNDOE_IS_FOR_SURE_A_NON_EXISTING_SYSTEM_ENVIRONMENT_VARIABLE")
		self.assertFalse(environment.getValues()["JOHNDOE_IS_FOR_SURE_A_NON_EXISTING_SYSTEM_ENVIRONMENT_VARIABLE"])

	def testSetValues(self):
		"""
		This method tests :meth:`foundations.environment.Environment.setValues` method.
		"""

		environment = Environment()
		self.assertTrue(environment.setValues(JOHN="DOE"))
		self.assertIn("JOHN", os.environ)
		self.assertTrue(environment.setValues(JOHN="EOD", DOE="JOHN"))
		self.assertIn("DOE", os.environ)
		self.assertEqual(environment.getValues()["JOHN"], "EOD")

	def testGetValue(self):
		"""
		This method tests :meth:`foundations.environment.Environment.getValue` method.
		"""

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			environment = Environment("APPDATA")
		elif platform.system() == "Darwin":
			environment = Environment("HOME")
		elif platform.system() == "Linux":
			environment = Environment("HOME")
		self.assertTrue(environment.getValue())
		self.assertIsInstance(environment.getValue(), str)
		environment.setValues(JOHN="DOE")
		self.assertEqual(environment.getValue("JOHN"), "DOE")
		self.assertFalse(environment.getValue("JOHNDOE_IS_FOR_SURE_A_NON_EXISTING_SYSTEM_ENVIRONMENT_VARIABLE"))

	def testSetValue(self):
		"""
		This method tests :meth:`foundations.environment.Environment.setValue` method.
		"""

		environment = Environment()
		self.assertTrue(environment.setValue("JANE", "DOE"))
		self.assertIn("JANE", os.environ)
		self.assertEqual(environment.getValue("JANE"), "DOE")

class GetSystemApplicationDataDirectoryTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.common.getSystemApplicationDataDirectory` definition units tests methods.
	"""

	def testGetSystemApplicationDataDirectory(self):
		"""
		This method tests :func:`foundations.common.getSystemApplicationDataDirectory` definition.
		"""

		path = foundations.environment.getSystemApplicationDataDirectory()
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

		path = foundations.environment.getUserApplicationDataDirectory()
		self.assertIsInstance(path, str)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
