#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_environment.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.environment` module.

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
import tempfile

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.environment
from foundations.environment import Environment

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestEnvironment",
		"TestGetTemporaryDirectory",
		"TestGetSystemApplicationDataDirectory",
		"TestGetUserApplicationDataDirectory", ]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TestEnvironment(unittest.TestCase):
	"""
	Defines :class:`foundations.environment.Environment` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("variables",)

		for attribute in required_attributes:
			self.assertIn(attribute, dir(Environment))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("get_values",
						"set_values",
						"get_value",
						"set_value")

		for method in required_methods:
			self.assertIn(method, dir(Environment))

	def test_get_values(self):
		"""
		Tests :meth:`foundations.environment.Environment.get_values` method.
		"""

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			variable = "APPDATA"
		elif platform.system() == "Darwin":
			variable = "HOME"
		elif platform.system() == "Linux":
			variable = "HOME"

		environment = Environment(variable)
		self.assertIsInstance(environment.get_values(), dict)
		self.assertIsInstance(environment.get_values(variable), dict)

		self.assertIsInstance(environment.get_values().get(variable), unicode)
		self.assertEqual(environment.get_values()[variable], os.environ[variable])
		environment.get_values("JOHNDOE_IS_FOR_SURE_A_NON_EXISTING_SYSTEM_ENVIRONMENT_VARIABLE")
		self.assertFalse(environment.get_values()["JOHNDOE_IS_FOR_SURE_A_NON_EXISTING_SYSTEM_ENVIRONMENT_VARIABLE"])

	def test_set_values(self):
		"""
		Tests :meth:`foundations.environment.Environment.set_values` method.
		"""

		environment = Environment()
		self.assertTrue(environment.set_values(JOHN="DOE"))
		self.assertIn("JOHN", os.environ)
		self.assertTrue(environment.set_values(JOHN="EOD", DOE="JOHN"))
		self.assertIn("DOE", os.environ)
		self.assertEqual(environment.get_values()["JOHN"], "EOD")

	def test_get_value(self):
		"""
		Tests :meth:`foundations.environment.Environment.get_value` method.
		"""

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			environment = Environment("APPDATA")
		elif platform.system() == "Darwin":
			environment = Environment("HOME")
		elif platform.system() == "Linux":
			environment = Environment("HOME")
		self.assertTrue(environment.get_value())
		self.assertIsInstance(environment.get_value(), unicode)
		environment.set_values(JOHN="DOE")
		self.assertEqual(environment.get_value("JOHN"), "DOE")
		self.assertFalse(environment.get_value("JOHNDOE_IS_FOR_SURE_A_NON_EXISTING_SYSTEM_ENVIRONMENT_VARIABLE"))

	def test_set_value(self):
		"""
		Tests :meth:`foundations.environment.Environment.set_value` method.
		"""

		environment = Environment()
		self.assertTrue(environment.set_value("JANE", "DOE"))
		self.assertIn("JANE", os.environ)
		self.assertEqual(environment.get_value("JANE"), "DOE")

class TestGetTemporaryDirectory(unittest.TestCase):
	"""
	Defines :func:`foundations.common.get_temporary_directory` definition units tests methods.
	"""

	def test_get_temporary_directory(self):
		"""
		Tests :func:`foundations.common.get_temporary_directory` definition.
		"""

		path = foundations.environment.get_temporary_directory()
		self.assertIsInstance(path, unicode)
		self.assertTrue(os.path.exists(path))
		self.assertEqual(path, tempfile.gettempdir())

class TestGetSystemApplicationDataDirectory(unittest.TestCase):
	"""
	Defines :func:`foundations.common.get_system_application_data_directory` definition units tests methods.
	"""

	def test_get_system_application_data_directory(self):
		"""
		Tests :func:`foundations.common.get_system_application_data_directory` definition.
		"""

		path = foundations.environment.get_system_application_data_directory()
		self.assertIsInstance(path, unicode)
		self.assertTrue(os.path.exists(path))

class TestGetUserApplicationDataDirectory(unittest.TestCase):
	"""
	Defines :func:`foundations.common.get_user_application_data_directory` definition units tests methods.
	"""

	def test_get_user_application_data_directory(self):
		"""
		Tests :func:`foundations.common.get_user_application_data_directory` definition.
		"""

		path = foundations.environment.get_user_application_data_directory()
		self.assertIsInstance(path, unicode)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
