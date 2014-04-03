#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package exceptions and others exception handling related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import ast
import functools
import inspect
import sys

if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
import textwrap
import traceback
import types

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
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
		   "getInnerMostFrame",
		   "extractStack",
		   "extractArguments",
		   "extractLocals",
		   "extractException",
		   "formatException",
		   "formatReport",
		   "baseExceptionHandler",
		   "installExceptionHandler",
		   "uninstallExceptionHandler",
		   "handleExceptions",
		   "AbstractError",
		   "ExecutionError",
		   "BreakIteration",
		   "AbstractParsingError",
		   "FileStructureParsingError",
		   "AttributeStructureParsingError",
		   "AbstractIOError",
		   "FileReadError",
		   "FileWriteError",
		   "UrlReadError",
		   "UrlWriteError",
		   "DirectoryCreationError",
		   "PathCopyError",
		   "PathRemoveError",
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
		   "ServerOperationError",
		   "AnsiEscapeCodeExistsError"]

LOGGER = foundations.verbose.installLogger()

EXCEPTIONS_FRAME_SYMBOL = "_exceptions__frame__"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getInnerMostFrame(trcback):
	"""
	Returns the inner most frame of given traceback.

	:param trcback: Traceback.
	:type trcback: Traceback
	:return: Frame.
	:rtype: Frame
	"""

	frames = inspect.getinnerframes(trcback)
	return frames.pop()[0] if frames else None

def extractStack(frame, context=10, exceptionsFrameSymbol=EXCEPTIONS_FRAME_SYMBOL):
	"""
	Extracts the stack from given frame while excluded any symbolized frame.

	:param frame: Frame.
	:type frame: Frame
	:param context: Context to extract.
	:type context: int
	:param exceptionsFrameSymbol: Stack trace frame tag.
	:type exceptionsFrameSymbol: unicode
	:return: Stack.
	:rtype: list
	"""

	decode = lambda x: unicode(x, Constants.defaultCodec, Constants.codecError)

	stack = []

	for frame, fileName, lineNumber, name, context, index in inspect.getouterframes(frame, context):
		if frame.f_locals.get(exceptionsFrameSymbol):
			continue

		stack.append((frame,
					  decode(fileName),
					  lineNumber,
					  decode(name),
					  context if context is not None else [],
					  index if index is not None else -1))

	return list(reversed(stack))

def extractArguments(frame):
	"""
	Extracts the arguments from given frame.

	:param frame: Frame.
	:type frame: object
	:return: Arguments.
	:rtype: tuple
	"""

	arguments = ([], None, None)
	try:
		source = textwrap.dedent("".join(inspect.getsourcelines(frame)[0]).replace("\\\n", ""))
	except (IOError, TypeError) as error:
		return arguments

	try:
		node = ast.parse(source)
	except:
		return arguments

	if not node.body:
		return arguments

	node = node.body[0]
	if not isinstance(node, ast.FunctionDef):
		return arguments

	return [arg.id for arg in node.args.args], node.args.vararg, node.args.kwarg

def extractLocals(trcback):
	"""
	Extracts the frames locals of given traceback.

	:param trcback: Traceback.
	:type trcback: Traceback
	:return: Frames locals.
	:rtype: list
	"""

	output = []
	stack = extractStack(getInnerMostFrame(trcback))
	for frame, fileName, lineNumber, name, context, index in stack:
		argsNames, nameless, keyword = extractArguments(frame)
		arguments, namelessArgs, keywordArgs, locals = OrderedDict(), [], {}, {}
		for key, data in frame.f_locals.iteritems():
			if key == nameless:
				namelessArgs = map(repr, frame.f_locals.get(nameless, ()))
			elif key == keyword:
				keywordArgs = dict((arg, repr(value)) for arg, value in frame.f_locals.get(keyword, {}).iteritems())
			elif key in argsNames:
				arguments[key] = repr(data)
			else:
				locals[key] = repr(data)
		output.append(((name, fileName, lineNumber), (arguments, namelessArgs, keywordArgs, locals)))
	return output

def extractException(*args):
	"""
	Extracts the exception from given arguments or from :func:`sys.exc_info`.

	:param \*args: Arguments.
	:type \*args: \*
	:return: Extracted exception.
	:rtype: tuple
	"""

	cls, instance, trcback = sys.exc_info()

	exceptions = filter(lambda x: issubclass(type(x), BaseException), args)
	trcbacks = filter(lambda x: issubclass(type(x), types.TracebackType), args)

	cls, instance = (type(exceptions[0]), exceptions[0]) if exceptions else (cls, instance)
	trcback = trcbacks[0] if trcbacks else trcback

	return cls, instance, trcback

