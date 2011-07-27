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
	This definition provides overall verbosity levels through an integer.

	@param verbosityLevel: Verbosity level. ( Integer )
	@return: Definition success. ( Boolean )
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
	This is the StandardMessageHook class.
	"""

	def __init__(self, logger):
		"""
		This method initializes the class.

		@param logger: LOGGER. ( Object )
		"""

		self.__logger = logger

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def logger(self):
		"""
		This method is the property for the _logger attribute.

		@return: self.__logger. ( Object )
		"""

		return self.__logger

	@logger.setter
	def logger(self, value):
		"""
		This method is the setter method for the _logger attribute.

		@param value: Attribute value. ( Object )
		"""

		raise Exception("'{0}' attribute is read only!".format("logger"))

	@logger.deleter
	def logger(self):
		"""
		This method is the deleter method for the _logger attribute.
		"""

		raise Exception("'{0}' attribute is not deletable!".format("logger"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	def write(self, message):
		"""
		This method logs the current stdout message.

		@param message: Message. ( String )
		@return: Method success. ( Boolean )
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
	This definition returns the requested frame.

	@param level: Frame index. ( Object )
	@return: Frame. ( Frame )
	"""

	return sys._getframe(index)

def getCodeLayerName():
	"""
	This definition returns the frame code layer name.

	@return: Code layer name. ( String )
	"""

	for frameIndex in range(len(inspect.stack())):
		frame = getFrame(frameIndex)
		if frame.f_code.co_name not in IGNORED_CODE_LAYERS:
			return frame.f_code.co_name
	return UNDEFINED_CODE_LAYER

def getModule(object):
	"""
	This definition returns the frame Module name.

	@param object: Object. ( Object )
	@return: Frame Module. ( Module )
	"""

	return inspect.getmodule(object)

def getObjectName(object):
	"""
	This definition returns the object name related to the provided frame.

	@param object: Object. ( Object )
	@return: Object name. ( String )
	"""

	moduleName = getModule(inspect.getmodule(object)).__name__
	codeLayerName = getCodeLayerName()
	codeLayerName = codeLayerName != UNDEFINED_CODE_LAYER and codeLayerName != "<module>" and "{0}.".format(codeLayerName) or ""

	return hasattr(object, "__name__") and "{0} | {1}{2}()".format(moduleName, codeLayerName, object.__name__) or UNDEFINED_OBJECT

def executionTrace(object):
	"""
	This decorator is used for function tracing.

	@param object: Object to decorate. ( Object )
	@return: Object. ( Object )
	"""

	origin = getObjectName(object)

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used for function tracing.

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
	This is the Structure class.
	"""

	@executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		@param kwargs: Key / value pairs. ( Key / value pairs )
		"""

		self.__dict__.update(kwargs)

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
