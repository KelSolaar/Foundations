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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import inspect
import linecache
import sys
import traceback

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"extractStack"
			"defaultExceptionsHandler",
			"handleExceptions",
			"AbstractError",
			"BreakIteration",
			"AbstractParsingError",
			"FileStructureParsingError",
			"AttributeStructureParsingError",
			"AbstractOsError",
			"PathExistsError",
			"DirectoryExistsError",
			"FileExistsError",
			"AbstractObjectError",
			"ObjectTypeError",
			"ObjectExistsError",
			"AbstractUserError",
			"ProgrammingError",
			"UserError",
			"AbstractNodeError",
			"NodeAttributeTypeError",
			"NodeAttributeExistsError",
			"AbstractLibraryError",
			"LibraryInstantiationError",
			"LibraryInitializationError",
			"LibraryExecutionError",
			"AbstractServerError",
			"ServerOperationError"]

LOGGER = foundations.verbose.installLogger()

EXCEPTIONS_FRAME_SYMBOL = "_exceptions__frame__"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def extractStack(frame, exceptionsFrameSymbol=EXCEPTIONS_FRAME_SYMBOL):
	"""
	| This definition extracts the stack from provided frame.
	| The code is similar to :func:`traceback.extract_stack` except that it allows frames to be excluded
		from the stack if the given stack trace frame tag is found in the frame locals and set **True**.
	
	:param frame: Frame. ( Frame )
	:param exceptionsFrameSymbol: Stack trace frame tag. ( String )
	:return: Stack. ( List )
	"""

	stack = []
	while frame is not None:
		if not frame.f_locals.get(EXCEPTIONS_FRAME_SYMBOL):
			lineNumber = frame.f_lineno
			code = frame.f_code
			codeName = code.co_name
			filename = code.co_filename
			linecache.checkcache(filename)
			line = linecache.getline(filename, lineNumber, frame.f_globals)
			line = line.strip() if line else None
			stack.append((filename, lineNumber, codeName, line))
		frame = frame.f_back
	stack.reverse()

	return stack

def defaultExceptionsHandler(exception, traceName, *args, **kwargs):
	"""
	This definition provides the default exception handler.
	
	This handler verboses some informations about the handled exception:
	
		- Exception traceName.
		- Exception class.
		- Exception description / documentation.
		- Error message.
		- Exception traceback.
		
	:param exception: Exception. ( Exception )
	:param traceName: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Definition success. ( Boolean )
	"""

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))
	LOGGER.error("!> Exception in '{0}'.".format(traceName))
	LOGGER.error("!> Exception class: '{0}'.".format(exception.__class__.__name__))
	LOGGER.error("!> Exception description: '{0}'.".format(exception.__doc__ and exception.__doc__.strip() or \
															Constants.nullObject))

	for i, line in enumerate(str(exception).split("\n")):
		LOGGER.error("!> Exception message line no. '{0}' : '{1}'.".format(i + 1, line))

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))

	exceptionType, exceptionValue, trcback = sys.exc_info()
	stack = extractStack(trcback.tb_frame.f_back)
	frames = inspect.getinnerframes(trcback)
	for frame , filename, lineNumber, name, line, value in frames:
		skipFrame = frame.f_locals.get(EXCEPTIONS_FRAME_SYMBOL)
		skipFrame or stack.append((filename, lineNumber, name, str().join(line) if line else str()))

	sys.stderr.write("Traceback (most recent call last):\n")
	for filename, lineNumber, name, line in stack:
		sys.stderr.write("  File \"{0}\", line {1}, in {2}\n".format(filename, lineNumber, name))
		line and sys.stderr.write("   {0}\n".format(line.strip()))
	for line in traceback.format_exception_only(exceptionType, exceptionValue):
		sys.stderr.write("{0}".format(line))

	return True

def handleExceptions(handler=defaultExceptionsHandler, raiseException=False, *args):
	"""
	| This decorator is used for exceptions handling.
	| It's possible to specify an user defined exception handler,
		if not, :func:`defaultExceptionsHandler` handler will be used.
	| The decorator uses given exceptions objects
		or the default Python `Exception <http://docs.python.org/library/exceptions.html#exceptions.Exception>`_ class.
	
	Usage::

		@handleExceptions(None, False, ZeroDivisionError)
		def raiseAnException(value):
			'''
			This definition raises a 'ZeroDivisionError' exception.
			'''

			return value / 0

	:param handler: Custom handler. ( Object )
	:param raiseException: Raise the exception. ( Boolean )
	:param \*args: Exceptions. ( Exceptions )
	:return: Object. ( Object )
	"""

	exceptions = list(args)
	exceptions.append(Exception)

	def handleExceptionsDecorator(object):
		"""
		This decorator is used for exceptions handling.

		:param object: Object to decorate. ( Object )
		:return: Object. ( Object )
		"""

		traceName = foundations.trace.getTraceName(object)

		@functools.wraps(object)
		def handleExceptionsWrapper(*args, **kwargs):
			"""
			This decorator is used for exceptions handling.

			:param \*args: Arguments. ( \* )
			:param \*\*kwargs: Keywords arguments. ( \*\* )
			"""

			_exceptions__frame__ = True

			exception = None

			try:
				return object(*args, **kwargs)
			except exceptions as exception:
				handler(exception, traceName, *args, **kwargs)
			finally:
				if raiseException and exception:
					raise exception

		return handleExceptionsWrapper

	return handleExceptionsDecorator

