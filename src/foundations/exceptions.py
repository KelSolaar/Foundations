#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package exceptions and others exception handling related objects. 

**Others:**

"""

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
def exceptionsHandler(handler=None, raise_=False, *args):
	"""
	| This decorator is used for exceptions handling.
	| It's possible to specify an user defined exception handler, if not, :func:`foundations.exceptions.defaultExceptionsHandler` handler will be used.
	| The decorator uses provided exceptions objects or the default Python `Exception <http://docs.python.org/library/exceptions.html#exceptions.Exception>`_ class.
	
	Usage::
	
		@exceptionsHandler(None, False, ZeroDivisionError)
		def raiseAnException(value):
			'''
			This definition raises a 'ZeroDivisionError' exception.
			'''
			return value / 0;

	:param handler: Custom handler. ( Object )
	:param raise_: Raise the exception. ( Boolean )
	:param \*args: Exceptions. ( Exceptions )
	:return: Object. ( Object )
	"""

	exceptions = tuple((exception for exception in args))
	handler = handler or defaultExceptionsHandler

	def wrapper(object_):
		"""
		This decorator is used for exceptions handling.

		:param object_: Object to decorate. ( Object )
		:return: Object. ( Object )
		"""

		origin = core.getObjectName(object_)

		@functools.wraps(object_)
		def function(*args, **kwargs):
			"""
			This decorator is used for exceptions handling.

			:param \*args: Arguments. ( \* )
			:param \*\*kwargs: Arguments. ( \* )
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
	| This definition provides the default exception handler.
	
	This handler will verbose some informations about the handled exception::
	
		- Exception origin.
		- Exception class.
		- Exception description / documentation.
		- Error message.
		- Exception traceback.
		
	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Arguments. ( \* )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
		"""

		return str(self.value)

class NetworkError(Exception):
	"""
	This class is used for network errors.
	"""

	@core.executionTrace
	def __init__(self, value):
		"""
		This method initializes the class.

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
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

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.value = value

	@core.executionTrace
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
		"""

		return str(self.value)
