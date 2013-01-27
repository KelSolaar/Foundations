#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**dummy.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines helpers objects for **Foundations** package units tests.

**Others:**

"""

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.trace

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["GLOBAL_RETURN_VALUE",
		"Dummy",
		"dummy1",
		"dummy2",
		"dummy3"]

GLOBAL_RETURN_VALUE = range(10)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Dummy(object):
	"""
	This class is a dummy class mainly used to test :mod:`foundations.trace` module.
	"""

	def __init__(self):
		self.__attribute = GLOBAL_RETURN_VALUE

	@property
	def attribute(self):
		return self.__attribute

	@attribute.setter
	def attribute(self, value):
		self.__attribute = value

	@attribute.deleter
	def attribute(self):
		return

	def __str__(self):
		pass

	def __repr__(self):
		pass

	def __privateMethod(self):
		return self.__privateMethod.__name__

	def publicMethod(self):
		return self.publicMethod.__name__

	@foundations.trace.untracable
	def untracedPublic(self):
		return self.untracedPublic.__name__

	@staticmethod
	def staticMethod():
		return Dummy.staticMethod.__name__

	@classmethod
	def clsMethod(cls):
		return cls.clsMethod.__name__

def dummy1():
	return GLOBAL_RETURN_VALUE

@foundations.trace.untracable
def dummy2():
	return GLOBAL_RETURN_VALUE

def dummy3():
	return GLOBAL_RETURN_VALUE
