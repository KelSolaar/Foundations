#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_strings.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.strings` module.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
import re
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

import foundations.strings

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestToString",
		"TestGetNiceName",
		"TestGetVersionRank",
		"TestGetSplitextBasename",
		"TestGetCommonAncestor",
		"TestGetCommonPathsAncestor",
		"TestGetWords",
		"TestFilterWords",
		"TestReplace",
		"TestToForwardSlashes",
		"TestToBackwardSlashes",
		"TestToPosixPath",
		"TestGetNormalizedPath",
		"TestGetRandomSequence",
		"TestIsEmail",
		"TestIsWebsite"]

class TestToString(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.to_string` definition units tests methods.
	"""

	def test_to_string(self):
		"""
		Tests :func:`foundations.strings.to_string` definition.
		"""

		self.assertIsInstance(foundations.strings.to_string(str("myData")), unicode)
		self.assertIsInstance(foundations.strings.to_string(u"myData"), unicode)
		self.assertIsInstance(foundations.strings.to_string(0), unicode)
		self.assertIsInstance(foundations.strings.to_string(None), unicode)
		self.assertIsInstance(foundations.strings.to_string(True), unicode)

class TestGetNiceName(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_nice_name` definition units tests methods.
	"""

	def test_get_nice_name(self):
		"""
		Tests :func:`foundations.strings.get_nice_name` definition.
		"""

		self.assertIsInstance(foundations.strings.get_nice_name("testGetNiceName"), unicode)
		self.assertEqual(foundations.strings.get_nice_name("testGetNiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.get_nice_name("TestGetNiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.get_nice_name("_testGetNiceName"), "_Test Get Nice Name")
		self.assertEqual(foundations.strings.get_nice_name("Test Get NiceName"), "Test Get Nice Name")
		self.assertEqual(foundations.strings.get_nice_name("testGetMeANiceName"), "Test Get Me A Nice Name")

class TestGetVersionRank(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_version_rank` definition units tests methods.
	"""

	def test_get_version_rank(self):
		"""
		Tests :func:`foundations.strings.get_version_rank` definition.
		"""

		self.assertTrue(type(foundations.strings.get_version_rank("0.0.0")), (int, long))
		self.assertEqual(foundations.strings.get_version_rank("0.0.0"), 0)
		self.assertEqual(foundations.strings.get_version_rank("0.1.0"), 1000000000)
		self.assertEqual(foundations.strings.get_version_rank("1.1.0"), 1001000000000)
		self.assertEqual(foundations.strings.get_version_rank("1.2.3.4.5"), 1002003004000)
		self.assertEqual(foundations.strings.get_version_rank("4.0"), 4000000000000)
		self.assertEqual(foundations.strings.get_version_rank(""), 0)

class TestGetSplitextBasename(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_splitext_basename` definition units tests methods.
	"""

	def test_get_splitext_basename(self):
		"""
		Tests :func:`foundations.strings.get_splitext_basename` definition.
		"""

		self.assertIsInstance(foundations.strings.get_splitext_basename("/Users/JohnDoe/Documents"), unicode)
		self.assertEqual(foundations.strings.get_splitext_basename("/Users/JohnDoe/Documents/Test.txt"), "Test")
		self.assertEqual(foundations.strings.get_splitext_basename("/Users/JohnDoe/Documents/Test"), "Test")
		self.assertEqual(foundations.strings.get_splitext_basename("/Users/JohnDoe/Documents/Test/"), "Test")

class TestGetCommonAncestor(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_common_ancestor` definition units tests methods.
	"""

	def test_get_common_ancestor(self):
		"""
		Tests :func:`foundations.strings.get_common_ancestor` definition.
		"""

		self.assertTupleEqual(foundations.strings.get_common_ancestor(("1", "2", "3"), ("1", "2", "0"), ("1", "2", "3", "4")),
														("1", "2"))
		self.assertEqual(foundations.strings.get_common_ancestor("azerty", "azetty", "azello"), "aze")
		self.assertEqual(foundations.strings.get_common_ancestor(
		"/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt"),
		"/Users/JohnDoe/Documents")
		self.assertFalse(foundations.strings.get_common_ancestor("azerty", "qwerty"))

class TestGetCommonPathsAncestor(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_common_paths_ancestor` definition units tests methods.
	"""

	def test_get_common_paths_ancestor(self):
		"""
		Tests :func:`foundations.strings.get_common_paths_ancestor` definition.
		"""

		self.assertEqual(foundations.strings.get_common_paths_ancestor("{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents"))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents", "Test.txt")))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents"))))

		self.assertFalse(foundations.strings.get_common_paths_ancestor("{0}{1}".format(os.sep,
														os.sep.join(("JohnDoe", "Documents"))),
														"{0}{1}".format(os.sep,
														os.sep.join(("Users", "JohnDoe", "Documents", "Test.txt")))))

