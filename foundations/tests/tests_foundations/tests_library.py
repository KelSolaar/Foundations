#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**tests_library.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.library` module.

**Others:**

"""

from __future__ import unicode_literals

import ctypes
import os
import platform
import sys

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest

from foundations.library import Library
from foundations.library import LibraryHook

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
           "LIBRARIES_DIRECTORY",
           "FREEIMAGE_LIBRARY",
           "LIBRARIES",
           "LIBRARIES_FUNCTIONS",
           "LIBRARIES_TESTS_CASES",
           "TestLibrary"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
LIBRARIES_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "libraries")
if platform.system() == "Windows" or platform.system() == "Microsoft":
    FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeimage/FreeImage.dll")
elif platform.system() == "Darwin":
    FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeimage/libfreeimage.dylib")
elif platform.system() == "Linux":
    FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeimage/libfreeimage.so")

LIBRARIES = {"freeimage": os.path.normpath(os.path.join(os.path.dirname(__file__), FREEIMAGE_LIBRARY))}

LIBRARIES_FUNCTIONS = {"freeimage": (LibraryHook(name="FreeImage_GetVersion",
                                                 arguments_types=None,
                                                 return_value=ctypes.c_char_p),
                                     LibraryHook(name="FreeImage_GetCopyrightMessage",
                                                 arguments_types=None,
                                                 return_value=ctypes.c_char_p))}

LIBRARIES_TESTS_CASES = {"freeimage": {"FreeImage_GetVersion": "3.15.1",
                                       "FreeImage_GetCopyrightMessage": "This program uses FreeImage, a free, open source image library supporting all common bitmap formats. See http://freeimage.sourceforge.net for details"}}


class TestLibrary(unittest.TestCase):
    """
    Defines :class:`foundations.library.Library` class units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("callback",
                               "instances",
                               "initialized",
                               "path",
                               "functions",
                               "library")
        for attribute in required_attributes:
            self.assertIn(attribute, dir(Library))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ("bind_library",
                            "bind_function")

        for method in required_methods:
            self.assertIn(method, dir(Library))

    def test_bind_function(self):
        """
        Tests :meth:`foundations.library.Library.bind_function` method.
        """

        for name, path in LIBRARIES.iteritems():
            library = Library(path)
            library.functions = LIBRARIES_FUNCTIONS[name]
            for function in LIBRARIES_FUNCTIONS[name]:
                hasattr(library, function.name) and delattr(library, function.name)
                library.bind_function(function)
                self.assertTrue(hasattr(library, function.name))

    def test_bind_library(self):
        """
        Tests :meth:`foundations.library.Library.bind_library` method.
        """

        for name, path in LIBRARIES.iteritems():
            library = Library(path, bind_library=False)
            library.functions = LIBRARIES_FUNCTIONS[name]
            library.bind_library()
            for function in LIBRARIES_FUNCTIONS[name]:
                self.assertTrue(hasattr(library, function.name))

    def test_library(self):
        """
        Tests :class:`foundations.library.Library` class binding.
        """

        for name, path in LIBRARIES.iteritems():
            library = Library(path, LIBRARIES_FUNCTIONS[name])
            for function, value in LIBRARIES_TESTS_CASES[name].iteritems():
                self.assertEqual(getattr(library, function)(), value)


if __name__ == "__main__":
    import foundations.tests.utilities

    unittest.main()
