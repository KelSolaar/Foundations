#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsStreamObject.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.streamObject` module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from foundations.streamObject import StreamObject

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["StreamObjectTestCase"]

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class StreamObjectTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.streamObject.StreamObject` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("stream",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(StreamObject))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("write",
							"flush")

		for method in requiredMethods:
			self.assertIn(method, dir(StreamObject))

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
