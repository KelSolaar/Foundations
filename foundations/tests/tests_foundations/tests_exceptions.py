#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_exceptions.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.exceptions` module.

**Others:**

"""

from __future__ import unicode_literals

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

import foundations.exceptions

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["EXCEPTIONS"
           "TestGetInnerMostFrame",
           "TestExtractStack",
           "TestExtractArguments",
           "TestExtractLocals",
           "TestExtractException",
           "TestFormatException",
           "TestFormatReport",
           "TestInstallExceptionHandler",
           "TestUninstallExceptionHandler",
           "TestExceptions",
           "TestAttributeStructureParsingError"]

EXCEPTIONS = []


def _gather_exceptions():
    """
    Gathers the exceptions.
    """

    for attribute in dir(foundations.exceptions):
        object = getattr(foundations.exceptions, attribute)
        if not inspect.isclass(object):
            continue
        if issubclass(object, BaseException):
            EXCEPTIONS.append(object)


_gather_exceptions()


class TestGetInnerMostFrame(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.get_inner_most_frame` definition units tests methods.
    """

    def test_get_inner_most_frame(self):
        """
        Tests :func:`foundations.exceptions.get_inner_most_frame` definition.
        """

        try:
            raise Exception("This is a test exception!")
        except Exception as error:
            cls, instance, trcback = foundations.exceptions.extract_exception(error)
            self.assertIsInstance(foundations.exceptions.get_inner_most_frame(trcback), types.FrameType)
            self.assertEqual(foundations.exceptions.get_inner_most_frame(None), None)


