#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**library.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module provides objects for C / C++ libraries binding.

**Others:**

"""

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
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LibraryHook(core.Structure):
	"""
	This class represents a library hook used by the :class:`foundations.library.Library` class to bind target library functions.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.
		
		Example::
			
			LibraryHook(name="FreeImage_GetVersion", argumentsTypes=None, returnValue=ctypes.c_char_p),

		:param name: Name of the target library function to bind.. ( String )
		:param argumentsTypes: Required function arguments type (Refer to Python `ctypes - 15.17.1.7 <http://docs.python.org/library/ctypes.html#specifying-the-required-argument-types-function-prototypes>`_ module for more informations). ( List )
		:param returnValue: Function return type (Refer to Python `ctypes - 15.17.1.8 <http://docs.python.org/library/ctypes.html#return-types>`_ module for more informations). ( Object )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__dict__.update(kwargs)

class Library(object):
	"""
	This class provides methods to bind a C / C++ Library.
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

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Arguments. ( \* )
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

		:param libraryPath: Library path. ( String )
		:param functions: Binding functions list. ( Tuple )
		"""

		if hasattr(self.librariesInstances[libraryPath], "_Library__libraryInstantiated"):
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
		This method is the property for **self.__libraryInstantiated** attribute.

		:return: self.__libraryInstantiated. ( String )
		"""

		return self.__libraryInstantiated

	@libraryInstantiated.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def libraryInstantiated(self, value):
		"""
		This method is the setter method for **self.__libraryInstantiated** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not settable!".format("libraryInstantiated"))

	@libraryInstantiated.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryInstantiated(self):
		"""
		This method is the deleter method for **self.__libraryInstantiated** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("libraryInstantiated"))

	@property
	def libraryPath(self):
		"""
		This method is the property for **self.__libraryPath** attribute.

		:return: self.__libraryPath. ( String )
		"""

		return self.__libraryPath

	@libraryPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def libraryPath(self, value):
		"""
		This method is the setter method for **self.__libraryPath** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("libraryPath", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("libraryPath", value)
		self.__libraryPath = value

	@libraryPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryPath(self):
		"""
		This method is the deleter method for **self.__libraryPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("libraryPath"))

	@property
	def functions(self):
		"""
		This method is the property for **self.__functions** attribute.

		:return: self.__functions. ( String )
		"""

		return self.__functions

	@functions.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def functions(self, value):
		"""
		This method is the setter method for **self.__functions** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("functions", value)
		self.__functions = value

	@functions.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def functions(self):
		"""
		This method is the deleter method for **self.__functions** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("functions"))

	@property
	def library(self):
		"""
		This method is the property for **self.__library** attribute.

		:return: self.__library. ( Object )
		"""

		return self.__library

	@library.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def library(self, value):
		"""
		This method is the setter method for **self.__library** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__library = value

	@library.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def library(self):
		"""
		This method is the deleter method for **self.__library** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("library"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def bindFunction(self, function):
		"""
		This method binds a function.

		:param function: Function to bind. ( Tuple )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Binding '{0}' library '{1}' function.".format(self.__class__.__name__, function.name))

		functionObject = getattr(self.__library, function.name)
		setattr(self, function.name, functionObject)
		if function.argumentsTypes:
			functionObject.argtypes = function.argumentsTypes
		if function.returnValue:
			functionObject.restype = function.returnValue
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, AttributeError)
	def bindLibrary(self):
		"""
		This method binds the Library.

		:return: Method success. ( Boolean )
		"""

		if self.__functions:
			for function in self.__functions:
				self.bindFunction(function)
		return True

