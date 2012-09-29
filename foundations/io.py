#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**io.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module provides file input / output objects and resources manipulation objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import shutil

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
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

__all__ = ["LOGGER", "File", "setDirectory", "copy", "remove"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class File(object):
	"""
	This class provides methods to read / write and append to files.
	"""

	def __init__(self, file=None, content=None):
		"""
		This method initializes the class.
		
		Usage::
		
			>>> file = File("file.txt")
			>>> file.content = ["Some file content ...\\n", "... ready to be saved!\\n"]
			>>> file.write()
			True
			>>> file.read()
			>>> file.content
			['Some file content ...\\n', '... ready to be saved!\\n']

		:param file: File path. ( String )
		:param content: Content. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__file = None
		self.file = file
		self.__content = None
		self.content = content or []

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def file(self):
		"""
		This method is the property for **self.__file** attribute.

		:return: self.__file. ( String )
		"""

		return self.__file

	@file.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def file(self, value):
		"""
		This method is the setter method for **self.__file** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("file", value)
		self.__file = value

	@file.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def file(self):
		"""
		This method is the deleter method for **self.__file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file"))

	@property
	def content(self):
		"""
		This method is the property for **self.__content** attribute.

		:return: self.__content. ( List )
		"""

		return self.__content

	@content.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def content(self, value):
		"""
		This method is the setter method for **self.__content** attribute.

		:param value: Attribute value. ( List )
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("content", value)
		self.__content = value

	@content.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def content(self):
		"""
		This method is the deleter method for **self.__content** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "content"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.exceptionsHandler(None, False, IOError)
	def read(self, mode="r"):
		"""
		This method reads given file content.

		:param mode: File read mode. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Current file path: '{0}'.".format(self.__file))
		LOGGER.debug("> Reading current file content.")

		with open(self.__file, mode) as file:
			self.__content = file.readlines()
			return True

	@foundations.exceptions.exceptionsHandler(None, False, IOError)
	def readAll(self):
		"""
		This method reads given file content and returns it.

		:param mode: File read mode. ( String )
		:return: File content. ( String )
		"""

		if self.read():
			return "".join(self.__content)

	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def write(self, mode="w"):
		"""
		This method writes content to given file.

		:param mode: File write mode. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Current file path: '{0}'.".format(self.__file))

		with open(self.__file, mode) as file:
			for line in self.__content:
				file.write(line)
			return True

	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def append(self, mode="a"):
		"""
		This method appends content to given file.

		:param mode: File write mode. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Current file path: '{0}'.".format(self.__file))

		with open(self.__file, mode) as file:
			for line in self.__content:
				file.write(line)
			return True

@foundations.exceptions.exceptionsHandler(None, False, OSError)
def setDirectory(path):
	"""
	| This definition creates a directory with given path.
	| The directory creation is delegated to
		Python :func:`os.makedirs` definition so that directories hierarchy is recursively created. 
	
	:param path: Directory path. ( String )
	:return: Definition success. ( Boolean )
	"""

	if not foundations.common.pathExists(path):
		LOGGER.debug("> Creating directory: '{0}'.".format(path))
		os.makedirs(path)
		return True
	else:
		LOGGER.debug("> '{0}' directory already exist, skipping creation!".format(path))
		return True

@foundations.exceptions.exceptionsHandler(None, False, OSError)
def copy(source, destination):
	"""
	This definition copies the given file or directory to destination.

	:param source: Source to copy from. ( String )
	:param destination: Destination to copy to. ( String )
	:return: Method success. ( Boolean )
	"""

	if os.path.isfile(source):
		LOGGER.debug("> Copying '{0}' file to '{1}'.".format(source, destination))
		shutil.copyfile(source, destination)
	else:
		LOGGER.debug("> Copying '{0}' directory to '{1}'.".format(source, destination))
		shutil.copytree(source, destination)
	return True

@foundations.exceptions.exceptionsHandler(None, False, OSError)
def remove(path):
	"""
	This definiton removes the given file or directory.

	:param path: Resource to remove. ( String )
	:return: Method success. ( Boolean )
	"""

	if os.path.isfile(path):
		LOGGER.debug("> Removing '{0}' file.".format(path))
		os.remove(path)
	elif os.path.isdir(path):
		LOGGER.debug("> Removing '{0}' directory.".format(path))
		shutil.rmtree(path)
	return True
