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

from __future__ import unicode_literals

import os
import platform
import tempfile

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
from foundations.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"Environment"
		"get_temporary_directory",
		"get_system_application_data_directory",
		"get_user_application_data_directory"]

LOGGER = foundations.verbose.install_logger()

class Environment(object):
	"""
	Defines methods to manipulate environment variables.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initializes the class.

		Usage::

			>>> environment = Environment(JOHN="DOE", DOE="JOHN")
			>>> environment.set_values()
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
		self.__add_variables(*args, **kwargs)

	@property
	def variables(self):
		"""
		Property for **self.__variables** attribute.

		:return: self.__variables.
		:rtype: dict
		"""

		return self.__variables

	@variables.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def variables(self):
		"""
		Deleter for **self.__variables** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "variables"))

	def __add_variables(self, *args, **kwargs):
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

	def get_values(self, *args):
		"""
		Gets environment variables values.

		Usage::

			>>> environment = Environment("HOME")
			>>> environment.get_values()
			{'HOME': u'/Users/JohnDoe'}
			>>> environment.get_values("USER")
			{'HOME': u'/Users/JohnDoe', 'USER': u'JohnDoe'}

		:param \*args: Additional variables names to retrieve values from.
		:type \*args: \*
		:return: Variables : Values.
		:rtype: dict
		"""

		args and self.__add_variables(*args)

		LOGGER.debug("> Object environment variables: '{0}'.".format(
		",".join((key for key in self.__variables if key))))
		LOGGER.debug("> Available system environment variables: '{0}'".format(os.environ.keys()))

		for variable in self.__variables:
			value = os.environ.get(variable, None)
			self.__variables[variable] = foundations.strings.to_string(value) if value else None
		return self.__variables

	def set_values(self, **kwargs):
		"""
		Sets environment variables values.

		Usage::

			>>> environment = Environment()
			>>> environment.set_values(JOHN="DOE", DOE="JOHN")
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

	def get_value(self, variable=None):
		"""
		Gets given environment variable value.

		:param variable: Variable to retrieve value.
		:type variable: unicode
		:return: Variable value.
		:rtype: unicode

		:note: If the **variable** argument is not given the first **self.__variables** attribute value will be returned.
		"""

		if variable:
			self.get_values(variable)
			return self.__variables[variable]
		else:
			self.get_values()
			return foundations.common.get_first_item(self.__variables.values())

	def set_value(self, variable, value):
		"""
		Sets given environment variable with given value.

		:param variable: Variable to set value.
		:type variable: unicode
		:param value: Variable value.
		:type value: unicode
		:return: Method success.
		:rtype: bool
		"""

		return self.set_values(**{variable : value})

def get_temporary_directory():
	"""
	Returns the system temporary directory.

	:return: System temporary directory.
	:rtype: unicode
	"""

	return foundations.strings.to_string(tempfile.gettempdir())

def get_system_application_data_directory():
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
		return environment.get_value()
	elif platform.system() == "Darwin":
		environment = Environment("HOME")
		return os.path.join(environment.get_value(), "Library", "Preferences")
	elif platform.system() == "Linux":
		environment = Environment("HOME")
		return environment.get_value()

def get_user_application_data_directory():
	"""
	| Returns the user Application directory.
	| The difference between :func:`get_user_application_data_directory`
		and :func:`get_system_application_data_directory` definitions is that :func:`get_user_application_data_directory` definition
		will append :attr:`foundations.globals.constants.Constants.provider_directory`
		and :attr:`foundations.globals.constants.Constants.application_directory` attributes values to the path returned.
	| If the user Application directory is not available, the function will fallback to system temporary directory.
 
	Examples directories::

		- 'C:\\Users\\$USER\\AppData\\Roaming\\Provider\\Application' on Windows 7.
		- 'C:\\Documents and Settings\\$USER\\Application Data\\Provider\\Application' on Windows XP.
		- '/Users/$USER/Library/Preferences/Provider/Application' on Mac Os X.
		- '/home/$USER/.Provider/Application' on Linux.

	:return: User Application directory.
	:rtype: unicode
	"""

	system_application_data_directory = get_system_application_data_directory()
	if not foundations.common.path_exists(system_application_data_directory):
		LOGGER.error("!> Undefined or non existing system Application data directory, using 'HOME' directory as fallback!")
		system_application_data_directory = Environment("HOME").get_value()

	if not foundations.common.path_exists(system_application_data_directory):
		temporary_directory = get_temporary_directory()
		LOGGER.error("!> Undefined or non existing 'HOME' directory, using system temporary directory as fallback!")
		system_application_data_directory = temporary_directory

	return os.path.join(system_application_data_directory, Constants.provider_directory, Constants.application_directory)

