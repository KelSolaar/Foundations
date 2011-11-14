#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**core.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package core objects.
	Those objects are mostly related to logging and execution tracing.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import hashlib
import inspect
import linecache
import logging
import sys
import threading
from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["THREADS_IDENTIFIERS",
			"setVerbosityLevel",
			"StandardMessageHook",
			"LOGGER",
			"LOGGING_DEFAULT_FORMATTER",
			"LOGGING_EXTENDED_FORMATTER",
			"LOGGING_STANDARD_FORMATTER",
			"IGNORED_CODE_LAYERS",
			"UNDEFINED_CODE_LAYER",
			"UNDEFINED_MODULE",
			"UNDEFINED_OBJECT",
			"getFrame",
			"getCodeLayerName",
			"getModule",
			"getObjectName",
			"extractStack",
			"executionTrace",
			"memoize",
			"NestedAttribute",
			"Structure",
			"OrderedStructure",
			"Lookup"]

#**********************************************************************************************************************
#***	Logging classes and definitions.
#**********************************************************************************************************************
THREADS_IDENTIFIERS = {}

def _LogRecord_getAttribute(self, attribute):
	"""
	This definition overrides logging.LogRecord.__getattribute__ method
	in order to manipulate requested attributes values.

	:param attribute: Attribute name. ( String )
	:return: Modified method. ( Object )
	"""

	if attribute == "__dict__":
		threadIdent = threading.currentThread().ident
		if not threadIdent in THREADS_IDENTIFIERS.keys():
			THREADS_IDENTIFIERS[threadIdent] = (threading.currentThread().name,
												hashlib.md5(threading.currentThread().name).hexdigest()[:8])
		object.__getattribute__(self, attribute)["threadName"] = THREADS_IDENTIFIERS[threadIdent][1]
		return object.__getattribute__(self, attribute)
	else:
		return object.__getattribute__(self, attribute)
logging.LogRecord.__getattribute__ = _LogRecord_getAttribute

