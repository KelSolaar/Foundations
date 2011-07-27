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
**walker.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Walker Module.

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
import re
import hashlib

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Walker(object):
	"""
	This class provides methods for walking in a directory.
	"""

	@core.executionTrace
	def __init__(self, root=None, hashSize=8):
		"""
		This method initializes the class.

		@param root: Root directory path to recurse. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__root = None
		self.root = root
		self.__hashSize = None
		self.hashSize = hashSize

		self.__files = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def root(self):
		"""
		This method is the property for the _root attribute.

		@return: self.__root. ( String )
		"""

		return self.__root

	@root.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def root(self, value):
		"""
		This method is the setter method for the _root attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("root", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' directory doesn't exists!".format("root", value)
		self.__root = value

	@root.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def root(self):
		"""
		This method is the deleter method for the _root attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("root"))

	@property
	def hashSize(self):
		"""
		This method is the property for the _hashSize attribute.

		@return: self.__hashSize. ( String )
		"""

		return self.__hashSize

	@hashSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hashSize(self, value):
		"""
		This method is the setter method for the _hashSize attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("hashSize", value)
		self.__hashSize = value

	@hashSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hashSize(self):
		"""
		This method is the deleter method for the _hashSize attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("hashSize"))

	@property
	def files(self):
		"""
		This method is the property for the _files attribute.

		@return: self.__files. ( Dictionary )
		"""

		return self.__files

	@files.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def files(self, value):
		"""
		This method is the setter method for the _files attribute.

		@param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("files", value)
		self.__files = value

	@files.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def files(self):
		"""
		This method is the deleter method for the _files attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("files"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler()
	def walk(self, filtersIn=None, filtersOut=None, flags=0, shorterHashKey=True):
		"""
		This method gets root directory files list as a dictionary.

		@param filtersIn: Regex filtersin list. ( List / tuple )
		@param filtersIn: Regex filtersout list. ( List / tuple )
		@param flags: Regex flags. ( Object )
		@return: Files list. ( Dictionary or none )
		"""

		if filtersIn:
			LOGGER.debug("> Current filtersin: '{0}'.".format(filtersIn))

		if self.__root:
				self.__files = {}
				for root, dirs, files in os.walk(self.__root, topdown=False, followlinks=True):
					for item in files:
						LOGGER.debug("> Current file: '{0}' in '{1}'.".format(item, self.__root))
						itemPath = strings.toForwardSlashes(os.path.join(root, item))
						if os.path.isfile(itemPath):
							if not strings.filterWords((itemPath,), filtersIn, filtersOut, flags):
								continue

							LOGGER.debug("> '{0}' file filtered in!".format(itemPath))

							hashKey = hashlib.md5(itemPath).hexdigest()
							itemName = namespace.setNamespace(os.path.splitext(item)[0], shorterHashKey and hashKey[:self.__hashSize] or hashKey)
							LOGGER.debug("> Adding '{0}' with path: '{1}' to files list.".format(itemName, itemPath))
							self.__files[itemName] = itemPath

				return self.__files

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
