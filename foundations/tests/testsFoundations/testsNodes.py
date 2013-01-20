#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsNodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.nodes` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import pickle
import re
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from foundations.nodes import AbstractCompositeNode
from foundations.nodes import AbstractNode
from foundations.nodes import Attribute

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["AttributeTestCase", "AbstractNodeTestCase", "AbstractCompositeNode"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class AttributeTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.nodes.Attribute` class units tests methods.
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
	This class defines :class:`foundations.nodes.AbstractNode` class units tests methods.
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
		This method tests :class:`foundations.nodes.AbstractNode` class family property.
		"""

		nodeA = AbstractNode("MyNode")
		self.assertEqual(nodeA.family, "Abstract")

	def testName(self):
		"""
		This method tests :class:`foundations.nodes.AbstractNode` class name resolving consistency.
		"""

		nodeA = AbstractNode("MyNodeA")
		self.assertEqual(nodeA.name, "MyNodeA")
		nodeB = AbstractNode()
		self.assertEqual(nodeB.name, "Abstract{0}".format(nodeB.identity))

	def testGetNodeByIdentity(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractNode.getNodeByIdentity` method.
		"""

		nodeA = AbstractNode()
		self.assertIsInstance(AbstractNode.getNodeByIdentity(nodeA.identity), AbstractNode)
		nodeB = AbstractNode()
		self.assertIsInstance(AbstractNode.getNodeByIdentity(nodeB.identity), AbstractNode)
		self.assertEqual(AbstractNode.getNodeByIdentity(nodeB.identity), nodeB)

	def testListAttributes(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractNode.listAttributes` method.
		"""

		nodeA = AbstractNode("MyNodeA")
		self.assertListEqual(nodeA.listAttributes(), [])
		nodeB = AbstractNode("MyNodeB", attributeA=Attribute(), attributeB=Attribute())
		self.assertListEqual(sorted(nodeB.listAttributes()), ["attributeA", "attributeB"])

	def testGetAttributes(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractNode.getAttributes` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA", **attributes)
		for attribute in attributes.itervalues():
			self.assertIn(attribute, nodeA.getAttributes())

	def testHasAttribute(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractNode.attributeExists` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA", **attributes)
		for attribute in attributes:
			self.assertTrue(nodeA.attributeExists(attribute))
		nodeB = AbstractNode("MyNodeB", nonAttribute="Non Attribute")
		self.assertFalse(nodeB.attributeExists("nonAttribute"))

	def testAddAttribute(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractNode.addAttribute` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA")
		for attribute, value in attributes.iteritems():
			self.assertTrue(nodeA.addAttribute(attribute, value))
			self.assertTrue(nodeA.attributeExists(attribute))

	def testRemoveAttribute(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractNode.removeAttribute` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		nodeA = AbstractNode("MyNodeA")
		for attribute, value in attributes.iteritems():
			self.assertTrue(nodeA.addAttribute(attribute, value))
			self.assertTrue(nodeA.removeAttribute(attribute))
			self.assertFalse(nodeA.attributeExists(attribute))

	def testAbstractNodePickle(self):
		"""
		This method tests :class:`foundations.nodes.AbstractNode` class pickling.
		"""

		nodeA = AbstractNode("MyNodeA", attributeA=Attribute(), attributeB=Attribute())

		data = pickle.dumps(nodeA)
		data = pickle.loads(data)
		self.assertEqual(nodeA, data)

		data = pickle.dumps(nodeA, pickle.HIGHEST_PROTOCOL)
		data = pickle.loads(data)
		self.assertEqual(nodeA, data)

class AbstractCompositeNodeTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.nodes.AbstractCompositeNode` class units tests methods.
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
							"hasChildren",
							"childrenCount",
							"sortChildren",
							"findChildren",
							"findFamily",
							"listNode")

		for method in requiredMethods:
			self.assertIn(method, dir(AbstractCompositeNode))

	def testChild(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.child` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		self.assertEqual(nodeA.child(0), nodeB)
		self.assertEqual(nodeA.child(1), nodeC)
		self.assertEqual(nodeA.child(2), None)

	def testIndexOf(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.indexOf` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		self.assertEqual(nodeA.indexOf(nodeB), 0)

	def testRow(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.row` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		nodeD = AbstractCompositeNode("MyNodeD", nodeA)
		for i, node in enumerate((nodeB, nodeC, nodeD)):
			self.assertEqual(node.row(), i)

	def testAddChild(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.addChild` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB")
		self.assertListEqual(nodeA.children, [])
		self.assertTrue(nodeA.addChild(nodeB))
		self.assertIn(nodeB, nodeA.children)
		self.assertEqual(nodeB.parent, nodeA)

	def testRemoveChild(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.removeChild` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		self.assertEqual(nodeA.removeChild(0), nodeB)
		self.assertListEqual(nodeA.children, [])
		self.assertEqual(nodeB.parent, None)

	def testInsertChild(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.insertChild` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		nodeD = AbstractCompositeNode("MyNodeD")
		self.assertTrue(nodeA.insertChild(nodeD, 1))
		for i, node in enumerate((nodeB, nodeD, nodeC)):
			self.assertEqual(nodeA.indexOf(node), i)

	def testHasChildren(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.hasChildren` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		self.assertFalse(nodeA.hasChildren())
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		self.assertTrue(nodeA.hasChildren())

	def testChildrenCount(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.childrenCount` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		self.assertEqual(nodeA.childrenCount(), 0)
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		self.assertEqual(nodeA.childrenCount(), 2)

	def testFindChildren(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.findChildren` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		nodeD = AbstractCompositeNode("MyNodeD", nodeC)

		self.assertListEqual(nodeA.findChildren("MyNodeD"), [nodeD])
		for node in nodeA.findChildren("mynode.*", re.IGNORECASE):
			self.assertIn(node, (nodeB, nodeC, nodeD))

	def testSortChildrenNode(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.sortChildren` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA", attributeA=Attribute(value="A"), attributeB=Attribute(value="1"))
		nodeC = AbstractCompositeNode("MyNodeC", nodeA, attributeA=Attribute(value="C"), attributeB=Attribute(value="3"))
		nodeB = AbstractCompositeNode("MyNodeB", nodeA, attributeA=Attribute(value="B"), attributeB=Attribute(value="2"))
		nodeG = AbstractCompositeNode("MyNodeG", nodeB, attributeA=Attribute(value="G"))
		nodeE = AbstractCompositeNode("MyNodeE", nodeB, attributeA=Attribute(value="E"), attributeB=Attribute(value="5"))
		nodeF = AbstractCompositeNode("MyNodeF", nodeB, attributeA=Attribute(value="F"), attributeB=Attribute(value="6"))
		nodeD = AbstractCompositeNode("MyNodeD", nodeB, attributeA=Attribute(value="D"), attributeB=Attribute(value="4"))

		self.assertTrue(nodeA.sortChildren())
		self.assertEqual(nodeA.children[0], nodeB)
		self.assertEqual(nodeA.children[1], nodeC)
		self.assertEqual(nodeA.children[0].children[0], nodeD)
		self.assertEqual(nodeA.children[0].children[1], nodeE)
		self.assertEqual(nodeA.children[0].children[2], nodeF)

		self.assertTrue(nodeA.sortChildren(reverseOrder=True))
		self.assertEqual(nodeA.children[0], nodeC)
		self.assertEqual(nodeA.children[1], nodeB)
		self.assertEqual(nodeA.children[1].children[0], nodeG)
		self.assertEqual(nodeA.children[1].children[1], nodeF)
		self.assertEqual(nodeA.children[1].children[2], nodeE)
		self.assertEqual(nodeA.children[1].children[3], nodeD)

		self.assertTrue(nodeA.sortChildren(attribute="attributeA"))
		self.assertEqual(nodeA.children[0], nodeB)
		self.assertEqual(nodeA.children[1], nodeC)
		self.assertEqual(nodeA.children[0].children[0], nodeD)
		self.assertEqual(nodeA.children[0].children[1], nodeE)
		self.assertEqual(nodeA.children[0].children[2], nodeF)

		self.assertTrue(nodeA.sortChildren(attribute="attributeA", reverseOrder=True))
		self.assertEqual(nodeA.children[0], nodeC)
		self.assertEqual(nodeA.children[1], nodeB)
		self.assertEqual(nodeA.children[1].children[0], nodeG)
		self.assertEqual(nodeA.children[1].children[1], nodeF)
		self.assertEqual(nodeA.children[1].children[2], nodeE)
		self.assertEqual(nodeA.children[1].children[3], nodeD)

		self.assertTrue(nodeA.sortChildren(attribute="attributeB"))
		self.assertEqual(nodeA.children[0], nodeB)
		self.assertEqual(nodeA.children[1], nodeC)
		self.assertEqual(nodeA.children[0].children[0], nodeD)
		self.assertEqual(nodeA.children[0].children[1], nodeE)
		self.assertEqual(nodeA.children[0].children[2], nodeF)
		self.assertEqual(nodeA.children[0].children[3], nodeG)

		self.assertTrue(nodeA.sortChildren(attribute="attributeB", reverseOrder=True))
		self.assertEqual(nodeA.children[0], nodeC)
		self.assertEqual(nodeA.children[1], nodeB)
		self.assertEqual(nodeA.children[1].children[0], nodeF)
		self.assertEqual(nodeA.children[1].children[1], nodeE)
		self.assertEqual(nodeA.children[1].children[2], nodeD)
		self.assertEqual(nodeA.children[1].children[3], nodeG)

	def testListFamily(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.listFamily` method.
		"""

		class FamilyB(AbstractCompositeNode):
			__family = "B"

		class FamilyC(AbstractCompositeNode):
			__family = "C"

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = FamilyB("MyNodeB", nodeA)
		nodeC = FamilyC("MyNodeC", nodeA)
		nodeD = FamilyB("MyNodeD", nodeC)
		nodeE = FamilyB("MyNodeE", nodeD)
		nodeF = FamilyC("MyNodeE", nodeE)

		familyNodes = [nodeB, nodeD, nodeE]
		foundNodes = nodeA.findFamily("B")
		for node in familyNodes:
			self.assertIn(node, foundNodes)

		familyNodes = [nodeC, nodeF]
		foundNodes = nodeA.findFamily("C")
		for node in familyNodes:
			self.assertIn(node, foundNodes)

		self.assertEqual(nodeA.findFamily("C", node=nodeE).pop(), nodeF)

	def testListNode(self):
		"""
		This method tests :meth:`foundations.nodes.AbstractCompositeNode.listNode` method.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		self.assertIsInstance(nodeA.listNode(), str)

	def testAbstractCompositeNodePickle(self):
		"""
		This method tests :class:`foundations.nodes.AbstractCompositeNode` class pickling.
		
		:note: :data:`pickle.HIGHEST_PROTOCOL` must be used to pickle :class:`foundations.nodes.AbstractCompositeNode` class.
		"""

		nodeA = AbstractCompositeNode("MyNodeA", attributeA=Attribute(value="A"), attributeB=Attribute(value="1"))
		nodeB = AbstractCompositeNode("MyNodeB", nodeA, attributeA=Attribute(value="B"), attributeB=Attribute(value="2"))
		nodeC = AbstractCompositeNode("MyNodeC", nodeA, attributeA=Attribute(value="C"), attributeB=Attribute(value="3"))
		nodeD = AbstractCompositeNode("MyNodeD", nodeB, attributeA=Attribute(value="D"), attributeB=Attribute(value="4"))

		data = pickle.dumps(nodeA, pickle.HIGHEST_PROTOCOL)
		data = pickle.loads(data)
		self.assertEqual(nodeA, data)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
