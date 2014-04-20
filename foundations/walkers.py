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

__all__ = ["LOGGER", "files_walker", "depth_walker", "dictionaries_walker", "nodes_walker"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def files_walker(directory, filters_in=None, filters_out=None, flags=0):
	"""
	Defines a generator used to walk files using given filters.

	Usage::

		>>> for file in files_walker("./foundations/tests/tests_foundations/resources/standard/level_0"):
		...     print(file)
		...
		./foundations/tests/tests_foundations/resources/standard/level_0/level_1/level_2/standard.sIBLT
		./foundations/tests/tests_foundations/resources/standard/level_0/level_1/lorem_ipsum.txt
		./foundations/tests/tests_foundations/resources/standard/level_0/level_1/standard.rc
		./foundations/tests/tests_foundations/resources/standard/level_0/standard.ibl
		>>> for file in files_walker("./foundations/tests/tests_foundations/resources/standard/level_0", ("\.sIBLT",)):
		...     print(file)
		...
		./foundations/tests/tests_foundations/resources/standard/level_0/level_1/level_2/standard.sIBLT

	:param directory: Directory to recursively walk.
	:type directory: unicode
	:param filters_in: Regex filters in list.
	:type filters_in: tuple or list
	:param filters_in: Regex filters out list.
	:type filters_in: tuple or list
	:param flags: Regex flags.
	:type flags: int
	:return: File.
	:rtype: unicode
	"""

	if filters_in:
		LOGGER.debug("> Current filters in: '{0}'.".format(filters_in))

	if filters_out:
		LOGGER.debug("> Current filters out: '{0}'.".format(filters_out))

	for parent_directory, directories, files in os.walk(directory, topdown=False, followlinks=True):
		for file in files:
			LOGGER.debug("> Current file: '{0}' in '{1}'.".format(file, directory))
			path = foundations.strings.to_forward_slashes(os.path.join(parent_directory, file))
			if os.path.isfile(path):
				if not foundations.strings.filter_words((path,), filters_in, filters_out, flags):
					continue

				LOGGER.debug("> '{0}' file filtered in!".format(path))

				yield path

def depth_walker(directory, maximum_depth=1):
	"""
	Defines a generator used to walk into directories using given maximum depth.

	Usage::

		>>> for item in depth_walker("./foundations/tests/tests_foundations/resources/standard/level_0"):
		...     print(item)
		...
		(u'./foundations/tests/tests_foundations/resources/standard/level_0', [u'level_1'], [u'standard.ibl'])
		(u'./foundations/tests/tests_foundations/resources/standard/level_0/level_1', [u'level_2'], [u'lorem_ipsum.txt', u'standard.rc'])
		>>> for item in depth_walker(tests_foundations, 2):
		...     print(item)
		...
		(u'./foundations/tests/tests_foundations/resources/standard/level_0', [u'level_1'], [u'standard.ibl'])
		(u'./foundations/tests/tests_foundations/resources/standard/level_0/level_1', [u'level_2'], [u'lorem_ipsum.txt', u'standard.rc'])
		(u'./foundations/tests/tests_foundations/resources/standard/level_0/level_1/level_2', [], [u'standard.sIBLT'])

	:param directory: Directory to walk.
	:type directory: unicode
	:param maximum_depth: Maximum depth.
	:type maximum_depth: int
	:return: Parent directory, directories, files.
	:rtype: tuple
	"""

	separator = os.path.sep
	base_depth = directory.count(separator)

	for parent_directory, directories, files in os.walk(directory):
		yield parent_directory, directories, files
		if base_depth + maximum_depth <= parent_directory.count(separator):
			del directories[:]

def dictionaries_walker(dictionary, path=()):
	"""
	Defines a generator used to walk into nested dictionaries.

	Usage::

		>>> nested_dictionary = {"Level 1A":{"Level 2A": { "Level 3A" : "Higher Level"}}, "Level 1B" : "Lower level"}
		>>> dictionaries_walker(nested_dictionary)
		<generator object dictionaries_walker at 0x10131a320>
		>>> for value in dictionaries_walker(nested_dictionary):
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
			for value in dictionaries_walker(dictionary[key], path + (key,)):
				yield value

def nodes_walker(node, ascendants=False):
	"""
	Defines a generator used to walk into Nodes hierarchy.

	Usage::

		>>> node_a = AbstractCompositeNode("MyNodeA")
		>>> node_b = AbstractCompositeNode("MyNodeB", node_a)
		>>> node_c = AbstractCompositeNode("MyNodeC", node_a)
		>>> node_d = AbstractCompositeNode("MyNodeD", node_b)
		>>> node_e = AbstractCompositeNode("MyNodeE", node_b)
		>>> node_f = AbstractCompositeNode("MyNodeF", node_d)
		>>> node_g = AbstractCompositeNode("MyNodeG", node_f)
		>>> node_h = AbstractCompositeNode("MyNodeH", node_g)
		>>> for node in nodes_walker(node_a):
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

		for sub_element in nodes_walker(element, ascendants=ascendants):
			yield sub_element
