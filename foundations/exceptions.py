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
import itertools

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
			"extractStack",
			"extractArguments",
			"extractLocals",
			"getInnerMostFrame",
			"formatException",
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
def extractStack(frame, context=10, exceptionsFrameSymbol=EXCEPTIONS_FRAME_SYMBOL):
	"""
	This definition extracts the stack from given frame while excluded any symbolized frame.
	
	:param frame: Frame. ( Frame )
	:param context: Context to extract. ( Integer )
	:param exceptionsFrameSymbol: Stack trace frame tag. ( String )
	:return: Stack. ( List )
	"""

	return list(reversed(filter(lambda x: not x[0].f_locals.get(exceptionsFrameSymbol),
								inspect.getouterframes(frame, context))))

def extractArguments(frame):
	"""
	This definition extracts the arguments from given frame.
	
	:param frame: Frame. ( Object )
	:return: Arguments. ( Tuple )
	"""

	arguments = ([], None, None)
	try:
		source = textwrap.dedent(str().join(inspect.getsourcelines(frame)[0]).replace("\\\n", str()))
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
	This definition extracts the frames locals of given traceback.
	
	:param trcback: Traceback. ( Traceback )
	:return: Frames locals. ( List )
	"""

	output = []
	stack = extractStack(getInnerMostFrame(trcback))
	for frame, fileName, lineNumber, name, context, index in stack:
		argsNames, nameless, keyword = extractArguments(frame)
		arguments, namelessArgs, keywordArgs, locals = OrderedDict(), [], {}, {}
		for key, data in frame.f_locals.iteritems():
			try:
				value = repr(data)
			except:
				value = Constants.nullObject
			if key == nameless:
				namelessArgs = frame.f_locals.get(nameless, ())
			elif key == keyword:
				keywordArgs = frame.f_locals.get(keyword, {})
			elif key in argsNames:
				arguments[key] = value
			else:
				locals[key] = value
		output.append(((name, fileName, lineNumber), (arguments, namelessArgs, keywordArgs, locals)))
	return output

def getInnerMostFrame(trcback):
	"""
	This definition returns the inner most frame of given traceback.
	
	:param trcback: Traceback. ( Traceback )
	:return: Frame. ( List )
	"""

	frame = inspect.getinnerframes(trcback).pop()[0]
	return frame

def formatException(cls, instance, trcback, context=1):
	"""
	| This definition formats given exception.
	| The code produce a similar output to :func:`traceback.format_exception` except that it allows frames to be excluded
		from the stack if the given stack trace frame tag is found in the frame locals and set **True**.
	
	:param cls: Exception class. ( Object )
	:param instance: Exception instance. ( Object )
	:param trcback: Traceback. ( Traceback )
	:return: Formated exception. ( List )
	"""

	stack = extractStack(getInnerMostFrame(trcback), context=context)
	output = []
	output.append("Traceback (most recent call last):")
	for frame, fileName, lineNumber, name, context, index in stack:
		output.append("  File \"{0}\", line {1}, in {2}".format(fileName, lineNumber, name))
		output.append("    {0}".format(context.pop().strip()))
	for line in traceback.format_exception_only(cls, instance):
		output.append("{0}".format(line))
	return output

def defaultExceptionsHandler(exception, object, *args, **kwargs):
	"""
	This definition provides the default exception handler.
	
	This handler verboses some informations about the handled exception:
	
		- Exception traceName.
		- Exception class.
		- Exception description / documentation.
		- Error instance.
		- Exception traceback.
		
	:param exception: Exception. ( Exception )
	:param object: Object raising the exception. ( Object )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Definition success. ( Boolean )
	"""

	traceName = foundations.trace.getTraceName(object)
	cls, instance, trcback = sys.exc_info()

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))
	LOGGER.error("!> Exception in '{0}'.".format(traceName))
	LOGGER.error("!> Exception class: '{0}'.".format(exception.__class__.__name__))
	LOGGER.error("!> Exception description: '{0}'.".format(exception.__doc__ and exception.__doc__.strip() or \
															Constants.nullObject))
	for i, line in enumerate(str(exception).split("\n")):
		LOGGER.error("!> Exception instance line no. '{0}' : '{1}'.".format(i + 1, line))

	LOGGER.error("!> {0}".format(Constants.loggingSeparators))
	for frame, locals in extractLocals(trcback):
		LOGGER.error("!> Frame '{0}' in '{1}' at line '{2}':".format(*frame))
		arguments, namelessArgs, keywordArgs, locals = locals
		any((arguments, namelessArgs, keywordArgs)) and LOGGER.error("!> {0:>40}".format("Arguments:"))
		for key, value in arguments.iteritems():
			LOGGER.error("!> {0:>40} = {1}".format(key, value))
		for value in namelessArgs:
			LOGGER.error("!> {0:>40}".format(value))
		for key, value in sorted(keywordArgs.iteritems()):
			LOGGER.error("!> {0:>40} = {1}".format(key, value))
		locals and LOGGER.error("!> {0:>40}".format("Locals:"))
		for key, value in sorted(locals.iteritems()):
			LOGGER.error("!> {0:>40} = {1}".format(key, value))
		LOGGER.error("!>")
	LOGGER.error("!> {0}".format(Constants.loggingSeparators))

	sys.stderr.write("\n".join(formatException(cls, instance, trcback)))

	return True

def handleExceptions(*args):
	"""
	| This decorator is used for exceptions handling.
	| It's possible to specify an user defined exception handler,
		if not, :func:`defaultExceptionsHandler` handler will be used.
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

	exceptions = tuple(itertools.chain(filter(lambda x: isinstance(x, Exception), args), (Exception,)))
	handlers = filter(lambda x: inspect.isfunction(x), args) or (defaultExceptionsHandler,)

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

			exception = None

			try:
				return object(*args, **kwargs)
			except exceptions as exception:
				for handler in handlers:
					handler(exception, object, *args, **kwargs)

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
