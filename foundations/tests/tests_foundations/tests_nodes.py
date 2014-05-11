#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.nodes` module.

**Others:**

"""

from __future__ import unicode_literals

import pickle
import re
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

from foundations.nodes import AbstractCompositeNode
from foundations.nodes import AbstractNode
from foundations.nodes import Attribute

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestAttribute", "TestAbstractNode", "AbstractCompositeNode"]

class TestAttribute(unittest.TestCase):
	"""
	Defines :class:`foundations.nodes.Attribute` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("name",
							"value")

		for attribute in required_attributes:
			self.assertIn(attribute, dir(Attribute))

class TestAbstractNode(unittest.TestCase):
	"""
	Defines :class:`foundations.nodes.AbstractNode` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("family",
							"identity",
							"nodes_instances",
							"name")

		for attribute in required_attributes:
			self.assertIn(attribute, dir(AbstractNode))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("get_node_by_identity",
							"list_attributes",
							"get_attributes",
							"attribute_exists",
							"add_attribute",
							"remove_attribute")

		for method in required_methods:
			self.assertIn(method, dir(AbstractNode))

	def test_family(self):
		"""
		Tests :class:`foundations.nodes.AbstractNode` class family property.
		"""

		node_a = AbstractNode("MyNode")
		self.assertEqual(node_a.family, "Abstract")

	def test_name(self):
		"""
		Tests :class:`foundations.nodes.AbstractNode` class name resolving consistency.
		"""

		node_a = AbstractNode("MyNodeA")
		self.assertEqual(node_a.name, "MyNodeA")
		node_b = AbstractNode()
		self.assertEqual(node_b.name, "Abstract{0}".format(node_b.identity))

	def test_get_node_by_identity(self):
		"""
		Tests :meth:`foundations.nodes.AbstractNode.get_node_by_identity` method.
		"""

		node_a = AbstractNode()
		self.assertIsInstance(AbstractNode.get_node_by_identity(node_a.identity), AbstractNode)
		node_b = AbstractNode()
		self.assertIsInstance(AbstractNode.get_node_by_identity(node_b.identity), AbstractNode)
		self.assertEqual(AbstractNode.get_node_by_identity(node_b.identity), node_b)

	def test_list_attributes(self):
		"""
		Tests :meth:`foundations.nodes.AbstractNode.list_attributes` method.
		"""

		node_a = AbstractNode("MyNodeA")
		self.assertListEqual(node_a.list_attributes(), [])
		node_b = AbstractNode("MyNodeB", attributeA=Attribute(), attributeB=Attribute())
		self.assertListEqual(sorted(node_b.list_attributes()), ["attributeA", "attributeB"])

	def test_get_attributes(self):
		"""
		Tests :meth:`foundations.nodes.AbstractNode.get_attributes` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		node_a = AbstractNode("MyNodeA", **attributes)
		for attribute in attributes.itervalues():
			self.assertIn(attribute, node_a.get_attributes())

	def test_has_attribute(self):
		"""
		Tests :meth:`foundations.nodes.AbstractNode.attribute_exists` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		node_a = AbstractNode("MyNodeA", **attributes)
		for attribute in attributes:
			self.assertTrue(node_a.attribute_exists(attribute))
		node_b = AbstractNode("MyNodeB", nonAttribute="Non Attribute")
		self.assertFalse(node_b.attribute_exists("nonAttribute"))

	def test_add_attribute(self):
		"""
		Tests :meth:`foundations.nodes.AbstractNode.add_attribute` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		node_a = AbstractNode("MyNodeA")
		for attribute, value in attributes.iteritems():
			self.assertTrue(node_a.add_attribute(attribute, value))
			self.assertTrue(node_a.attribute_exists(attribute))

	def test_remove_attribute(self):
		"""
		Tests :meth:`foundations.nodes.AbstractNode.remove_attribute` method.
		"""

		attributes = {"attributeA" : Attribute(), "attributeB" : Attribute()}

		node_a = AbstractNode("MyNodeA")
		for attribute, value in attributes.iteritems():
			self.assertTrue(node_a.add_attribute(attribute, value))
			self.assertTrue(node_a.remove_attribute(attribute))
			self.assertFalse(node_a.attribute_exists(attribute))

	def test_abstract_node_pickle(self):
		"""
		Tests :class:`foundations.nodes.AbstractNode` class pickling.
		"""

		node_a = AbstractNode("MyNodeA", attributeA=Attribute(), attributeB=Attribute())

		data = pickle.dumps(node_a)
		data = pickle.loads(data)
		self.assertEqual(node_a, data)

		data = pickle.dumps(node_a, pickle.HIGHEST_PROTOCOL)
		data = pickle.loads(data)
		self.assertEqual(node_a, data)

