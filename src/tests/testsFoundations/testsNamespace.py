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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**testsNamespace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Namespace tests Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.namespace as namespace

#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************

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

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
