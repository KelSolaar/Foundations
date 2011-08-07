#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**io.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module provides file input / output manipulation objects.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class File(object):
	"""
	This class provides methods to read / write and append to files.
	"""

	@core.executionTrace
	def __init__(self, file=None, content=None):
		"""
		This method initializes the class.
		
		Usage::
		
			>>> file = File("file.txt")
			>>> file.content = ["Some file content ...\\n", "... ready to be saved!\\n"]
			>>> file.write()
			True
			>>> file.read()
			>>> print file.content
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

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("file", value)
		self.__file = value

	@file.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def file(self):
		"""
		This method is the deleter method for **self.__file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("file"))

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

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("content", value)
		self.__content = value

	@content.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def content(self):
		"""
		This method is the deleter method for **self.__content** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("content"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, IOError)
	def read(self, mode="r"):
		"""
		This method reads provided file and return the content as a list.

		:param mode: File read mode. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Current file path: '{0}'.".format(self.__file))
		LOGGER.debug("> Reading current file content.")

		with open(self.__file, mode) as file:
			self.__content = file.readlines()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def write(self, mode="w"):
		"""
		This method writes content to provided file.

		:param mode: File write mode. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Current file path: '{0}'.".format(self.__file))

		with open(self.__file, mode) as file:
			for line in self.__content:
				file.write(line)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def append(self, mode="a"):
		"""
		This method appends content to provided file.

		:param mode: File write mode. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Current file path: '{0}'.".format(self.__file))

		with open(self.__file, mode) as file:
			for line in self.__content:
				file.write(line)
			return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, OSError)
def setLocalDirectory(path):
	"""
	| This definition creates a directory with provided path.
	| The directory creation is delegated to Python :func:`os.makedirs` definition.
	| The provided directories hierarchy will be recursively created. 
	
	:param path: Directory path. ( String )
	:return: Definition success. ( Boolean )
	"""

	if not os.path.exists(path):
		LOGGER.debug("> Creating directory: '{0}'.".format(path))
		os.makedirs(path)
		return True
	else:
		LOGGER.debug("> '{0}' directory already exist, skipping creation!".format(path))
		return True
