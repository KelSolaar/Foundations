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
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Exceptions Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import traceback

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def exceptionsHandler(handler=None, raise_=False, *args):
	"""
	This decorator is used for exceptions handling.

	@param handler: Custom handler. ( Object )
	@param raise_: Is default exception handler catching / raising the exception. ( Boolean )
	@param *args: Exceptions. ( Exceptions )
	@return: Object. ( Object )
	"""

	exceptions = tuple((exception for exception in args))
	handler = handler or defaultExceptionsHandler

	def wrapper(object_):
		"""
		This decorator is used for exceptions handling.

		@param object_: Object to decorate. ( Object )
		@return: Object. ( Object )
		"""

		origin = core.getObjectName(object_)

		@functools.wraps(object_)
		def function(*args, **kwargs):
			"""
			This decorator is used for exceptions handling.

			@param *args: Arguments. ( * )
			@param **kwargs: Arguments. ( * )
			"""

			exception = None

			try:
				return object_(*args, **kwargs)
			except exceptions as exception:
				handler(exception , origin, *args, **kwargs)
			except Exception as exception:
				handler(exception , origin, *args, **kwargs)
			finally:
				if raise_ and exception:
					raise exception
		return function
	return wrapper

@core.executionTrace
def defaultExceptionsHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides an exception handler.

	@param exception: Exception. ( Exception )
	@param origin: Function / Method raising the exception. ( String )
	@param *args: Arguments. ( * )
	@param **kwargs: Arguments. ( * )
	"""

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))

	LOGGER.error("!> Exception in '{0}'.".format(origin))
	LOGGER.error("!> Exception class: '{0}'.".format(exception.__class__.__name__))
	LOGGER.error("!> Exception description: '{0}'.".format(exception.__doc__ and exception.__doc__.strip() or Constants.nullObject))
	LOGGER.error("!> Error raised: '{0}'.".format(exception))

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))

	traceback_ = traceback.format_exc().splitlines()
	if len(traceback_) > 1:
		for line in traceback_:
			LOGGER.error("!> {0}".format(line))

		LOGGER.error("!> {0}".format(Constants.loggingSeparators))

class FileStructureError(Exception):
	"""
	This class is used for file content structure errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class AttributeStructureError(Exception):
	"""
	This class is used for errors in attribute structure.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class DirectoryExistsError(Exception):
	"""
	This class is used for non existing directory.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))


		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class FileExistsError(Exception):
	"""
	This class is used for non existing file.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))


		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class ObjectTypeError(Exception):
	"""
	This class is used for invalid object type.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class ObjectExistsError(Exception):
	"""
	This class is used for non existing object.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class DatabaseOperationError(Exception):
	"""
	This class is used for Database operation errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class ProgrammingError(Exception):
	"""
	This class is used for programming errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class UserError(Exception):
	"""
	This class is used for user errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class NetworkError(Exception):
	"""
	This class is used for networkerror errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class SocketConnectionError(Exception):
	"""
	This class is used for socket connection errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class ComponentActivationError(Exception):
	"""
	This class is used for Component activation errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class ComponentDeactivationError(Exception):
	"""
	This class is used for Component deactivation errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class ComponentReloadError(Exception):
	"""
	This class is used for Component reload errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class LibraryInstantiationError(Exception):
	"""
	This class is used for Library instantiation errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class LibraryInitializationError(Exception):
	"""
	This class is used for Library initialization errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)

class LibraryExecutionError(Exception):
	"""
	This class is used for Library execution errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		@param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		@return: Exception representation. ( String )
		"""

		return str(self.value)
#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
