#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**walker.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Walker Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import re
import hashlib

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
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
class Walker(object):
	"""
	This class provides methods for walking in a directory.
	"""

	@core.executionTrace
	def __init__(self, root=None, hashSize=8):
		"""
		This method initializes the class.

		:param root: Root directory path to recurse. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__root = None
		self.root = root
		self.__hashSize = None
		self.hashSize = hashSize

		self.__files = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def root(self):
		"""
		This method is the property for **self.__root** attribute.

		:return: self.__root. ( String )
		"""

		return self.__root

	@root.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def root(self, value):
		"""
		This method is the setter method for **self.__root** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("root", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' directory doesn't exists!".format("root", value)
		self.__root = value

	@root.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def root(self):
		"""
		This method is the deleter method for **self.__root** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("root"))

	@property
	def hashSize(self):
		"""
		This method is the property for **self.__hashSize** attribute.

		:return: self.__hashSize. ( String )
		"""

		return self.__hashSize

	@hashSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hashSize(self, value):
		"""
		This method is the setter method for **self.__hashSize** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("hashSize", value)
		self.__hashSize = value

	@hashSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hashSize(self):
		"""
		This method is the deleter method for **self.__hashSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("hashSize"))

	@property
	def files(self):
		"""
		This method is the property for **self.__files** attribute.

		:return: self.__files. ( Dictionary )
		"""

		return self.__files

	@files.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def files(self, value):
		"""
		This method is the setter method for **self.__files** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("files", value)
		self.__files = value

	@files.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def files(self):
		"""
		This method is the deleter method for **self.__files** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("files"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler()
	def walk(self, filtersIn=None, filtersOut=None, flags=0, shorterHashKey=True):
		"""
		This method gets root directory files list as a dictionary.

		:param filtersIn: Regex filters in list. ( List / Tuple )
		:param filtersIn: Regex filters out list. ( List / Tuple )
		:param flags: Regex flags. ( Object )
		:return: Files list. ( Dictionary or None )
		"""

		if filtersIn:
			LOGGER.debug("> Current filters in: '{0}'.".format(filtersIn))

		if filtersOut:
			LOGGER.debug("> Current filters out: '{0}'.".format(filtersOut))

		if self.__root:
				self.__files = {}
				for root, dirs, files in os.walk(self.__root, topdown=False, followlinks=True):
					for item in files:
						LOGGER.debug("> Current file: '{0}' in '{1}'.".format(item, self.__root))
						itemPath = strings.toForwardSlashes(os.path.join(root, item))
						if os.path.isfile(itemPath):
							if not strings.filterWords((itemPath,), filtersIn, filtersOut, flags):
								continue

							LOGGER.debug("> '{0}' file filtered in!".format(itemPath))

							hashKey = hashlib.md5(itemPath).hexdigest()
							itemName = namespace.setNamespace(os.path.splitext(item)[0], shorterHashKey and hashKey[:self.__hashSize] or hashKey)
							LOGGER.debug("> Adding '{0}' with path: '{1}' to files list.".format(itemName, itemPath))
							self.__files[itemName] = itemPath

				return self.__files
