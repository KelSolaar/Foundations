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
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**io.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	IO Classes And Definitions Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class File(object):
	"""
	This Class Provides Methods To Read / Write Files.
	"""

	@core.executionTrace
	def __init__(self, file=None, content=None):
		"""
		This Method Initializes The Class.

		@param file: File Path. ( String )
		@param content: Content. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.__file = None
		self.file = file
		self.__content = None
		self.content = content or []

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def file(self):
		"""
		This Method Is The Property For The _file Attribute.

		@return: self.__file. ( String )
		"""

		return self.__file

	@file.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def file(self, value):
		"""
		This Method Is The Setter Method For The _file Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("file", value)
		self.__file = value

	@file.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def file(self):
		"""
		This Method Is The Deleter Method For The _file Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("file"))

	@property
	def content(self):
		"""
		This Method Is The Property For The _content Attribute.
		
		@return: self.__content. ( List )
		"""

		return self.__content

	@content.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def content(self, value):
		"""
		This Method Is The Setter Method For The _content Attribute.
		
		@param value: Attribute Value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' Attribute: '{1}' Type Is Not 'list'!".format("content", value)
		self.__content = value

	@content.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def content(self):
		"""
		This Method Is The Deleter Method For The _content Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("content"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, IOError)
	def read(self, mode="r"):
		"""
		This Method Reads Provided File And Return The Content As A List.

		@param mode: File Read Mode. ( String )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Current File Path: '{0}'.".format(self.__file))
		LOGGER.debug("> Reading Current File Content.")

		with open(self.__file, mode) as file:
			self.__content = file.readlines()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def write(self, mode="w"):
		"""
		This Method Writes Content To Provided File.
		
		@param mode: File Write Mode. ( String )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Current File Path: '{0}'.".format(self.__file))

		with open(self.__file, mode) as file:
			for line in self.__content:
				file.write(line)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def append(self, mode="a"):
		"""
		This Method Append Content To Provided File.
		
		@param mode: File Write Mode. ( String )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Current File Path: '{0}'.".format(self.__file))

		with open(self.__file, mode) as file:
			for line in self.__content:
				file.write(line)
			return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, OSError)
def setLocalDirectory(path):
	"""
	This Definition Creates A Directory With Provided Path.

	@param path: Directory Path. ( String )
	@return: Definition Success. ( Boolean )		
	"""

	if not os.path.exists(path):
		LOGGER.debug("> Creating Directory: '{0}'.".format(path))
		os.makedirs(path)
		return True
	else:
		LOGGER.debug("> '{0}' Directory Already Exist, Skipping Creation!".format(path))
		return True

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
