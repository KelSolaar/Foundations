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
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.strings

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["EncodeTestCase",
		"GetNiceNameTestCase",
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
		"GetRandomSequenceTestCase",
		"IsEmailTestCase",
		"IsWebsiteTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EncodeTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.encode` definition units tests methods.
	"""

	def testEncode(self):
		"""
		This method tests :func:`foundations.strings.encode` definition.
		"""

		self.assertIsInstance(foundations.strings.encode("myData"), unicode)
		self.assertIsInstance(foundations.strings.encode(0), unicode)
		self.assertIsInstance(foundations.strings.encode(None), unicode)
		self.assertIsInstance(foundations.strings.encode(True), unicode)

class GetNiceNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getNiceName` definition units tests methods.
	"""

	def testGetNiceName(self):
		"""
		This method tests :func:`foundations.strings.getNiceName` definition.
		"""

		self.assertIsInstance(foundations.strings.getNiceName("testGetNiceName"), str)
		self.assertEqual(foundations.strings.getNiceName("testGetNiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.getNiceName("TestGetNiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.getNiceName("_testGetNiceName"), "_Test Get Nice Name")
		self.assertEqual(foundations.strings.getNiceName("Test Get NiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.getNiceName("testGetMeANiceName"), "Test Get Me A Nice Name")

class GetVersionRankTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getVersionRank` definition units tests methods.
	"""

	def testGetVersionRank(self):
		"""
		This method tests :func:`foundations.strings.getVersionRank` definition.
		"""

		self.assertTrue(type(foundations.strings.getVersionRank("0.0.0")), (int, long))
		self.assertEqual(foundations.strings.getVersionRank("0.0.0"), 0)
		self.assertEqual(foundations.strings.getVersionRank("0.1.0"), 1000000000)
		self.assertEqual(foundations.strings.getVersionRank("1.1.0"), 1001000000000)
		self.assertEqual(foundations.strings.getVersionRank("1.2.3.4.5"), 1002003004000)
		self.assertEqual(foundations.strings.getVersionRank("4.0"), 4000000000000)
		self.assertEqual(foundations.strings.getVersionRank(str()), 0)

class GetSplitextBasenameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getSplitextBasename` definition units tests methods.
	"""

	def testGetSplitextBasename(self):
		"""
		This method tests :func:`foundations.strings.getSplitextBasename` definition.
		"""

		self.assertIsInstance(foundations.strings.getSplitextBasename("/Users/JohnDoe/Documents"), str)
		self.assertEqual(foundations.strings.getSplitextBasename("/Users/JohnDoe/Documents/Test.txt"), "Test")
		self.assertEqual(foundations.strings.getSplitextBasename("/Users/JohnDoe/Documents/Test"), "Test")
		self.assertEqual(foundations.strings.getSplitextBasename("/Users/JohnDoe/Documents/Test/"), "Test")

class GetCommonAncestorTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getCommonAncestor` definition units tests methods.
	"""

	def testGetCommonAncestor(self):
		"""
		This method tests :func:`foundations.strings.getCommonAncestor` definition.
		"""

		self.assertTupleEqual(foundations.strings.getCommonAncestor(("1", "2", "3"), ("1", "2", "0"), ("1", "2", "3", "4")),
														("1", "2"))
		self.assertEqual(foundations.strings.getCommonAncestor("azerty", "azetty", "azello"), "aze")
		self.assertEqual(foundations.strings.getCommonAncestor(
		"/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt"),
		"/Users/JohnDoe/Documents")
		self.assertFalse(foundations.strings.getCommonAncestor("azerty", "qwerty"))

class GetCommonPathsAncestorTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getCommonPathsAncestor` definition units tests methods.
	"""

	def testGetCommonPathsAncestor(self):
		"""
		This method tests :func:`foundations.strings.getCommonPathsAncestor` definition.
		"""

		self.assertEqual(foundations.strings.getCommonPathsAncestor("{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents"))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents", "Test.txt")))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents"))))

		self.assertFalse(foundations.strings.getCommonPathsAncestor("{0}{1}".format(os.sep,
														os.sep.join(("JohnDoe", "Documents"))),
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

		self.assertIsInstance(foundations.strings.getWords("Users are John Doe and Jane Doe."), list)
		self.assertListEqual(foundations.strings.getWords("Users are John Doe and Jane Doe."),
							"Users are John Doe and Jane Doe".split())
		self.assertListEqual(foundations.strings.getWords("Users are: John Doe, Jane Doe, Z6PO."),
							"Users are John Doe Jane Doe Z6PO".split())

class FilterWordsTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.filterWords` definition units tests methods.
	"""

	def testFilterWords(self):
		"""
		This method tests :func:`foundations.strings.filterWords` definition.
		"""

		self.assertIsInstance(foundations.strings.filterWords("Users are John Doe and Jane Doe".split()), list)
		self.assertListEqual(foundations.strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersIn=("Users", "John")),
												"Users John".split())
		self.assertListEqual(foundations.strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersIn=("users", "john"),
												flags=re.IGNORECASE),
												"Users John".split())
		self.assertListEqual(foundations.strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersIn=("Nemo",)),
												[])
		self.assertListEqual(foundations.strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersOut=("Users", "John")),
												"are Doe and Jane Doe".split())
		self.assertListEqual(foundations.strings.filterWords("Users are John Doe and Jane Doe".split(),
												filtersOut=("Users are John Doe and Jane Doe".split())),
												[])
		self.assertListEqual(foundations.strings.filterWords("Users are John Doe and Jane Doe".split(),
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

		self.assertIsInstance(foundations.strings.replace("To@Forward|Slashes@Test|Case", {}), str)
		self.assertEqual(foundations.strings.replace("To@Forward|Slashes@Test|Case", {"@":"|", "|":":"}),
						"To:Forward:Slashes:Test:Case")
		self.assertEqual(foundations.strings.replace("To@Forward@Slashes@Test@Case", {"@":"|", "|":"@"}),
						"To@Forward@Slashes@Test@Case")

class RemoveStripTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.removeStrip` definition units tests methods.
	"""

	def testRemoveStrip(self):
		"""
		This method tests :func:`foundations.strings.removeStrip` definition.
		"""

		self.assertIsInstance(foundations.strings.removeStrip("John Doe", "John"), str)
		self.assertEqual(foundations.strings.removeStrip("John Doe", "John"), "Doe")
		self.assertEqual(foundations.strings.removeStrip("John Doe", "Doe"), "John")

class ToForwardSlashesTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.toForwardSlashes` definition units tests methods.
	"""

	def testToForwardSlashes(self):
		"""
		This method tests :func:`foundations.strings.toForwardSlashes` definition.
		"""

		self.assertIsInstance(foundations.strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), str)
		self.assertEqual(foundations.strings.toForwardSlashes("To\Forward\Slashes\Test\Case"),
						"To/Forward/Slashes/Test/Case")
		self.assertEqual(foundations.strings.toForwardSlashes("\Users/JohnDoe\Documents"), "/Users/JohnDoe/Documents")

class ToBackwardSlashesTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.toBackwardSlashes` definition units tests methods.
	"""

	def testToBackwardSlashes(self):
		"""
		This method tests :func:`foundations.strings.toBackwardSlashes` definition.
		"""

		self.assertIsInstance(foundations.strings.toBackwardSlashes("\Users\JohnDoe\Documents"), str)
		self.assertEqual(foundations.strings.toBackwardSlashes("To/Forward/Slashes/Test/Case"),
						"To\Forward\Slashes\Test\Case")
		self.assertEqual(foundations.strings.toBackwardSlashes("/Users/JohnDoe/Documents"), "\Users\JohnDoe\Documents")

class ToPosixPathTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.toPosixPath` definition units tests methods.
	"""

	def testToPosixPath(self):
		"""
		This method tests :func:`foundations.strings.toPosixPath` definition.
		"""

		self.assertIsInstance(foundations.strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), str)
		self.assertEqual(foundations.strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), "/Users/JohnDoe/Documents")
		self.assertEqual(foundations.strings.toPosixPath("\\Server\Users\\JohnDoe\\Documents"),
						"/Server/Users/JohnDoe/Documents")

class GetNormalizedPathTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getNormalizedPath` definition units tests methods.
	"""

	def testGetNormalizedPath(self):
		"""
		This method tests :func:`foundations.strings.getNormalizedPath` definition.
		"""

		self.assertIsInstance(foundations.strings.getNormalizedPath("/Users/JohnDoe/Documents"), str)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			self.assertEqual(foundations.strings.getNormalizedPath("C:/Users\JohnDoe/Documents"),
							r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(foundations.strings.getNormalizedPath("C://Users\/JohnDoe//Documents/"),
							r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(foundations.strings.getNormalizedPath("C:\\Users\\JohnDoe\\Documents"),
							r"C:\\Users\\JohnDoe\\Documents")
		else:
			self.assertEqual(foundations.strings.getNormalizedPath("/Users/JohnDoe/Documents/"), "/Users/JohnDoe/Documents")
			self.assertEqual(foundations.strings.getNormalizedPath("/Users\JohnDoe/Documents"), "/Users\JohnDoe/Documents")

class IsEmailTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.isEmail` definition units tests methods.
	"""

	def testIsEmail(self):
		"""
		This method tests :func:`foundations.strings.isEmail` definition.
		"""

		self.assertIsInstance(foundations.strings.isEmail("john.doe@domain.com"), bool)
		self.assertTrue(foundations.strings.isEmail("john.doe@domain.com"))
		self.assertTrue(foundations.strings.isEmail("john.doe@domain.server.department.company.com"))
		self.assertFalse(foundations.strings.isEmail("john.doe"))
		self.assertFalse(foundations.strings.isEmail("john.doe@domain"))

class IsWebsiteTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.isWebsite` definition units tests methods.
	"""

	def testIsWebsite(self):
		"""
		This method tests :func:`foundations.strings.isWebsite` definition.
		"""

		self.assertIsInstance(foundations.strings.isWebsite("http://domain.com"), bool)
		self.assertTrue(foundations.strings.isWebsite("http://www.domain.com"))
		self.assertTrue(foundations.strings.isWebsite("http://domain.com"))
		self.assertTrue(foundations.strings.isWebsite("https://domain.com"))
		self.assertTrue(foundations.strings.isWebsite("ftp://domain.com"))
		self.assertTrue(foundations.strings.isWebsite("http://domain.subdomain.com"))
		self.assertFalse(foundations.strings.isWebsite(".com"))
		self.assertFalse(foundations.strings.isWebsite("domain.com"))

class GetRandomSequenceTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.strings.getRandomSequence` definition units tests methods.
	"""

	def testGetRandomSequence(self):
		"""
		This method tests :func:`foundations.strings.getRandomSequence` definition.
		"""

		self.assertIsInstance(foundations.strings.getRandomSequence(), str)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
