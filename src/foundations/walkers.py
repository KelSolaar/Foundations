#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**walkers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`FilesWalker` class and others walking related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import hashlib

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
import foundations.strings as strings
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "FilesWalker", "depthWalker", "dictionariesWalker", "nodesWalker"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class FilesWalker(object):
	"""
	This class provides methods for walking in a directory and retrieving filters matched files.
	"""

	@core.executionTrace
	def __init__(self, root=None, hashSize=8):
		"""
		This method initializes the class.
	
		Usage::
		
			>>> filesWalker = FilesWalker("./Foundations/src/tests/testsFoundations/resources/standard/level_0")
			>>> filesWalker.walk().keys()
			['standard|0d24f027', 'standard|407ed3b2', 'standard|20efaeaf', 'loremIpsum|ddf30259']
			>>> filesWalker.walk(filtersIn=("\.sIBLT$",))
			{'standard|20efaeaf': 
			'./Foundations/src/tests/testsFoundations/resources/standard/level_0/level_1/level_2/standard.sIBLT'}
			>>> filesWalker.walk(filtersOut=("\.sIBLT$", "\.rc$", "\.ibl$")).values()
			['./Foundations/src/tests/testsFoundations/resources/standard/level_0/level_1/loremIpsum.txt']
			
		:param root: Root directory to recursively walk. ( String )
		:param hashSize: Hash affixe length. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__root = None
		self.root = root
		self.__hashSize = None
		self.hashSize = hashSize

		self.__files = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def root(self):
		"""
		This method is the property for **self.__root** attribute.

		:return: self.__root. ( String )
		"""

		return self.__root

	@root.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def root(self, value):
		"""
		This method is the setter method for **self.__root** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("root", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' directory doesn't exists!".format("root", value)
		self.__root = value

	@root.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def root(self):
		"""
		This method is the deleter method for **self.__root** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "root"))

	@property
	def hashSize(self):
		"""
		This method is the property for **self.__hashSize** attribute.

		:return: self.__hashSize. ( Integer )
		"""

		return self.__hashSize

	@hashSize.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hashSize(self, value):
		"""
		This method is the setter method for **self.__hashSize** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("hashSize", value)
		self.__hashSize = value

	@hashSize.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hashSize(self):
		"""
		This method is the deleter method for **self.__hashSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "hashSize"))

	@property
	def files(self):
		"""
		This method is the property for **self.__files** attribute.

		:return: self.__files. ( Dictionary )
		"""

		return self.__files

	@files.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def files(self, value):
		"""
		This method is the setter method for **self.__files** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "files"))

	@files.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def files(self):
		"""
		This method is the deleter method for **self.__files** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "files"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler()
	def walk(self, filtersIn=None, filtersOut=None, flags=0, shorterHashKey=True, visitor=None):
		"""
		This method gets root directory files list as a dictionary using given filters.

		:param filtersIn: Regex filters in list. ( Tuple / List )
		:param filtersIn: Regex filters out list. ( Tuple / List )
		:param flags: Regex flags. ( Integer )
		:param visitor: Visitor object. ( Object )
		:return: Files list. ( Dictionary or None )
		"""

		if filtersIn:
			LOGGER.debug("> Current filters in: '{0}'.".format(filtersIn))

		if filtersOut:
			LOGGER.debug("> Current filters out: '{0}'.".format(filtersOut))

		if not self.__root:
			return

		self.__files = {}
		for parentDirectory, directories, files in os.walk(self.__root, topdown=False, followlinks=True):
			for item in files:
				LOGGER.debug("> Current file: '{0}' in '{1}'.".format(item, self.__root))
				path = strings.toForwardSlashes(os.path.join(parentDirectory, item))
				if os.path.isfile(path):
					if not strings.filterWords((path,), filtersIn, filtersOut, flags):
						continue

					LOGGER.debug("> '{0}' file filtered in!".format(path))

					hashKey = hashlib.md5(path).hexdigest()
					name = namespace.setNamespace(foundations.common.getFirstItem(os.path.splitext(item)),
													hashKey[:self.__hashSize] if shorterHashKey else hashKey)
					LOGGER.debug("> Adding '{0}' with path: '{1}' to files list.".format(name, path))
					self.__files[name] = path

					visitor and visitor(self.__files, name)

		return self.__files

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def depthWalker(directory, maximumDepth=1):
	"""
	This definition is a generator used to walk into directories using given maximum depth.

	:param directory: Directory to walk. ( String )
	:param maximumDepth: Maximum depth. ( Integer )
	:return: Parent directory, directories, files. ( Tuple )
	"""

	separator = os.path.sep
	baseDepth = directory.count(separator)

	for parentDirectory, directories, files in os.walk(directory):
		yield parentDirectory, directories, files
		if baseDepth + maximumDepth <= parentDirectory.count(separator):
			del directories[:]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def dictionariesWalker(dictionary, path=()):
	"""
	This definition is a generator used to walk into nested dictionaries.
	
	Usage::
		
		>>> nestedDictionary = {"Level 1A":{"Level 2A": { "Level 3A" : "Higher Level"}}, "Level 1B" : "Lower level"}
		>>> dictionariesWalker(nestedDictionary)
		<generator object dictionariesWalker at 0x10131a320>
		>>> for value in dictionariesWalker(nestedDictionary):
		...	print value
		(('Level 1A', 'Level 2A'), 'Level 3A', 'Higher Level')
		((), 'Level 1B', 'Lower level')

	:param dictionary: Dictionary to walk. ( Dictionary )
	:param path: Walked paths. ( Tuple )
	:return: Path, key, value. ( Tuple )
	
	:note: This generator won't / can't yield any dictionaries, if you want to be able to retrieve dictionaries anyway,
		you will have to either encapsulate them in another object, or mutate their base class.
	"""

	for key in dictionary:
		if not isinstance(dictionary[key], dict):
			yield path, key, dictionary[key]
		else:
			for value in dictionariesWalker(dictionary[key], path + (key,)):
				yield value

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def nodesWalker(node, ascendants=False):
	"""
	This definition is a generator used to walk into nodes hierarchy.
	
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

	:param node: Node to walk. ( AbstractCompositeNode )
	:param ascendants: Ascendants instead of descendants will be yielded. ( Boolean )
	:return: Node. ( AbstractNode / AbstractCompositeNode )
	"""

	attribute = "children" if not ascendants else "parent"
	if not hasattr(node, attribute):
		return

	elements = getattr(node, attribute)
	elements = elements if isinstance(elements, list) else [elements]

	for element in elements:
		yield element

		if not getattr(element, attribute):
			continue

		for subElement in nodesWalker(element, ascendants=ascendants):
			yield subElement
