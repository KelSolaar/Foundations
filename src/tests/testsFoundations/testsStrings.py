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
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**testsStrings.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Strings Tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports.
#***********************************************************************************************
import platform
import re
import unittest

#***********************************************************************************************
#***	Internal Imports.
#***********************************************************************************************
import foundations.strings as strings

#***********************************************************************************************
#***	Overall Variables.
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions.
#***********************************************************************************************
class GetNiceNameTestCase(unittest.TestCase):
	"""
	This Class Is The GetNiceNameTestCase Class.
	"""

	def testGetNiceName(self):
		"""
		This Method Tests The "getNiceName" Definition.
		"""

		self.assertIsInstance(strings.getNiceName("testGetNiceName"), str)
		self.assertEqual(strings.getNiceName("testGetNiceName"), "Test Get Nice Name")
		self.assertEqual(strings.getNiceName("TestGetNiceName"), "Test Get Nice Name")
		self.assertEqual(strings.getNiceName("_testGetNiceName"), "_test Get Nice Name")
		self.assertEqual(strings.getNiceName("Test Get NiceName"), "Test Get NiceName")

class GetVersionRankTestCase(unittest.TestCase):
	"""
	This Class Is The GetVersionRankTestCase Class.
	"""

	def testGetVersionRank(self):
		"""
		This Method Tests The "getVersionRank" Definition.
		"""

		self.assertIsInstance(strings.getVersionRank("0.0.0"), int)
		self.assertEqual(strings.getVersionRank("0.0.0"), 0)
		self.assertEqual(strings.getVersionRank("0.1.0"), 10)
		self.assertEqual(strings.getVersionRank("1.1.0"), 110)
		self.assertEqual(strings.getVersionRank("1.2.3.4.5"), 12345)

class GetSplitextBasenameTestCase(unittest.TestCase):
	"""
	This Class Is The GetSplitextBasenameTestCase Class.
	"""

	def testGetSplitextBasename(self):
		"""
		This Method Tests The "getSplitextBasename" Definition.
		"""

		self.assertIsInstance(strings.getSplitextBasename("/Users/JohnDoe/Documents"), str)
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test.txt"), "Test")
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test"), "Test")
		self.assertEqual(strings.getSplitextBasename("/Users/JohnDoe/Documents/Test/"), "Test")

class GetWordsTestCase(unittest.TestCase):
	"""
	This Class Is The GetWordsTestCase Class.
	"""

	def testGetWords(self):
		"""
		This Method Tests The "getWords" Definition.
		"""

		self.assertIsInstance(strings.getWords("Users are John Doe and Jane Doe."), list)
		self.assertListEqual(strings.getWords("Users are John Doe and Jane Doe."), "Users are John Doe and Jane Doe".split())
		self.assertListEqual(strings.getWords("Users are: John Doe, Jane Doe, Z6PO."), "Users are John Doe Jane Doe Z6PO".split())

class FilterWordsTestCase(unittest.TestCase):
	"""
	This Class Is The FilterWordsTestCase Class.
	"""

	def testFilterWords(self):
		"""
		This Method Tests The "filterWords" Definition.
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
	This Class Is The ReplaceTestCase Class.
	"""

	def testReplace(self):
		"""
		This Method Tests The "replace" Definition.
		"""

		self.assertIsInstance(strings.replace("To@Forward|Slashes@Test|Case", {}), str)
		self.assertEqual(strings.replace("To@Forward|Slashes@Test|Case", {"@":"|", "|":":"}), "To:Forward:Slashes:Test:Case")
		self.assertEqual(strings.replace("To@Forward@Slashes@Test@Case", {"@":"|", "|":"@", "@":"|" }), "To@Forward@Slashes@Test@Case")

class ToForwardSlashesTestCase(unittest.TestCase):
	"""
	This Class Is The ToForwardSlashesTestCase Class.
	"""

	def testToForwardSlashes(self):
		"""
		This Method Tests The "toForwardSlashes" Definition.
		"""

		self.assertIsInstance(strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), str)
		self.assertEqual(strings.toForwardSlashes("To\Forward\Slashes\Test\Case"), "To/Forward/Slashes/Test/Case")
		self.assertEqual(strings.toForwardSlashes("\Users/JohnDoe\Documents"), "/Users/JohnDoe/Documents")

class ToBackwardSlashesTestCase(unittest.TestCase):
	"""
	This Class Is The ToBackwardSlashesTestCase Class.
	"""

	def testToBackwardSlashes(self):
		"""
		This Method Tests The "toBackwardSlashes" Definition.
		"""

		self.assertIsInstance(strings.toBackwardSlashes("\Users\JohnDoe\Documents"), str)
		self.assertEqual(strings.toBackwardSlashes("To/Forward/Slashes/Test/Case"), "To\Forward\Slashes\Test\Case")
		self.assertEqual(strings.toBackwardSlashes("/Users/JohnDoe/Documents"), "\Users\JohnDoe\Documents")

class ToPosixPathTestCase(unittest.TestCase):
	"""
	This Class Is The ToPosixPathTestCase Class.
	"""

	def testToPosixPath(self):
		"""
		This Method Tests The "toPosixPath" Definition.
		"""

		self.assertIsInstance(strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), str)
		self.assertEqual(strings.toPosixPath("c:\\Users\\JohnDoe\\Documents"), "/Users/JohnDoe/Documents")
		self.assertEqual(strings.toPosixPath("\\Server\Users\\JohnDoe\\Documents"), "/Server/Users/JohnDoe/Documents")

class GetNormalizedPathTestCase(unittest.TestCase):
	"""
	This Class Is The GetNormalizedPathTestCase Class.
	"""

	def testGetNormalizedPath(self):
		"""
		This Method Tests The "getNormalizedPath" Definition.
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
	This Class Is The IsEmailTestCase Class.
	"""

	def testIsEmail(self):
		"""
		This Method Tests The "isEmail" Definition.
		"""

		self.assertIsInstance(strings.isEmail("john.doe@domain.com"), bool)
		self.assertTrue(strings.isEmail("john.doe@domain.com"))
		self.assertTrue(strings.isEmail("john.doe@domain.server.department.company.com"))
		self.assertFalse(strings.isEmail("john.doe"))
		self.assertFalse(strings.isEmail("john.doe@domain"))

class IsWebsiteTestCase(unittest.TestCase):
	"""
	This Class Is The IsWebsiteTestCase Class.
	"""

	def testIsWebsite(self):
		"""
		This Method Tests The "isWebsite" Definition.
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

#***********************************************************************************************
#***	Python End.
#***********************************************************************************************
