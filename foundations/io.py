#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**io.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Provides file input / output objects and resources manipulation objects.

**Others:**

"""

from __future__ import unicode_literals

import codecs
import os
import shutil
import urllib2

import foundations.common
import foundations.verbose
import foundations.exceptions
import foundations.strings
from foundations.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "File", "set_directory", "copy", "remove", "is_writable", "is_readable", "is_binary_file"]

LOGGER = foundations.verbose.install_logger()

class File(object):
	"""
	Defines methods to read / write and append to files or retrieve online file content.
	"""

	def __init__(self, path=None, content=None):
		"""
		Initializes the class.

		Usage::

			>>> file = File(u"file.txt")
			>>> file.content = [u"Some file content ...\\n", u"... ready to be saved!\\n"]
			>>> file.write()
			True
			>>> file.read()
			u'Some file content ...\\n... ready to be saved!\\n'

		:param path: File path.
		:type path: unicode
		:param content: Content.
		:type content: list
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__path = None
		self.path = path
		self.__content = None
		self.content = content or []

	@property
	def path(self):
		"""
		Property for **self.__path** attribute.

		:return: self.__path.
		:rtype: unicode
		"""

		return self.__path

	@path.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def path(self, value):
		"""
		Setter for **self.__path** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("path", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		Deleter for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

	@property
	def content(self):
		"""
		Property for **self.__content** attribute.

		:return: self.__content.
		:rtype: list
		"""

		return self.__content

	@content.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def content(self, value):
		"""
		Setter for **self.__content** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("content", value)
		self.__content = value

	@content.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def content(self):
		"""
		Deleter for **self.__content** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "content"))

	@foundations.exceptions.handle_exceptions(foundations.exceptions.UrlReadError,
											 foundations.exceptions.FileReadError,
											 IOError)
	def cache(self, mode="r", encoding=Constants.default_codec, errors=Constants.codec_error):
		"""
		Reads given file content and stores it in the content cache.

		:param mode: File read mode.
		:type mode: unicode
		:param encoding: File encoding codec.
		:type encoding: unicode
		:param errors: File encoding errors handling.
		:type errors: unicode
		:return: Method success.
		:rtype: bool
		"""

		self.uncache()

		if foundations.strings.is_website(self.__path):
			try:
				LOGGER.debug("> Caching '{0}' online file content.".format(self.__path))
				self.__content = urllib2.urlopen(self.__path).readlines()
				return True
			except urllib2.URLError as error:
				raise foundations.exceptions.UrlReadError(
					"!> {0} | '{1}' url is not readable: '{2}'.".format(self.__class__.__name__, self.__path, error))
		elif foundations.common.path_exists(self.__path):
			if not is_readable(self.__path):
				raise foundations.exceptions.FileReadError(
					"!> {0} | '{1}' file is not readable!".format(self.__class__.__name__, self.__path))

			with codecs.open(self.__path, mode, encoding, errors) as file:
				LOGGER.debug("> Caching '{0}' file content.".format(self.__path))
				self.__content = file.readlines()
				return True
		return False

	def uncache(self):
		"""
		Uncaches the cached content.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uncaching '{0}' file content.".format(self.__path))

		self.__content = []
		return True

	def read(self):
		"""
		Returns defined file content.

		:return: File content.
		:rtype: unicode
		"""

		return "".join(self.__content) if self.cache() else ""

	@foundations.exceptions.handle_exceptions(foundations.exceptions.UrlWriteError, foundations.exceptions.FileWriteError)
	def write(self, mode="w", encoding=Constants.default_codec, errors=Constants.codec_error):
		"""
		Writes content to defined file.

		:param mode: File write mode.
		:type mode: unicode
		:param encoding: File encoding codec.
		:type encoding: unicode
		:param errors: File encoding errors handling.
		:type errors: unicode
		:return: Method success.
		:rtype: bool
		"""

		if foundations.strings.is_website(self.__path):
			raise foundations.exceptions.UrlWriteError(
					"!> {0} | '{1}' url is not writable!".format(self.__class__.__name__, self.__path))

		if foundations.common.path_exists(self.__path):
			if not is_writable(self.__path):
				raise foundations.exceptions.FileWriteError(
					"!> {0} | '{1}' file is not writable!".format(self.__class__.__name__, self.__path))

		with codecs.open(self.__path, mode, encoding, errors) as file:
			LOGGER.debug("> Writing '{0}' file content.".format(self.__path))
			for line in self.__content:
				file.write(line)
			return True
		return False

	@foundations.exceptions.handle_exceptions(foundations.exceptions.UrlWriteError, foundations.exceptions.FileWriteError)
	def append(self, mode="a", encoding=Constants.default_codec, errors=Constants.codec_error):
		"""
		Appends content to defined file.

		:param mode: File write mode.
		:type mode: unicode
		:param encoding: File encoding codec.
		:type encoding: unicode
		:param errors: File encoding errors handling.
		:type errors: unicode
		:return: Method success.
		:rtype: bool
		"""

		if foundations.strings.is_website(self.__path):
			raise foundations.exceptions.UrlWriteError(
					"!> {0} | '{1}' url is not writable!".format(self.__class__.__name__, self.__path))

		if foundations.common.path_exists(self.__path):
			if not is_writable(self.__path):
				raise foundations.exceptions.FileWriteError(
					"!> {0} | '{1}' file is not writable!".format(self.__class__.__name__, self.__path))

		with codecs.open(self.__path, mode, encoding, errors) as file:
			LOGGER.debug("> Appending to '{0}' file content.".format(self.__path))
			for line in self.__content:
				file.write(line)
			return True
		return False

	@foundations.exceptions.handle_exceptions(foundations.exceptions.UrlWriteError)
	def clear(self, encoding=Constants.default_codec):
		"""
		Clears the defined file content.

		:param encoding: File encoding codec.
		:type encoding: unicode
		:return: Method success.
		:rtype: bool
		"""

		if foundations.strings.is_website(self.__path):
			raise foundations.exceptions.UrlWriteError(
					"!> {0} | '{1}' url is not writable!".format(self.__class__.__name__, self.__path))

		if self.uncache():
			LOGGER.debug("> Clearing '{0}' file content.".format(self.__path))
			return self.write(encoding=encoding)
		else:
			return False

