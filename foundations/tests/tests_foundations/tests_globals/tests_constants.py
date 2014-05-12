#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_constants.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.globals.constants` module.

**Others:**

"""

from __future__ import unicode_literals

import sys

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest

from foundations.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestConstants"]


class TestConstants(unittest.TestCase):
    """
    Defines :class:`foundations.globals.constants.Constants` class units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("application_name",
                               "major_version",
                               "minor_version",
                               "change_version",
                               "version",
                               "logger",
                               "verbosity_level",
                               "verbosity_labels",
                               "logging_default_formatter",
                               "logging_separators",
                               "default_codec",
                               "codec_error",
                               "application_directory",
                               "provider_directory",
                               "null_object")

        for attribute in required_attributes:
            self.assertIn(attribute, Constants.__dict__)

    def test_application_name_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.application_name` attribute.
        """

        self.assertRegexpMatches(Constants.application_name, "\w+")

    def test_major_version_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.major_version` attribute.
        """

        self.assertRegexpMatches(Constants.version, "\d")

    def test_minor_version_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.minor_version` attribute.
        """

        self.assertRegexpMatches(Constants.version, "\d")

    def test_change_version_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.change_version` attribute.
        """

        self.assertRegexpMatches(Constants.version, "\d")

    def test_version_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.version` attribute.
        """

        self.assertRegexpMatches(Constants.version, "\d\.\d\.\d")

    def test_logger_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.logger` attribute.
        """

        self.assertRegexpMatches(Constants.logger, "\w+")

    def test_verbosity_level_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.verbosity_level` attribute.
        """

        self.assertIsInstance(Constants.verbosity_level, int)
        self.assertGreaterEqual(Constants.verbosity_level, 0)
        self.assertLessEqual(Constants.verbosity_level, 4)

    def test_verbosity_labels_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.verbosity_labels` attribute.
        """

        self.assertIsInstance(Constants.verbosity_labels, tuple)
        for label in Constants.verbosity_labels:
            self.assertIsInstance(label, unicode)

    def test_logging_default_formatter_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.logging_default_formatter` attribute.
        """

        self.assertIsInstance(Constants.logging_default_formatter, unicode)

    def test_logging_separators_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.logging_separators` attribute.
        """

        self.assertIsInstance(Constants.logging_separators, unicode)

    def test_encoding_codec_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.default_codec` attribute.
        """

        valid_encodings = ("utf-8",
                           "cp1252")

        self.assertIn(Constants.default_codec, valid_encodings)

    def test_codec_error_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.codec_error` attribute.
        """

        valid_encodings_errors = ("strict",
                                  "ignore",
                                  "replace",
                                  "xmlcharrefreplace")

        self.assertIn(Constants.codec_error, valid_encodings_errors)

    def test_application_directory_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.application_directory` attribute.
        """

        self.assertRegexpMatches(Constants.application_directory, "\w+")

    def test_provider_directory_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.provider_directory` attribute.
        """

        self.assertRegexpMatches(Constants.provider_directory, "\.*\w")

    def test_null_object_attribute(self):
        """
        Tests :attr:`foundations.globals.constants.Constants.null_object` attribute.
        """

        self.assertRegexpMatches(Constants.null_object, "\w+")


if __name__ == "__main__":
    unittest.main()
