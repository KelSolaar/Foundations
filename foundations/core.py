#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**core.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package core objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import inspect
import linecache
import sys
import time

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
			"IGNORED_CODE_LAYERS",
			"UNDEFINED_CODE_LAYER",
			"UNDEFINED_MODULE",
			"UNDEFINED_OBJECT",
			"getFrame",
			"getCodeLayerName",
			"getModule",
			"getTraceName",
			"extractStack",
			"executionTrace",
			"executionTime",
			"memoize",
			"removeLoggingHandler",
			"exit",
			"wait"]

LOGGER = foundations.verbose.installLogger()

IGNORED_CODE_LAYERS = ("getFrame",
					"getCodeLayerName",
					"getTraceName",
					"executionTrace",
					"wrapper")

UNDEFINED_CODE_LAYER = "UndefinedCodeLayer"
UNDEFINED_MODULE = "UndefinedModule"
UNDEFINED_OBJECT = "UndefinedObject"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def _castStr(object, length=Constants.executionTraceArgumentMaximumLength):
	"""
	This definition casts given object to string with a length limit.
	
	:param object: Object. ( Object )
	:param length: String maximum length. ( Integer )
	:return: Truncated string. ( String )
	"""

	try:
		string = str(object)
	except AttributeError:
		# LOGGER.error("!> {0} | Exception raised while casting '{1}' object to 'str'!".format(
		# inspect.getmodule(_castStr).__name__, id(object)))
		string = str(None)

	if len(string) > length:
		return "{0} ...".format(string[:length])
	else:
		return string

def getFrame(index=0):
	"""
	This definition returns requested execution frame.

	:param level: Frame index. ( Integer )
	:return: Frame. ( Frame )
	"""

	return sys._getframe(index)

def getCodeLayerName():
	"""
	This definition returns first candidate frame code layer name. 

	:return: Code layer name. ( String )
	
	:note: Candidates names matching any :attr:`foundations.core.IGNORED_CODE_LAYERS` members will be skipped.
		If no appropriate candidate name is found, then :attr:`foundations.core.UNDEFINED_CODE_LAYER` is returned.
	"""

	frame = getFrame()
	while frame:
		codeLayerName = frame.f_code.co_name
		if codeLayerName not in IGNORED_CODE_LAYERS:
			return codeLayerName
		frame = frame.f_back
	return UNDEFINED_CODE_LAYER

def getModule(object):
	"""
	This definition returns given object module name.

	:param object: Object. ( Object )
	:return: Frame Module. ( Module )
	"""

	return inspect.getmodule(object)

def getTraceName(object):
	"""
	This definition returns object name composited with current execution frame.
	
	Examples names::

		'foundations.environment | getUserApplicationDataDirectory()'.
		'__main__ | _setUserApplicationDataDirectory()'.
		'__main__ | Preferences.__init__()'.
		'UndefinedObject'.

	:param object: Object. ( Object )
	:return: Object name. ( String )
	"""

	module = getModule(object)
	moduleName = module and module.__name__ or UNDEFINED_MODULE
	codeLayerName = getCodeLayerName()
	codeLayerName = codeLayerName != UNDEFINED_CODE_LAYER and codeLayerName != "<module>" and \
					"{0}.".format(codeLayerName) or ""

	return hasattr(object, "__name__") and "{0} | {1}{2}()".format(moduleName, codeLayerName, object.__name__) or \
	UNDEFINED_OBJECT

def extractStack(frame, stackTraceFrameTag="__stackTraceFrameTag__"):
	"""
	| This definition extracts the stack from provided frame.
	| The code is similar to :func:`traceback.extract_stack` except that it allows frames to be excluded
		from the stack if the given stack trace frame tag is found in the frame locals and set **True**.
	
	:param frame: Frame. ( Frame )
	:param stackTraceFrameTag: Stack trace frame tag. ( String )
	:return: Stack. ( List )
	"""

	stack = []
	while frame is not None:
		skipFrame = frame.f_locals.get(stackTraceFrameTag)
		if not skipFrame:
			lineNumber = frame.f_lineno
			code = frame.f_code
			codeName = code.co_name
			filename = code.co_filename
			linecache.checkcache(filename)
			line = linecache.getline(filename, lineNumber, frame.f_globals)
			line = line and line.strip() or None
			stack.append((filename, lineNumber, codeName, line))
		frame = frame.f_back
	stack.reverse()

	return stack

