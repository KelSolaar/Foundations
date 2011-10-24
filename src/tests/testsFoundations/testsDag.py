#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsDag.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.dag` module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from foundations.dag import Attribute, AbstractNode, AbstractCompositeNode

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["AttributeTestCase", "AbstractNodeTestCase", "AbstractCompositeNode"]

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class AttributeTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.dag.Attribute` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("name",
							"value")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(Attribute))

class AbstractNodeTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.dag.AbstractNode` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("family",
							"identity",
							"nodesInstances",
							"name")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(AbstractNode))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("getNodeByIdentity",
							"listAttributes",
							"getAttributes",
							"attributeExists",
							"addAttribute",
							"removeAttribute")

		for method in requiredMethods:
			self.assertIn(method, dir(AbstractNode))

	def testFamily(self):
		"""
		This method tests :class:`foundations.dag.AbstractNode` class family property.
		"""

		nodeA = AbstractNode("MyNode")
		self.assertEqual(nodeA.family, "Abstract")

	def testName(self):
		"""
		This method tests :class:`foundations.dag.AbstractNode` class name resolving consistency.
		"""

		nodeA = AbstractNode("MyNodeA")
		self.assertEqual(nodeA.name, "MyNodeA")
		nodeB = AbstractNode()
		self.assertEqual(nodeB.name, "Abstract{0}".format(nodeB.identity))

	def testGetNodeByIdentity(self):
		"""
		This method tests :meth:`foundations.dag.AbstractNode.getNodeByIdentity` method.
		"""

		nodeA = AbstractNode()
		self.assertIsInstance(AbstractNode.getNodeByIdentity(nodeA.identity), AbstractNode)
		nodeB = AbstractNode()
		self.assertIsInstance(AbstractNode.getNodeByIdentity(nodeB.identity), AbstractNode)
		self.assertEqual(AbstractNode.getNodeByIdentity(nodeB.identity), nodeB)

	def testListAttributes(self):
		"""
		This method tests :meth:`foundations.dag.AbstractNode.listAttributes` method.
		"""

		nodeA = AbstractNode("MyNodeA")
		self.assertListEqual(nodeA.listAttributes(), [])
		nodeB = AbstractNode("MyNodeB", attributeA=Attribute(), attributeB=Attribute())
		self.assertListEqual(sorted(nodeB.listAttributes()), ["attributeA", "attributeB"])

	def testGetAttributes(self):
		"""
		This method tests :meth:`foundations.dag.AbstractNode.getAttributes` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA", **attributes)
		for attribute in attributes.values():
			self.assertIn(attribute, nodeA.getAttributes())

	def testHasAttribute(self):
		"""
		This method tests :meth:`foundations.dag.AbstractNode.attributeExists` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA", **attributes)
		for attribute in attributes.keys():
			self.assertTrue(nodeA.attributeExists(attribute))
		nodeB = AbstractNode("MyNodeB", nonAttribute="Non Attribute")
		self.assertFalse(nodeA.attributeExists("nonAttribute"))

	def testAddAttribute(self):
		"""
		This method tests :meth:`foundations.dag.AbstractNode.addAttribute` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA")
		for attribute, value in attributes.items():
			self.assertTrue(nodeA.addAttribute(attribute, value))
			self.assertTrue(nodeA.attributeExists(attribute))

	def testRemoveAttribute(self):
		"""
		This method tests :meth:`foundations.dag.AbstractNode.removeAttribute` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA")
		for attribute, value in attributes.items():
			self.assertTrue(nodeA.addAttribute(attribute, value))
			self.assertTrue(nodeA.removeAttribute(attribute))
			self.assertFalse(nodeA.attributeExists(attribute))

class AbstractCompositeNodeTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.dag.AbstractCompositeNode` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("family",
							"identity",
							"nodesInstances",
							"name",
							"parent",
							"children")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(AbstractCompositeNode))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("getNodeByIdentity",
							"listAttributes",
							"getAttributes",
							"attributeExists",
							"addAttribute",
							"removeAttribute",
							"child",
							"indexOf",
							"row",
							"addChild",
							"removeChild",
							"insertChild",
							"childrenCount",
							"listNode")

		for method in requiredMethods:
			self.assertIn(method, dir(AbstractCompositeNode))

	def testChild(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.child` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		self.assertEqual(nodeA.child(0), nodeB)

	def testIndexOf(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.indexOf` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		self.assertEqual(nodeA.indexOf(nodeB), 0)

	def testRow(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.row` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		nodeD = AbstractCompositeNode("MyNodeD", nodeA)
		for i, node in enumerate((nodeB, nodeC, nodeD)):
			self.assertEqual(node.row(), i)

	def testAddChild(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.addChild` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB")
		self.assertListEqual(nodeA.children, [])
		self.assertTrue(nodeA.addChild(nodeB))
		self.assertIn(nodeB, nodeA.children)

	def testRemoveChild(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.removeChild` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		self.assertTrue(nodeA.removeChild(0))
		self.assertListEqual(nodeA.children, [])

	def testInsertChild(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.insertChild` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		nodeD = AbstractCompositeNode("MyNodeD")
		self.assertTrue(nodeA.insertChild(nodeD, 1))
		for i, node in enumerate((nodeB, nodeD, nodeC)):
			self.assertEqual(nodeA.indexOf(node), i)

	def testChildrenCount(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.childrenCount` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		self.assertEqual(nodeA.childrenCount(), 0)
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		self.assertEqual(nodeA.childrenCount(), 2)

	def testListNode(self):
		"""
		This method tests :meth:`foundations.dag.AbstractCompositeNode.listNode` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		self.assertIsInstance(nodeA.listNode(), str)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
