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
**testsConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Constants tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class ConstantsTestCase(unittest.TestCase):
	"""
	This class is the ConstantsTests class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("applicationName",
								"logger",
								"verbosityLevel",
								"verbosityLabels",
								"loggingDefaultFormatter",
								"loggingSeparators",
								"encodingFormat",
								"encodingError",
								"applicationDirectory",
								"providerDirectory",
								"nullObject")

		for attribute in requiredAttributes:
			self.assertIn(attribute, Constants.__dict__)

	def testApplicationNameAttribute(self):
		"""
		This method tests the "applicationName" attribute.
		"""

		self.assertRegexpMatches(Constants.applicationName, "\w+")

	def testLoggerAttribute(self):
		"""
		This method tests the "logger" attribute.
		"""

		self.assertRegexpMatches(Constants.logger, "\w+")

	def testVerbosityLevelAttribute(self):
		"""
		This method tests the "verbosityLevel" attribute.
		"""

		self.assertIsInstance(Constants.verbosityLevel, int)
		self.assertGreaterEqual(Constants.verbosityLevel, 0)
		self.assertLessEqual(Constants.verbosityLevel, 4)

	def testVerbosityLabelsAttribute(self):
		"""
		This method tests the "verbosityLabels" attribute.
		"""

		self.assertIsInstance(Constants.verbosityLabels, tuple)
		for label in Constants.verbosityLabels:
			self.assertIsInstance(label, str)

	def testLoggingDefaultFormaterAttribute(self):
		"""
		This method tests the "loggingDefaultFormatter" attribute.
		"""

		self.assertIsInstance(Constants.loggingDefaultFormatter, str)

	def testLoggingSeparatorsAttribute(self):
		"""
		This method tests the "loggingSeparators" attribute.
		"""

		self.assertIsInstance(Constants.loggingSeparators, str)

	def testEncodingFormatAttribute(self):
		"""
		This method tests the "encodingFormat" attribute.
		"""

		validEncodings = ("ascii",
						"utf-8",
						"cp1252")

		self.assertIn(Constants.encodingFormat, validEncodings)

	def testEncodingErrorAttribute(self):
		"""
		This method tests the "encodingError" attribute.
		"""

		validEncodings = ("strict",
						"ignore",
						"replace",
						"xmlcharrefreplace")

		self.assertIn(Constants.encodingError, validEncodings)

	def testApplicationDirectoryAttribute(self):
		"""
		This method tests the "applicationDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.applicationDirectory, "\w+")

	def testProviderDirectoryAttribute(self):
		"""
		This method tests the "providerDirectory" attribute.
		"""

		self.assertRegexpMatches(Constants.providerDirectory, "\.*\w")

	def testNullObjectAttribute(self):
		"""
		This method tests the "nullObject" attribute.
		"""

		self.assertRegexpMatches(Constants.nullObject, "\w+")

if __name__ == "__main__":
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
