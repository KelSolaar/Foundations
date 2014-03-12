#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsExceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.exceptions` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import itertools
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
	from ordereddict import OrderedDict
else:
	import unittest
	from collections import OrderedDict
import types

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["EXCEPTIONS"
		"GetInnerMostFrameCase",
		"ExtractStackCase",
		"ExtractArgumentsCase",
		"ExtractLocalsCase",
		"ExtractExceptionCase",
		"FormatExceptionCase",
		"FormatReportCase",
		"InstallExceptionHandlerCase",
		"UninstallExceptionHandlerCase",
		"ExceptionsTestCase",
		"AttributeStructureParsingErrorTestCase"]

EXCEPTIONS = []

def _gatherExceptions():
	"""
	Gathers the exceptions.
	"""

	for attribute in dir(foundations.exceptions):
		object = getattr(foundations.exceptions, attribute)
		if not inspect.isclass(object):
			continue
		if issubclass(object, BaseException):
			EXCEPTIONS.append(object)

_gatherExceptions()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GetInnerMostFrameCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.getInnerMostFrame` definition units tests methods.
	"""

	def testGetInnerMostFrame(self):
		"""
		Tests :func:`foundations.exceptions.getInnerMostFrame` definition.
		"""

		try:
			raise Exception("This is a test exception!")
		except Exception as error:
			cls, instance, trcback = foundations.exceptions.extractException(error)
			self.assertIsInstance(foundations.exceptions.getInnerMostFrame(trcback), types.FrameType)
			self.assertEqual(foundations.exceptions.getInnerMostFrame(None), None)

class ExtractStackCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.extractStack` definition units tests methods.
	"""

	def testExtractStack(self):
		"""
		Tests :func:`foundations.exceptions.extractStack` definition.
		"""

		try:
			raise Exception("This is a test exception!")
		except Exception as error:
			cls, instance, trcback = foundations.exceptions.extractException(error)
			stack = foundations.exceptions.extractStack(foundations.exceptions.getInnerMostFrame(trcback))
			self.assertIsInstance(stack, list)
			for frame, fileName, lineNumber, name, context, index in stack:
				self.assertIsInstance(frame, types.FrameType)
				self.assertIsInstance(fileName, unicode)
				self.assertIsInstance(lineNumber, int)
				self.assertIsInstance(name, unicode)
				self.assertIsInstance(context, list)
				self.assertIsInstance(index, int)

class ExtractArgumentsCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.extractArguments` definition units tests methods.
	"""

	def testExtractArguments(self, testArgument="My Value!", *args, **kwargs):
		"""
		Tests :func:`foundations.exceptions.extractArguments` definition.

		:param testArgument: Test argument.
		:type testArgument: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		try:
			raise Exception("This is a test exception!")
		except Exception as error:
			cls, instance, trcback = foundations.exceptions.extractException(error)
			arguments, namelessArgs, keywordArgs = \
			foundations.exceptions.extractArguments(foundations.exceptions.getInnerMostFrame(trcback))

			self.assertListEqual(arguments, ["self", "testArgument"])
			self.assertEqual(namelessArgs, "args")
			self.assertEqual(keywordArgs, "kwargs")

class ExtractLocalsCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.extractLocals` definition units tests methods.
	"""

	def testExtractLocals(self, testArgument="My Value!", *args, **kwargs):
		"""
		Tests :func:`foundations.exceptions.extractLocals` definition.

		:param testArgument: Test argument.
		:type testArgument: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		try:
			raise Exception("This is a test exception!")
		except Exception as error:
			cls, instance, trcback = foundations.exceptions.extractException(error)
			extractedLocals = foundations.exceptions.extractLocals(trcback)
			self.assertIsInstance(extractedLocals, list)
			for frame, locals in extractedLocals:
				self.assertIsInstance(frame, tuple)
				self.assertIsInstance(frame[0], unicode)
				self.assertIsInstance(frame[1], unicode)
				self.assertIsInstance(frame[2], int)

				arguments, namelessArgs, keywordArgs, locals = locals
				self.assertIsInstance(arguments, OrderedDict)
				self.assertIsInstance(namelessArgs, list)
				self.assertIsInstance(keywordArgs, dict)
				self.assertIsInstance(locals, dict)

class ExtractExceptionCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.extractException` definition units tests methods.
	"""

	def testExtractException(self):
		"""
		Tests :func:`foundations.exceptions.extractException` definition.
		"""

		try:
			raise Exception("This is a test exception!")
		except Exception as error:
			cls, instance, trcback = foundations.exceptions.extractException(error)
			self.assertEqual(cls, Exception)
			self.assertIsInstance(instance, Exception)
			self.assertIsInstance(trcback, types.TracebackType)
			cls, instance, trcback = foundations.exceptions.extractException(*sys.exc_info())
			self.assertEqual(cls, Exception)
			self.assertIsInstance(instance, Exception)
			self.assertIsInstance(trcback, types.TracebackType)

class FormatExceptionCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.formatException` definition units tests methods.
	"""

	def testFormatException(self):
		"""
		Tests :func:`foundations.exceptions.formatException` definition.
		"""

		try:
			raise Exception("This is a test exception!")
		except Exception as error:
			output = foundations.exceptions.formatException(*sys.exc_info())
			self.assertIsInstance(output, list)
			for line in output:
				self.assertIsInstance(line, unicode)

class FormatReportCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.formatReport` definition units tests methods.
	"""

	def testFormatReport(self):
		"""
		Tests :func:`foundations.exceptions.formatReport` definition.
		"""

		try:
			raise Exception("This is a test exception!")
		except Exception as error:
			header, frames, trcback = foundations.exceptions.formatReport(*sys.exc_info())
			self.assertIsInstance(header, list)
			self.assertIsInstance(frames, list)
			self.assertIsInstance(trcback, list)
			for line in itertools.chain(header, frames, trcback):
				self.assertIsInstance(line, unicode)

class InstallExceptionHandlerCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.installExceptionHandler` definition units tests methods.
	"""

	def testInstallExceptionHandler(self):
		"""
		Tests :func:`foundations.exceptions.installExceptionHandler` definition.
		"""

		exceptHook = sys.excepthook
		self.assertTrue(foundations.exceptions.installExceptionHandler())
		self.assertNotEqual(sys.excepthook, exceptHook)
		foundations.exceptions.uninstallExceptionHandler()

class UninstallExceptionHandlerCase(unittest.TestCase):
	"""
	Defines :func:`foundations.exceptions.uninstallExceptionHandler` definition units tests methods.
	"""

	def testUninstallExceptionHandler(self):
		"""
		Tests :func:`foundations.exceptions.uninstallExceptionHandler` definition.
		"""

		exceptHook = sys.excepthook
		foundations.exceptions.installExceptionHandler()
		self.assertTrue(foundations.exceptions.uninstallExceptionHandler())
		self.assertEqual(sys.excepthook, exceptHook)

class ExceptionsTestCase(unittest.TestCase):
	"""
	Defines :mod:`foundations.exceptions` module exceptions classes units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		Tests presence of required attributes.
		"""

		requiredAttributes = ("value",)
		for exception in EXCEPTIONS:
			exceptionInstance = exception(None)
			for attribute in requiredAttributes:
				self.assertIn(attribute, dir(exceptionInstance))

	def test__str__(self):
		"""
		Tests exceptions classes **__str__** method.
		"""

		for exception in EXCEPTIONS:
			exceptionInstance = exception("{0} Exception raised!".format(exception.__class__))
			self.assertIsInstance(exceptionInstance.__str__(), str)
			exceptionInstance = exception([exception.__class__, "Exception raised!"])
			self.assertIsInstance(exceptionInstance.__str__(), str)
			exceptionInstance = exception(0)
			self.assertIsInstance(exceptionInstance.__str__(), str)

class AttributeStructureParsingErrorTestCase(unittest.TestCase):
	"""
	Defines :class:`foundations.exceptions.AttributeStructureParsingError` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		Tests presence of required attributes.
		"""

		requiredAttributes = ("value", "line")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(foundations.exceptions.AttributeStructureParsingError))

if __name__ == "__main__":
	unittest.main()