@foundations.exceptions.handle_exceptions(foundations.exceptions.DirectoryCreationError)
def set_directory(path):
	"""
	| Creates a directory with given path.
	| The directory creation is delegated to
		Python :func:`os.makedirs` definition so that directories hierarchy is recursively created.

	:param path: Directory path.
	:type path: unicode
	:return: Definition success.
	:rtype: bool
	"""

	try:
		if not foundations.common.path_exists(path):
			LOGGER.debug("> Creating directory: '{0}'.".format(path))
			os.makedirs(path)
			return True
		else:
			LOGGER.debug("> '{0}' directory already exist, skipping creation!".format(path))
			return True
	except Exception as error:
		raise foundations.exceptions.DirectoryCreationError("!> {0} | Cannot create '{1}' directory: '{2}'".format(__name__, path, error))

@foundations.exceptions.handle_exceptions(foundations.exceptions.PathCopyError)
def copy(source, destination):
	"""
	Copies given file or directory to destination.

	:param source: Source to copy from.
	:type source: unicode
	:param destination: Destination to copy to.
	:type destination: unicode
	:return: Method success.
	:rtype: bool
	"""

	try:
		if os.path.isfile(source):
			LOGGER.debug("> Copying '{0}' file to '{1}'.".format(source, destination))
			shutil.copyfile(source, destination)
		else:
			LOGGER.debug("> Copying '{0}' directory to '{1}'.".format(source, destination))
			shutil.copytree(source, destination)
		return True
	except Exception as error:
		raise foundations.exceptions.PathCopyError("!> {0} | Cannot copy '{1}' path: '{2}'".format(__name__, source, error))

@foundations.exceptions.handle_exceptions(foundations.exceptions.PathRemoveError)
def remove(path):
	"""
	Removes given path.

	:param path: Path to remove.
	:type path: unicode
	:return: Method success.
	:rtype: bool
	"""

	try:
		if os.path.isfile(path):
			LOGGER.debug("> Removing '{0}' file.".format(path))
			os.remove(path)
		elif os.path.isdir(path):
			LOGGER.debug("> Removing '{0}' directory.".format(path))
			shutil.rmtree(path)
		return True
	except Exception as error:
		raise foundations.exceptions.PathRemoveError("!> {0} | Cannot remove '{1}' path: '{2}'".format(__name__, path, error))

def is_readable(path):
	"""
	Returns if given path is readable.

	:param path: Path to check access.
	:type path: unicode
	:return: Is path writable.
	:rtype: bool
	"""

	if os.access(path, os.R_OK):
		LOGGER.debug("> '{0}' path is readable.".format(path))
		return True
	else:
		LOGGER.debug("> '{0}' path is not readable.".format(path))
		return False

def is_writable(path):
	"""
	Returns if given path is writable.

	:param path: Path to check access.
	:type path: unicode
	:return: Is path writable.
	:rtype: bool
	"""

	if os.access(path, os.W_OK):
		LOGGER.debug("> '{0}' path is writable.".format(path))
		return True
	else:
		LOGGER.debug("> '{0}' path is not writable.".format(path))
		return False

def is_binary_file(file):
	"""
	Returns if given file is a binary file.

	:param file: File path.
	:type file: unicode
	:return: Is file binary.
	:rtype: bool
	"""

	file_handle = open(file, "rb")
	try:
		chunk_size = 1024
		while True:
			chunk = file_handle.read(chunk_size)
			if chr(0) in chunk:
				return True
			if len(chunk) < chunk_size:
				break
	finally:
		file_handle.close()
	return False