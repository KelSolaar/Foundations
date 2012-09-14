#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**pkzip.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module provides archives files manipulation objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from cStringIO import StringIO
import logging
import os
import zipfile

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.io as io
import foundations.exceptions
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Pkzip"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Pkzip(object):
	"""
	This class provides methods to manipulate zip files.
	"""

	@core.executionTrace
	def __init__(self, archive=None):
		"""
		This method initializes the class.

		Usage::

			>>> import tempfile
			>>> tempDirectory = tempfile.mkdtemp()
			>>> zipFile = Pkzip("zipFile.zip")
			>>> zipFile.extract(tempDirectory)
			True

		:param archive: Archive to manipulate. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__archive = None
		self.archive = archive

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def archive(self):
		"""
		This method is the property for **self.__archive** attribute.

		:return: self.__archive. ( String )
		"""

		return self.__archive

	@archive.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def archive(self, value):
		"""
		This method is the setter method for **self.__archive** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"archive", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("archive", value)
		self.__archive = value

	@archive.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def archive(self):
		"""
		This method is the deleter method for **self.__archive** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "archive"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, OSError, Exception)
	def extract(self, target):
		"""
		This method extracts archive file to given directory.

		:param target: Target extraction directory. ( String )
		:return: Method success. ( Boolean )
		"""

		archive = zipfile.ZipFile(self.__archive)
		content = archive.namelist()

		directories = [item for item in content if item.endswith("/")]
		files = [item for item in content if not item.endswith("/")]

		directories.sort()
		directories.reverse()

		for directory in directories:
			not os.path.isdir(os.path.join(target, directory)) and io.setDirectory(os.path.join(target, directory))

		for file in files:
			LOGGER.info("{0} | Extracting '{1}' file!".format(self.__class__.__name__, file))
			with open(os.path.join(target, file), "w") as output:
				buffer = StringIO(archive.read(file))
				bufferSize = 2 ** 20
				data = buffer.read(bufferSize)
				while data:
					output.write(data)
					data = buffer.read(bufferSize)
		return True