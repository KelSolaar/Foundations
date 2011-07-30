#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**environment.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Environment Module.

**Others:**

"""

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

