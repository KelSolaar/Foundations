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
**pkzip.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Zip file manipulation Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
from cStringIO import StringIO
import logging
import os
import zipfile

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.io as io
import foundations.exceptions
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Pkzip(object):
	"""
	This class provides methods to manipulate zip files.
	"""

	@core.executionTrace
	def __init__(self, archive=None):
		"""
		This method initializes the class.

		@param archive: Variable to manipulate. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__archive = None
		self.archive = archive

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def archive(self):
		"""
		This method is the property for the _archive attribute.

		@return: self.__archive. ( String )
		"""

		return self.__archive

	@archive.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def archive(self, value):
		"""
		This method is the setter method for the _archive attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("archive", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("archive", value)
		self.__archive = value

	@archive.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def archive(self):
		"""
		This method is the deleter method for the _archive attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("archive"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError)
	def extract(self, target):
		"""
		This method extracts the archive file to the provided directory.

		@return: Method success. ( Boolean )
		"""

		archive = zipfile.ZipFile(self.__archive)
		content = archive.namelist()

		directories = [item for item in content if item.endswith("/")]
		files = [item for item in content if not item.endswith("/")]

		directories.sort()
		directories.reverse()

		for directory in directories:
			not os.path.isdir(os.path.join(target, directory)) and io.setLocalDirectory(os.path.join(target, directory))

		for file in files:
			LOGGER.info("{0} | Extracting '{1}' file!".format(self.__class__.__name__, file))
			with open(os.path.join(target, file), "w") as output:
				buffer = StringIO(archive.read(file))
				bufferSize = 2 ** 20
				datas = buffer.read(bufferSize)
				while datas:
					output.write(datas)
					datas = buffer.read(bufferSize)
		return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