class TestGetWords(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_words` definition units tests methods.
	"""

	def test_get_words(self):
		"""
		Tests :func:`foundations.strings.get_words` definition.
		"""

		self.assertIsInstance(foundations.strings.get_words("Users are John Doe and Jane Doe."), list)
		self.assertListEqual(foundations.strings.get_words("Users are John Doe and Jane Doe."),
							"Users are John Doe and Jane Doe".split())
		self.assertListEqual(foundations.strings.get_words("Users are: John Doe, Jane Doe, Z6PO."),
							"Users are John Doe Jane Doe Z6PO".split())

class TestFilterWords(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.filter_words` definition units tests methods.
	"""

	def test_filter_words(self):
		"""
		Tests :func:`foundations.strings.filter_words` definition.
		"""

		self.assertIsInstance(foundations.strings.filter_words("Users are John Doe and Jane Doe".split()), list)
		self.assertListEqual(foundations.strings.filter_words("Users are John Doe and Jane Doe".split(),
												filters_in=("Users", "John")),
												"Users John".split())
		self.assertListEqual(foundations.strings.filter_words("Users are John Doe and Jane Doe".split(),
												filters_in=("users", "john"),
												flags=re.IGNORECASE),
												"Users John".split())
		self.assertListEqual(foundations.strings.filter_words("Users are John Doe and Jane Doe".split(),
												filters_in=("Nemo",)),
												[])
		self.assertListEqual(foundations.strings.filter_words("Users are John Doe and Jane Doe".split(),
												filters_out=("Users", "John")),
												"are Doe and Jane Doe".split())
		self.assertListEqual(foundations.strings.filter_words("Users are John Doe and Jane Doe".split(),
												filters_out=("Users are John Doe and Jane Doe".split())),
												[])
		self.assertListEqual(foundations.strings.filter_words("Users are John Doe and Jane Doe".split(),
												filters_in=("Users",),
												filters_out=("Users",)),
												[])

class TestReplace(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.replace` definition units tests methods.
	"""

	def test_replace(self):
		"""
		Tests :func:`foundations.strings.replace` definition.
		"""

		self.assertIsInstance(foundations.strings.replace("To@Forward|Slashes@Test|Case", {}), unicode)
		self.assertEqual(foundations.strings.replace("To@Forward|Slashes@Test|Case", {"@":"|", "|":":"}),
						"To:Forward:Slashes:Test:Case")
		self.assertEqual(foundations.strings.replace("To@Forward@Slashes@Test@Case", {"@":"|", "|":"@"}),
						"To@Forward@Slashes@Test@Case")

class TestRemoveStrip(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.remove_strip` definition units tests methods.
	"""

	def test_remove_strip(self):
		"""
		Tests :func:`foundations.strings.remove_strip` definition.
		"""

		self.assertIsInstance(foundations.strings.remove_strip("John Doe", "John"), unicode)
		self.assertEqual(foundations.strings.remove_strip("John Doe", "John"), "Doe")
		self.assertEqual(foundations.strings.remove_strip("John Doe", "Doe"), "John")

class TestToForwardSlashes(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.to_forward_slashes` definition units tests methods.
	"""

	def test_to_forward_slashes(self):
		"""
		Tests :func:`foundations.strings.to_forward_slashes` definition.
		"""

		self.assertIsInstance(foundations.strings.to_forward_slashes("To\\Forward\\Slashes\\Test\\Case"), unicode)
		self.assertEqual(foundations.strings.to_forward_slashes("To\\Forward\\Slashes\\Test\\Case"),
						"To/Forward/Slashes/Test/Case")
		self.assertEqual(foundations.strings.to_forward_slashes("\\Users/JohnDoe\\Documents"), "/Users/JohnDoe/Documents")

class TestToBackwardSlashes(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.to_backward_slashes` definition units tests methods.
	"""

	def test_to_backward_slashes(self):
		"""
		Tests :func:`foundations.strings.to_backward_slashes` definition.
		"""

		self.assertIsInstance(foundations.strings.to_backward_slashes("\\Users\\JohnDoe\\Documents"), unicode)
		self.assertEqual(foundations.strings.to_backward_slashes("To/Forward/Slashes/Test/Case"),
						"To\\Forward\\Slashes\\Test\\Case")
		self.assertEqual(foundations.strings.to_backward_slashes("/Users/JohnDoe/Documents"), "\\Users\\JohnDoe\\Documents")

class TestToPosixPath(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.to_posix_path` definition units tests methods.
	"""

	def test_to_posix_path(self):
		"""
		Tests :func:`foundations.strings.to_posix_path` definition.
		"""

		self.assertIsInstance(foundations.strings.to_posix_path("c:\\Users\\JohnDoe\\Documents"), unicode)
		self.assertEqual(foundations.strings.to_posix_path("c:\\Users\\JohnDoe\\Documents"), "/Users/JohnDoe/Documents")
		self.assertEqual(foundations.strings.to_posix_path("\\Server\\Users\\JohnDoe\\Documents"),
						"/Server/Users/JohnDoe/Documents")

class TestGetNormalizedPath(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_normalized_path` definition units tests methods.
	"""

	def test_get_normalized_path(self):
		"""
		Tests :func:`foundations.strings.get_normalized_path` definition.
		"""

		self.assertIsInstance(foundations.strings.get_normalized_path("/Users/JohnDoe/Documents"), unicode)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			self.assertEqual(foundations.strings.get_normalized_path("C:/Users\JohnDoe/Documents"),
							r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(foundations.strings.get_normalized_path("C://Users\/JohnDoe//Documents/"),
							r"C:\\Users\\JohnDoe\\Documents")
			self.assertEqual(foundations.strings.get_normalized_path("C:\\Users\\JohnDoe\\Documents"),
							r"C:\\Users\\JohnDoe\\Documents")
		else:
			self.assertEqual(foundations.strings.get_normalized_path("/Users/JohnDoe/Documents/"), "/Users/JohnDoe/Documents")
			self.assertEqual(foundations.strings.get_normalized_path("/Users\JohnDoe/Documents"), "/Users\JohnDoe/Documents")

class TestIsEmail(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.is_email` definition units tests methods.
	"""

	def test_is_email(self):
		"""
		Tests :func:`foundations.strings.is_email` definition.
		"""

		self.assertIsInstance(foundations.strings.is_email("john.doe@domain.com"), bool)
		self.assertTrue(foundations.strings.is_email("john.doe@domain.com"))
		self.assertTrue(foundations.strings.is_email("john.doe@domain.server.department.company.com"))
		self.assertFalse(foundations.strings.is_email("john.doe"))
		self.assertFalse(foundations.strings.is_email("john.doe@domain"))

class TestIsWebsite(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.is_website` definition units tests methods.
	"""

	def test_is_website(self):
		"""
		Tests :func:`foundations.strings.is_website` definition.
		"""

		self.assertIsInstance(foundations.strings.is_website("http://domain.com"), bool)
		self.assertTrue(foundations.strings.is_website("http://www.domain.com"))
		self.assertTrue(foundations.strings.is_website("http://domain.com"))
		self.assertTrue(foundations.strings.is_website("https://domain.com"))
		self.assertTrue(foundations.strings.is_website("ftp://domain.com"))
		self.assertTrue(foundations.strings.is_website("http://domain.subdomain.com"))
		self.assertFalse(foundations.strings.is_website(".com"))
		self.assertFalse(foundations.strings.is_website("domain.com"))

class TestGetRandomSequence(unittest.TestCase):
	"""
	Defines :func:`foundations.strings.get_random_sequence` definition units tests methods.
	"""

	def test_get_random_sequence(self):
		"""
		Tests :func:`foundations.strings.get_random_sequence` definition.
		"""

		self.assertIsInstance(foundations.strings.get_random_sequence(), unicode)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
