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
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.strings
import foundations.walkers
from foundations.nodes import AbstractCompositeNode

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
			"ROOT_DIRECTORY",
			"FILES_TREE_HIERARCHY",
			"TREE_HIERARCHY",
			"FilesWalkerTestCase",
			"DepthWalkerTestCase",
			"DictionariesWalkerTestCase",
			"NodesWalkerTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
ROOT_DIRECTORY = "standard"
FILES_TREE_HIERARCHY = ("loremIpsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
					"level_0/standard.ibl",
					"level_0/level_1/loremIpsum.txt", "level_0/level_1/standard.rc",
					"level_0/level_1/level_2/standard.sIBLT")
TREE_HIERARCHY = ((["level_0"], ["loremIpsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT"]),
					(["level_1"], ["standard.ibl"]),
					(["level_2"], ["loremIpsum.txt", "standard.rc"]),
					([], ["standard.sIBLT"]))

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class FilesWalkerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.walkers.filesWalker` definition units tests methods.
	"""

	def testFilesWalker(self):
		"""
		This method tests :func:`foundations.walkers.filesWalker` definition.
		"""


		rootDirectory = os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY)
		for path in foundations.walkers.filesWalker(rootDirectory):
			self.assertTrue(os.path.exists(path))

		referencePaths = [foundations.strings.replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path),
											{"/":"|", "\\":"|"}) for path in FILES_TREE_HIERARCHY]
		walkerFiles = \
		[foundations.strings.replace(path, {"/":"|", "\\":"|"}) for path in foundations.walkers.filesWalker(rootDirectory)]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)

		walkerFiles = \
		[foundations.strings.replace(path, {"/":"|", "\\":"|"}) \
		for path in foundations.walkers.filesWalker(rootDirectory, filtersOut=("\.rc$",))]
		for item in walkerFiles:
			self.assertTrue(not re.search(r"\.rc$", item))


		walkerFiles = \
		[foundations.strings.replace(path, {"/":"|", "\\":"|"}) \
		for path in foundations.walkers.filesWalker(rootDirectory, filtersOut=("\.ibl", "\.rc$", "\.sIBLT$", "\.txt$"))]
		self.assertTrue(not walkerFiles)

		return
		referencePaths = [foundations.strings.replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path),
										{"/":"|", "\\":"|"}) for path in FILES_TREE_HIERARCHY if re.search(r"\.rc$", path)]
		walkerFiles = \
		[foundations.strings.replace(path, {"/":"|", "\\":"|"}) \
		for path in foundations.walkers.filesWalker(rootDirectory, filtersIn=("\.rc$",))]
		for item in referencePaths:
			self.assertIn(item, walkerFiles)
		for item in walkerFiles:
			self.assertTrue(re.search(filter, item))

class DepthWalkerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.walkers.depthWalker` definition units tests methods.
	"""

	def testDepthWalker(self):
		"""
		This method tests :func:`foundations.walkers.depthWalker` definition.
		"""

		for i, value in \
		enumerate(foundations.walkers.depthWalker(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY), maximumDepth=2)):
			parentDirectory, directories, files = value
			self.assertEqual((directories, sorted(files)), (TREE_HIERARCHY[i][0], sorted(TREE_HIERARCHY[i][1])))

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
		values = [nodeB, nodeC, nodeD, nodeE, nodeF, nodeG, nodeH]
		for node in values:
			self.assertIn(node, list(foundations.walkers.nodesWalker(nodeA)))

		values = [nodeG, nodeF, nodeD, nodeB, nodeA]
		self.assertEquals(list(foundations.walkers.nodesWalker(nodeH, ascendants=True)), values)

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
