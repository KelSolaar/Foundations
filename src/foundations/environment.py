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
	This Class Provides Methods To Manipulate Environment Variables.
	"""

	@core.executionTrace
	def __init__(self, variable=None):
		"""
		This Method Initializes The Class.

		@param variable: Variable To Manipulate. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__variable = None
		self.variable = variable

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def variable(self):
		"""
		This Method Is The Property For The _variable Attribute.

		@return: self.__variable. ( String )
		"""

		return self.__variable

	@variable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def variable(self, value):
		"""
		This Method Is The Setter Method For The _variable Attribute.

		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("variable", value)
			assert not re.search("\W", value), "'{0}' Attribute: '{1}' Contains Non AlphaNumerics Characters!".format("variable", value)
		self.__variable = value

	@variable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def variable(self):
		"""
		This Method Is The Deleter Method For The _variable Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("variable"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getPath(self):
		"""
		This Method Gets The Chosen Environment Variable Path As A String.

		@return: Variable Path. ( String )
		"""

		if not self.__variable:
			return

		LOGGER.debug("> Current Environment Variable: '{0}'.".format(self.__variable))
		LOGGER.debug("> Available System Environment Variables: '{0}'".format(os.environ.keys()))

		if self.__variable in os.environ.keys():
			return os.environ[self.__variable]

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
