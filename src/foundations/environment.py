#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**environment.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module provides environment variables manipulation objects.

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

__all__ = ["LOGGER", "Environment"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Environment(object):
	"""
	This class provides methods to manipulate environment variables.
	"""

	@core.executionTrace
	def __init__(self, *args, **kwargs):
		"""
		This method initializes the class.
		
		Usage::
			
			>>> environment = Environment(JOHN="DOE", DOE="JOHN")
			>>> environment.setValues()
			True
			>>> import os
			>>> os.environ["JOHN"]
			'DOE'
			>>> os.environ["DOE"]
			'JOHN'
		
		:param \*args: Variables. ( \* )
		:param \*\*kwargs: Variables : Values. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__variables = {}
		self.__addVariables(*args, **kwargs)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def variables(self):
		"""
		This method is the property for **self.__variables** attribute.

		:return: self.__variables. ( Dictionary )
		"""

		return self.__variables

	@variables.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def variables(self, value):
		"""
		This method is the setter method for **self.__variables** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("variables", value)
		self.__variables = value

	@variables.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def variables(self):
		"""
		This method is the deleter method for **self.__variables** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("variables"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __addVariables(self, *args, **kwargs):
		"""
		This method adds provided variables to __variables attribute.

		:param \*args: Variables. ( \* )
		:param \*\*kwargs: Variables : Values. ( \* )
		:return: Method success. ( Boolean )
		"""

		for variable in args:
			self.__variables[variable] = None
		self.__variables.update(kwargs)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getValues(self, *args):
		"""
		This method gets environment variables values.

		Usage::
			
			>>> environment = Environment("HOME")
			>>> environment.getValues()
			{'HOME': '/Users/JohnDoe'}
			>>> environment.getValues("USER")
			{'HOME': '/Users/JohnDoe', 'USER': 'JohnDoe'}

		:param \*args: Additional variables names to retrieve values from. ( \* )
		:return: Variables : Values. ( Dictionary )
		"""

		args and self.__addVariables(*args)

		LOGGER.debug("> Object environment variables: '{0}'.".format(",".join((key for key in self.__variables.keys() if key))))
		LOGGER.debug("> Available system environment variables: '{0}'".format(os.environ.keys()))

		for variable in self.__variables.keys():
			self.__variables[variable] = os.environ.get(variable, None)
		return self.__variables

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setValues(self, **kwargs):
		"""
		This method sets environment variables values.

		Usage::
			
			>>> environment = Environment()
			>>> environment.setValues(JOHN="DOE", DOE="JOHN")
			True
			>>> import os
			>>> os.environ["JOHN"]
			'DOE'
			>>> os.environ["DOE"]
			'JOHN'

		:param \*\*kwargs: Variables : Values. ( \* )
		:return: Method success. ( String )
		
		:note: Any variable with a **None** value will be skipped.
		"""

		self.__variables.update(kwargs)

		for key, value in self.__variables.items():
			if value is None:
				continue
			LOGGER.debug("> Setting environment variable '{0}' with value '{1}'.".format(key, value))
			os.environ[key] = value
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getValue(self, variable=None):
		"""
		This method gets provided environment variable value.

		:param variable: Variable to retrieve value. ( String )
		:return: Variable value. ( String )
		
		:note: If the **variable** argument is not provided the first **self.__variables** attribute value will be returned.
		"""

		if variable:
			self.getValues(variable)
			return self.__variables[variable]
		else:
			self.getValues()
			return self.__variables.values() and self.__variables.values()[0]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setValue(self, variable, value):
		"""
		This method sets provided environment variable with provided value.

		:param variable: Variable to set value. ( String )
		:param value: Variable value. ( String )
		:return: Method success. ( Boolean )
		"""

		return self.setValues(**{variable : value})
