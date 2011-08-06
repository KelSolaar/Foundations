#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**testsLibrary.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Library tests Module.

**Others:**

"""

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
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
LIBRARIES_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "libraries")
if platform.system() == "Windows" or platform.system() == "Microsoft":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/FreeImage.dll")
elif platform.system() == "Darwin":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/libfreeimage.dylib")
elif platform.system() == "Linux":
	FREEIMAGE_LIBRARY = os.path.join(LIBRARIES_DIRECTORY, "freeImage/libfreeimage.so")

LIBRARIES = {"freeImage":os.path.normpath(os.path.join(os.path.dirname(__file__), FREEIMAGE_LIBRARY))}

LIBRARIES_FUNCTIONS = {"freeImage":(LibraryHook(name="FreeImage_GetVersion" , affixe="@0", argumentsTypes=None, returnValue=ctypes.c_char_p),
								LibraryHook(name="FreeImage_GetCopyrightMessage" , affixe="@0", argumentsTypes=None, returnValue=ctypes.c_char_p))}

LIBRARIES_TESTS_CASES = {"freeImage":{"FreeImage_GetVersion":"3.13.1",
							"FreeImage_GetCopyrightMessage":"This program uses FreeImage, a free, open source image library supporting all common bitmap formats. See http://freeimage.sourceforge.net for details"}}
#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LibraryTestCase(unittest.TestCase):
	"""
	This class is the **LibraryTestCase** class.
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
		This method tests **Library** class **bindFunction** method.
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
		This method tests **Library** class **bindLibrary** method.
		"""

		for name, path in LIBRARIES.items():
			library = Library(path, bindLibrary=False)
			library.functions = LIBRARIES_FUNCTIONS[name]
			library.bindLibrary()
			for function in LIBRARIES_FUNCTIONS[name]:
				self.assertTrue(hasattr(library, function.name))

	def testLibrary(self):
		"""
		This method tests **Library** class binding.
		"""

		for name, path in LIBRARIES.items():
			library = Library(path, LIBRARIES_FUNCTIONS[name])
			for function, value in LIBRARIES_TESTS_CASES[name].items():
				self.assertEqual(getattr(library, function)(), value)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

