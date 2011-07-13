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
#***********************************************************s************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
************************************************************************************************
***	walker.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Walker Module
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
import logging
import os
import re
import hashlib

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Walker(object):
	"""
	This Class Provides Methods For Walking In A Directory.
	"""

	@core.executionTrace
	def __init__(self, root=None, hashSize=8):
		"""
		This Method Initializes The Class.

		@param root: Root Directory Path To Recurse. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self.__root = None
		self.root = root
		self.__hashSize = None
		self.hashSize = hashSize

		self.__files = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def root(self):
		"""
		This Method Is The Property For The _root Attribute.

		@return: self.__root. ( String )
		"""

		return self.__root

	@root.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def root(self, value):
		"""
		This Method Is The Setter Method For The _root Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("root", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' Directory Doesn't Exists!".format("root", value)
		self.__root = value

	@root.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def root(self):
		"""
		This Method Is The Deleter Method For The _root Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("root"))

	@property
	def hashSize(self):
		"""
		This Method Is The Property For The _hashSize Attribute.

		@return: self.__hashSize. ( String )
		"""

		return self.__hashSize

	@hashSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hashSize(self, value):
		"""
		This Method Is The Setter Method For The _hashSize Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) is int, "'{0}' Attribute: '{1}' Type Is Not 'int'!".format("hashSize", value)
		self.__hashSize = value

	@hashSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hashSize(self):
		"""
		This Method Is The Deleter Method For The _hashSize Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("hashSize"))

	@property
	def files(self):
		"""
		This Method Is The Property For The _files Attribute.

		@return: self.__files. ( Dictionary )
		"""

		return self.__files

	@files.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def files(self, value):
		"""
		This Method Is The Setter Method For The _files Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' Attribute: '{1}' Type Is Not 'dict'!".format("files", value)
		self.__files = value

	@files.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def files(self):
		"""
		This Method Is The Deleter Method For The _files Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("files"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler()
	def walk(self, filtersIn=None, filtersOut=None, flags=0, shorterHashKey=True):
		"""
		This Method Gets Root Directory Files List As A Dictionary.

		@param filtersIn: Regex filtersIn List. ( List / Tuple )
		@param filtersIn: Regex filtersOut List. ( List / Tuple )
		@param flags: Regex Flags. ( Object )
		@return: Files List. ( Dictionary Or None )
		"""

		if filtersIn:
			LOGGER.debug("> Current filtersIn: '{0}'.".format(filtersIn))

		if self.__root:
				self.__files = {}
				for root, dirs, files in os.walk(self.__root, topdown=False):
					for item in files:
						LOGGER.debug("> Current File: '{0}' In '{1}'.".format(item, self.__root))
						itemPath = strings.toForwardSlashes(os.path.join(root, item))
						if os.path.isfile(itemPath):
							if not strings.filterWords((itemPath,), filtersIn, filtersOut, flags):
								continue

							LOGGER.debug("> '{0}' File Filtered In!".format(itemPath))

							hashKey = hashlib.md5(itemPath).hexdigest()
							itemName = namespace.setNamespace(os.path.splitext(item)[0], shorterHashKey and hashKey[:self.__hashSize] or hashKey)
							LOGGER.debug("> Adding '{0}' With Path: '{1}' To Files List.".format(itemName, itemPath))
							self.__files[itemName] = itemPath

				return self.__files

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
