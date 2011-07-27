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
**streamObject.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Stream object Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class StreamObject(object):
	"""
	This class is the StreamObject class.
	"""

	def __init__(self, stream=None):
		"""
		This method initializes the class.

		@param stream: Stream object. ( Object )
		"""

		self.__stream = []

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def stream(self):
		"""
		This method is the property for the _stream attribute.

		@return: self.__stream. ( List )
		"""

		return self.__stream

	@stream.setter
	def stream(self, value):
		"""
		This method is the setter method for the _stream attribute.

		@param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("stream", value)
		self.__stream = value

	@stream.deleter
	def stream(self):
		"""
		This method is the deleter method for the _stream attribute.
		"""

		raise Exception("'{0}' attribute is not deletable!".format("stream"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	def write(self, message):
		"""
		This method provides write ability to the class.

		@param message: Current message. ( String )
		"""

		self.__stream.append(message)

	def flush(self):
		"""
		This method flushes the current stream.
		"""

		pass

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
