#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**rotatingbackup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Rotating backup Module.

**Others:**
	Code extracted from rotatingbackup.py written by leo.ss.pku@gmail.com
"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import shutil

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
class RotatingBackup(object):
	"""
	This class is the RotatingBackup class.
	"""

	@core.executionTrace
	def __init__(self, source=None, destination=None, count=3):
		"""
		This method initializes the class.

		@param source: Backup source. ( String )
		@param destination: Backup destination. ( String )
		@param count: Backup count. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__source = None
		self.__source = source
		self.__destination = None
		self.__destination = destination
		self.__count = None
		self.__count = count

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def source(self):
		"""
		This method is the property for the _source attribute.

		@return: self.__source. ( String )
		"""

		return self.__source

	@source.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def source(self, value):
		"""
		This method is the setter method for the _source attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("source", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("source", value)
		self.__source = value

	@source.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def source(self):
		"""
		This method is the deleter method for the _source attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("source"))

	@property
	def destination(self):
		"""
		This method is the property for the _destination attribute.

		@return: self.__destination. ( String )
		"""

		return self.__destination

	@destination.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def destination(self, value):
		"""
		This method is the setter method for the _destination attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("destination", value)
		self.__destination = value

	@destination.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def destination(self):
		"""
		This method is the deleter method for the _destination attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("destination"))

	@property
	def count(self):
		"""
		This method is the property for the _count attribute.

		@return: self.__count. ( Integer )
		"""

		return self.__count

	@count.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def count(self, value):
		"""
		This method is the setter method for the _count attribute.

		@param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format("count", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("count", value)
		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("count"))

	@count.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def count(self):
		"""
		This method is the deleter method for the _count attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("count"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def backup(self):
		"""
		This method does the rotating backup.

		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing '{0}' file backup.".format(self.__source))

		if not self.__source and not self.__destination:
			return True

		os.path.exists(self.__destination) or os.mkdir(self.__destination)
		destination = os.path.join(self.__destination, os.path.basename(self.__source))
		for i in range(self.__count - 1, 0, -1):
			sfn = "{0}.{1}".format(destination, i)
			dfn = "{0}.{1}".format(destination, i + 1)
			if os.path.exists(sfn):
				if os.path.exists(dfn):
					self.delete(dfn)
				os.renames(sfn, dfn)
		os.path.exists(destination) and os.rename(destination, destination + ".1")
		self.copy(self.__source, destination)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def copy(self, source, destination):
		"""
		This method copies the provided path to destination.

		@param source: Source to copy from. ( String )
		@param destination: Destination to copy to. ( String )
		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Copying '{0}' file to '{1}'.".format(source, destination))

		if os.path.isfile(source):
			shutil.copyfile(source, destination)
		else:
			shutil.copytree(source, destination)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def delete(self, path):
		"""
		This method deletes the provided resource.

		@param path: Resource to delete. ( String )
		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing '{0}' file.".format(path))

		if os.path.isfile(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)
		return True

