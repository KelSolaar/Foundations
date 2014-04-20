#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**library.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Provides objects for C / C++ libraries binding.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
import foundations.data_structures
import foundations.exceptions
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LibraryHook", "Library"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LibraryHook(foundations.data_structures.Structure):
	"""
	Defines a library hook used by the :class:`Library` class to bind target library functions.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.
		
		Usage::
			
			LibraryHook(name="FreeImage_GetVersion", arguments_types=None, return_value=ctypes.c_char_p)

		:param name: Name of the target library function to bind.
		:type name: unicode
		:param arguments_types: Required function arguments type (Refer to Python `ctypes - 15.17.1.7
			<http://docs.python.org/library/ctypes.html#specifying-the-required-argument-types-function-prototypes>`_
			module for more informations). ( List )
		:param return_value: Function return type (Refer to Python `ctypes - 15.17.1.8
			<http://docs.python.org/library/ctypes.html#return-types>`_ module for more informations). ( Object )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

class Library(object):
	"""
	| Defines methods to bind a C / C++ Library.
	| The class is a singleton and will bind only one time a given library.
		Each unique library instance is stored in :attr:`Library.instances` attribute
		and get returned if the library is requested again through a new instantiation.
	"""

	__instances = {}
	"""
	:param __instances: Libraries instances.
	:type __instances: dict
	"""

	callback = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p)
	"""
	:param callback: callback.
	:type callback: ctypes.CFUNCTYPE
	"""

	@foundations.exceptions.handle_exceptions(foundations.exceptions.LibraryInstantiationError)
	def __new__(cls, *args, **kwargs):
		"""
		Constructor of the class.
		
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Class instance.
		:rtype: Library
		"""

		path = foundations.common.get_first_item(args)
		if foundations.common.path_exists(path):
			if not path in cls._Library__instances:
				cls._Library__instances[path] = object.__new__(cls)
			return cls._Library__instances[path]
		else:
			raise foundations.exceptions.LibraryInstantiationError(
			"{0} | '{1}' library path doesn't exists!".format(cls.__class__.__name__, path))

	@foundations.exceptions.handle_exceptions(foundations.exceptions.LibraryInitializationError)
	def __init__(self, path, functions=None, bind_library=True):
		"""
		Initializes the class.
		
		Usage::
			
			>>> import ctypes 
			>>> path = "FreeImage.dll"
			>>> functions = (LibraryHook(name="FreeImage_GetVersion", arguments_types=None, return_value=ctypes.c_char_p),)
			>>> library = Library(path, functions)
			>>> library.FreeImage_GetVersion()
			'3.15.1'

		:param path: Library path.
		:type path: unicode
		:param functions: Binding functions list.
		:type functions: tuple
		:param bind_library: Library will be binded on initialization.
		:type bind_library: bool
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
			loading_function = ctypes.windll
		else:
			loading_function = ctypes.cdll

		if self.path:
			self.__library = loading_function.LoadLibrary(path)
		else:
			raise foundations.exceptions.LibraryInitializationError("{0} | '{1}' library not found!".format(
			self.__class__.__name__, path))

		bind_library and self.bind_library()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def instances(self):
		"""
		Property for **self.__instances** attribute.

		:return: self.__instances.
		:rtype: WeakValueDictionary
		"""

		return self.__instances

	@instances.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def instances(self, value):
		"""
		Setter for **self.__instances** attribute.

		:param value: Attribute value.
		:type value: WeakValueDictionary
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "instances"))

	@instances.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def instances(self):
		"""
		Deleter for **self.__instances** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "instances"))

	@property
	def initialized(self):
		"""
		Property for **self.__initialized** attribute.

		:return: self.__initialized.
		:rtype: unicode
		"""

		return self.__initialized

	@initialized.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def initialized(self, value):
		"""
		Setter for **self.__initialized** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "initialized"))

	@initialized.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def initialized(self):
		"""
		Deleter for **self.__initialized** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "initialized"))

	@property
	def path(self):
		"""
		Property for **self.__path** attribute.

		:return: self.__path.
		:rtype: unicode
		"""

		return self.__path

	@path.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def path(self, value):
		"""
		Setter for **self.__path** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"path", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("path", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		Deleter for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

	@property
	def functions(self):
		"""
		Property for **self.__functions** attribute.

		:return: self.__functions.
		:rtype: tuple
		"""

		return self.__functions

	@functions.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def functions(self, value):
		"""
		Setter for **self.__functions** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""

		if value is not None:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("functions", value)
			for element in value:
				assert type(element) is LibraryHook, "'{0}' attribute: '{1}' type is not 'LibraryHook'!".format(
				"functions", element)
		self.__functions = value

	@functions.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def functions(self):
		"""
		Deleter for **self.__functions** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "functions"))

	@property
	def library(self):
		"""
		Property for **self.__library** attribute.

		:return: self.__library.
		:rtype: object
		"""

		return self.__library

	@library.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def library(self, value):
		"""
		Setter for **self.__library** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		self.__library = value

	@library.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def library(self):
		"""
		Deleter for **self.__library** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "library"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def bind_function(self, function):
		"""
		Binds given function to a class object attribute.

		Usage::
			
			>>> import ctypes 
			>>> path = "FreeImage.dll"
			>>> function = LibraryHook(name="FreeImage_GetVersion", arguments_types=None, return_value=ctypes.c_char_p)
			>>> library = Library(path, bind_library=False)
			>>> library.bind_function(function)
			True
			>>> library.FreeImage_GetVersion()
			'3.15.1'

		:param function: Function to bind.
		:type function: LibraryHook
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Binding '{0}' library '{1}' function.".format(self.__class__.__name__, function.name))

		function_object = getattr(self.__library, function.name)
		setattr(self, function.name, function_object)
		if function.arguments_types:
			function_object.argtypes = function.arguments_types
		if function.return_value:
			function_object.restype = function.return_value
		return True

	def bind_library(self):
		"""
		Binds the Library using functions registered in the **self.__functions** attribute.

		Usage::
			
			>>> import ctypes 
			>>> path = "FreeImage.dll"
			>>> functions = (LibraryHook(name="FreeImage_GetVersion", arguments_types=None, return_value=ctypes.c_char_p),)
			>>> library = Library(path, functions, bind_library=False)
			>>> library.bind_library()
			True
			>>> library.FreeImage_GetVersion()
			'3.15.1'

		:return: Method success.
		:rtype: bool
		"""

		if self.__functions:
			for function in self.__functions:
				self.bind_function(function)
		return True
