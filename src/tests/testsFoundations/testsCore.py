#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**testsCore.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Core tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Overall variables.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class StandardMessageHookTestCase(unittest.TestCase):
	"""
	This class is the StandardMessageHookTestCase class.
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
	This class is the SetVerbosityLevelTestCase class.
	"""

	def testSetVerbosityLevel(self):
		"""
		This method tests the "setVerbosityLevel" definition.
		"""

		LOGGER = logging.getLogger(Constants.logger)
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.items():
			core.setVerbosityLevel(value)
			self.assertEqual(level, LOGGER.level)

class GetFrameTestCase(unittest.TestCase):
	"""
	This class is the GetFrameTestCase class.
	"""

	def testGetFrame(self):
		"""
		This method tests the "getFrame" definition.
		"""

		self.assertIsInstance(core.getFrame(0), inspect.currentframe().__class__)

class GetCodeLayerNameTestCase(unittest.TestCase):
	"""
	This class is the GetCodeLayerNameTestCase class.
	"""

	def testGetCodeLayerName(self):
		"""
		This method tests the "getCodeLayerName" definition.
		"""

		codeLayerName = core.getCodeLayerName()
		self.assertIsInstance(codeLayerName, str)
		self.assertEqual(codeLayerName, inspect.currentframe().f_code.co_name)

class GetModuleTestCase(unittest.TestCase):
	"""
	This class is the GetCodeLayerNameTestCase class.
	"""

	def testGetModule(self):
		"""
		This method tests the "getModule" definition.
		"""

		self.assertEqual(type(core.getModule(object)), types.ModuleType)
		self.assertEqual(core.getModule(object), inspect.getmodule(object))

class GetObjectNameTestCase(unittest.TestCase):
	"""
	This class is the GetObjectNameTestCase class.
	"""

	def testGetObjectName(self):
		"""
		This method tests the "getObjectName" definition.
		"""

		objectName = core.getObjectName(object)
		self.assertIsInstance(objectName, str)
		self.assertEqual(objectName, "__builtin__ | testGetObjectName.object()")

if __name__ == "__main__":
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
