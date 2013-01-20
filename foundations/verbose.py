#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**verbose.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package verbose and logging objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import hashlib
import inspect
import itertools
import logging
import sys
import threading
import tempfile

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.trace
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

__all__ = ["THREADS_IDENTIFIERS",
			"INDENT_LEVEL",
			"LOGGER",
			"LOGGING_DEFAULT_FORMATTER",
			"LOGGING_EXTENDED_FORMATTER",
			"LOGGING_STANDARD_FORMATTER",
			"TRACER_LOGGING_FUNCTION",
			"Streamer"
			"StandardOutputStreamer",
			"indentMessage",
			"tracer",
			"installLogger",
			"uninstallLogger",
			"getLoggingConsoleHandler",
			"getLoggingFileHandler",
			"getLoggingStreamHandler",
			"removeLoggingHandler",
			"setVerbosityLevel"]

THREADS_IDENTIFIERS = {}

INDENT_LEVEL = 0

#**********************************************************************************************************************
#***	Logging classes and definitions.
#**********************************************************************************************************************
def _LogRecord_getAttribute(self, attribute):
	"""
	This definition overrides logging.LogRecord.__getattribute__ method
	in order to manipulate requested attributes values.

	:param attribute: Attribute name. ( String )
	:return: Modified method. ( Object )
	"""

	if attribute == "__dict__":
		threadIdent = threading.currentThread().ident
		if not threadIdent in THREADS_IDENTIFIERS:
			THREADS_IDENTIFIERS[threadIdent] = (threading.currentThread().name,
												hashlib.md5(threading.currentThread().name).hexdigest()[:8])
		object.__getattribute__(self, attribute)["threadName"] = THREADS_IDENTIFIERS[threadIdent][1]
		return object.__getattribute__(self, attribute)
	else:
		return object.__getattribute__(self, attribute)

logging.LogRecord.__getattribute__ = _LogRecord_getAttribute

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_DEFAULT_FORMATTER = logging.Formatter("%(levelname)-8s: %(message)s")
LOGGING_EXTENDED_FORMATTER = logging.Formatter("%(asctime)s - %(threadName)s - %(levelname)-8s: %(message)s")
LOGGING_STANDARD_FORMATTER = logging.Formatter()

TRACER_LOGGING_FUNCTION = LOGGER.info

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Streamer(object):
	"""
	This class is intented to be used as a stream object for :class:`logging.StreamHandler` logging handler. 
	"""

	def __init__(self, stream=None):
		"""
		This method initializes the class.

		:param stream: Stream object. ( Object )
		"""

		self.__stream = []

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def stream(self):
		"""
		This method is the property for **self.__stream** attribute.

		:return: self.__stream. ( List )
		"""

		return self.__stream

	@stream.setter
	def stream(self, value):
		"""
		This method is the setter method for **self.__stream** attribute.

		:param value: Attribute value. ( List )
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("stream", value)
		self.__stream = value

	@stream.deleter
	def stream(self):
		"""
		This method is the deleter method for **self.__stream** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "stream"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def write(self, message):
		"""
		This method provides write ability to the class.

		:param message: Current message. ( String )
		"""

		self.__stream.append(message)

	def flush(self):
		"""
		This method flushes the current stream.
		"""

		pass

class StandardOutputStreamer(object):
	"""
	| This class is a redirection object intented to be used for :data:`sys.stdout` and :data:`sys.stderr` streams.
	| Logging messages will be written to given logger handlers.
	"""

	def __init__(self, logger):
		"""
		This method initializes the class.

		:param logger: Logger. ( Object )
		"""

		self.__logger = logger

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def logger(self):
		"""
		This method is the property for **self.__logger** attribute.

		:return: self.__logger. ( Logger )
		"""

		return self.__logger

	@logger.setter
	def logger(self, value):
		"""
		This method is the setter method for **self.__logger** attribute.

		:param value: Attribute value. ( Logger )
		"""

		raise Exception("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "logger"))

	@logger.deleter
	def logger(self):
		"""
		This method is the deleter method for **self.__logger** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "logger"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def write(self, message):
		"""
		This method writes given message to logger handlers.

		:param message: Message. ( String )
		:return: Method success. ( Boolean )
		"""

		for handler in self.__logger.__dict__["handlers"]:
			handler.stream.write(message)
		return True

def indentMessage(message):
	"""
	This definition idents given message using the attr`INDENT_LEVEL` attribute value.

	:param message: Message to indent. ( String )
	:return: indented message. ( String )
	"""

	return "{0}{1}".format(" " * 4 * INDENT_LEVEL, message)

def tracer(object):
	"""
	| This decorator is used for execution tracing.
	| Any method / definition decorated will have it's execution traced through debug messages.
	| Both object entry and exit are logged.
	
	Entering in an object::
		
		INFO    : ---> foundations.environment.getUserApplicationDataDirectory() <<<---
		
	Exiting from an object::
		
		INFO   : <--- foundations.environment.getSystemApplicationDataDirectory() ^ '...' --->
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	@functools.partial(foundations.trace.validateTracer, object)
	def tracerWrapper(*args, **kwargs):
		"""
		This decorator is used for execution tracing.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
		"""

		global INDENT_LEVEL

		traceName = foundations.trace.getTraceName(object)

		code = object.func_code
		argsCount = code.co_argcount
		argsNames = code.co_varnames[:argsCount]
		functionDefaults = object.func_defaults or list()
		argsDefaults = dict(zip(argsNames[-len(functionDefaults):], functionDefaults))

		positionalArgs = map(foundations.trace.formatArgument, zip(argsNames, args))
		defaultedArgs = [foundations.trace.formatArgument((name, argsDefaults[name])) \
						for name in argsNames[len(args):] if name not in kwargs]
		namelessArgs = map(repr, args[argsCount:])
		keywordArgs = map(foundations.trace.formatArgument, kwargs.items())
		TRACER_LOGGING_FUNCTION(indentMessage("---> {0}({1}) <---".format(traceName,
																", ".join(itertools.chain(positionalArgs,
																						defaultedArgs,
																						namelessArgs,
																						keywordArgs)))))

		INDENT_LEVEL += 1
		value = object(*args, **kwargs)
		INDENT_LEVEL -= 1

		TRACER_LOGGING_FUNCTION(indentMessage("<--- {0} ^ {1} --->".format(traceName, repr(value))))

		return value

	return tracerWrapper

def installLogger(logger=None, module=None):
	"""
	This definition installs given logger in given module or default logger in caller introspected module.

	:param logger: Logger to install. ( Logger )
	:param module: Module. ( Module )
	:return: Logger. ( Logger )
	"""

	logger = logging.getLogger(Constants.logger) if logger is None else logger
	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])
	setattr(module, "LOGGER", logger)

	foundations.trace.registerModule(module)

	return logger