def setVerbosityLevel(verbosityLevel):
	"""
	This definition defines logging verbosity level.

	Available verbosity levels::

		0: Critical.
		1: Error.
		2: Warning.
		3: Info.
		4: Debug.

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

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
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

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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

def getObjectName(object):
	"""
	This definition returns object name composited with current execution frame.
	
	Examples names::

		'foundations.common | getUserApplicationDataDirectory()'.
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
	|The code is similar to :def:`traceback.extract_stack` except that it allows frames to be excluded
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
		
		DEBUG   : --->>> 'foundations.common | getUserApplicationDataDirectory()' <<<---
		
	Exiting from an object::
		
		DEBUG   : --->>> 'foundations.common | getSystemApplicationDataDirectory()' <<<---
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	origin = getObjectName(object)

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used for execution tracing.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		:return: Object. ( Object )
		"""

		__stackTraceFrameTag__ = Constants.excludeTaggedFramesFromStackTrace

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("--->>> '{0}' <<<---".format(origin))

		value = object(*args, **kwargs)

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("---<<< '{0}' >>>---".format(origin))

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
		def function(*args):
			"""
			This decorator is used for object memoization.
	
			:param \*args: Arguments. ( \* )
			:return: Object. ( Object )
			"""

			if args not in cache:
				cache[args] = object(*args)
			return cache[args]
		return function
	return wrapper

class NestedAttribute(object):
	"""
	This class is an helper object providing methods to manipulate nested attributes.
	
	Usage:
		
		>>> nest = NestedAttribute()
		>>> nest.my.nested.attribute = "Value"
		>>> nest.my.nested.attribute
		Value
		>>> nest.another.very.deeply.nested.attribute = 64
		>>> nest.another.very.deeply.nested.attribute
		64
	"""

	@executionTrace
	def __getattr__(self, attribute):
		"""
		This method returns requested attribute.
	
		:param attribute: Attribute name. ( String )
		:return: Attribute. ( Object )
		"""

		self.__dict__[attribute] = NestedAttribute()
		return self.__dict__[attribute]

	@executionTrace
	def __setattr__(self, attribute, value):
		"""
		This method sets given attribute with given value.
	
		:param attribute: Attribute name. ( String )
		:param name: Attribute value. ( Object )
		"""

		namespaces = attribute.split(".")
		object.__setattr__(reduce(object.__getattribute__, namespaces[:-1], self), namespaces[-1], value)

	@executionTrace
	def __delattr__(self, attribute):
		"""
		This method deletes given attribute with.
	
		:param attribute: Attribute name. ( String )
		"""

		namespaces = attribute.split(".")
		object.__delattr__(reduce(object.__getattribute__, namespaces[:-1], self), namespaces[-1])

class Structure(dict):
	"""
	This class creates an object similar to C/C++ structured type.
	
	Usage:
		
		>>> person = Structure(firstName="Doe", lastName="John", gender="male")
		>>> person.firstName
		'Doe'
		>>> person.keys()
		['gender', 'firstName', 'lastName']
		>>> person["gender"]
		'male'
		>>> del(person["gender"])
		>>> person["gender"]
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		KeyError: 'gender'
		>>> person.gender
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		AttributeError: 'Structure' object has no attribute 'gender'
	"""

	@executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		# :note: The following statement ensures that attributes defined in parent classes are propagated.
		kwargs.update(self.__dict__)

		dict.__init__(self, **kwargs)
		self.__dict__ = self

class OrderedStructure(OrderedDict):
	"""
	| This class creates an object similar to C/C++ structured type.
	| Contrary to the :class:`Structure` since this class inherits from :class:`collections.OrderedDict`,
	its content is ordered.

	Usage:

		>>> people = OrderedStructure([("personA", "John"), ("personB", "Jane"), ("personC", "Luke")])
		>>> people
		OrderedStructure([('personA', 'John'), ('personB', 'Jane'), ('personC', 'Luke')])
		>>> people.keys()
		['personA', 'personB', 'personC']
		>>> people.personA
		'John'
		>>> del(people["personA"])
		>>> people["personA"]
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		KeyError: 'personA'
		>>> people.personA
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		AttributeError: 'OrderedStructure' object has no attribute 'personA'
		>>> people.personB = "Kate"
		>>> people["personB"]
		'Kate'
		>>> people.personB
		'Kate'
	"""

	@executionTrace
	def __init__(self, *args, **kwargs):
		"""
		This method initializes the class.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		OrderedDict.__init__(self, *args, **kwargs)

	@executionTrace
	def __setitem__(self, key, value, *args, **kwargs):
		"""
		This method sets a key and sibling attribute with given value.

		:param key.: Key. ( Object )
		:param value.: Value. ( Object )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		OrderedDict.__setitem__(self, key, value, *args, **kwargs)
		OrderedDict.__setattr__(self, key, value)

	@executionTrace
	def __delitem__(self, key, *args, **kwargs):
		"""
		This method deletes both key and sibling attribute.

		:param key.: Key. ( Object )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		OrderedDict.__delitem__(self, key, *args, **kwargs)
		OrderedDict.__delattr__(self, key)

	@executionTrace
	def __setattr__(self, attribute, value):
		"""
		This method sets both key and sibling attribute with given value.

		:param attribute.: Attribute. ( Object )
		:param value.: Value. ( Object )
		"""

		if hasattr(self, "_OrderedDict__root") and hasattr(self, "_OrderedDict__map"):
			if self._OrderedDict__root:
				OrderedDict.__setitem__(self, attribute, value)
		OrderedDict.__setattr__(self, attribute, value)

	@executionTrace
	def __delattr__(self, attribute):
		"""
		This method deletes both key and sibling attribute.

		:param attribute.: Attribute. ( Object )
		"""

		if hasattr(self, "_OrderedDict__root") and hasattr(self, "_OrderedDict__map"):
			if self._OrderedDict__root:
				OrderedDict.__delitem__(self, attribute)
		OrderedDict.__delattr__(self, attribute)

class Lookup(dict):
	"""
	This class extend dict type to provide a lookup by value(s).

	Usage:

		>>> person = Lookup(firstName="Doe", lastName="John", gender="male")
		>>> person.getFirstKeyFromValue("Doe")
		'firstName'
		>>> persons = foundations.core.Lookup(John="Doe", Jane="Doe", Luke="Skywalker")
		>>> persons.getKeysFromValue("Doe")
		['Jane', 'John']
	"""

	@executionTrace
	def getFirstKeyFromValue(self, value):
		"""
		This method gets the first key from given value.

		:param value.: Value. ( Object )
		:return: Key. ( Object )
		"""

		for item in self.items():
			if item[1] == value:
				return item[0]

	@executionTrace
	def getKeysFromValue(self, value):
		"""
		This method gets the keys from given value.

		:param value.: Value. ( Object )
		:return: Keys. ( Object )
		"""

		return [item[0] for item in self.items() if item[1] == value]