class TestAbstractCompositeNode(unittest.TestCase):
	"""
	Defines :class:`foundations.nodes.AbstractCompositeNode` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("family",
							"identity",
							"nodes_instances",
							"name",
							"parent",
							"children")

		for attribute in required_attributes:
			self.assertIn(attribute, dir(AbstractCompositeNode))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("get_node_by_identity",
							"list_attributes",
							"get_attributes",
							"attribute_exists",
							"add_attribute",
							"remove_attribute",
							"child",
							"index_of",
							"row",
							"add_child",
							"remove_child",
							"insert_child",
							"has_children",
							"children_count",
							"sort_children",
							"find_children",
							"find_family",
							"list_node")

		for method in required_methods:
			self.assertIn(method, dir(AbstractCompositeNode))

	def test_child(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.child` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		node_c = AbstractCompositeNode("MyNodeC", node_a)
		self.assertEqual(node_a.child(0), node_b)
		self.assertEqual(node_a.child(1), node_c)
		self.assertEqual(node_a.child(2), None)

	def test_index_of(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.index_of` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		self.assertEqual(node_a.index_of(node_b), 0)

	def test_row(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.row` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		node_c = AbstractCompositeNode("MyNodeC", node_a)
		node_d = AbstractCompositeNode("MyNodeD", node_a)
		for i, node in enumerate((node_b, node_c, node_d)):
			self.assertEqual(node.row(), i)

	def test_add_child(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.add_child` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB")
		self.assertListEqual(node_a.children, [])
		self.assertTrue(node_a.add_child(node_b))
		self.assertIn(node_b, node_a.children)
		self.assertEqual(node_b.parent, node_a)

	def test_remove_child(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.remove_child` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		self.assertEqual(node_a.remove_child(0), node_b)
		self.assertListEqual(node_a.children, [])
		self.assertEqual(node_b.parent, None)

	def test_insert_child(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.insert_child` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		node_c = AbstractCompositeNode("MyNodeC", node_a)
		node_d = AbstractCompositeNode("MyNodeD")
		self.assertTrue(node_a.insert_child(node_d, 1))
		for i, node in enumerate((node_b, node_d, node_c)):
			self.assertEqual(node_a.index_of(node), i)

	def test_has_children(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.has_children` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		self.assertFalse(node_a.has_children())
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		self.assertTrue(node_a.has_children())

	def test_children_count(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.children_count` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		self.assertEqual(node_a.children_count(), 0)
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		node_c = AbstractCompositeNode("MyNodeC", node_a)
		self.assertEqual(node_a.children_count(), 2)

	def test_find_children(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.find_children` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		node_c = AbstractCompositeNode("MyNodeC", node_a)
		node_d = AbstractCompositeNode("MyNodeD", node_c)

		self.assertListEqual(node_a.find_children("MyNodeD"), [node_d])
		for node in node_a.find_children("mynode.*", re.IGNORECASE):
			self.assertIn(node, (node_b, node_c, node_d))

	def test_sort_children(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.sort_children` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA", attributeA=Attribute(value="A"), attributeB=Attribute(value="1"))
		node_c = AbstractCompositeNode("MyNodeC", node_a, attributeA=Attribute(value="C"), attributeB=Attribute(value="3"))
		node_b = AbstractCompositeNode("MyNodeB", node_a, attributeA=Attribute(value="B"), attributeB=Attribute(value="2"))
		node_g = AbstractCompositeNode("MyNodeG", node_b, attributeA=Attribute(value="G"))
		node_e = AbstractCompositeNode("MyNodeE", node_b, attributeA=Attribute(value="E"), attributeB=Attribute(value="5"))
		node_f = AbstractCompositeNode("MyNodeF", node_b, attributeA=Attribute(value="F"), attributeB=Attribute(value="6"))
		node_d = AbstractCompositeNode("MyNodeD", node_b, attributeA=Attribute(value="D"), attributeB=Attribute(value="4"))

		self.assertTrue(node_a.sort_children())
		self.assertEqual(node_a.children[0], node_b)
		self.assertEqual(node_a.children[1], node_c)
		self.assertEqual(node_a.children[0].children[0], node_d)
		self.assertEqual(node_a.children[0].children[1], node_e)
		self.assertEqual(node_a.children[0].children[2], node_f)

		self.assertTrue(node_a.sort_children(reverse_order=True))
		self.assertEqual(node_a.children[0], node_c)
		self.assertEqual(node_a.children[1], node_b)
		self.assertEqual(node_a.children[1].children[0], node_g)
		self.assertEqual(node_a.children[1].children[1], node_f)
		self.assertEqual(node_a.children[1].children[2], node_e)
		self.assertEqual(node_a.children[1].children[3], node_d)

		self.assertTrue(node_a.sort_children(attribute="attributeA"))
		self.assertEqual(node_a.children[0], node_b)
		self.assertEqual(node_a.children[1], node_c)
		self.assertEqual(node_a.children[0].children[0], node_d)
		self.assertEqual(node_a.children[0].children[1], node_e)
		self.assertEqual(node_a.children[0].children[2], node_f)

		self.assertTrue(node_a.sort_children(attribute="attributeA", reverse_order=True))
		self.assertEqual(node_a.children[0], node_c)
		self.assertEqual(node_a.children[1], node_b)
		self.assertEqual(node_a.children[1].children[0], node_g)
		self.assertEqual(node_a.children[1].children[1], node_f)
		self.assertEqual(node_a.children[1].children[2], node_e)
		self.assertEqual(node_a.children[1].children[3], node_d)

		self.assertTrue(node_a.sort_children(attribute="attributeB"))
		self.assertEqual(node_a.children[0], node_b)
		self.assertEqual(node_a.children[1], node_c)
		self.assertEqual(node_a.children[0].children[0], node_d)
		self.assertEqual(node_a.children[0].children[1], node_e)
		self.assertEqual(node_a.children[0].children[2], node_f)
		self.assertEqual(node_a.children[0].children[3], node_g)

		self.assertTrue(node_a.sort_children(attribute="attributeB", reverse_order=True))
		self.assertEqual(node_a.children[0], node_c)
		self.assertEqual(node_a.children[1], node_b)
		self.assertEqual(node_a.children[1].children[0], node_f)
		self.assertEqual(node_a.children[1].children[1], node_e)
		self.assertEqual(node_a.children[1].children[2], node_d)
		self.assertEqual(node_a.children[1].children[3], node_g)

	def test_list_family(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.listFamily` method.
		"""

		class FamilyB(AbstractCompositeNode):
			__family = "B"

		class FamilyC(AbstractCompositeNode):
			__family = "C"

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = FamilyB("MyNodeB", node_a)
		node_c = FamilyC("MyNodeC", node_a)
		node_d = FamilyB("MyNodeD", node_c)
		node_e = FamilyB("MyNodeE", node_d)
		node_f = FamilyC("MyNodeE", node_e)

		family_nodes = [node_b, node_d, node_e]
		found_nodes = node_a.find_family("B")
		for node in family_nodes:
			self.assertIn(node, found_nodes)

		family_nodes = [node_c, node_f]
		found_nodes = node_a.find_family("C")
		for node in family_nodes:
			self.assertIn(node, found_nodes)

		self.assertEqual(node_a.find_family("C", node=node_e).pop(), node_f)

	def test_list_node(self):
		"""
		Tests :meth:`foundations.nodes.AbstractCompositeNode.list_node` method.
		"""

		node_a = AbstractCompositeNode("MyNodeA")
		node_b = AbstractCompositeNode("MyNodeB", node_a)
		node_c = AbstractCompositeNode("MyNodeC", node_a)
		self.assertIsInstance(node_a.list_node(), unicode)

	def test_abstract_composite_node_pickle(self):
		"""
		Tests :class:`foundations.nodes.AbstractCompositeNode` class pickling.

		:note: :data:`pickle.HIGHEST_PROTOCOL` must be used to pickle :class:`foundations.nodes.AbstractCompositeNode` class.
		"""

		node_a = AbstractCompositeNode("MyNodeA", attributeA=Attribute(value="A"), attributeB=Attribute(value="1"))
		node_b = AbstractCompositeNode("MyNodeB", node_a, attributeA=Attribute(value="B"), attributeB=Attribute(value="2"))
		node_c = AbstractCompositeNode("MyNodeC", node_a, attributeA=Attribute(value="C"), attributeB=Attribute(value="3"))
		node_d = AbstractCompositeNode("MyNodeD", node_b, attributeA=Attribute(value="D"), attributeB=Attribute(value="4"))

		data = pickle.dumps(node_a, pickle.HIGHEST_PROTOCOL)
		data = pickle.loads(data)
		self.assertEqual(node_a, data)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
