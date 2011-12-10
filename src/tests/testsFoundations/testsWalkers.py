#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**testsWalkers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.walkers` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import re
import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.namespace as namespace
import foundations.strings as strings
import foundations.walkers
from foundations.walkers import OsWalker
from foundations.dag import AbstractCompositeNode

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
			"ROOT_DIRECTORY",
			"TREE_HIERARCHY",
			"OsWalkerTestCase",
			"DictionariesWalkerTestCase",
			"NodesWalkerTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
ROOT_DIRECTORY = "standard"
TREE_HIERARCHY = ("loremIpsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
					"level_0/standard.ibl",
					"level_0/level_1/loremIpsum.txt", "level_0/level_1/standard.rc",
					"level_0/level_1/level_2/standard.sIBLT")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class OsWalkerTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.walkers.OsWalker` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("root",
								"hashSize",
								"files")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(OsWalker))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("walk",)

		for method in requiredMethods:
			self.assertIn(method, dir(OsWalker))

	def testWalk(self):
		"""
		This method tests :meth:`foundations.walkers.OsWalker.walk` method.
		"""

		osWalker = OsWalker()
		osWalker.root = os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY)
		osWalker.walk()
		for path in osWalker.files.itervalues():
			self.assertTrue(os.path.exists(path))

		referencePaths = [strings.replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path),
											{"/":"|", "\\":"|"}) for path in TREE_HIERARCHY]
		walkerFiles = [strings.replace(path, {"/":"|", "\\":"|"}) for path in osWalker.files.itervalues()]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)

		osWalker.walk(filtersOut=("\.rc$",))
		walkerFiles = [strings.replace(path, {"/":"|", "\\":"|"}) for path in osWalker.files.itervalues()]
		for item in walkerFiles:
			self.assertTrue(not re.search(r"\.rc$", item))

		osWalker.walk(filtersOut=("\.ibl", "\.rc$", "\.sIBLT$", "\.txt$"))
		self.assertTrue(not osWalker.files)

		referencePaths = [strings.replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path),
										{"/":"|", "\\":"|"}) for path in TREE_HIERARCHY if re.search(r"\.rc$", path)]
		filter = "\.rc$"
		osWalker.walk(filtersIn=(filter,))
		walkerFiles = [strings.replace(path, {"/":"|", "\\":"|"}) for path in osWalker.files.itervalues()]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)
		for item in walkerFiles:
			self.assertTrue(re.search(filter, item))

		osWalker.hashSize = 24
		osWalker.walk()
		for item in osWalker.files:
			self.assertEqual(len(namespace.removeNamespace(item)), osWalker.hashSize)

class DictionariesWalkerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.walkers.dictionariesWalker` definition units tests methods.
	"""

	def testDictionariesWalker(self):
		"""
		This method tests :func:`foundations.walkers.dictionariesWalker` definition.
		"""

		nestedDictionary = {"Level 1A":{"Level 2A": { "Level 3A" : "Higher Level"}},
							"Level 1B" : "Lower level", "Level 1C" : {}}
		yieldedValues = ((("Level 1A", "Level 2A"), "Level 3A", "Higher Level"), ((), "Level 1B", "Lower level"))
		for value in foundations.walkers.dictionariesWalker(nestedDictionary):
			self.assertIsInstance(value, tuple)
			self.assertIn(value, yieldedValues)
		for path, key, value in foundations.walkers.dictionariesWalker(nestedDictionary):
			self.assertIsInstance(path, tuple)
			self.assertIsInstance(key, str)
			self.assertIsInstance(value, str)

class NodesWalkerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.walkers.nodesWalker` definition units tests methods.
	"""

	def testNodesWalker(self):
		"""
		This method tests :func:`foundations.walkers.nodesWalker` definition.
		"""

		nodeA = AbstractCompositeNode("MyNodeA")
		nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		nodeD = AbstractCompositeNode("MyNodeD", nodeB)
		nodeE = AbstractCompositeNode("MyNodeE", nodeB)
		nodeF = AbstractCompositeNode("MyNodeF", nodeD)
		nodeG = AbstractCompositeNode("MyNodeG", nodeF)
		nodeH = AbstractCompositeNode("MyNodeH", nodeG)
		yieldedValues = (nodeB, nodeC, nodeD, nodeE, nodeF, nodeG, nodeH)
		for node in foundations.walkers.nodesWalker(nodeA):
			self.assertIn(node, yieldedValues)
		
if __name__ == "__main__":
	import tests.utilities
	unittest.main()
