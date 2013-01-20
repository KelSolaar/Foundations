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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.verbose
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"getSystemApplicationDataDirectory",
			"getUserApplicationDataDirectory",
			"Environment"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Environment(object):
	"""
	This class provides methods to manipulate environment variables.
	"""

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

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def variables(self):
		"""
		This method is the property for **self.__variables** attribute.

		:return: self.__variables. ( Dictionary )
		"""

		return self.__variables

	@variables.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def variables(self, value):
		"""
		This method is the setter method for **self.__variables** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("variables", value)
			for key, element in value.iteritems():
				assert type(key) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"variables", key)
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"variables", element)
		self.__variables = value

	@variables.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def variables(self):
		"""
		This method is the deleter method for **self.__variables** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "variables"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __addVariables(self, *args, **kwargs):
		"""
		This method adds given variables to __variables attribute.

		:param \*args: Variables. ( \* )
		:param \*\*kwargs: Variables : Values. ( \* )
		"""

		for variable in args:
			self.__variables[variable] = None
		self.__variables.update(kwargs)

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

		LOGGER.debug("> Object environment variables: '{0}'.".format(
		",".join((key for key in self.__variables if key))))
		LOGGER.debug("> Available system environment variables: '{0}'".format(os.environ.keys()))

		for variable in self.__variables:
			self.__variables[variable] = os.environ.get(variable, None)
		return self.__variables

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

		for key, value in self.__variables.iteritems():
			if value is None:
				continue
			LOGGER.debug("> Setting environment variable '{0}' with value '{1}'.".format(key, value))
			os.environ[key] = value
		return True

	def getValue(self, variable=None):
		"""
		This method gets given environment variable value.

		:param variable: Variable to retrieve value. ( String )
		:return: Variable value. ( String )
		
		:note: If the **variable** argument is not given the first **self.__variables** attribute value will be returned.
		"""

		if variable:
			self.getValues(variable)
			return self.__variables[variable]
		else:
			self.getValues()
			return foundations.common.getFirstItem(self.__variables.values())

	def setValue(self, variable, value):
		"""
		This method sets given environment variable with given value.

		:param variable: Variable to set value. ( String )
		:param value: Variable value. ( String )
		:return: Method success. ( Boolean )
		"""

		return self.setValues(**{variable : value})

def getSystemApplicationDataDirectory():
	"""
	This definition returns the system Application data directory.
	
	Examples directories::

		- 'C:\Users\$USER\AppData\Roaming' on Windows 7.
		- 'C:\Documents and Settings\$USER\Application Data' on Windows XP.
		- '/Users/$USER/Library/Preferences' on Mac Os X.
		- '/home/$USER' on Linux.

	:return: User Application data directory. ( String )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		environmentVariable = Environment("APPDATA")
		return environmentVariable.getValue()

	elif platform.system() == "Darwin":
		environmentVariable = Environment("HOME")
		return os.path.join(environmentVariable.getValue(), "Library/Preferences")

	elif platform.system() == "Linux":
		environmentVariable = Environment("HOME")
		return environmentVariable.getValue()

def getUserApplicationDataDirectory():
	"""
	| This definition returns the user Application directory.
	| The difference between :func:`getSystemApplicationDataDirectory`
		and :func:`getSystemApplicationDataDirectory` definitions is that :func:`getUserApplicationDataDirectory` definition
		will append :attr:`foundations.globals.constants.Constants.providerDirectory`
		and :attr:`foundations.globals.constants.Constants.applicationDirectory` attributes values to the path returned.

	Examples directories::

		- 'C:\Users\$USER\AppData\Roaming\Provider\Application' on Windows 7.
		- 'C:\Documents and Settings\$USER\Application Data\Provider\Application' on Windows XP.
		- '/Users/$USER/Library/Preferences/Provider/Application' on Mac Os X.
		- '/home/$USER/.Provider/Application' on Linux.

	:return: User Application directory. ( String )
	"""

	return os.path.join(getSystemApplicationDataDirectory(), Constants.providerDirectory, Constants.applicationDirectory)

