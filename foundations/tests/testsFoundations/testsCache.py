#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**testsCache.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.cache` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from foundations.cache import Cache

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
			"CacheTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class CacheTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.cache.Cache` class units tests methods.
	"""

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("addContent",
							"removeContent",
							"getContent",
							"flushContent")

		for method in requiredMethods:
			self.assertIn(method, dir(Cache))

	def testAddContent(self):
		"""
		This method tests :meth:`foundations.cache.Cache.addContent` method.
		"""

		cache = Cache()
		self.assertTrue(cache.addContent(John="Doe", Luke="Skywalker"))
		self.assertDictEqual(cache, {"John" : "Doe", "Luke" : "Skywalker"})

	def testRemoveContent(self):
		"""
		This method tests :meth:`foundations.cache.Cache.removeContent` method.
		"""

		cache = Cache()
		cache.addContent(John="Doe", Luke="Skywalker")
		self.assertTrue(cache.removeContent("John", "Luke"))
		self.assertDictEqual(cache, {})

	def testGetContent(self):
		"""
		This method tests :meth:`foundations.cache.Cache.getContent` method.
		"""

		cache = Cache()
		content = {"John" : "Doe", "Luke" : "Skywalker"}
		cache.addContent(**content)
		for key, value in content.iteritems():
			self.assertEqual(cache.getContent(key), value)

	def testFlushContent(self):
		"""
		This method tests :meth:`foundations.cache.Cache.flushContent` method.
		"""

		cache = Cache()
		cache.addContent(John="Doe", Luke="Skywalker")
		self.assertTrue(cache.flushContent())
		self.assertDictEqual(cache, {})

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
