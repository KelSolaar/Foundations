#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**streamObject.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Stream object Module.

**Others:**

"""

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class StreamObject(object):
	"""
	This class is the **StreamObject** class.
	"""

	def __init__(self, stream=None):
		"""
		This method initializes the class.

		:param stream: Stream object. ( Object )
		"""

		self.__stream = []

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def stream(self):
		"""
		This method is the property for **self.__stream** attribute.

		:return: self.__stream. ( List )
		"""

		return self.__stream

	@stream.setter
	def stream(self, value):
		"""
		This method is the setter method for **self.__stream** attribute.

		:param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("stream", value)
		self.__stream = value

	@stream.deleter
	def stream(self):
		"""
		This method is the deleter method for **self.__stream** attribute.
		"""

		raise Exception("'{0}' attribute is not deletable!".format("stream"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	def write(self, message):
		"""
		This method provides write ability to the class.

		:param message: Current message. ( String )
		"""

		self.__stream.append(message)

	def flush(self):
		"""
		This method flushes the current stream.
		"""

		pass