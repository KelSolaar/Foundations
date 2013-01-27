#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**rotatingbackup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`RotatingBackup` class.

**Others:**
	Code extracted from rotatingbackup.py written by leo.ss.pku@gmail.com
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.io
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

__all__ = ["LOGGER", "RotatingBackup"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RotatingBackup(object):
	"""
	This class provides a rotating backup system.
	"""

	def __init__(self, source=None, destination=None, count=3):
		"""
		This method initializes the class.

		.. warning::

			Backups destination folder should not be the same than the folder containing the source to be backuped!

		Usage::
		
			>>> file = "File.txt"
			>>> destination = "backup"
			>>> backup = RotatingBackup(file, destination)
			>>> backup.backup()
			True
			>>> for i in range(3):
			...	backup.backup()
			...
			True
			True
			True
			>>> import os
			>>> os.listdir(destination)
			['File.txt', 'File.txt.1', 'File.txt.2', 'File.txt.3']

		:param source: Backup source. ( String )
		:param destination: Backup destination. ( String )
		:param count: Backups count. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__source = None
		self.__source = source
		self.__destination = None
		self.__destination = destination
		self.__count = None
		self.__count = count

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def source(self):
		"""
		This method is the property for **self.__source** attribute.

		:return: self.__source. ( String )
		"""

		return self.__source

	@source.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def source(self, value):
		"""
		This method is the setter method for **self.__source** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"source", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("source", value)
		self.__source = value

	@source.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def source(self):
		"""
		This method is the deleter method for **self.__source** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "source"))

	@property
	def destination(self):
		"""
		This method is the property for **self.__destination** attribute.

		:return: self.__destination. ( String )
		"""

		return self.__destination

	@destination.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def destination(self, value):
		"""
		This method is the setter method for **self.__destination** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"destination", value)
		self.__destination = value

	@destination.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def destination(self):
		"""
		This method is the deleter method for **self.__destination** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "destination"))

	@property
	def count(self):
		"""
		This method is the property for **self.__count** attribute.

		:return: self.__count. ( Integer )
		"""

		return self.__count

	@count.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def count(self, value):
		"""
		This method is the setter method for **self.__count** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format(
			"count", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("count", value)
		self.__count = value

	@count.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def count(self):
		"""
		This method is the deleter method for **self.__count** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "count"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def backup(self):
		"""
		This method does the rotating backup.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing '{0}' file backup.".format(self.__source))

		foundations.common.pathExists(self.__destination) or foundations.io.setDirectory(self.__destination)
		destination = os.path.join(self.__destination, os.path.basename(self.__source))
		for i in range(self.__count - 1, 0, -1):
			sfn = "{0}.{1}".format(destination, i)
			dfn = "{0}.{1}".format(destination, i + 1)
			if foundations.common.pathExists(sfn):
				if foundations.common.pathExists(dfn):
					foundations.io.remove(dfn)
				os.renames(sfn, dfn)
		foundations.common.pathExists(destination) and os.rename(destination, destination + ".1")
		foundations.io.copy(self.__source, destination)
		return True
