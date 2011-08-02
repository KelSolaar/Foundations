#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**core.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package core objects. Those objects are mostly related to logging and execution tracing.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import hashlib
import inspect
import logging
import sys
import threading

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
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

#***********************************************************************************************
#***	Logging classes and definitions.
#***********************************************************************************************
THREADS_IDENTIFIERS = {}
"""Threads identifiers module cache: '{ '**Thread identity**' : ('**Thread name**', '**Thread hash**')}' ( Dictionary )"""

def _LogRecord_getAttribute(self, name):
	"""
	This definition overrides logging.LogRecord.__getattribute__ method in order to manipulate requested attributes values.

	:param name: Attribute name. ( String )
	:return: Modified method. ( Object )
	"""

	if name == "__dict__":
		threadIdent = threading.currentThread().ident
		if not threadIdent in THREADS_IDENTIFIERS.keys():
			THREADS_IDENTIFIERS[threadIdent] = (threading.currentThread().name, hashlib.md5(threading.currentThread().name).hexdigest()[:8])
		object.__getattribute__(self, name)["threadName"] = THREADS_IDENTIFIERS[threadIdent][1]
		return object.__getattribute__(self, name)
	else:
		return object.__getattribute__(self, name)
logging.LogRecord.__getattribute__ = _LogRecord_getAttribute

def setVerbosityLevel(verbosityLevel):
	"""
	This definition defines logging verbosity level.

	Available verbosity levels::

		- 0: Critical.
		- 1: Error.
		- 2: Warning.
		- 3: Info.
		- 4: Debug.

	:param verbosityLevel: Verbosity level. ( Integer )
	:return: Definition success. ( Boolean )
	"""

	if verbosityLevel == 0:
		LOGGER.setLevel(logging.CRITICAL)
	elif verbosityLevel == 1:
		LOGGER.setLevel(logging.ERROR)
	elif verbosityLevel == 2:
		LOGGER.setLevel(logging.WARNING)
	elif verbosityLevel == 3:
		LOGGER.setLevel(logging.INFO)
	elif verbosityLevel == 4:
		LOGGER.setLevel(logging.DEBUG)
	return True

class StandardMessageHook(object):
	"""
	| This class is a redirection object intented to be used for **sys.stdout** (http://docs.python.org/library/sys.html#sys.stdout) and **sys.stderr** (http://docs.python.org/library/sys.html#sys.stderr) streams.
	| Logging messages will be written to provided logger handlers.
	"""

	def __init__(self, logger):
		"""
		This method initializes the class.

		:param logger: Logger. ( Object )
		"""

		self.__logger = logger

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		raise Exception("'{0}' attribute is read only!".format("logger"))

	@logger.deleter
	def logger(self):
		"""
		This method is the deleter method for **self.__logger** attribute.
		"""

		raise Exception("'{0}' attribute is not deletable!".format("logger"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	def write(self, message):
		"""
		This method writes provided message to logger handlers.

		:param message: Message. ( String )
		:return: Method success. ( Boolean )
		"""

		for handler in self.__logger.__dict__["handlers"]:
			handler.stream.write(message)
		return True

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

LOGGING_DEFAULT_FORMATTER = logging.Formatter("%(levelname)-8s: %(message)s")
LOGGING_EXTENDED_FORMATTER = logging.Formatter("%(asctime)s - %(threadName)s - %(levelname)-8s: %(message)s")
LOGGING_STANDARD_FORMATTER = logging.Formatter()

IGNORED_CODE_LAYERS = ("getFrame",
					"getCodeLayerName",
					"getObjectName",
					"executionTrace",
					"wrapper")

UNDEFINED_CODE_LAYER = "UndefinedCodeLayer"
UNDEFINED_MODULE = "UndefinedModule"
UNDEFINED_OBJECT = "UndefinedObject"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
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
	
	:note: Candidates names matching any :attr:`foundations.core.IGNORED_CODE_LAYERS` members will be skipped. If no appropriate candidate name is found, then :attr:`foundations.core.UNDEFINED_CODE_LAYER` is returned.
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
	This definition returns provided object module name.

	:param object: Object. ( Object )
	:return: Frame Module. ( Module )
	"""

	return inspect.getmodule(object)

def getObjectName(object):
	"""
	This definition returns object name composited with current execution frame.
	
	Examples names::

		- 'foundations.common | getUserApplicationDatasDirectory()'.
		- '__main__ | _setUserApplicationDatasDirectory()'.
		- '__main__ | Preferences.__init__()'.
		- 'UndefinedObject'.

	:param object: Object. ( Object )
	:return: Object name. ( String )
	"""
	module = getModule(object)
	moduleName = module and module.__name__ or UNDEFINED_MODULE
	codeLayerName = getCodeLayerName()
	codeLayerName = codeLayerName != UNDEFINED_CODE_LAYER and codeLayerName != "<module>" and "{0}.".format(codeLayerName) or ""

	return hasattr(object, "__name__") and "{0} | {1}{2}()".format(moduleName, codeLayerName, object.__name__) or UNDEFINED_OBJECT

def executionTrace(object):
	"""
	| This decorator is used for execution tracing.
	| Any method / definition decorated will have it's execution traced through debug messages.
	| Both object entry and exit are logged.
	
	Entering in an object::
		
		DEBUG   : --->>> 'foundations.common | getUserApplicationDatasDirectory()' <<<---
		
	Exiting from an object::
		
		DEBUG   : --->>> 'foundations.common | getSystemApplicationDatasDirectory()' <<<---
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	origin = getObjectName(object)

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used for execution tracing.

		:param *args: Arguments. ( * )
		:param **kwargs: Arguments. ( * )
		:return: Object. ( Object )
		"""

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("--->>> '{0}' <<<---".format(origin))

		value = object(*args, **kwargs)

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("---<<< '{0}' >>>---".format(origin))

		return value

	return function

class Structure(object):
	"""
	This class creates an object similar to C/C++ structured type.
	
	Usage:
		
		>>> person = Structure(firstName="Doe", lastName="John", gender="male")
		>>> person.firstName
		'Doe'

	"""

	@executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		self.__dict__.update(kwargs)

