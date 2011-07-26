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
**rotatingBackup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Rotating Backup Module.

**Others:**
	Code Extracted From rotatingbackup.py Written By leo.ss.pku@gmail.com
"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Global variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class RotatingBackup(object):
	"""
	This Class Is The RotatingBackup Class.
	"""

	@core.executionTrace
	def __init__(self, source=None, destination=None, count=3):
		"""
		This Method Initializes The Class.

		@param source: Backup Source. ( String )
		@param destination: Backup Destination. ( String )
		@param count: Backup Count. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

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
		This Method Is The Property For The _source Attribute.

		@return: self.__source. ( String )
		"""

		return self.__source

	@source.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def source(self, value):
		"""
		This Method Is The Setter Method For The _source Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("source", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' File Doesn't Exists!".format("source", value)
		self.__source = value

	@source.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def source(self):
		"""
		This Method Is The Deleter Method For The _source Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("source"))

	@property
	def destination(self):
		"""
		This Method Is The Property For The _destination Attribute.

		@return: self.__destination. ( String )
		"""

		return self.__destination

	@destination.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def destination(self, value):
		"""
		This Method Is The Setter Method For The _destination Attribute.
		
		@param value: Attribute Value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("destination", value)
		self.__destination = value

	@destination.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def destination(self):
		"""
		This Method Is The Deleter Method For The _destination Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("destination"))

	@property
	def count(self):
		"""
		This Method Is The Property For The _count Attribute.

		@return: self.__count. ( Integer )
		"""

		return self.__count

	@count.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def count(self, value):
		"""
		This Method Is The Setter Method For The _count Attribute.
		
		@param value: Attribute Value. ( Integer )
		"""

		if value:
			assert type(value) in (int, float), "'{0}' Attribute: '{1}' Type Is Not 'int' or 'float'!".format("count", value)
			assert value > 0, "'{0}' Attribute: '{1}' Need To Be Exactly Positive!".format("count", value)
		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("count"))

	@count.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def count(self):
		"""
		This Method Is The Deleter Method For The _count Attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("count"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def backup(self):
		"""
		This Method Does The Rotating Backup.
		
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Storing '{0}' File Backup.".format(self.__source))

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
		This Method Copies The Provided Path To Destination.

		@param source: Source To Copy From. ( String )
		@param destination: Destination To Copy To. ( String )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Copying '{0}' File To '{1}'.".format(source, destination))

		if os.path.isfile(source):
			shutil.copyfile(source, destination)
		else:
			shutil.copytree(source, destination)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def delete(self, path):
		"""
		This Method Deletes The Provided Resource.

		@param path: Resource To Delete. ( String )
		@return: Method Success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' File.".format(path))

		if os.path.isfile(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)
		return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
