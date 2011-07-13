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
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
************************************************************************************************
***	testsConstants.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Constants Tests Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ConstantsTestCase(unittest.TestCase):
	"""
	This Class Is The ConstantsTests Class.
	"""

	def testRequiredAttributes(self):
		"""
		This Method Tests Presence Of Required Attributes.
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
		This Method Tests The "applicationName" Attribute.
		"""

		self.assertRegexpMatches(Constants.applicationName, "\w")

	def testLoggerAttribute(self):
		"""
		This Method Tests The "logger" Attribute.
		"""

		self.assertRegexpMatches(Constants.logger, "\w")

	def testVerbosityLevelAttribute(self):
		"""
		This Method Tests The "verbosityLevel" Attribute.
		"""

		self.assertIsInstance(Constants.verbosityLevel, int)
		self.assertGreaterEqual(Constants.verbosityLevel, 0)
		self.assertLessEqual(Constants.verbosityLevel, 4)

	def testVerbosityLabelsAttribute(self):
		"""
		This Method Tests The "verbosityLabels" Attribute.
		"""

		self.assertIsInstance(Constants.verbosityLabels, tuple)
		for label in Constants.verbosityLabels:
			self.assertIsInstance(label, str)

	def testLoggingDefaultFormaterAttribute(self):
		"""
		This Method Tests The "loggingDefaultFormatter" Attribute.
		"""

		self.assertIsInstance(Constants.loggingDefaultFormatter, str)

	def testLoggingSeparatorsAttribute(self):
		"""
		This Method Tests The "loggingSeparators" Attribute.
		"""

		self.assertIsInstance(Constants.loggingSeparators, str)

	def testEncodingFormatAttribute(self):
		"""
		This Method Tests The "encodingFormat" Attribute.
		"""

		validEncodings = ("ascii",
						"utf-8",
						"cp1252")

		self.assertIn(Constants.encodingFormat, validEncodings)

	def testEncodingErrorAttribute(self):
		"""
		This Method Tests The "encodingError" Attribute.
		"""

		validEncodings = ("strict",
						"ignore",
						"replace",
						"xmlcharrefreplace")

		self.assertIn(Constants.encodingError, validEncodings)

	def testApplicationDirectoryAttribute(self):
		"""
		This Method Tests The "applicationDirectory" Attribute.
		"""

		self.assertRegexpMatches(Constants.applicationDirectory, "\w")

	def testProviderDirectoryAttribute(self):
		"""
		This Method Tests The "providerDirectory" Attribute.
		"""

		self.assertRegexpMatches(Constants.providerDirectory, "\.*\w")

	def testNullObjectAttribute(self):
		"""
		This Method Tests The "nullObject" Attribute.
		"""

		self.assertRegexpMatches(Constants.nullObject, "\w")

if __name__ == '__main__':
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
