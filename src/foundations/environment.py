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
**environment.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Environment Module.

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

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Environment(object):
	"""
	This class provides methods to manipulate environment variables.
	"""

	@core.executionTrace
	def __init__(self, variable=None):
		"""
		This method initializes the class.

		@param variable: Variable to manipulate. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__variable = None
		self.variable = variable

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def variable(self):
		"""
		This method is the property for the _variable attribute.

		@return: self.__variable. ( String )
		"""

		return self.__variable

	@variable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def variable(self, value):
		"""
		This method is the setter method for the _variable attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("variable", value)
			assert not re.search("\W", value), "'{0}' attribute: '{1}' contains non alphanumerics characters!".format("variable", value)
		self.__variable = value

	@variable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def variable(self):
		"""
		This method is the deleter method for the _variable attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("variable"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getPath(self):
		"""
		This method gets the chosen environment variable path as a string.

		@return: Variable path. ( String )
		"""

		if not self.__variable:
			return

		LOGGER.debug("> Current environment variable: '{0}'.".format(self.__variable))
		LOGGER.debug("> Available system environment variables: '{0}'".format(os.environ.keys()))

		if self.__variable in os.environ.keys():
			return os.environ[self.__variable]

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
