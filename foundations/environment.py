#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**environment.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Provides environment variables manipulation objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform
import tempfile

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"Environment"
		"getTemporaryDirectory",
		"getSystemApplicationDataDirectory",
		"getUserApplicationDataDirectory"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Environment(object):
	"""
	Defines methods to manipulate environment variables.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initializes the class.

		Usage::

			>>> environment = Environment(JOHN="DOE", DOE="JOHN")
			>>> environment.setValues()
			True
			>>> import os
			>>> os.environ["JOHN"]
			u'DOE'
			>>> os.environ["DOE"]
			u'JOHN'

		:param \*args: Variables.
		:type \*args: \*
		:param \*\*kwargs: Variables : Values.
		:type \*\*kwargs: \*
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
		Property for **self.__variables** attribute.

		:return: self.__variables.
		:rtype: dict
		"""

		return self.__variables

	@variables.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def variables(self, value):
		"""
		Setter for **self.__variables** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("variables", value)
			for key, element in value.iteritems():
				assert type(key) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"variables", key)
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"variables", element)
		self.__variables = value

	@variables.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def variables(self):
		"""
		Deleter for **self.__variables** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "variables"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __addVariables(self, *args, **kwargs):
		"""
		Adds given variables to __variables attribute.

		:param \*args: Variables.
		:type \*args: \*
		:param \*\*kwargs: Variables : Values.
		:type \*\*kwargs: \*
		"""

		for variable in args:
			self.__variables[variable] = None
		self.__variables.update(kwargs)

	def getValues(self, *args):
		"""
		Gets environment variables values.

		Usage::

			>>> environment = Environment("HOME")
			>>> environment.getValues()
			{'HOME': u'/Users/JohnDoe'}
			>>> environment.getValues("USER")
			{'HOME': u'/Users/JohnDoe', 'USER': u'JohnDoe'}

		:param \*args: Additional variables names to retrieve values from.
		:type \*args: \*
		:return: Variables : Values.
		:rtype: dict
		"""

		args and self.__addVariables(*args)

		LOGGER.debug("> Object environment variables: '{0}'.".format(
		",".join((key for key in self.__variables if key))))
		LOGGER.debug("> Available system environment variables: '{0}'".format(os.environ.keys()))

		for variable in self.__variables:
			value = os.environ.get(variable, None)
			self.__variables[variable] = foundations.strings.toString(value) if value else None
		return self.__variables

	def setValues(self, **kwargs):
		"""
		Sets environment variables values.

		Usage::

			>>> environment = Environment()
			>>> environment.setValues(JOHN="DOE", DOE="JOHN")
			True
			>>> import os
			>>> os.environ["JOHN"]
			'DOE'
			>>> os.environ["DOE"]
			'JOHN'

		:param \*\*kwargs: Variables : Values.
		:type \*\*kwargs: \*
		:return: Method success.
		:rtype: unicode

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
		Gets given environment variable value.

		:param variable: Variable to retrieve value.
		:type variable: unicode
		:return: Variable value.
		:rtype: unicode

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
		Sets given environment variable with given value.

		:param variable: Variable to set value.
		:type variable: unicode
		:param value: Variable value.
		:type value: unicode
		:return: Method success.
		:rtype: bool
		"""

		return self.setValues(**{variable : value})

def getTemporaryDirectory():
	"""
	Returns the system temporary directory.

	:return: System temporary directory.
	:rtype: unicode
	"""

	return foundations.strings.toString(tempfile.gettempdir())

def getSystemApplicationDataDirectory():
	"""
	Returns the system Application data directory.

	Examples directories::

		- 'C:\\Users\\$USER\\AppData\\Roaming' on Windows 7.
		- 'C:\\Documents and Settings\\$USER\\Application Data' on Windows XP.
		- '/Users/$USER/Library/Preferences' on Mac Os X.
		- '/home/$USER' on Linux.

	:return: User Application data directory.
	:rtype: unicode
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		environment = Environment("APPDATA")
		return environment.getValue()
	elif platform.system() == "Darwin":
		environment = Environment("HOME")
		return os.path.join(environment.getValue(), "Library", "Preferences")
	elif platform.system() == "Linux":
		environment = Environment("HOME")
		return environment.getValue()

def getUserApplicationDataDirectory():
	"""
	| Returns the user Application directory.
	| The difference between :func:`getUserApplicationDataDirectory`
		and :func:`getSystemApplicationDataDirectory` definitions is that :func:`getUserApplicationDataDirectory` definition
		will append :attr:`foundations.globals.constants.Constants.providerDirectory`
		and :attr:`foundations.globals.constants.Constants.applicationDirectory` attributes values to the path returned.
	| If the user Application directory is not available, the function will fallback to system temporary directory.
 
	Examples directories::

		- 'C:\\Users\\$USER\\AppData\\Roaming\\Provider\\Application' on Windows 7.
		- 'C:\\Documents and Settings\\$USER\\Application Data\\Provider\\Application' on Windows XP.
		- '/Users/$USER/Library/Preferences/Provider/Application' on Mac Os X.
		- '/home/$USER/.Provider/Application' on Linux.

	:return: User Application directory.
	:rtype: unicode
	"""

	systemApplicationDataDirectory = getSystemApplicationDataDirectory()
	if not foundations.common.pathExists(systemApplicationDataDirectory):
		LOGGER.error("!> Undefined or non existing system Application data directory, using 'HOME' directory as fallback!")
		systemApplicationDataDirectory = Environment("HOME").getValue()

	if not foundations.common.pathExists(systemApplicationDataDirectory):
		temporaryDirectory = getTemporaryDirectory()
		LOGGER.error("!> Undefined or non existing 'HOME' directory, using system temporary directory as fallback!")
		systemApplicationDataDirectory = temporaryDirectory

	return os.path.join(systemApplicationDataDirectory, Constants.providerDirectory, Constants.applicationDirectory)

