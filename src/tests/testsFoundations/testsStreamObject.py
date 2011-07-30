#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsStreamObject.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	StreamObject tests Module.

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

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class StreamObjectTestCase(unittest.TestCase):
	"""
	This class is the StreamObjectTestCase class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		streamObject = StreamObject()
		requiredAttributes = ("stream",)

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(streamObject))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		streamObject = StreamObject()
		requiredMethods = ("write",
							"flush")

		for method in requiredMethods:
			self.assertIn(method, dir(streamObject))

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

