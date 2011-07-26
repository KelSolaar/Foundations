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
**core.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Core Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Logging classes and definitions.
#***********************************************************************************************
def _LogRecord_getAttribute(self, name):
	if name == "__dict__":
		object.__getattribute__(self, name)["threadName"] = hashlib.md5(threading.currentThread().name).hexdigest()[:8]
		return object.__getattribute__(self, name)
	else:
		return object.__getattribute__(self, name)

logging.LogRecord.__getattribute__ = _LogRecord_getAttribute

def setVerbosityLevel(verbosityLevel):
	"""
	This Definition Provides Overall Verbosity Levels Through An Integer.

	@param verbosityLevel: Verbosity Level. ( Integer )
	@return: Definition Success. ( Boolean )		
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
	This Is The StandardMessageHook Class.
	"""

	def __init__(self, logger):
		"""
		This Method Initializes The Class.

		@param logger: LOGGER. ( Object )
		"""

		self.__logger = logger

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def logger(self):
		"""
		This Method Is The Property For The _logger Attribute.

		@return: self.__logger. ( Object )
		"""

		return self.__logger

	@logger.setter
	def logger(self, value):
		"""
		This Method Is The Setter Method For The _logger Attribute.
		
		@param value: Attribute Value. ( Object )
		"""

		raise Exception("'{0}' Attribute Is Read Only!".format("logger"))

	@logger.deleter
	def logger(self):
		"""
		This Method Is The Deleter Method For The _logger Attribute.
		"""

		raise Exception("'{0}' Attribute Is Not Deletable!".format("logger"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	def write(self, message):
		"""
		This Method Logs The Current StdOut Message.
		
		@param message: Message. ( String )
		@return: Method Success. ( Boolean )		
		"""

		for handler in self.__logger.__dict__["handlers"]:
			handler.stream.write(message)
		return True

#***********************************************************************************************
#***	Global variables.
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
UNDEFINED_OBJECT = "UndefinedObject"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def getFrame(index):
	"""
	This Definition Returns The Requested Frame.

	@param level: Frame Index. ( Object )
	@return: Frame. ( Frame )
	"""

	return sys._getframe(index)

def getCodeLayerName():
	"""
	This Definition Returns The Frame Code Layer Name.

	@return: Code Layer Name. ( String )
	"""

	for frameIndex in range(len(inspect.stack())):
		frame = getFrame(frameIndex)
		if frame.f_code.co_name not in IGNORED_CODE_LAYERS:
			return frame.f_code.co_name
	return UNDEFINED_CODE_LAYER

def getModule(object):
	"""
	This Definition Returns The Frame Module Name.

	@param object: Object. ( Object )
	@return: Frame Module. ( Module )
	"""

	return inspect.getmodule(object)

def getObjectName(object):
	"""
	This Definition Returns The Object Name Related To The Provided Frame.

	@param object: Object. ( Object )
	@return: Object Name. ( String )
	"""

	moduleName = getModule(inspect.getmodule(object)).__name__
	codeLayerName = getCodeLayerName()
	codeLayerName = codeLayerName != UNDEFINED_CODE_LAYER and codeLayerName != "<module>" and "{0}.".format(codeLayerName) or ""

	return hasattr(object, "__name__") and "{0} | {1}{2}()".format(moduleName, codeLayerName, object.__name__) or UNDEFINED_OBJECT

def executionTrace(object):
	"""
	This Decorator Is Used For Function Tracing.

	@param object: Object To Decorate. ( Object )
	@return: Object. ( Object )
	"""

	origin = getObjectName(object)

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This Decorator Is Used For Function Tracing.
		
		@param *args: Arguments. ( * )
		@param **kwargs: Arguments. ( * )
		@return: Object. ( Object )
		"""

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("--->>> '{0}' <<<---".format(origin))

		value = object(*args, **kwargs)

		LOGGER and LOGGER.__dict__["handlers"] != {} and LOGGER.debug("---<<< '{0}' >>>---".format(origin))

		return value

	return function

class Structure(object):
	"""
	This Is The Structure Class.
	"""

	@executionTrace
	def __init__(self, **kwargs):
		"""
		This Method Initializes The Class.

		@param kwargs: Key / Value Pairs. ( Key / Value Pairs )
		"""

		self.__dict__.update(kwargs)

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
