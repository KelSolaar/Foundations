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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import ctypes
import os
import platform

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.dataStructures
import foundations.exceptions
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LibraryHook", "Library"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LibraryHook(foundations.dataStructures.Structure):
	"""
	This class represents a library hook used by the :class:`Library` class to bind target library functions.
	"""

	def __init__(self, **kwargs):
		"""
		This method initializes the class.
		
		Usage::
			
			LibraryHook(name="FreeImage_GetVersion", argumentsTypes=None, returnValue=ctypes.c_char_p)

		:param name: Name of the target library function to bind. ( String )
		:param argumentsTypes: Required function arguments type (Refer to Python `ctypes - 15.17.1.7
			<http://docs.python.org/library/ctypes.html#specifying-the-required-argument-types-function-prototypes>`_
			module for more informations). ( List )
		:param returnValue: Function return type (Refer to Python `ctypes - 15.17.1.8
			<http://docs.python.org/library/ctypes.html#return-types>`_ module for more informations). ( Object )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Library(object):
	"""
	| This class provides methods to bind a C / C++ Library.
	| The class is a singleton and will bind only one time a given library.
		Each unique library instance is stored in :attr:`Library.instances` attribute
		and get returned if the library is requested again through a new instantiation.
	"""

	__instances = {}
	"""Libraries instances: Each library is instanced once and stored in this attribute. ( Dictionary )"""

	callback = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p)
	"""callback: Defines library callback default function.	( ctypes.CFUNCTYPE )"""

	@foundations.exceptions.handleExceptions(foundations.exceptions.LibraryInstantiationError)
	def __new__(cls, *args, **kwargs):
		"""
		This method is the constructor of the class.
		
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Class instance. ( Library )
		"""

		path = foundations.common.getFirstItem(args)
		if foundations.common.pathExists(path):
			if not path in cls._Library__instances:
				cls._Library__instances[path] = object.__new__(cls)
			return cls._Library__instances[path]
		else:
			raise foundations.exceptions.LibraryInstantiationError(
			"{0} | '{1}' library path doesn't exists!".format(cls.__class__.__name__, path))

	@foundations.exceptions.handleExceptions(foundations.exceptions.LibraryInitializationError)
	def __init__(self, path, functions=None, bindLibrary=True):
		"""
		This method initializes the class.
		
		Usage::
			
			>>> path = "FreeImage.dll"
			>>> functions = (LibraryHook(name="FreeImage_GetVersion", argumentsTypes=None, returnValue=ctypes.c_char_p),)
			>>> library = Library(path, functions)
			>>> library.FreeImage_GetVersion()
			3.13.1

		:param path: Library path. ( String )
		:param functions: Binding functions list. ( Tuple )
		:param bindLibrary: Library will be binded on initialization. ( Boolean )
		"""

		if hasattr(self.instances[path], "_Library__initialized"):
			return

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__initialized = True

		self.__path = None
		self.path = path
		self.__functions = None
		self.functions = functions

		self.__library = None

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			loadingFunction = ctypes.windll
		else:
			loadingFunction = ctypes.cdll

		if self.path:
			self.__library = loadingFunction.LoadLibrary(path)
		else:
			raise foundations.exceptions.LibraryInitializationError("{0} | '{1}' library not found!".format(
			self.__class__.__name__, path))

		bindLibrary and self.bindLibrary()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def instances(self):
		"""
		This method is the property for **self.__instances** attribute.

		:return: self.__instances. ( WeakValueDictionary )
		"""

		return self.__instances

	@instances.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def instances(self, value):
		"""
		This method is the setter method for **self.__instances** attribute.

		:param value: Attribute value. ( WeakValueDictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "instances"))

	@instances.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def instances(self):
		"""
		This method is the deleter method for **self.__instances** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "instances"))

	@property
	def initialized(self):
		"""
		This method is the property for **self.__initialized** attribute.

		:return: self.__initialized. ( String )
		"""

		return self.__initialized

	@initialized.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def initialized(self, value):
		"""
		This method is the setter method for **self.__initialized** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "initialized"))

	@initialized.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def initialized(self):
		"""
		This method is the deleter method for **self.__initialized** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "initialized"))

	@property
	def path(self):
		"""
		This method is the property for **self.__path** attribute.

		:return: self.__path. ( String )
		"""

		return self.__path

	@path.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"path", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("path", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

	@property
	def functions(self):
		"""
		This method is the property for **self.__functions** attribute.

		:return: self.__functions. ( Tuple )
		"""

		return self.__functions

	@functions.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def functions(self, value):
		"""
		This method is the setter method for **self.__functions** attribute.

		:param value: Attribute value. ( Tuple )
		"""

		if value is not None:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("functions", value)
			for element in value:
				assert type(element) is LibraryHook, "'{0}' attribute: '{1}' type is not 'LibraryHook'!".format(
				"functions", element)
		self.__functions = value

	@functions.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def functions(self):
		"""
		This method is the deleter method for **self.__functions** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "functions"))

	@property
	def library(self):
		"""
		This method is the property for **self.__library** attribute.

		:return: self.__library. ( Object )
		"""

		return self.__library

	@library.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def library(self, value):
		"""
		This method is the setter method for **self.__library** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__library = value

	@library.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def library(self):
		"""
		This method is the deleter method for **self.__library** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "library"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def bindFunction(self, function):
		"""
		This method binds given function to a class object attribute.

		Usage::
			
			>>> path = "FreeImage.dll"
			>>> function = LibraryHook(name="FreeImage_GetVersion", argumentsTypes=None, returnValue=ctypes.c_char_p)
			>>> library = Library(path, bindLibrary=False)
			>>> library.bindFunction(function)
			True
			>>> library.FreeImage_GetVersion()
			3.13.1

		:param function: Function to bind. ( LibraryHook )
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

	def bindLibrary(self):
		"""
		This method binds the Library using functions registered in the **self.__functions** attribute.

		Usage::
			
			>>> path = "FreeImage.dll"
			>>> functions = (LibraryHook(name="FreeImage_GetVersion", argumentsTypes=None, returnValue=ctypes.c_char_p),)
			>>> library = Library(path, functions, bindLibrary=False)
			>>> library.bindLibrary()
			True
			>>> library.FreeImage_GetVersion()
			3.13.1

		:return: Method success. ( Boolean )
		"""

		if self.__functions:
			for function in self.__functions:
				self.bindFunction(function)
		return True
