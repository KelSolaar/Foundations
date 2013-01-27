#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsVerbose.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.verbose` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest
import tempfile

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.tests.testsFoundations.resources.dummy
import foundations.verbose
from foundations.tests.testsFoundations.resources.dummy import dummy1

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["StreamerTestCase",
		"StandardOutputStreamerTestCase",
		"IndentMessageTestCase",
		"TracerTestCase",
		"InstallLoggerTestCase",
		"UninstallLoggerTestCase",
		"GetLoggingConsoleHandlerTestCase",
		"GetLoggingFileHandlerTestCase",
		"GetLoggingStreamHandlerTestCase",
		"RemoveLoggingHandlerTestCase",
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

class IndentMessageTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.indentMessage` definition units tests methods.
	"""

	def testIndentMessage(self):
		"""
		This method tests :func:`foundations.verbose.indentMessage` definition.
		"""

		self.assertIsInstance(foundations.verbose.indentMessage("message"), str)

class TracerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.tracer` definition units tests methods.
	"""

	def testTracer(self):
		"""
		This method tests :func:`foundations.trace.tracer` definition.
		"""

		object = foundations.verbose.tracer(dummy1)
		self.assertTrue(foundations.trace.isTraced(object))
		self.assertEqual(object(), foundations.tests.testsFoundations.resources.dummy.GLOBAL_RETURN_VALUE)

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
		foundations.verbose.uninstallLogger()

class UninstallLoggerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.uninstallLogger` definition units tests methods.
	"""

	def testUninstallLogger(self):
		"""
		This method tests :func:`foundations.verbose.uninstallLogger` definition.
		"""

		foundations.verbose.installLogger()
		self.assertTrue(hasattr(sys.modules.get(__name__), "LOGGER"))
		foundations.verbose.uninstallLogger()
		self.assertTrue(not hasattr(sys.modules.get(__name__), "LOGGER"))

class GetLoggingConsoleHandlerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.getLoggingConsoleHandler` definition units tests methods.
	"""

	def testGetLoggingConsoleHandler(self):
		"""
		This method tests :func:`foundations.verbose.getLoggingConsoleHandler` definition.
		"""

		foundations.verbose.installLogger()
		handler = foundations.verbose.getLoggingConsoleHandler()
		self.assertIsInstance(handler, logging.Handler)
		self.assertIn(handler, LOGGER.handlers)
		del LOGGER.handlers[:]
		foundations.verbose.uninstallLogger()

class GetLoggingFileHandlerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.getLoggingFileHandler` definition units tests methods.
	"""

	def testGetLoggingFileHandler(self):
		"""
		This method tests :func:`foundations.verbose.getLoggingFileHandler` definition.
		"""

		foundations.verbose.installLogger()
		fileDescriptor, path = tempfile.mkstemp()
		handler = foundations.verbose.getLoggingFileHandler(file=path,
															formatter=foundations.verbose.LOGGING_STANDARD_FORMATTER)
		self.assertIsInstance(handler, logging.Handler)
		self.assertIn(handler, LOGGER.handlers)
		message = "This is a test error message!"
		LOGGER.error(message)
		with file(path) as f:
			content = f.readlines()
		self.assertEqual(message, content.pop().strip())
		del LOGGER.handlers[:]
		foundations.verbose.uninstallLogger()
		os.close(fileDescriptor)

class GetLoggingStreamHandlerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.getLoggingStreamHandler` definition units tests methods.
	"""

	def testGetLoggingStreamHandler(self):
		"""
		This method tests :func:`foundations.verbose.getLoggingStreamHandler` definition.
		"""

		foundations.verbose.installLogger()
		handler = foundations.verbose.getLoggingStreamHandler(formatter=foundations.verbose.LOGGING_STANDARD_FORMATTER)
		self.assertIsInstance(handler, logging.Handler)
		self.assertIn(handler, LOGGER.handlers)
		message = "This is a test error message!"
		LOGGER.error(message)
		self.assertEqual(message, handler.stream.stream.pop().strip())
		del LOGGER.handlers[:]
		foundations.verbose.uninstallLogger()

class RemoveLoggingHandlerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.removeLoggingHandler` definition units tests methods.
	"""

	def testRemoveLoggingHandler(self):
		"""
		This method tests :func:`foundations.verbose.removeLoggingHandler` definition.
		"""

		foundations.verbose.installLogger()
		foundations.verbose.removeLoggingHandler(foundations.verbose.getLoggingConsoleHandler())
		foundations.verbose.removeLoggingHandler(foundations.verbose.getLoggingStreamHandler())
		self.assertListEqual(LOGGER.handlers, list())
		foundations.verbose.uninstallLogger()

class SetVerbosityLevelTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.verbose.setVerbosityLevel` definition units tests methods.
	"""

	def testSetVerbosityLevel(self):
		"""
		This method tests :func:`foundations.verbose.setVerbosityLevel` definition.
		"""

		foundations.verbose.installLogger()
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.iteritems():
			foundations.verbose.setVerbosityLevel(value)
			self.assertEqual(level, LOGGER.level)
		foundations.verbose.uninstallLogger()

if __name__ == "__main__":
	unittest.main()
