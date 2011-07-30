#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsStrings.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Strings tests Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import platform
import re
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.strings as strings

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
class GetNiceNameTestCase(unittest.TestCase):
	"""
	This class is the GetNiceNameTestCase class.
	"""

	def testGetNiceName(self):
		"""
		This method tests the "getNiceName" definition.
		"""

		self.assertIsInstance(strings.getNiceName("testGetNiceName"), str)
		self.assertEqual(strings.getNiceName("testGetNiceName"), "Test Get Nice Name")
		self.assertEqual(strings.getNiceName("TestGetNiceName"), "Test Get Nice Name")
		self.assertEqual(strings.getNiceName("_testGetNiceName"), "_test Get Nice Name")
		self.assertEqual(strings.getNiceName("Test Get NiceName"), "Test Get NiceName")

class GetVersionRankTestCase(unittest.TestCase):
	"""
	This class is the GetVersionRankTestCase class.
	"""

	def testGetVersionRank(self):
		"""
		This method tests the "getVersionRank" definition.
		"""

		self.assertIsInstance(strings.getVersionRank("0.0.0"), int)
		self.assertEqual(strings.getVersionRank("0.0.0"), 0)
		self.assertEqual(strings.getVersionRank("0.1.0"), 10)
		self.assertEqual(strings.getVersionRank("1.1.0"), 110)
		self.assertEqual(strings.getVersionRank("1.2.3.4.5"), 12345)

class GetSplitextBasenameTestCase(unittest.TestCase):
	"""
	This class is the GetSplitextBasenameTestCase class.
	"""

	def testGetSplitextBasename(self):
		"""
		This method tests the "getSplitextBasename" definition.
		"""

		self.assertIsInstance(strings.getSplitextBasename("/Users/JohnDoe/Documents"), str)
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test.txt"), "Test")
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test"), "Test")
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test/"), "Test")

class GetWordsTestCase(unittest.TestCase):
	"""
	This class is the GetWordsTestCase class.
	"""

	def testGetWords(self):
		"""
		This method tests the "getWords" definition.
		"""

		self.assertIsInstance(strings.getWords("Users are John Doe and Jane Doe."), list)
		self.assertListEqual(strings.getWords("Users are John Doe and Jane Doe."), "Users are John Doe and Jane Doe".split())
		self.assertListEqual(strings.getWords("Users are: John Doe, Jane Doe, Z6PO."), "Users are John Doe Jane Doe Z6PO".split())

class FilterWordsTestCase(unittest.TestCase):
	"""
	This class is the FilterWordsTestCase class.
	"""

	def testFilterWords(self):
		"""
		This method tests the "filterWords" definition.
		"""

		self.assertIsInstance(strings.filterWords("Users are John Doe and Jane Doe".split()), list)
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(), filtersIn=("Users", "John")), "Users John".split())
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(), filtersIn=("users", "john"), flags=re.IGNORECASE), "Users John".split())
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(), filtersIn=("Nemo",)), [])
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(), filtersOut=("Users", "John")), "are Doe and Jane Doe".split())
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(), filtersOut=("Users are John Doe and Jane Doe".split())), [])
		self.assertListEqual(strings.filterWords("Users are John Doe and Jane Doe".split(), filtersIn=("Users",), filtersOut=("Users",)), [])

class ReplaceTestCase(unittest.TestCase):
	"""
	This class is the ReplaceTestCase class.
	"""

	def testReplace(self):
		"""
		This method tests the "replace" definition.
		"""

		self.assertIsInstance(strings.replace("To@Forward|Slashes@Test|Case", {}), str)
		self.assertEqual(strings.replace("To@Forward|Slashes@Test|Case", {"@":"|", "|":":"}), "To:Forward:Slashes:Test:Case")
		self.assertEqual(strings.replace("To@Forward@Slashes@Test@Case", {"@":"|", "|":"@", "@":"|" }), "To@Forward@Slashes@Test@Case")

class ToForwardSlashesTestCase(unittest.TestCase):
	"""
	This class is the ToForwardSlashesTestCase class.
	"""

	def testToForwardSlashes(self):
		"""
		This method tests the "toForwardSlashes" definition.
		"""

		self.assertIsInstance(strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), str)
		self.assertEqual(strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), "To/Forward/Slashes/Test/Case")
		self.assertEqual(strings.toForwardSlashes("\Users/JohnDoe\Documents"), "/Users/JohnDoe/Documents")

class ToBackwardSlashesTestCase(unittest.TestCase):
	"""
	This class is the ToBackwardSlashesTestCase class.
	"""

	def testToBackwardSlashes(self):
		"""
		This method tests the "toBackwardSlashes" definition.
		"""

		self.assertIsInstance(strings.toBackwardSlashes("\Users\JohnDoe\Documents"), str)
		self.assertEqual(strings.toBackwardSlashes("To/Forward/Slashes/Test/Case"), "To\Forward\Slashes\Test\Case")
		self.assertEqual(strings.toBackwardSlashes("/Users/JohnDoe/Documents"), "\Users\JohnDoe\Documents")

class ToPosixPathTestCase(unittest.TestCase):
	"""
	This class is the ToPosixPathTestCase class.
	"""

	def testToPosixPath(self):
		"""
		This method tests the "toPosixPath" definition.
		"""

		self.assertIsInstance(strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), str)
		self.assertEqual(strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), "/Users/JohnDoe/Documents")
		self.assertEqual(strings.toPosixPath("\\Server\Users\\JohnDoe\\Documents"), "/Server/Users/JohnDoe/Documents")

class GetNormalizedPathTestCase(unittest.TestCase):
	"""
	This class is the GetNormalizedPathTestCase class.
	"""

	def testGetNormalizedPath(self):
		"""
		This method tests the "getNormalizedPath" definition.
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
	This class is the IsEmailTestCase class.
	"""

	def testIsEmail(self):
		"""
		This method tests the "isEmail" definition.
		"""

		self.assertIsInstance(strings.isEmail("john.doe@domain.com"), bool)
		self.assertTrue(strings.isEmail("john.doe@domain.com"))
		self.assertTrue(strings.isEmail("john.doe@domain.server.department.company.com"))
		self.assertFalse(strings.isEmail("john.doe"))
		self.assertFalse(strings.isEmail("john.doe@domain"))

class IsWebsiteTestCase(unittest.TestCase):
	"""
	This class is the IsWebsiteTestCase class.
	"""

	def testIsWebsite(self):
		"""
		This method tests the "isWebsite" definition.
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

