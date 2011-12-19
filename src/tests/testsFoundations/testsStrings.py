#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsStrings.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.strings` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform
import re
import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.strings as strings

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["GetNiceNameTestCase",
		"GetVersionRankTestCase",
		"GetSplitextBasenameTestCase",
		"GetCommonAncestorTestCase",
		"GetCommonPathsAncestorTestCase",
		"GetWordsTestCase",
		"FilterWordsTestCase",
		"ReplaceTestCase",
		"ToForwardSlashesTestCase",
		"ToBackwardSlashesTestCase",
		"ToPosixPathTestCase",
		"GetNormalizedPathTestCase",
		"IsEmailTestCase",
		"IsWebsiteTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GetNiceNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getNiceName` definition units tests methods.
	"""

	def testGetNiceName(self):
		"""
		This method tests :func:`foundations.strings.getNiceName` definition.
		"""

		self.assertIsInstance(strings.getNiceName("testGetNiceName"), str)
		self.assertEqual(strings.getNiceName("testGetNiceName"), "Test Get Nice Name")
		self.assertEqual(strings.getNiceName("TestGetNiceName"), "Test Get Nice Name")
		self.assertEqual(strings.getNiceName("_testGetNiceName"), "_Test Get Nice Name")
		self.assertEqual(strings.getNiceName("Test Get NiceName"), "Test Get Nice Name")
		self.assertEqual(strings.getNiceName("testGetMeANiceName"), "Test Get Me A Nice Name")

class GetVersionRankTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getVersionRank` definition units tests methods.
	"""

	def testGetVersionRank(self):
		"""
		This method tests :func:`foundations.strings.getVersionRank` definition.
		"""

		self.assertIsInstance(strings.getVersionRank("0.0.0"), int)
		self.assertEqual(strings.getVersionRank("0.0.0"), 0)
		self.assertEqual(strings.getVersionRank("0.1.0"), 10)
		self.assertEqual(strings.getVersionRank("1.1.0"), 110)
		self.assertEqual(strings.getVersionRank("1.2.3.4.5"), 12345)

class GetSplitextBasenameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getSplitextBasename` definition units tests methods.
	"""

	def testGetSplitextBasename(self):
		"""
		This method tests :func:`foundations.strings.getSplitextBasename` definition.
		"""

		self.assertIsInstance(strings.getSplitextBasename("/Users/JohnDoe/Documents"), str)
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test.txt"), "Test")
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test"), "Test")
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test/"), "Test")

class GetCommonAncestorTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getCommonAncestor` definition units tests methods.
	"""

	def testGetCommonAncestor(self):
		"""
		This method tests :func:`foundations.strings.getCommonAncestor` definition.
		"""

		self.assertTupleEqual(strings.getCommonAncestor(("1", "2", "3"), ("1", "2", "0"), ("1", "2", "3", "4")),
														("1", "2"))
		self.assertEqual(strings.getCommonAncestor("azerty", "azetty", "azello"), "aze")
		self.assertEqual(strings.getCommonAncestor("/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt"),
						"/Users/JohnDoe/Documents")
		self.assertFalse(strings.getCommonAncestor("azerty", "qwerty"))

class GetCommonPathsAncestorTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getCommonPathsAncestor` definition units tests methods.
	"""

	def testGetCommonPathsAncestor(self):
		"""
		This method tests :func:`foundations.strings.getCommonPathsAncestor` definition.
		"""

		self.assertEqual(strings.getCommonPathsAncestor("{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents"))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents", "Test.txt")))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents"))))

		self.assertFalse(strings.getCommonPathsAncestor("{0}{1}".format(os.sep, os.sep.join(("JohnDoe", "Documents"))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents", "Test.txt")))))

class GetWordsTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getWords` definition units tests methods.
	"""

	def testGetWords(self):
		"""
		This method tests :func:`foundations.strings.getWords` definition.
		"""

		self.assertIsInstance(strings.getWords("Users are John Doe and Jane Doe."), list)
		self.assertListEqual(strings.getWords("Users are John Doe and Jane Doe."),
							"Users are John Doe and Jane Doe".split())
		self.assertListEqual(strings.getWords("Users are: John Doe, Jane Doe, Z6PO."),
							"Users are John Doe Jane Doe Z6PO".split())

class FilterWordsTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.filterWords` definition units tests methods.
	"""

	def testFilterWords(self):
		"""
		This method tests :func:`foundations.strings.filterWords` definition.
		"""

		self.assertIsInstance(strings.filterWords("Users are John Doe and Jane Doe".split()), list)
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersIn=("Users", "John")),
												"Users John".split())
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersIn=("users", "john"),
												flags=re.IGNORECASE),
												"Users John".split())
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersIn=("Nemo",)),
												[])
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersOut=("Users", "John")),
												"are Doe and Jane Doe".split())
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersOut=("Users are John Doe and Jane Doe".split())),
												[])
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersIn=("Users",),
												filtersOut=("Users",)),
												[])

class ReplaceTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.replace` definition units tests methods.
	"""

	def testReplace(self):
		"""
		This method tests :func:`foundations.strings.replace` definition.
		"""

		self.assertIsInstance(strings.replace("To@Forward|Slashes@Test|Case", {}), str)
		self.assertEqual(strings.replace("To@Forward|Slashes@Test|Case", {"@":"|", "|":":"}),
						"To:Forward:Slashes:Test:Case")
		self.assertEqual(strings.replace("To@Forward@Slashes@Test@Case", {"@":"|", "|":"@", "@":"|" }),
						"To@Forward@Slashes@Test@Case")

class RemoveStripTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.removeStrip` definition units tests methods.
	"""

	def testRemoveStrip(self):
		"""
		This method tests :func:`foundations.strings.removeStrip` definition.
		"""

		self.assertIsInstance(strings.removeStrip("John Doe", "John"), str)
		self.assertEqual(strings.removeStrip("John Doe", "John"), "Doe")
		self.assertEqual(strings.removeStrip("John Doe", "Doe"), "John")

class ToForwardSlashesTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.toForwardSlashes` definition units tests methods.
	"""

	def testToForwardSlashes(self):
		"""
		This method tests :func:`foundations.strings.toForwardSlashes` definition.
		"""

		self.assertIsInstance(strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), str)
		self.assertEqual(strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), "To/Forward/Slashes/Test/Case")
		self.assertEqual(strings.toForwardSlashes("\Users/JohnDoe\Documents"), "/Users/JohnDoe/Documents")

class ToBackwardSlashesTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.toBackwardSlashes` definition units tests methods.
	"""

	def testToBackwardSlashes(self):
		"""
		This method tests :func:`foundations.strings.toBackwardSlashes` definition.
		"""

		self.assertIsInstance(strings.toBackwardSlashes("\Users\JohnDoe\Documents"), str)
		self.assertEqual(strings.toBackwardSlashes("To/Forward/Slashes/Test/Case"), "To\Forward\Slashes\Test\Case")
		self.assertEqual(strings.toBackwardSlashes("/Users/JohnDoe/Documents"), "\Users\JohnDoe\Documents")

class ToPosixPathTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.toPosixPath` definition units tests methods.
	"""

	def testToPosixPath(self):
		"""
		This method tests :func:`foundations.strings.toPosixPath` definition.
		"""

		self.assertIsInstance(strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), str)
		self.assertEqual(strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), "/Users/JohnDoe/Documents")
		self.assertEqual(strings.toPosixPath("\\Server\Users\\JohnDoe\\Documents"), "/Server/Users/JohnDoe/Documents")

class GetNormalizedPathTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getNormalizedPath` definition units tests methods.
	"""

	def testGetNormalizedPath(self):
		"""
		This method tests :func:`foundations.strings.getNormalizedPath` definition.
		"""

		self.assertIsInstance(strings.getNormalizedPath("/Users/JohnDoe/Documents"), str)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			self.assertEqual(strings.getNormalizedPath("C:/Users\JohnDoe/Documents"), r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(strings.getNormalizedPath("C://Users\/JohnDoe//Documents/"), r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(strings.getNormalizedPath("C:\\Users\\JohnDoe\\Documents"), r"C:\\Users\\JohnDoe\\Documents")
		else:
			self.assertEqual(strings.getNormalizedPath("/Users/JohnDoe/Documents/"), "/Users/JohnDoe/Documents")
			self.assertEqual(strings.getNormalizedPath("/Users\JohnDoe/Documents"), "/Users\JohnDoe/Documents")

class IsEmailTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.isEmail` definition units tests methods.
	"""

	def testIsEmail(self):
		"""
		This method tests :func:`foundations.strings.isEmail` definition.
		"""

		self.assertIsInstance(strings.isEmail("john.doe@domain.com"), bool)
		self.assertTrue(strings.isEmail("john.doe@domain.com"))
		self.assertTrue(strings.isEmail("john.doe@domain.server.department.company.com"))
		self.assertFalse(strings.isEmail("john.doe"))
		self.assertFalse(strings.isEmail("john.doe@domain"))

class IsWebsiteTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.isWebsite` definition units tests methods.
	"""

	def testIsWebsite(self):
		"""
		This method tests :func:`foundations.strings.isWebsite` definition.
		"""

		self.assertIsInstance(strings.isWebsite("http://domain.com"), bool)
		self.assertTrue(strings.isWebsite("http://www.domain.com"))
		self.assertTrue(strings.isWebsite("http://domain.com"))
		self.assertTrue(strings.isWebsite("https://domain.com"))
		self.assertTrue(strings.isWebsite("ftp://domain.com"))
		self.assertTrue(strings.isWebsite("http://domain.subdomain.com"))
		self.assertFalse(strings.isWebsite(".com"))
		self.assertFalse(strings.isWebsite("domain.com"))

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