def executionTrace(object):
	"""
	| This decorator is used for execution tracing.
	| Any method / definition decorated will have it's execution traced through debug messages.
	| Both object entry and exit are logged.
	
	Entering in an object::
		
		DEBUG   : --->>> 'foundations.environment | getUserApplicationDataDirectory()' <<<---
		
	Exiting from an object::
		
		DEBUG   : --->>> 'foundations.environment | getSystemApplicationDataDirectory()' <<<---
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	traceExecution = False
	if LOGGER:
		if LOGGER.__dict__["handlers"]:
			traceExecution = True

	traceName = traceExecution and getTraceName(object) or str()

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used for execution tracing.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
		"""

		__stackTraceFrameTag__ = Constants.excludeTaggedFramesFromStackTrace

		if traceExecution:
			LOGGER.debug("--->>> '{0}' <<<---".format(traceName))
			signature = inspect.getargspec(object)
			code = object.func_code
			for name, value in zip(signature.args, args[:code.co_argcount]):
				LOGGER.debug("   >>> Argument: '{0}' = '{1}' <<<".format(name, _castStr(value)))
			for value in args[code.co_argcount:]:
				LOGGER.debug("   >>> Argument: '{0}' <<<".format(_castStr(value)))
			for key, value in kwargs.iteritems():
				LOGGER.debug("   >>> Argument: '{0}' = '{1}'<<<".format(key, _castStr(value)))

		value = object(*args, **kwargs)

		if traceExecution:
			LOGGER.debug("   <<< Return: '{0}' >>>".format(repr(value)))
			LOGGER.debug("---<<< '{0}' >>>---".format(traceName))

		return value

	return function

def executionTime(object):
	"""
	| This decorator is used for execution timing.
	| Any method / definition decorated will have it's execution timed through information messages.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used for execution timing.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
		"""

		startTime = time.time()

		value = object(*args, **kwargs)

		endTime = time.time()

		LOGGER.info("{0} | '{1}' object processed during '{2:f}' ms!".format(
		inspect.getmodulename(__file__), object.__name__, (endTime - startTime) * 1000.0))

		return value

	return function

def memoize(cache=None):
	"""
	| This decorator is used for method / definition memoization.
	| Any method / definition decorated will get its return value cached and restored whenever called
		with the same arguments.
	
	:param cache: Alternate cache. ( Dictionary )
	:return: Object. ( Object )
	"""

	if cache is None:
		cache = {}

	def wrapper(object):
		"""
		This decorator is used for object memoization.

		:param object: Object to decorate. ( Object )
		:return: Object. ( Object )
		"""

		@functools.wraps(object)
		def function(*args, **kwargs):
			"""
			This decorator is used for object memoization.
	
			:param \*args: Arguments. ( \* )
			:param \*\*kwargs: Keywords arguments. ( \*\* )
			:return: Object. ( Object )
			"""

			if kwargs:
				key = args, frozenset(kwargs.iteritems())
			else:
				key = args

			if key not in cache:
				cache[key] = object(*args, **kwargs)

			return cache[key]

		return function

	return wrapper

def exit(exitCode=1):
	"""
	This definition shuts down current process logging, associated handlers and then exits to system.
	
	:param exitCode: System exit code. ( Integer / String / Object )

	:note: **exitCode** argument is passed to Python :func:`sys.exit` definition.
	"""

	LOGGER.debug("> {0} | Exiting current process!".format(getModule(exit).__name__))

	LOGGER.debug("> Stopping logging handlers and logger!")
	for handler in LOGGER.__dict__["handlers"]:
		foundations.verbose.removeLoggingHandler(LOGGER, handler)

	sys.exit(exitCode)

def wait(waitTime):
	"""
	This definition halts current process exection for an user defined time.

	:param waitTime: Current sleep time in seconds. ( Float )
	:return: Definition success. ( Boolean )
	"""

	LOGGER.debug("> Waiting '{0}' seconds!".format(waitTime))

	time.sleep(waitTime)
	return True