def formatException(cls, instance, trcback, context=1):
	"""
	| Formats given exception.
	| The code produce a similar output to :func:`traceback.format_exception` except that it allows frames to be excluded
		from the stack if the given stack trace frame tag is found in the frame locals and set **True**.

	:param cls: Exception class.
	:type cls: object
	:param instance: Exception instance.
	:type instance: object
	:param trcback: Traceback.
	:type trcback: Traceback
	:param context: Context being included.
	:type context: int
	:return: Formated exception.
	:rtype: list
	"""

	stack = extractStack(getInnerMostFrame(trcback), context=context)
	output = []
	output.append("Traceback (most recent call last):")
	for frame, fileName, lineNumber, name, context, index in stack:
		output.append("  File \"{0}\", line {1}, in {2}".format(fileName, lineNumber, name))
		for line in context:
			output.append("    {0}".format(line.strip()))
	for line in traceback.format_exception_only(cls, instance):
		output.append("{0}".format(line))
	return output

def formatReport(cls, instance, trcback, context=1):
	"""
	Formats a report using given exception.

	:param cls: Exception class.
	:type cls: object
	:param instance: Exception instance.
	:type instance: object
	:param trcback: Traceback.
	:type trcback: Traceback
	:param context: Context being included.
	:type context: int
	:return: Formated report.
	:rtype: tuple
	"""

	header = []
	header.append("Exception in '{0}'.".format(getInnerMostFrame(trcback).f_code.co_name))
	header.append("Exception class: '{0}'.".format(cls.__name__))
	header.append("Exception description: '{0}'.".format(instance.__doc__ and instance.__doc__.strip() or \
														 Constants.nullObject))
	for i, line in enumerate(str(instance).split("\n")):
		header.append("Exception message line no. '{0}' : '{1}'.".format(i + 1, line))

	frames = []
	for frame, locals in extractLocals(trcback):
		frames.append("Frame '{0}' in '{1}' at line '{2}':".format(*frame))
		arguments, namelessArgs, keywordArgs, locals = locals
		any((arguments, namelessArgs, keywordArgs)) and frames.append("{0:>40}".format("Arguments:"))
		for key, value in arguments.iteritems():
			frames.append("{0:>40} = {1}".format(key, value))
		for value in namelessArgs:
			frames.append("{0:>40}".format(value))
		for key, value in sorted(keywordArgs.iteritems()):
			frames.append("{0:>40} = {1}".format(key, value))
		locals and frames.append("{0:>40}".format("Locals:"))
		for key, value in sorted(locals.iteritems()):
			frames.append("{0:>40} = {1}".format(key, value))
		frames.append("")

	trcback = formatException(cls, instance, trcback)

	return header, frames, trcback

def baseExceptionHandler(*args):
	"""
	Provides the base exception handler.

	:param \*args: Arguments.
	:type \*args: \*
	:return: Definition success.
	:rtype: bool
	"""

	header, frames, trcback = formatReport(*extractException(*args))

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))
	map(lambda x: LOGGER.error("!> {0}".format(x)), header)

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))
	map(lambda x: LOGGER.error("!> {0}".format(x)), frames)

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))
	sys.stderr.write("\n".join(trcback))

	return True

def installExceptionHandler(handler=None):
	"""
	Installs the given exceptions handler.

	:param handler: Exception handler.
	:type handler: object
	:return: Definition success.
	:rtype: bool
	"""

	sys.excepthook = handler if handler is not None else baseExceptionHandler
	return True

def uninstallExceptionHandler():
	"""
	Uninstalls the exceptions handler.

	:return: Definition success.
	:rtype: bool
	"""

	sys.excepthook = sys.__excepthook__
	return True

def handleExceptions(*args):
	"""
	| Handles exceptions.
	| It's possible to specify an user defined exception handler,
		if not, :func:`baseExceptionHandler` handler will be used.
	| The decorator uses given exceptions objects
		or the default Python `Exception <http://docs.python.org/library/exceptions.html#exceptions.Exception>`_ class.

	Usage::

		@handleExceptions(ZeroDivisionError)
		def raiseAnException(value):
			'''
			Raises a 'ZeroDivisionError' exception.
			'''

			return value / 0

			:param \*args: Arguments.
			:type \*args: \*

	:return: Object.
	:rtype: object
	"""

	exceptions = tuple(filter(lambda x: issubclass(x, Exception),
							  filter(lambda x: isinstance(x, (type, types.ClassType)), args)))
	handlers = filter(lambda x: inspect.isfunction(x), args) or (baseExceptionHandler,)

	def handleExceptionsDecorator(object):
		"""
		Handles exceptions.

		:param object: Object to decorate.
		:type object: object
		:return: Object.
		:rtype: object
		"""

		@functools.wraps(object)
		def handleExceptionsWrapper(*args, **kwargs):
			"""
			Handles exceptions.

			:param \*args: Arguments.
			:type \*args: \*
			:param \*\*kwargs: Keywords arguments.
			:type \*\*kwargs: \*\*
			"""

			_exceptions__frame__ = True

			try:
				return object(*args, **kwargs)
			except exceptions as error:
				for handler in handlers:
					handler(error)

		return handleExceptionsWrapper

	return handleExceptionsDecorator

class AbstractError(Exception):
	"""
	Defines the abstract base class for all **Foundations** package exceptions.
	"""

	def __init__(self, value):
		"""
		Initializes the class.

		:param value: Error value or message.
		:type value: unicode
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
		Property for **self.__value** attribute.

		:return: self.__value.
		:rtype: object
		"""

		return self.__value

	@value.setter
	def value(self, value):
		"""
		Setter for **self.__value** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		self.__value = value

	@value.deleter
	def value(self):
		"""
		Deleter for **self.__value** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "value"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __str__(self):
		"""
		Returns the exception representation.

		:return: Exception representation.
		:rtype: unicode
		"""

		return str(self.__value)

