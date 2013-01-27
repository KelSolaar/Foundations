#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.globals.constants` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["ConstantsTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ConstantsTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.globals.constants.Constants` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("applicationName",
								"majorVersion",
								"minorVersion",
								"changeVersion",
								"releaseVersion",
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
		This method tests :attr:`foundations.globals.constants.Constants.applicationName` attribute.
		"""

		self.assertRegexpMatches(Constants.applicationName, "\w+")

	def testMajorVersionAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.majorVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d")

	def testMinorVersionAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.minorVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d")

	def testChangeVersionAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.changeVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d")

	def testReleaseVersionAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.releaseVersion` attribute.
		"""

		self.assertRegexpMatches(Constants.releaseVersion, "\d\.\d\.\d")

	def testLoggerAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.logger` attribute.
		"""

		self.assertRegexpMatches(Constants.logger, "\w+")

	def testVerbosityLevelAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.verbosityLevel` attribute.
		"""

		self.assertIsInstance(Constants.verbosityLevel, int)
		self.assertGreaterEqual(Constants.verbosityLevel, 0)
		self.assertLessEqual(Constants.verbosityLevel, 4)

	def testVerbosityLabelsAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.verbosityLabels` attribute.
		"""

		self.assertIsInstance(Constants.verbosityLabels, tuple)
		for label in Constants.verbosityLabels:
			self.assertIsInstance(label, str)

	def testLoggingDefaultFormaterAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.loggingDefaultFormatter` attribute.
		"""

		self.assertIsInstance(Constants.loggingDefaultFormatter, str)

	def testLoggingSeparatorsAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.loggingSeparators` attribute.
		"""

		self.assertIsInstance(Constants.loggingSeparators, str)

	def testEncodingFormatAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.encodingFormat` attribute.
		"""

		validEncodings = ("ascii",
						"utf-8",
						"cp1252")

		self.assertIn(Constants.encodingFormat, validEncodings)

	def testEncodingErrorAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.encodingError` attribute.
		"""

		validEncodings = ("strict",
						"ignore",
						"replace",
						"xmlcharrefreplace")

		self.assertIn(Constants.encodingError, validEncodings)

	def testApplicationDirectoryAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.applicationDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.applicationDirectory, "\w+")

	def testProviderDirectoryAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.providerDirectory` attribute.
		"""

		self.assertRegexpMatches(Constants.providerDirectory, "\.*\w")

	def testNullObjectAttribute(self):
		"""
		This method tests :attr:`foundations.globals.constants.Constants.nullObject` attribute.
		"""

		self.assertRegexpMatches(Constants.nullObject, "\w+")

if __name__ == "__main__":
	unittest.main()
