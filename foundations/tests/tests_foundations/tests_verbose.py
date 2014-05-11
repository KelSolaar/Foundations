#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_verbose.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.verbose` module.

**Others:**

"""

from __future__ import unicode_literals

import logging
import os
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest
import tempfile

import foundations.tests.tests_foundations.resources.dummy
import foundations.verbose
from foundations.tests.tests_foundations.resources.dummy import dummy1

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestStreamer",
		"TestStandardOutputStreamer",
		"TestIndentMessage",
		"TestTracer",
		"TestInstallLogger",
		"TestUninstallLogger",
		"TestGetLoggingConsoleHandler",
		"TestGetLoggingFileHandler",
		"TestGetLoggingStreamHandler",
		"TestRemoveLoggingHandler",
		"TestSetVerbosityLevel"]

class TestStreamer(unittest.TestCase):
	"""
	Defines :class:`foundations.verbose.Streamer` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("stream",)

		for attribute in required_attributes:
			self.assertIn(attribute, dir(foundations.verbose.Streamer))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("write",
							"flush")

		for method in required_methods:
			self.assertIn(method, dir(foundations.verbose.Streamer))

class TestStandardOutputStreamer(unittest.TestCase):
	"""
	Defines :class:`foundations.core.StandardOutputStreamer` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("logger",)

		for attribute in required_attributes:
			self.assertIn(attribute, dir(foundations.verbose.StandardOutputStreamer))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("write",)

		for method in required_methods:
			self.assertIn(method, dir(foundations.verbose.StandardOutputStreamer))

class TestIndentMessage(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.indent_message` definition units tests methods.
	"""

	def test_indent_message(self):
		"""
		Tests :func:`foundations.verbose.indent_message` definition.
		"""

		self.assertIsInstance(foundations.verbose.indent_message("message"), unicode)

class TestTracer(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.tracer` definition units tests methods.
	"""

	def test_tracer(self):
		"""
		Tests :func:`foundations.trace.tracer` definition.
		"""

		object = foundations.verbose.tracer(dummy1)
		self.assertTrue(foundations.trace.is_traced(object))
		self.assertEqual(object(), foundations.tests.tests_foundations.resources.dummy.GLOBAL_RETURN_VALUE)

class TestInstallLogger(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.install_logger` definition units tests methods.
	"""

	def test_install_logger(self):
		"""
		Tests :func:`foundations.verbose.install_logger` definition.
		"""

		self.assertTrue(not hasattr(sys.modules.get(__name__), "LOGGER"))
		foundations.verbose.install_logger()
		self.assertTrue(hasattr(sys.modules.get(__name__), "LOGGER"))
		self.assertIsInstance(LOGGER, logging.Logger)
		foundations.verbose.uninstall_logger()

class TestUninstallLogger(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.uninstall_logger` definition units tests methods.
	"""

	def test_uninstall_logger(self):
		"""
		Tests :func:`foundations.verbose.uninstall_logger` definition.
		"""

		foundations.verbose.install_logger()
		self.assertTrue(hasattr(sys.modules.get(__name__), "LOGGER"))
		foundations.verbose.uninstall_logger()
		self.assertTrue(not hasattr(sys.modules.get(__name__), "LOGGER"))

class TestGetLoggingConsoleHandler(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.get_logging_console_handler` definition units tests methods.
	"""

	def test_get_logging_console_handler(self):
		"""
		Tests :func:`foundations.verbose.get_logging_console_handler` definition.
		"""

		foundations.verbose.install_logger()
		handler = foundations.verbose.get_logging_console_handler()
		self.assertIsInstance(handler, logging.Handler)
		self.assertIn(handler, LOGGER.handlers)
		del LOGGER.handlers[:]
		foundations.verbose.uninstall_logger()

class TestGetLoggingFileHandler(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.get_logging_file_handler` definition units tests methods.
	"""

	def test_get_logging_file_handler(self):
		"""
		Tests :func:`foundations.verbose.get_logging_file_handler` definition.
		"""

		foundations.verbose.install_logger()
		file_descriptor, path = tempfile.mkstemp()
		handler = foundations.verbose.get_logging_file_handler(file=path,
															formatter=foundations.verbose.LOGGING_STANDARD_FORMATTER)
		self.assertIsInstance(handler, logging.Handler)
		self.assertIn(handler, LOGGER.handlers)
		message = "This is a test error message!"
		LOGGER.error(message)
		with file(path) as f:
			content = f.readlines()
		self.assertEqual(message, content.pop().strip())
		del LOGGER.handlers[:]
		foundations.verbose.uninstall_logger()
		os.close(file_descriptor)

class TestGetLoggingStreamHandler(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.get_logging_stream_handler` definition units tests methods.
	"""

	def test_get_logging_stream_handler(self):
		"""
		Tests :func:`foundations.verbose.get_logging_stream_handler` definition.
		"""

		foundations.verbose.install_logger()
		handler = foundations.verbose.get_logging_stream_handler(formatter=foundations.verbose.LOGGING_STANDARD_FORMATTER)
		self.assertIsInstance(handler, logging.Handler)
		self.assertIn(handler, LOGGER.handlers)
		message = "This is a test error message!"
		LOGGER.error(message)
		self.assertEqual(message, handler.stream.stream.pop().strip())
		del LOGGER.handlers[:]
		foundations.verbose.uninstall_logger()

class TestRemoveLoggingHandler(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.remove_logging_handler` definition units tests methods.
	"""

	def test_remove_logging_handler(self):
		"""
		Tests :func:`foundations.verbose.remove_logging_handler` definition.
		"""

		foundations.verbose.install_logger()
		foundations.verbose.remove_logging_handler(foundations.verbose.get_logging_console_handler())
		foundations.verbose.remove_logging_handler(foundations.verbose.get_logging_stream_handler())
		self.assertListEqual(LOGGER.handlers, list())
		foundations.verbose.uninstall_logger()

class TestSetVerbosityLevel(unittest.TestCase):
	"""
	Defines :func:`foundations.verbose.set_verbosity_level` definition units tests methods.
	"""

	def test_set_verbosity_level(self):
		"""
		Tests :func:`foundations.verbose.set_verbosity_level` definition.
		"""

		foundations.verbose.install_logger()
		levels = {logging.CRITICAL:0, logging.ERROR:1, logging.WARNING:2, logging.INFO:3, logging.DEBUG:4  }
		for level, value in levels.iteritems():
			foundations.verbose.set_verbosity_level(value)
			self.assertEqual(level, LOGGER.level)
		foundations.verbose.uninstall_logger()

if __name__ == "__main__":
	unittest.main()
