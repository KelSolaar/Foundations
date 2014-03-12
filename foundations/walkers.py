#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**walkers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines various walking related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.strings
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "filesWalker", "depthWalker", "dictionariesWalker", "nodesWalker"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def filesWalker(directory, filtersIn=None, filtersOut=None, flags=0):
	"""
	Defines a generator used to walk files using given filters.

	Usage::
		
		>>> for file in filesWalker("./foundations/tests/testsFoundations/resources/standard/level_0"):
		...     print(file)
		...
		./foundations/tests/testsFoundations/resources/standard/level_0/level_1/level_2/standard.sIBLT
		./foundations/tests/testsFoundations/resources/standard/level_0/level_1/loremIpsum.txt
		./foundations/tests/testsFoundations/resources/standard/level_0/level_1/standard.rc
		./foundations/tests/testsFoundations/resources/standard/level_0/standard.ibl		
		>>> for file in filesWalker("./foundations/tests/testsFoundations/resources/standard/level_0", ("\.sIBLT",)):
		...     print(file)
		...
		./foundations/tests/testsFoundations/resources/standard/level_0/level_1/level_2/standard.sIBLT

	:param directory: Directory to recursively walk.
	:type directory: unicode
	:param filtersIn: Regex filters in list.
	:type filtersIn: tuple or list
	:param filtersIn: Regex filters out list.
	:type filtersIn: tuple or list
	:param flags: Regex flags.
	:type flags: int
	:return: File.
	:rtype: unicode
	"""

	if filtersIn:
		LOGGER.debug("> Current filters in: '{0}'.".format(filtersIn))

	if filtersOut:
		LOGGER.debug("> Current filters out: '{0}'.".format(filtersOut))

	for parentDirectory, directories, files in os.walk(directory, topdown=False, followlinks=True):
		for item in files:
			LOGGER.debug("> Current file: '{0}' in '{1}'.".format(item, directory))
			path = foundations.strings.toForwardSlashes(os.path.join(parentDirectory, item))
			if os.path.isfile(path):
				if not foundations.strings.filterWords((path,), filtersIn, filtersOut, flags):
					continue

				LOGGER.debug("> '{0}' file filtered in!".format(path))

				yield path

def depthWalker(directory, maximumDepth=1):
	"""
	Defines a generator used to walk into directories using given maximum depth.

	Usage::
		
		>>> for item in depthWalker("./foundations/tests/testsFoundations/resources/standard/level_0"):
		...     print(item)
		...
		(u'./foundations/tests/testsFoundations/resources/standard/level_0', [u'level_1'], [u'standard.ibl'])
		(u'./foundations/tests/testsFoundations/resources/standard/level_0/level_1', [u'level_2'], [u'loremIpsum.txt', u'standard.rc'])
		>>> for item in depthWalker("./foundations/tests/testsFoundations/resources/standard/level_0", 2):
		...     print(item)
		...
		(u'./foundations/tests/testsFoundations/resources/standard/level_0', [u'level_1'], [u'standard.ibl'])
		(u'./foundations/tests/testsFoundations/resources/standard/level_0/level_1', [u'level_2'], [u'loremIpsum.txt', u'standard.rc'])
		(u'./foundations/tests/testsFoundations/resources/standard/level_0/level_1/level_2', [], [u'standard.sIBLT'])

	:param directory: Directory to walk.
	:type directory: unicode
	:param maximumDepth: Maximum depth.
	:type maximumDepth: int
	:return: Parent directory, directories, files.
	:rtype: tuple
	"""

	separator = os.path.sep
	baseDepth = directory.count(separator)

	for parentDirectory, directories, files in os.walk(directory):
		yield parentDirectory, directories, files
		if baseDepth + maximumDepth <= parentDirectory.count(separator):
			del directories[:]

def dictionariesWalker(dictionary, path=()):
	"""
	Defines a generator used to walk into nested dictionaries.
	
	Usage::
		
		>>> nestedDictionary = {"Level 1A":{"Level 2A": { "Level 3A" : "Higher Level"}}, "Level 1B" : "Lower level"}
		>>> dictionariesWalker(nestedDictionary)
		<generator object dictionariesWalker at 0x10131a320>
		>>> for value in dictionariesWalker(nestedDictionary):
		...	print value
		(('Level 1A', 'Level 2A'), 'Level 3A', 'Higher Level')
		((), 'Level 1B', 'Lower level')

	:param dictionary: Dictionary to walk.
	:type dictionary: dict
	:param path: Walked paths.
	:type path: tuple
	:return: Path, key, value.
	:rtype: tuple
	
	:note: This generator won't / can't yield any dictionaries, if you want to be able to retrieve dictionaries anyway,
		you will have to either encapsulate them in another object, or mutate their base class.
	"""

	for key in dictionary:
		if not isinstance(dictionary[key], dict):
			yield path, key, dictionary[key]
		else:
			for value in dictionariesWalker(dictionary[key], path + (key,)):
				yield value

def nodesWalker(node, ascendants=False):
	"""
	Defines a generator used to walk into Nodes hierarchy.
	
	Usage::
		
		>>> nodeA = AbstractCompositeNode("MyNodeA")
		>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
		>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
		>>> nodeD = AbstractCompositeNode("MyNodeD", nodeB)
		>>> nodeE = AbstractCompositeNode("MyNodeE", nodeB)
		>>> nodeF = AbstractCompositeNode("MyNodeF", nodeD)
		>>> nodeG = AbstractCompositeNode("MyNodeG", nodeF)
		>>> nodeH = AbstractCompositeNode("MyNodeH", nodeG)
		>>> for node in nodesWalker(nodeA):
		...	print node.name
		MyNodeB
		MyNodeD
		MyNodeF
		MyNodeG
		MyNodeH
		MyNodeE
		MyNodeC

	:param node: Node to walk.
	:type node: AbstractCompositeNode
	:param ascendants: Ascendants instead of descendants will be yielded.
	:type ascendants: bool
	:return: Node.
	:rtype: AbstractNode or AbstractCompositeNode
	"""

	attribute = "children" if not ascendants else "parent"
	if not hasattr(node, attribute):
		return

	elements = getattr(node, attribute)
	elements = elements if isinstance(elements, list) else [elements]

	for element in elements:
		yield element

		if not hasattr(element, attribute):
			continue

		if not getattr(element, attribute):
			continue

		for subElement in nodesWalker(element, ascendants=ascendants):
			yield subElement
