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
**testsLibrary.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Library tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import ctypes
import os
import platform
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from foundations.library import Library, LibraryHook

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
LIBRARIES_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "libraries")
if platform.system() == "Windows" or platform.system() == "Microsoft":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/FreeImage.dll")
elif platform.system() == "Darwin":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/libfreeimage.dylib")
elif platform.system() == "Linux":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/libfreeimage.so")


LIBRARIES = {"freeImage":os.path.normpath(os.path.join(os.path.dirname(__file__), FREEIMAGE_LIBRARY))}

LIBRARIES_FUNCTIONS = {"freeImage":(LibraryHook(name="FreeImage_GetVersion" , affixe="@0", argumentsType=None, returnValue=ctypes.c_char_p),
								LibraryHook(name="FreeImage_GetCopyrightMessage" , affixe="@0", argumentsType=None, returnValue=ctypes.c_char_p))}

LIBRARIES_TESTS_CASES = {"freeImage":{"FreeImage_GetVersion":"3.13.1",
							"FreeImage_GetCopyrightMessage":"This program uses FreeImage, a free, open source image library supporting all common bitmap formats. See http://freeimage.sourceforge.net for details"}}
#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LibraryTestCase(unittest.TestCase):
	"""
	This class is the LibraryTestCase class.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		library = Library(LIBRARIES["freeImage"], LIBRARIES_FUNCTIONS["freeImage"])
		requiredAttributes = ("libraryInstantiated",
								"libraryPath",
								"functions",
								"library")
		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(library))

		requiredClassAttributes = ("librariesInstances",
								"callback",)
		for classAttribute in requiredClassAttributes:
			self.assertIn(classAttribute, dir(library))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		library = Library(LIBRARIES["freeImage"], LIBRARIES_FUNCTIONS["freeImage"])
		requiredMethods = ("bindLibrary",
							"bindFunction")

		for method in requiredMethods:
			self.assertIn(method, dir(library))

	def testBindFunction(self):
		"""
		This method tests the "Library" class "bindFunction" method.
		"""

		for name, path in LIBRARIES.items():
			library = Library(path)
			library.functions = LIBRARIES_FUNCTIONS[name]
			for function in LIBRARIES_FUNCTIONS[name]:
				hasattr(library, function.name) and delattr(library, function.name)
				library.bindFunction(function)
				self.assertTrue(hasattr(library, function.name))

	def testBindLibrary(self):
		"""
		This method tests the "Library" class "bindLibrary" method.
		"""

		for name, path in LIBRARIES.items():
			library = Library(path)
			library.functions = LIBRARIES_FUNCTIONS[name]
			for function in LIBRARIES_FUNCTIONS[name]:
				hasattr(library, function.name) and delattr(library, function.name)
			library.bindLibrary()
			for function in LIBRARIES_FUNCTIONS[name]:
				self.assertTrue(hasattr(library, function.name))

	def testLibrary(self):
		"""
		This method tests the "Library" class binding.
		"""

		for name, path in LIBRARIES.items():
			library = Library(path, LIBRARIES_FUNCTIONS[name])
			for function, value in LIBRARIES_TESTS_CASES[name].items():
				self.assertEqual(getattr(library, function)(), value)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
