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
**library.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	C / c++ binding Library Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import ctypes
import logging
import os
import platform

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LibraryHook(core.Structure):
	"""
	This is the LibraryHook class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		@param kwargs: name, affixe, argumentstype, returnvalue. ( Key / value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__dict__.update(kwargs)

class Library(object):
	"""
	This class provides methods to bind a c / c++ Library.
	"""

	librariesInstances = {}

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		callback = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p)
	else:
		callback = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.LibraryInstantiationError)
	def __new__(self, *args, **kwargs):
		"""
		This method is the constructor of the class.

		@param *args: Arguments. ( * )
		@param **kwargs: Arguments. ( * )
		"""

		libraryPath = args[0]
		if os.path.exists(libraryPath):
			if not args[0] in self.librariesInstances.keys():
				self.librariesInstances[args[0]] = object.__new__(self)
			return self.librariesInstances[args[0]]
		else:
			raise foundations.exceptions.LibraryInstantiationError("'{0}' library path doesn't exists!".format(libraryPath))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.LibraryInitializationError)
	def __init__(self, libraryPath, functions=None):
		"""
		This method initializes the class.

		@param libraryPath: Library path. ( String )
		@param functions: Binding functions list. ( Tuple )
		"""

		if hasattr(self.librariesInstances[libraryPath], "_libraryInstantiated"):
			return

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__libraryInstantiated = True

		self.__libraryPath = None
		self.libraryPath = libraryPath
		self.__functions = None
		self.functions = functions

		self.__library = None

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			loadingFunction = ctypes.windll
		else:
			loadingFunction = ctypes.cdll

		if self.libraryPath:
			self.__library = loadingFunction.LoadLibrary(libraryPath)
		else:
			raise foundations.exceptions.LibraryInitializationError, "'{0}' library not found!".format(self.__class__.__name__)

		self.bindLibrary()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def libraryInstantiated(self):
		"""
		This method is the property for the _libraryInstantiated attribute.

		@return: self.__libraryInstantiated. ( String )
		"""

		return self.__libraryInstantiated

	@libraryInstantiated.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def libraryInstantiated(self, value):
		"""
		This method is the setter method for the _libraryInstantiated attribute.

		@param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not settable!".format("libraryInstantiated"))

	@libraryInstantiated.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryInstantiated(self):
		"""
		This method is the deleter method for the _libraryInstantiated attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("libraryInstantiated"))

	@property
	def libraryPath(self):
		"""
		This method is the property for the _libraryPath attribute.

		@return: self.__libraryPath. ( String )
		"""

		return self.__libraryPath

	@libraryPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def libraryPath(self, value):
		"""
		This method is the setter method for the _libraryPath attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("libraryPath", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("libraryPath", value)
		self.__libraryPath = value

	@libraryPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryPath(self):
		"""
		This method is the deleter method for the _libraryPath attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("libraryPath"))

	@property
	def functions(self):
		"""
		This method is the property for the _functions attribute.

		@return: self.__functions. ( String )
		"""

		return self.__functions

	@functions.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def functions(self, value):
		"""
		This method is the setter method for the _functions attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("functions", value)
		self.__functions = value

	@functions.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def functions(self):
		"""
		This method is the deleter method for the _functions attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("functions"))

	@property
	def library(self):
		"""
		This method is the property for the _library attribute.

		@return: self.__library. ( Object )
		"""

		return self.__library

	@library.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def library(self, value):
		"""
		This method is the setter method for the _library attribute.

		@param value: Attribute value. ( Object )
		"""

		self.__library = value

	@library.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def library(self):
		"""
		This method is the deleter method for the _library attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("library"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def bindFunction(self, function):
		"""
		This method bind a function.

		@param function: Function to bind. ( Tuple )
		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Binding '{0}' library '{1}' function.".format(self.__class__.__name__, function.name))

		returnType = function.returnValue
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			functionObject = getattr(self.__library, "{0}".format(function.name, function.affixe))
		else:
			functionObject = getattr(self.__library, function.name)
		setattr(self, function.name, functionObject)
		if returnType:
			functionObject.restype = returnType

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, AttributeError)
	def bindLibrary(self):
		"""
		This method bind the Library.

		@return: Method success. ( Boolean )
		"""

		if self.__functions:
			for function in self.__functions:
				self.bindFunction(function)
		return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
