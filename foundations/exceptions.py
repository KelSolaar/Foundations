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
def getInnerMostFrame(trcback):
	"""
	Returns the inner most frame of given traceback.
	
	:param trcback: Traceback. ( Traceback )
	:return: Frame. ( Frame )
	"""

	frames = inspect.getinnerframes(trcback)
	return frames.pop()[0] if frames else None

def extractStack(frame, context=10, exceptionsFrameSymbol=EXCEPTIONS_FRAME_SYMBOL):
	"""
	Extracts the stack from given frame while excluded any symbolized frame.
	
	:param frame: Frame. ( Frame )
	:param context: Context to extract. ( Integer )
	:param exceptionsFrameSymbol: Stack trace frame tag. ( String )
	:return: Stack. ( List )
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
					context	if context is not None else [],
					index if index is not None else -1))

	return list(reversed(stack))

def extractArguments(frame):
	"""
	Extracts the arguments from given frame.
	
	:param frame: Frame. ( Object )
	:return: Arguments. ( Tuple )
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
	
	:param trcback: Traceback. ( Traceback )
	:return: Frames locals. ( List )
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
	
	:param \*args: Arguments. ( \* )
	:return: Extracted exception. ( Tuple )
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
	
	:param cls: Exception class. ( Object )
	:param instance: Exception instance. ( Object )
	:param trcback: Traceback. ( Traceback )
	:param context: Context being included. ( Integer )
	:return: Formated exception. ( List )
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
	
	:param cls: Exception class. ( Object )
	:param instance: Exception instance. ( Object )
	:param trcback: Traceback. ( Traceback )
	:param context: Context being included. ( Integer )
	:return: Formated report. ( Tuple )
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
	
	:param \*args: Arguments. ( \* )
	:return: Definition success. ( Boolean )
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
	
	:param handler: Exception handler. ( Object )
	:return: Definition success. ( Boolean )
	"""

	sys.excepthook = handler if handler is not None else baseExceptionHandler
	return True

def uninstallExceptionHandler():
	"""
	Uninstalls the exceptions handler.
	
	:return: Definition success. ( Boolean )
	"""

	sys.excepthook = sys.__excepthook__
	return True

def handleExceptions(*args):
	"""
	| This decorator is used for exceptions handling.
	| It's possible to specify an user defined exception handler,
		if not, :func:`baseExceptionHandler` handler will be used.
	| The decorator uses given exceptions objects
		or the default Python `Exception <http://docs.python.org/library/exceptions.html#exceptions.Exception>`_ class.
	
	Usage::

		@handleExceptions(ZeroDivisionError)
		def raiseAnException(value):
			'''
			This definition raises a 'ZeroDivisionError' exception.
			'''

			return value / 0

			:param \*args: Arguments. ( \* )

	:return: Object. ( Object )
	"""

	exceptions = tuple(filter(lambda x: issubclass(x, Exception),
								filter(lambda x: isinstance(x, (type, types.ClassType)), args)))
	handlers = filter(lambda x: inspect.isfunction(x), args) or (baseExceptionHandler,)

	def handleExceptionsDecorator(object):
		"""
		This decorator is used for exceptions handling.

		:param object: Object to decorate. ( Object )
		:return: Object. ( Object )
		"""

		@functools.wraps(object)
		def handleExceptionsWrapper(*args, **kwargs):
			"""
			This decorator is used for exceptions handling.

			:param \*args: Arguments. ( \* )
			:param \*\*kwargs: Keywords arguments. ( \*\* )
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
		Property for **self.__value** attribute.

		:return: self.__value. ( Object )
		"""

		return self.__value

	@value.setter
	def value(self, value):
		"""
		Setter for **self.__value** attribute.

		:param value: Attribute value. ( Object )
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

		:return: Exception representation. ( String )
		"""

		return str(self.__value)

class ExecutionError(AbstractError):
	"""
	Defines execution exceptions.
	"""

	pass

class BreakIteration(AbstractError):
	"""
	Breaks nested loop iterations.
	"""

	pass

class AbstractParsingError(AbstractError):
	"""
	Defines the abstract base class for parsing related exceptions.
	"""

	pass

class FileStructureParsingError(AbstractParsingError):
	"""
	Defines exceptions raised while parsing file structure.
	"""

	pass

class AttributeStructureParsingError(AbstractParsingError):
	"""
	Defines exceptions raised while parsing attribute structure.
	"""

	def __init__(self, value, line=None):
		"""
		Initializes the class.

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
		Property for **self.__line** attribute.

		:return: self.__line. ( Integer )
		"""

		return self.__line

	@line.setter
	@handleExceptions(AssertionError)
	def line(self, value):
		"""
		Setter for **self.__line** attribute.

		:param value: Attribute value. ( Integer )
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

		:return: Exception representation. ( String )
		"""

		if self.__line:
			return "Line '{0}': '{1}'.".format(self.__line, str(self.value))
		else:
			return str(self.value)

class AbstractOsError(AbstractError):
	"""
	Defines the abstract base class for os related exceptions.
	"""

	pass

class PathExistsError(AbstractOsError):
	"""
	Defines non existing path exceptions.
	"""

	pass

class DirectoryExistsError(PathExistsError):
	"""
	Defines non existing directory exceptions.
	"""

	pass

class FileExistsError(PathExistsError):
	"""
	Defines non existing file exceptions.
	"""

	pass

class AbstractObjectError(AbstractError):
	"""
	Defines the abstract base class for object related exceptions.
	"""

	pass

class ObjectTypeError(AbstractObjectError):
	"""
	Defines invalid object type exceptions.
	"""

	pass

class ObjectExistsError(AbstractObjectError):
	"""
	Defines non existing object exceptions.
	"""

	pass

class AbstractUserError(AbstractError):
	"""
	Defines the abstract base class for user related exceptions.
	"""

	pass

class ProgrammingError(AbstractUserError):
	"""
	Defines programming exceptions.
	"""

	pass

class UserError(AbstractUserError):
	"""
	Defines user exceptions.
	"""

	pass

class AbstractNodeError(AbstractError):
	"""
	Defines the abstract base class for Node related exceptions.
	"""

	pass

class NodeAttributeTypeError(AbstractNodeError, ObjectTypeError):
	"""
	Defines the abstract base class for Node attributes type related exceptions.
	"""

	pass

class NodeAttributeExistsError(AbstractNodeError, ObjectExistsError):
	"""
	Defines non existing Node attribute exceptions.
	"""

	pass

class AbstractLibraryError(AbstractError):
	"""
	Defines the abstract base class for :mod:`library` module exceptions.
	"""

	pass

class LibraryInstantiationError(AbstractLibraryError):
	"""
	Defines :mod:`library` module :class:`library.Library` class instantiation exceptions.
	"""

	pass

class LibraryInitializationError(AbstractLibraryError):
	"""
	Defines :mod:`library` module :class:`library.Library` class initialization exceptions.
	"""

	pass

class LibraryExecutionError(AbstractLibraryError):
	"""
	Defines :mod:`library` module :class:`library.Library` class execution exceptions.
	"""

	pass

class AbstractServerError(AbstractError):
	"""
	Defines the abstract base class for :mod:`tcpServer` module exceptions.
	"""

	pass

class ServerOperationError(AbstractServerError):
	"""
	Defines :mod:`tcpServer` module :class:`tcpServer.TCPServer` class operations exceptions.
	"""

	pass
