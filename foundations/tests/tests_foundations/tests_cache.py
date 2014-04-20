#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_cache.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.cache` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines :class:`foundations.cache.Cache` class units tests methods.
	"""

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("add_content",
							"remove_content",
							"get_content",
							"flush_content")

		for method in required_methods:
			self.assertIn(method, dir(Cache))

	def test_add_content(self):
		"""
		Tests :meth:`foundations.cache.Cache.add_content` method.
		"""

		cache = Cache()
		self.assertTrue(cache.add_content(John="Doe", Luke="Skywalker"))
		self.assertDictEqual(cache, {"John" : "Doe", "Luke" : "Skywalker"})

	def test_removeContent(self):
		"""
		Tests :meth:`foundations.cache.Cache.remove_content` method.
		"""

		cache = Cache()
		cache.add_content(John="Doe", Luke="Skywalker")
		self.assertTrue(cache.remove_content("John", "Luke"))
		self.assertDictEqual(cache, {})

	def test_get_content(self):
		"""
		Tests :meth:`foundations.cache.Cache.get_content` method.
		"""

		cache = Cache()
		content = {"John" : "Doe", "Luke" : "Skywalker"}
		cache.add_content(**content)
		for key, value in content.iteritems():
			self.assertEqual(cache.get_content(key), value)

	def test_flush_content(self):
		"""
		Tests :meth:`foundations.cache.Cache.flush_content` method.
		"""

		cache = Cache()
		cache.add_content(John="Doe", Luke="Skywalker")
		self.assertTrue(cache.flush_content())
		self.assertDictEqual(cache, {})

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
