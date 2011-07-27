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
**testsCommon.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Common tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.common

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class GetSystemApplicationDatasDirectoryTestCase(unittest.TestCase):
	"""
	This class is the GetSystemApplicationDatasDirectoryTestCase class.
	"""

	def testGetSystemApplicationDatasDirectory(self):
		"""
		This method tests the "getSystemApplicationDatasDirectory" definition.
		"""

		path = foundations.common.getSystemApplicationDatasDirectory()
		self.assertIsInstance(path, str)
		self.assertTrue(os.path.exists(path))

class GetUserApplicationDatasDirectoryTestCase(unittest.TestCase):
	"""
	This class is the GetUserApplicationDatasDirectory class.
	"""

	def testGetUserApplicationDatasDirectory(self):
		"""
		This method tests the "getUserApplicationDatasDirectory" definition.
		"""

		path = foundations.common.getUserApplicationDatasDirectory()
		self.assertIsInstance(path, str)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
