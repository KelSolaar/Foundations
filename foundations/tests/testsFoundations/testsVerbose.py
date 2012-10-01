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
import logging
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
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

__all__ = ["StreamerTestCase",
		"StandardOutputStreamerTestCase",
		"SetVerbosityLevelTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class StreamerTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.verbose.Streamer` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("stream",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(foundations.verbose.Streamer))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("write",
							"flush")

		for method in requiredMethods:
			self.assertIn(method, dir(foundations.verbose.Streamer))

class StandardOutputStreamerTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.core.StandardOutputStreamer` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("logger",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(foundations.verbose.StandardOutputStreamer))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("write",)

		for method in requiredMethods:
			self.assertIn(method, dir(foundations.verbose.StandardOutputStreamer))

class InstallLoggerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.installLogger` definition units tests methods.
	"""

	def testInstallLogger(self):
		"""
		This method tests :func:`foundations.verbose.installLogger` definition.
		"""

		self.assertTrue(not hasattr(sys.modules.get(__name__), "LOGGER"))
		foundations.verbose.installLogger()
		self.assertTrue(hasattr(sys.modules.get(__name__), "LOGGER"))
		self.assertIsInstance(LOGGER, logging.Logger)

class SetVerbosityLevelTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.setVerbosityLevel` definition units tests methods.
	"""

	def testSetVerbosityLevel(self):
		"""
		This method tests :func:`foundations.verbose.setVerbosityLevel` definition.
		"""

		logger = logging.getLogger(Constants.logger)
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.iteritems():
			foundations.verbose.setVerbosityLevel(value)
			self.assertEqual(level, logger.level)

if __name__ == "__main__":
	unittest.main()