def uninstallLogger(logger=None, module=None):
	"""
	This definition uninstalls given logger in given module or default logger in caller introspected module.

	:param logger: Logger to uninstall. ( Logger )
	:param module: Module. ( Module )
	:return: Definition success. ( Boolean )
	"""

	logger = logging.getLogger(Constants.logger) if logger is None else logger
	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])
	hasattr(module, "LOGGER") and delattr(module, "LOGGER")
	return True

def getLoggingConsoleHandler(logger=None, formatter=LOGGING_DEFAULT_FORMATTER):
	"""
	This definition adds a logging console handler to given logger or default logger.

	:param logger: Logger to add the handler to. ( Logger )
	:param formatter: Handler formatter. ( F )
	:return: Added handler. ( Handler )
	"""

	logger = LOGGER if logger is None else logger
	loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
	loggingConsoleHandler.setFormatter(formatter)
	logger.addHandler(loggingConsoleHandler)
	return loggingConsoleHandler

def getLoggingFileHandler(logger=None, file=None, formatter=LOGGING_DEFAULT_FORMATTER):
	"""
	This definition adds a logging file handler to given logger or default logger using given file.

	:param logger: Logger to add the handler to. ( Logger )
	:param file: File to verbose into. ( String )
	:param formatter: Handler formatter. ( Formatter )
	:return: Added handler. ( Handler )
	"""

	logger = LOGGER if logger is None else logger
	file = tempfile.NamedTemporaryFile().name if file is None else file
	loggingFileHandler = logging.FileHandler(file)
	loggingFileHandler.setFormatter(formatter)
	logger.addHandler(loggingFileHandler)
	return loggingFileHandler

def getLoggingStreamHandler(logger=None, formatter=LOGGING_DEFAULT_FORMATTER):
	"""
	This definition adds a logging stream handler to given logger or default logger using given file.

	:param logger: Logger to add the handler to. ( Logger )
	:param file: File to verbose into. ( String )
	:param formatter: Handler formatter. ( Formatter )
	:return: Added handler. ( Handler )
	"""

	logger = LOGGER if logger is None else logger
	loggingStreamHandler = logging.StreamHandler(Streamer())
	loggingStreamHandler.setFormatter(formatter)
	logger.addHandler(loggingStreamHandler)
	return loggingStreamHandler

def removeLoggingHandler(handler, logger=None):
	"""
	This definition removes given logging handler from given logger.

	:param handler: Handler. ( Handler )
	:param logger: Handler logger. ( Logger )
	:return: Definition success. ( Boolean )
	"""

	logger = LOGGER if logger is None else logger
	logger.handlers and LOGGER.debug("> Stopping handler: '{0}'.".format(handler))
	logger.removeHandler(handler)
	return True

def setVerbosityLevel(verbosityLevel=3, logger=None):
	"""
	This definition defines logging verbosity level.

	Available verbosity levels::

		0: Critical.
		1: Error.
		2: Warning.
		3: Info.
		4: Debug.

	:param verbosityLevel: Verbosity level. ( Integer )
	:param logger: Logger to set the verbosity level to. ( Logger )
	:return: Definition success. ( Boolean )
	"""

	logger = LOGGER if logger is None else logger
	if verbosityLevel == 0:
		logger.setLevel(logging.CRITICAL)
		logging.disable(logging.ERROR)
	elif verbosityLevel == 1:
		logger.setLevel(logging.ERROR)
		logging.disable(logging.WARNING)
	elif verbosityLevel == 2:
		logger.setLevel(logging.WARNING)
		logging.disable(logging.INFO)
	elif verbosityLevel == 3:
		logger.setLevel(logging.INFO)
		logging.disable(logging.DEBUG)
	elif verbosityLevel == 4:
		logger.setLevel(logging.DEBUG)
		logging.disable(logging.NOTSET)
	return True
