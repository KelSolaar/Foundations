#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module runs the tests suite.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************

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
def testsSuite():
	"""
	This definitions runs the tests suite.
	
	:return: Tests suite. ( TestSuite )
	"""

	testsLoader = unittest.TestLoader()
	return testsLoader.discover(os.path.dirname(__file__))

if __name__ == "__main__":
	import utilities
	unittest.TextTestRunner(verbosity=2).run(testsSuite())