class ExecutionError(AbstractError):
	"""
	Defines execution exception.
	"""

	pass

class BreakIteration(AbstractError):
	"""
	Breaks nested loop iteration.
	"""

	pass

class AbstractParsingError(AbstractError):
	"""
	Defines the abstract base class for parsing related exception.
	"""

	pass

class FileStructureParsingError(AbstractParsingError):
	"""
	Defines exception raised while parsing file structure.
	"""

	pass

class AttributeStructureParsingError(AbstractParsingError):
	"""
	Defines exception raised while parsing attribute structure.
	"""

	def __init__(self, value, line=None):
		"""
		Initializes the class.

		:param value: Error value or message.
		:type value: unicode
		:param line: Line number where exception occured.
		:type line: int
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
		Property for **self.__line** attribute.

		:return: self.__line.
		:rtype: int
		"""

		return self.__line

	@line.setter
	@handleExceptions(AssertionError)
	def line(self, value):
		"""
		Setter for **self.__line** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("line", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("line", value)
		self.__line = value

	@line.deleter
	@handleExceptions(Exception)
	def line(self):
		"""
		Deleter for **self.__line** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "line"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __str__(self):
		"""
		Returns the exception representation.

		:return: Exception representation.
		:rtype: unicode
		"""

		if self.__line:
			return "Line '{0}': '{1}'.".format(self.__line, str(self.value))
		else:
			return str(self.value)

class AbstractIOError(AbstractError):
	"""
	Defines the abstract base class for io related exception.
	"""

	pass

class FileReadError(AbstractIOError):
	"""
	Defines file read exception.
	"""

	pass

class FileWriteError(AbstractIOError):
	"""
	Defines file write exception.
	"""

	pass

class UrlReadError(AbstractIOError):
	"""
	Defines url read exception.
	"""

	pass

class UrlWriteError(AbstractIOError):
	"""
	Defines file write exception.
	"""

	pass

class DirectoryCreationError(AbstractIOError):
	"""
	Defines directory creation exception.
	"""

	pass

class PathCopyError(AbstractIOError):
	"""
	Defines path copy exception.
	"""

	pass

class PathRemoveError(AbstractIOError):
	"""
	Defines path remove exception.
	"""

	pass

class AbstractOsError(AbstractError):
	"""
	Defines the abstract base class for os related exception.
	"""

	pass

class PathExistsError(AbstractOsError):
	"""
	Defines non existing path exception.
	"""

	pass

class DirectoryExistsError(PathExistsError):
	"""
	Defines non existing directory exception.
	"""

	pass

class FileExistsError(PathExistsError):
	"""
	Defines non existing file exception.
	"""

	pass

class AbstractObjectError(AbstractError):
	"""
	Defines the abstract base class for object related exception.
	"""

	pass

class ObjectTypeError(AbstractObjectError):
	"""
	Defines invalid object type exception.
	"""

	pass

class ObjectExistsError(AbstractObjectError):
	"""
	Defines non existing object exception.
	"""

	pass

class AbstractUserError(AbstractError):
	"""
	Defines the abstract base class for user related exception.
	"""

	pass

class ProgrammingError(AbstractUserError):
	"""
	Defines programming exception.
	"""

	pass

class UserError(AbstractUserError):
	"""
	Defines user exception.
	"""

	pass

class AbstractNodeError(AbstractError):
	"""
	Defines the abstract base class for Node related exception.
	"""

	pass

class NodeAttributeTypeError(AbstractNodeError, ObjectTypeError):
	"""
	Defines the abstract base class for Node attributes type related exception.
	"""

	pass

class NodeAttributeExistsError(AbstractNodeError, ObjectExistsError):
	"""
	Defines non existing Node attribute exception.
	"""

	pass

class AbstractLibraryError(AbstractError):
	"""
	Defines the abstract base class for :mod:`library` module exception.
	"""

	pass

class LibraryInstantiationError(AbstractLibraryError):
	"""
	Defines :mod:`library` module :class:`library.Library` class instantiation exception.
	"""

	pass

class LibraryInitializationError(AbstractLibraryError):
	"""
	Defines :mod:`library` module :class:`library.Library` class initialization exception.
	"""

	pass

class LibraryExecutionError(AbstractLibraryError):
	"""
	Defines :mod:`library` module :class:`library.Library` class execution exception.
	"""

	pass

class AbstractServerError(AbstractError):
	"""
	Defines the abstract base class for :mod:`tcpServer` module exception.
	"""

	pass

class ServerOperationError(AbstractServerError):
	"""
	Defines :mod:`tcpServer` module :class:`tcpServer.TCPServer` class operations exception.
	"""

	pass

class AnsiEscapeCodeExistsError(AbstractError):
	"""
	Defines exception used for non existing *ANSI* escape codes.
	"""

	pass
