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
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
************************************************************************************************
***	library.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		C / C++ Binding Library Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import ctypes
import logging
import os
import platform

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class LibraryHook(core.Structure):
	"""
	This Is The LibraryHook Class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This Method Initializes The Class.

		@param kwargs: name, affixe, argumentsType, returnValue. ( Key / Value Pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting Class Attributes. ---
		self.__dict__.update(kwargs)

class Library(object):
	"""
	This Class Provides Methods To Bind A C / C++ Library.
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
		This Method Is The Constructor Of The Class.
		
		@param *args: Arguments. ( * )
		@param **kwargs: Arguments. ( * )
		"""

		libraryPath = args[0]
		if os.path.exists(libraryPath):
			if not args[0] in self.librariesInstances.keys():
				self.librariesInstances[args[0]] = object.__new__(self)
			return self.librariesInstances[args[0]]
		else:
			raise foundations.exceptions.LibraryInstantiationError("'{0}' Library Path Doesn't Exists!".format(libraryPath))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.LibraryInitializationError)
	def __init__(self, libraryPath, functions=None):
		"""
		This Method Initializes The Class.
		
		@param libraryPath: Library Path. ( String )
		@param functions: Binding Functions List. ( Tuple )
		"""

		if hasattr(self.librariesInstances[libraryPath], "_libraryInstantiated"):
			return

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
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
			raise foundations.exceptions.LibraryInitializationError, "'{0}' Library Not Found!".format(self.__class__.__name__)

		self.bindLibrary()

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def libraryInstantiated(self):
		"""
		This Method Is The Property For The _libraryInstantiated Attribute.
		
		@return: self.__libraryInstantiated. ( String )
		"""

		return self.__libraryInstantiated

	@libraryInstantiated.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def libraryInstantiated(self, value):
		"""
		This Method Is The Setter Method For The _libraryInstantiated Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Settable!".format("libraryInstantiated"))

	@libraryInstantiated.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryInstantiated(self):
		"""
		This Method Is The Deleter Method For The _libraryInstantiated Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("libraryInstantiated"))

	@property
	def libraryPath(self):
		"""
		This Method Is The Property For The _libraryPath Attribute.
		
		@return: self.__libraryPath. ( String )
		"""

		return self.__libraryPath

	@libraryPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def libraryPath(self, value):
		"""
		This Method Is The Setter Method For The _libraryPath Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("libraryPath", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' File Doesn't Exists!".format("libraryPath", value)
		self.__libraryPath = value

	@libraryPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryPath(self):
		"""
		This Method Is The Deleter Method For The _libraryPath Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("libraryPath"))

	@property
	def functions(self):
		"""
		This Method Is The Property For The _functions Attribute.
		
		@return: self.__functions. ( String )
		"""

		return self.__functions

	@functions.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def functions(self, value):
		"""
		This Method Is The Setter Method For The _functions Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) is tuple, "'{0}' Attribute: '{1}' Type Is Not 'tuple'!".format("functions", value)
		self.__functions = value

	@functions.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def functions(self):
		"""
		This Method Is The Deleter Method For The _functions Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("functions"))

	@property
	def library(self):
		"""
		This Method Is The Property For The _library Attribute.
		
		@return: self.__library. ( Object )
		"""

		return self.__library

	@library.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def library(self, value):
		"""
		This Method Is The Setter Method For The _library Attribute.
		
		@param value: Attribute Value. ( Object )
		"""

		self.__library = value

	@library.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def library(self):
		"""
		This Method Is The Deleter Method For The _library Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("library"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def bindFunction(self, function):
		"""
		This Method Bind A Function.
		
		@param function: Function To Bind. ( Tuple )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Binding '{0}' Library '{1}' Function.".format(self.__class__.__name__, function.name))

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
		This Method Bind The Library.

		@return: Method Success. ( Boolean )		
		"""

		if self.__functions:
			for function in self.__functions:
				self.bindFunction(function)
		return True

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
