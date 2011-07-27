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
**testsWalker.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Walker tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import re
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.namespace as namespace
import foundations.strings as strings
from foundations.walker import Walker

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
ROOT_DIRECTORY = "standard"
TREE_HIERARCHY = ("loremIpsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
					"level_0/standard.ibl",
					"level_0/level_1/loremIpsum.txt", "level_0/level_1/standard.rc",
					"level_0/level_1/level_2/standard.sIBLT")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class WalkerTestCase(unittest.TestCase):
	"""
	This class is the WalkerTestCase class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		walker = Walker(RESOURCES_DIRECTORY)
		requiredAttributes = ("root",
								"hashSize",
								"files")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(walker))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		walker = Walker(RESOURCES_DIRECTORY)
		requiredMethods = ("walk",)

		for method in requiredMethods:
			self.assertIn(method, dir(walker))

	def testWalk(self):
		"""
		This method tests the "Walker" class "walk" method.
		"""

		walker = Walker()
		walker.root = os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY)
		walker.walk()
		for path in walker.files.values():
			self.assertTrue(os.path.exists(path))

		referencePaths = [strings.replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path), {"/":"|", "\\":"|"}) for path in TREE_HIERARCHY]
		walkerFiles = [strings.replace(path, {"/":"|", "\\":"|"}) for path in walker.files.values()]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)

		walker.walk(filtersOut=("\.rc$",))
		walkerFiles = [strings.replace(path, {"/":"|", "\\":"|"}) for path in walker.files.values()]
		for item in walkerFiles:
			self.assertTrue(not re.search("\.rc$", item))

		walker.walk(filtersOut=("\.ibl", "\.rc$", "\.sIBLT$", "\.txt$"))
		self.assertTrue(not walker.files)

		referencePaths = [strings.replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path), {"/":"|", "\\":"|"}) for path in TREE_HIERARCHY if re.search("\.rc$", path)]
		filter = "\.rc$"
		walker.walk(filtersIn=(filter,))
		walkerFiles = [strings.replace(path, {"/":"|", "\\":"|"}) for path in walker.files.values()]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)
		for item in walkerFiles:
			self.assertTrue(re.search(filter, item))

		walker.hashSize = 24
		walker.walk()
		for item in walker.files.keys():
			self.assertEqual(len(namespace.removeNamespace(item)), walker.hashSize)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
