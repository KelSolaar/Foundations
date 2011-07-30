#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Tests Suite Module.

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
	testsLoader = unittest.TestLoader()
	return testsLoader.discover(os.path.dirname(__file__))

if __name__ == "__main__":
	import utilities
	unittest.TextTestRunner(verbosity=2).run(testsSuite())
