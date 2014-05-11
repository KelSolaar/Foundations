#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**tests_io.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.io` module.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
import shutil
import stat
import sys
import tempfile

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest

import foundations.io
from foundations.io import File

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
           "LIBRARIES_DIRECTORY",
           "LIBRARY",
           "TEXT_FILE",
           "FILE_CONTENT",
           "TestFile",
           "TestSetDirectory",
           "TestCopy",
           "TestRemove",
           "TestIsReadable",
           "TestIsWritable",
           "TestIsBinaryFile"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
LIBRARIES_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "libraries")
if platform.system() == "Windows" or platform.system() == "Microsoft":
    LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeimage/FreeImage.dll")
elif platform.system() == "Darwin":
    LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeimage/libfreeimage.dylib")
elif platform.system() == "Linux":
    LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeimage/libfreeimage.so")
TEXT_FILE = os.path.join(RESOURCES_DIRECTORY, "lorem_ipsum.txt")
FILE_CONTENT = [
    "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n",
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n",
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"]


class TestFile(unittest.TestCase):
    """
    Defines :class:`foundations.io.File` class units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("path",
                               "content")

        for attribute in required_attributes:
            self.assertIn(attribute, dir(File))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ("cache",
                            "uncache",
                            "read",
                            "write",
                            "append",
                            "clear")

        for method in required_methods:
            self.assertIn(method, dir(File))

    def test_cache(self):
        """
        Tests :meth:`foundations.io.File.cache` method.
        """

        io_file = File(TEXT_FILE)
        self.assertIsInstance(io_file.content, list)
        cache_success = io_file.cache()
        self.assertTrue(cache_success)
        self.assertIsInstance(io_file.content, list)
        self.assertListEqual(io_file.content, FILE_CONTENT)

    def test_uncache(self):
        """
        Tests :meth:`foundations.io.File.uncache` method.
        """

        io_file = File(TEXT_FILE)
        io_file.cache()
        self.assertListEqual(io_file.content, FILE_CONTENT)
        io_file.uncache()
        self.assertListEqual(io_file.content, [])

    def test_read(self):
        """
        Tests :meth:`foundations.io.File.read` method.
        """

        io_file = File(TEXT_FILE)
        self.assertIsInstance(io_file.content, list)
        content = io_file.read()
        self.assertIsInstance(io_file.content, list)
        self.assertEqual(content, "".join(FILE_CONTENT))

    def test_write(self):
        """
        Tests :meth:`foundations.io.File.write` method.
        """

        file_descriptor, path = tempfile.mkstemp()
        io_file = File(unicode(path))
        self.assertIsInstance(io_file.content, list)
        io_file.content = FILE_CONTENT
        write_success = io_file.write()
        self.assertTrue(write_success)
        io_file.cache()
        self.assertListEqual(io_file.content, FILE_CONTENT)
        os.close(file_descriptor)

    def test_append(self):
        """
        Tests :meth:`foundations.io.File.append` method.
        """

        file_descriptor, path = tempfile.mkstemp()
        io_file = File(unicode(path))
        self.assertIsInstance(io_file.content, list)
        io_file.content = FILE_CONTENT
        io_file.write()
        append = io_file.append()
        self.assertTrue(append)
        io_file.cache()
        self.assertListEqual(io_file.content, FILE_CONTENT + FILE_CONTENT)
        os.close(file_descriptor)

    def test_clear(self):
        """
        Tests :meth:`foundations.io.File.clear` method.
        """

        file_descriptor, path = tempfile.mkstemp()
        io_file = File(unicode(path))
        self.assertIsInstance(io_file.content, list)
        io_file.content = FILE_CONTENT
        io_file.write()
        self.assertTrue(io_file.clear())
        io_file.cache()
        self.assertListEqual(io_file.content, [])
        os.close(file_descriptor)


class TestSetDirectory(unittest.TestCase):
    """
    Defines :func:`foundations.io.set_directory` definition units tests methods.
    """

    def test_set_directory(self):
        """
        Tests :func:`foundations.io.set_directory` definition.
        """

        temp_directory = tempfile.mkdtemp()
        directories_tree = "tests/io/set_directory"
        directory = os.path.join(temp_directory, directories_tree)
        foundations.io.set_directory(directory)
        self.assertTrue(os.path.exists(directory))
        shutil.rmtree(temp_directory)


class TestCopy(unittest.TestCase):
    """
    Defines :func:`foundations.io.copy` definition units tests methods.
    """

    def test_copy(self):
        """
        Tests :func:`foundations.io.copy` definition.
        """

        temp_directory = tempfile.mkdtemp()
        destination = os.path.join(temp_directory, os.path.basename(TEXT_FILE))
        foundations.io.copy(TEXT_FILE, destination)
        self.assertTrue(os.path.exists(destination))
        shutil.rmtree(temp_directory)


class TestRemove(unittest.TestCase):
    """
    Defines :func:`foundations.io.remove` definition units tests methods.
    """

    def test_remove(self):
        """
        Tests :func:`foundations.io.remove` definition.
        """

        temp_directory = tempfile.mkdtemp()
        destination = os.path.join(temp_directory, os.path.basename(TEXT_FILE))
        foundations.io.copy(TEXT_FILE, destination)
        foundations.io.remove(destination)
        self.assertTrue(not os.path.exists(destination))
        shutil.rmtree(temp_directory)


class TestIsReadable(unittest.TestCase):
    """
    Defines :func:`foundations.io.is_readable` definition units tests methods.
    """

    def test_is_readable(self):
        """
        Tests :func:`foundations.io.is_readable` definition.
        """

        temp_directory = tempfile.mkdtemp()
        self.assertTrue(foundations.io.is_readable(temp_directory))
        os.chmod(temp_directory, stat.S_IROTH)
        self.assertFalse(foundations.io.is_readable(temp_directory))
        os.chmod(temp_directory, stat.S_IREAD)
        shutil.rmtree(temp_directory)


class TestIsWritable(unittest.TestCase):
    """
    Defines :func:`foundations.io.is_writable` definition units tests methods.
    """

    def test_is_writable(self):
        """
        Tests :func:`foundations.io.is_writable` definition.
        """

        temp_directory = tempfile.mkdtemp()
        self.assertTrue(foundations.io.is_writable(temp_directory))
        os.chmod(temp_directory, stat.S_IREAD)
        self.assertFalse(foundations.io.is_writable(temp_directory))
        shutil.rmtree(temp_directory)


class TestIsBinaryFile(unittest.TestCase):
    """
    Defines :func:`foundations.io.is_binary_file` definition units tests methods.
    """

    def test_is_binary_file(self):
        """
        Tests :func:`foundations.io.is_binary_file` definition.
        """

        self.assertTrue(foundations.io.is_binary_file(LIBRARY))
        self.assertFalse(foundations.io.is_binary_file(TEXT_FILE))


if __name__ == "__main__":
    import foundations.tests.utilities

    unittest.main()
