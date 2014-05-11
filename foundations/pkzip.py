#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**pkzip.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Provides archives files manipulation objects.

**Others:**

"""

from __future__ import unicode_literals

from cStringIO import StringIO
import os
import zipfile

import foundations.io
import foundations.exceptions
import foundations.verbose

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Pkzip"]

LOGGER = foundations.verbose.install_logger()

class Pkzip(object):
    """
    Defines methods to manipulate zip files.
    """

    def __init__(self, archive=None):
        """
        Initializes the class.

        Usage::

            >>> import tempfile
            >>> temp_directory = tempfile.mkdtemp()
            >>> zip_file = Pkzip("zip_file.zip")
            >>> zip_file.extract(temp_directory)
            True

        :param archive: Archive to manipulate.
        :type archive: unicode
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        # --- Setting class attributes. ---
        self.__archive = None
        self.archive = archive

    @property
    def archive(self):
        """
        Property for **self.__archive** attribute.

        :return: self.__archive.
        :rtype: unicode
        """

        return self.__archive

    @archive.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def archive(self, value):
        """
        Setter for **self.__archive** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                "archive", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("archive", value)
        self.__archive = value

    @archive.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def archive(self):
        """
        Deleter for **self.__archive** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "archive"))

    @foundations.exceptions.handle_exceptions(foundations.exceptions.DirectoryExistsError,
                                             foundations.exceptions.FileExistsError,
                                             zipfile.BadZipfile)
    def extract(self, target):
        """
        Extracts the archive file to given directory.

        :param target: Target extraction directory.
        :type target: unicode
        :return: Method success.
        :rtype: bool
        """

        if not foundations.common.path_exists(self.__archive):
            raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
                self.__class__.__name__, self.__archive))

        if not foundations.common.path_exists(target):
            raise foundations.exceptions.DirectoryExistsError("{0} | '{1}' directory doesn't exists!".format(
                self.__class__.__name__, target))

        archive = zipfile.ZipFile(self.__archive)
        content = archive.namelist()

        directories = [item for item in content if item.endswith("/")]
        files = [item for item in content if not item.endswith("/")]

        directories.sort()
        directories.reverse()

        for directory in directories:
            not os.path.isdir(os.path.join(target, directory)) and foundations.io.set_directory(
                os.path.join(target, directory))

        for file in files:
            LOGGER.info("{0} | Extracting '{1}' file!".format(self.__class__.__name__, file))
            with open(os.path.join(target, file), "w") as output:
                buffer = StringIO(archive.read(file))
                bufferSize = 2 ** 20
                data = buffer.read(bufferSize)
                while data:
                    output.write(data)
                    data = buffer.read(bufferSize)
        return True
