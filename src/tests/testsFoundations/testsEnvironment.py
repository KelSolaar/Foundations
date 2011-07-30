#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsEnvironment.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Environment tests Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import platform
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from foundations.environment import Environment

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
class EnvironmentTestCase(unittest.TestCase):
	"""
	This class is the EnvironmentTestCase class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		environment = Environment()
		requiredAttributes = ("variable",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(environment))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		environment = Environment()
		requiredMethods = ("getPath",)

		for method in requiredMethods:
			self.assertIn(method, dir(environment))

	def testGetPath(self):
		"""
		This method tests the "Environment" class "getPath" method.
		"""

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			environment = Environment("APPDATA")
		elif platform.system() == "Darwin":
			environment = Environment("HOME")
		elif platform.system() == "Linux":
			environment = Environment("HOME")
		self.assertTrue(environment.getPath())
		self.assertIsInstance(environment.getPath(), str)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