class AbstractError(Exception):
	"""
	This class is the abstract base class for all **Foundations** package exceptions.
	"""

	def __init__(self, value):
		"""
		This method initializes the class.

		:param value: Error value or message. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__value = value

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def value(self):
		"""
		This method is the property for **self.__value** attribute.

		:return: self.__value. ( Object )
		"""

		return self.__value

	@value.setter
	def value(self, value):
		"""
		This method is the setter method for **self.__value** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__value = value

	@value.deleter
	def value(self):
		"""
		This method is the deleter method for **self.__value** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "value"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
		"""

		return str(self.__value)

class BreakIteration(AbstractError):
	"""
	This class is used to break nested loop iterations.
	"""

	pass

class AbstractParsingError(AbstractError):
	"""
	This class is the abstract base class for parsing related exceptions.
	"""

	pass

class FileStructureParsingError(AbstractParsingError):
	"""
	This class is used for exceptions raised while parsing file structure.
	"""

	pass

class AttributeStructureParsingError(AbstractParsingError):
	"""
	This class is used for exceptions raised while parsing attribute structure.
	"""

	def __init__(self, value, line=None):
		"""
		This method initializes the class.

		:param value: Error value or message. ( String )
		:param line: Line number where exception occured. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractParsingError.__init__(self, value)

		# --- Setting class attributes. ---
		self.__line = None
		self.line = line

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def line(self):
		"""
		This method is the property for **self.__line** attribute.

		:return: self.__line. ( Integer )
		"""

		return self.__line

	@line.setter
	@handleExceptions(None, False, AssertionError)
	def line(self, value):
		"""
		This method is the setter method for **self.__line** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("line", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("line", value)
		self.__line = value

	@line.deleter
	@handleExceptions(None, False, Exception)
	def line(self):
		"""
		This method is the deleter method for **self.__line** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "line"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __str__(self):
		"""
		This method returns the exception representation.

		:return: Exception representation. ( String )
		"""

		if self.__line:
			return "Line '{0}': '{1}'.".format(self.__line, str(self.value))
		else:
			return str(self.value)

class AbstractOsError(AbstractError):
	"""
	This class is the abstract base class for os related exceptions.
	"""

	pass

class PathExistsError(AbstractOsError):
	"""
	This class is used for non existing path exceptions.
	"""

	pass

class DirectoryExistsError(PathExistsError):
	"""
	This class is used for non existing directory exceptions.
	"""

	pass

class FileExistsError(PathExistsError):
	"""
	This class is used for non existing file exceptions.
	"""

	pass

class AbstractObjectError(AbstractError):
	"""
	This class is the abstract base class for object related exceptions.
	"""

	pass

class ObjectTypeError(AbstractObjectError):
	"""
	This class is used for invalid object type exceptions.
	"""

	pass

class ObjectExistsError(AbstractObjectError):
	"""
	This class is used for non existing object exceptions.
	"""

	pass

class AbstractUserError(AbstractError):
	"""
	This class is the abstract base class for user related exceptions.
	"""

	pass

class ProgrammingError(AbstractUserError):
	"""
	This class is used for programming exceptions.
	"""

	pass

class UserError(AbstractUserError):
	"""
	This class is used for user exceptions.
	"""

	pass

class AbstractNodeError(AbstractError):
	"""
	This class is the abstract base class for node related exceptions.
	"""

	pass

class NodeAttributeTypeError(AbstractNodeError, ObjectTypeError):
	"""
	This class is the abstract base class for node attributes type related exceptions.
	"""

	pass

class NodeAttributeExistsError(AbstractNodeError, ObjectExistsError):
	"""
	This class is used for non existing node attribute exceptions.
	"""

	pass

class AbstractLibraryError(AbstractError):
	"""
	This class is the abstract base class for :mod:`library` module exceptions.
	"""

	pass

class LibraryInstantiationError(AbstractLibraryError):
	"""
	This class is used for :mod:`library` module :class:`library.Library` class instantiation exceptions.
	"""

	pass

class LibraryInitializationError(AbstractLibraryError):
	"""
	This class is used for :mod:`library` module :class:`library.Library` class initialization exceptions.
	"""

	pass

class LibraryExecutionError(AbstractLibraryError):
	"""
	This class is used for :mod:`library` module :class:`library.Library` class execution exceptions.
	"""

	pass

class AbstractServerError(AbstractError):
	"""
	This class is the abstract base class for :mod:`tcpServer` module exceptions.
	"""

	pass

class ServerOperationError(AbstractServerError):
	"""
	This class is used for :mod:`tcpServer` module :class:`tcpServer.TCPServer` class operations exceptions.
	"""

	pass