class TestExtractStack(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.extract_stack` definition units tests methods.
    """

    def test_extract_stack(self):
        """
        Tests :func:`foundations.exceptions.extract_stack` definition.
        """

        try:
            raise Exception("This is a test exception!")
        except Exception as error:
            cls, instance, trcback = foundations.exceptions.extract_exception(error)
            stack = foundations.exceptions.extract_stack(foundations.exceptions.get_inner_most_frame(trcback))
            self.assertIsInstance(stack, list)
            for frame, file_name, line_number, name, context, index in stack:
                self.assertIsInstance(frame, types.FrameType)
                self.assertIsInstance(file_name, unicode)
                self.assertIsInstance(line_number, int)
                self.assertIsInstance(name, unicode)
                self.assertIsInstance(context, list)
                self.assertIsInstance(index, int)


class TestExtractArguments(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.extract_arguments` definition units tests methods.
    """

    def test_extract_arguments(self, test_argument="My Value!", *args, **kwargs):
        """
        Tests :func:`foundations.exceptions.extract_arguments` definition.

        :param test_argument: Test argument.
        :type test_argument: unicode
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        try:
            raise Exception("This is a test exception!")
        except Exception as error:
            cls, instance, trcback = foundations.exceptions.extract_exception(error)
            arguments, nameless_args, keyword_args = \
                foundations.exceptions.extract_arguments(foundations.exceptions.get_inner_most_frame(trcback))

            self.assertListEqual(arguments, ["self", "test_argument"])
            self.assertEqual(nameless_args, "args")
            self.assertEqual(keyword_args, "kwargs")


class TestExtractLocals(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.extract_locals` definition units tests methods.
    """

    def test_extract_locals(self, test_argument="My Value!", *args, **kwargs):
        """
        Tests :func:`foundations.exceptions.extract_locals` definition.

        :param test_argument: Test argument.
        :type test_argument: unicode
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        try:
            raise Exception("This is a test exception!")
        except Exception as error:
            cls, instance, trcback = foundations.exceptions.extract_exception(error)
            extractedLocals = foundations.exceptions.extract_locals(trcback)
            self.assertIsInstance(extractedLocals, list)
            for frame, locals in extractedLocals:
                self.assertIsInstance(frame, tuple)
                self.assertIsInstance(frame[0], unicode)
                self.assertIsInstance(frame[1], unicode)
                self.assertIsInstance(frame[2], int)

                arguments, nameless_args, keyword_args, locals = locals
                self.assertIsInstance(arguments, OrderedDict)
                self.assertIsInstance(nameless_args, list)
                self.assertIsInstance(keyword_args, dict)
                self.assertIsInstance(locals, dict)


class TestExtractException(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.extract_exception` definition units tests methods.
    """

    def test_extract_exception(self):
        """
        Tests :func:`foundations.exceptions.extract_exception` definition.
        """

        try:
            raise Exception("This is a test exception!")
        except Exception as error:
            cls, instance, trcback = foundations.exceptions.extract_exception(error)
            self.assertEqual(cls, Exception)
            self.assertIsInstance(instance, Exception)
            self.assertIsInstance(trcback, types.TracebackType)
            cls, instance, trcback = foundations.exceptions.extract_exception(*sys.exc_info())
            self.assertEqual(cls, Exception)
            self.assertIsInstance(instance, Exception)
            self.assertIsInstance(trcback, types.TracebackType)


class TestFormatException(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.format_exception` definition units tests methods.
    """

    def test_format_exception(self):
        """
        Tests :func:`foundations.exceptions.format_exception` definition.
        """

        try:
            raise Exception("This is a test exception!")
        except Exception as error:
            output = foundations.exceptions.format_exception(*sys.exc_info())
            self.assertIsInstance(output, list)
            for line in output:
                self.assertIsInstance(line, unicode)


class TestFormatReport(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.format_report` definition units tests methods.
    """

    def test_format_report(self):
        """
        Tests :func:`foundations.exceptions.format_report` definition.
        """

        try:
            raise Exception("This is a test exception!")
        except Exception as error:
            header, frames, trcback = foundations.exceptions.format_report(*sys.exc_info())
            self.assertIsInstance(header, list)
            self.assertIsInstance(frames, list)
            self.assertIsInstance(trcback, list)
            for line in itertools.chain(header, frames, trcback):
                self.assertIsInstance(line, unicode)


class TestInstallExceptionHandler(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.install_exception_handler` definition units tests methods.
    """

    def test_install_exception_handler(self):
        """
        Tests :func:`foundations.exceptions.install_exception_handler` definition.
        """

        except_hook = sys.excepthook
        self.assertTrue(foundations.exceptions.install_exception_handler())
        self.assertNotEqual(sys.excepthook, except_hook)
        foundations.exceptions.uninstall_exception_handler()


class TestUninstallExceptionHandler(unittest.TestCase):
    """
    Defines :func:`foundations.exceptions.uninstall_exception_handler` definition units tests methods.
    """

    def test_uninstall_exception_handler(self):
        """
        Tests :func:`foundations.exceptions.uninstall_exception_handler` definition.
        """

        except_hook = sys.excepthook
        foundations.exceptions.install_exception_handler()
        self.assertTrue(foundations.exceptions.uninstall_exception_handler())
        self.assertEqual(sys.excepthook, except_hook)


class TestExceptions(unittest.TestCase):
    """
    Defines :mod:`foundations.exceptions` module exceptions classes units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("value",)
        for exception in EXCEPTIONS:
            exception_instance = exception(None)
            for attribute in required_attributes:
                self.assertIn(attribute, dir(exception_instance))

    def test__str__(self):
        """
        Tests exceptions classes **__str__** method.
        """

        for exception in EXCEPTIONS:
            exception_instance = exception("{0} Exception raised!".format(exception.__class__))
            self.assertIsInstance(exception_instance.__str__(), str)
            exception_instance = exception([exception.__class__, "Exception raised!"])
            self.assertIsInstance(exception_instance.__str__(), str)
            exception_instance = exception(0)
            self.assertIsInstance(exception_instance.__str__(), str)


class TestAttributeStructureParsingError(unittest.TestCase):
    """
    Defines :class:`foundations.exceptions.AttributeStructureParsingError` class units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("value", "line")

        for attribute in required_attributes:
            self.assertIn(attribute, dir(foundations.exceptions.AttributeStructureParsingError))


if __name__ == "__main__":
    unittest.main()
