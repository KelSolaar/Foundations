#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsNamespace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.namespace` module.

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
import foundations.namespace

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["SetNamespaceTestCase",
		"GetNamespaceTestCase",
		"RemoveNamespaceTestCase",
		"GetRootTestCase",
		"GetLeafTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SetNamespaceTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.namespace.setNamespace` definition units tests methods.
	"""

	def testSetNamespace(self):
		"""
		Tests :func:`foundations.namespace.setNamespace` definition.
		"""

		self.assertIsInstance(foundations.namespace.setNamespace("Namespace", "Attribute"), unicode)
		self.assertEqual(foundations.namespace.setNamespace("Namespace", "Attribute"), "Namespace|Attribute")
		self.assertEqual(foundations.namespace.setNamespace("Namespace", "Attribute", ":"), "Namespace:Attribute")

class GetNamespaceTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.namespace.getNamespace` definition units tests methods.
	"""

	def testGetNamespace(self):
		"""
		Tests :func:`foundations.namespace.getNamespace` definition.
		"""

		self.assertIsInstance(foundations.namespace.getNamespace("Namespace:Attribute", ":"), unicode)
		self.assertEqual(foundations.namespace.getNamespace("Namespace|Attribute"), "Namespace")
		self.assertEqual(foundations.namespace.getNamespace("Namespace:Attribute", ":"), "Namespace")
		self.assertEqual(foundations.namespace.getNamespace("Namespace|Attribute|Value", rootOnly=True), "Namespace")
		self.assertIsNone(foundations.namespace.getNamespace("Namespace"))

class RemoveNamespaceTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.namespace.removeNamespace` definition units tests methods.
	"""

	def testRemoveNamespace(self):
		"""
		Tests :func:`foundations.namespace.removeNamespace` definition.
		"""

		self.assertIsInstance(foundations.namespace.removeNamespace("Namespace|Attribute"), unicode)
		self.assertEqual(foundations.namespace.removeNamespace("Namespace|Attribute"), "Attribute")
		self.assertEqual(foundations.namespace.removeNamespace("Namespace:Attribute", ":"), "Attribute")
		self.assertEqual(foundations.namespace.removeNamespace("Namespace|Attribute|Value"), "Value")
		self.assertEqual(foundations.namespace.removeNamespace("Namespace|Attribute|Value", rootOnly=True), "Attribute|Value")

class GetRootTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.namespace.getRoot` definition units tests methods.
	"""

	def testGetRoot(self):
		"""
		Tests :func:`foundations.namespace.getRoot` definition.
		"""

		self.assertEqual(foundations.namespace.getRoot("Attribute"), None)
		self.assertEqual(foundations.namespace.getRoot("Namespace|Attribute"), "Namespace")
		self.assertEqual(foundations.namespace.getRoot("Namespace:Attribute", ":"), "Namespace")

class GetLeafTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.namespace.getLeaf` definition units tests methods.
	"""

	def testGetLeaf(self):
		"""
		Tests :func:`foundations.namespace.getLeaf` definition.
		"""

		self.assertEqual(foundations.namespace.getLeaf("Attribute"), "Attribute")
		self.assertEqual(foundations.namespace.getLeaf("Namespace|Attribute"), "Attribute")
		self.assertEqual(foundations.namespace.getLeaf("Namespace:Attribute", ":"), "Attribute")

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
