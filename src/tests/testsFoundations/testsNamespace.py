#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsNamespace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Namespace tests Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.namespace as namespace

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
class SetNamespaceTestCase(unittest.TestCase):
	"""
	This class is the SetNamespaceTestCase class.
	"""

	def testSetNamespace(self):
		"""
		This method tests the "setNamespace" definition.
		"""

		self.assertIsInstance(namespace.setNamespace("Namespace", "Attribute"), str)
		self.assertEqual(namespace.setNamespace("Namespace", "Attribute"), "Namespace|Attribute")
		self.assertEqual(namespace.setNamespace("Namespace", "Attribute", ":"), "Namespace:Attribute")

class GetNamespaceTestCase(unittest.TestCase):
	"""
	This class is the GetNamespaceTestCase class.
	"""

	def testGetNamespace(self):
		"""
		This method tests the "getNamespace" definition.
		"""

		self.assertIsInstance(namespace.getNamespace("Namespace:Attribute", ":"), str)
		self.assertEqual(namespace.getNamespace("Namespace|Attribute"), "Namespace")
		self.assertEqual(namespace.getNamespace("Namespace:Attribute", ":"), "Namespace")
		self.assertEqual(namespace.getNamespace("Namespace|Attribute|Value", rootOnly=True), "Namespace")
		self.assertIsNone(namespace.getNamespace("Namespace"))

class RemoveNamespaceTestCase(unittest.TestCase):
	"""
	This class is the RemoveNamespaceTestCase class.
	"""

	def testRemoveNamespace(self):
		"""
		This method tests the "testRemoveNamespace" definition.
		"""

		self.assertIsInstance(namespace.removeNamespace("Namespace|Attribute"), str)
		self.assertEqual(namespace.removeNamespace("Namespace|Attribute"), "Attribute")
		self.assertEqual(namespace.removeNamespace("Namespace:Attribute", ":"), "Attribute")
		self.assertEqual(namespace.removeNamespace("Namespace|Attribute|Value"), "Value")
		self.assertEqual(namespace.removeNamespace("Namespace|Attribute|Value", rootOnly=True), "Attribute|Value")

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

