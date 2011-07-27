#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**io.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	IO classes and definitions Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class File(object):
	"""
	This class provides methods to read / write files.
	"""

	@core.executionTrace
	def __init__(self, file=None, content=None):
		"""
		This method initializes the class.

		@param file: File path. ( String )
		@param content: Content. ( List )
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
		This method is the property for the _file attribute.

		@return: self.__file. ( String )
		"""

		return self.__file

	@file.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def file(self, value):
		"""
		This method is the setter method for the _file attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("file", value)
		self.__file = value

	@file.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def file(self):
		"""
		This method is the deleter method for the _file attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("file"))

	@property
	def content(self):
		"""
		This method is the property for the _content attribute.

		@return: self.__content. ( List )
		"""

		return self.__content

	@content.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def content(self, value):
		"""
		This method is the setter method for the _content attribute.

		@param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("content", value)
		self.__content = value

	@content.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def content(self):
		"""
		This method is the deleter method for the _content attribute.
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

		@param mode: File read mode. ( String )
		@return: Method success. ( Boolean )
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

		@param mode: File write mode. ( String )
		@return: Method success. ( Boolean )
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
		This method append content to provided file.

		@param mode: File write mode. ( String )
		@return: Method success. ( Boolean )
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
	This definition creates a directory with provided path.

	@param path: Directory path. ( String )
	@return: Definition success. ( Boolean )
	"""

	if not os.path.exists(path):
		LOGGER.debug("> Creating directory: '{0}'.".format(path))
		os.makedirs(path)
		return True
	else:
		LOGGER.debug("> '{0}' directory already exist, skipping creation!".format(path))
		return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
