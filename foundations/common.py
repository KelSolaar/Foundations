#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package common utilities objects that don't fall in any specific category.

**Others:**
	:func:`isBinaryFile` from Jorge Orpinel:
	http://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
	:func:`dependencyResolver` from Louis RIVIERE: http://code.activestate.com/recipes/576570-dependency-resolver/

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import itertools
import logging
import os

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
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

__all__ = ["LOGGER",
			"wait",
			"uniqify",
			"orderedUniqify",
			"pathExists",
			"getFirstItem",
			"getLastItem",
			"isBinaryFile",
			"repeat",
			"dependencyResolver"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def uniqify(sequence):
	"""
	This definition uniqifies the given sequence even if unhashable.

	:param sequence: Sequence. ( Object )
	:return: Uniqified sequence. ( List )
	
	:note: The sequence order is not maintained by this definition.
	"""

	return [key for key, group in itertools.groupby(sorted(sequence))]

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def orderedUniqify(sequence):
	"""
	This definition uniqifies the given hashable sequence while preserving its order.

	:param sequence: Sequence. ( Object )
	:return: Uniqified sequence. ( List )
	"""

	items = set()
	return [key for key in sequence if key not in items and not items.add(key)]

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def pathExists(path):
	"""
	This definition returns if given path exists.

	:param path: Path. ( String )
	:return: Path existence. ( Boolean )
	"""

	if not path:
		return False
	else:
		return os.path.exists(path)

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getFirstItem(iterable, default=None):
	"""
	This definition returns the first item of given iterable.

	:param iterable: Iterable. ( Object )
	:param default: Default value. ( Object )
	:return: First iterable item. ( Object )
	"""

	if not iterable:
		return default

	for item in iterable:
		return item

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getLastItem(iterable, default=None):
	"""
	This definition returns the last item of given iterable.

	:param iterable: Iterable. ( Object )
	:param default: Default value. ( Object )
	:return: Last iterable item. ( Object )
	"""

	if not iterable:
		return default

	return iterable[-1]

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def isBinaryFile(file):
	"""
	This definition returns if given file is a binary file.

	:param file: File path. ( String )
	:return: Is file binary. ( Boolean )
	"""

	fileHandle = open(file, "rb")
	try:
		chunkSize = 1024
		while True:
			chunk = fileHandle.read(chunkSize)
			if "\0" in chunk:
				return True
			if len(chunk) < chunkSize:
				break
	finally:
		fileHandle.close()
	return False

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def repeat(object, iterations=1):
	"""
	This definition repeats given object iterations times.

	:param object: Object to repeat. ( Object )
	:param iterations: Repetitions number. ( Integer )
	:return: Object return values. ( List )
	"""

	return [object() for i in range(iterations)]

@foundations.exceptions.exceptionsHandler(None, False, Exception)
def dependencyResolver(dependencies):
	"""
	This definition resolves given dependencies.

	:param dependencies: Dependencies to resolve. ( Dictionary )
	:return: Resolved dependencies. ( List )
	"""

	items = dict((key, set(dependencies[key])) for key in dependencies)
	resolvedDependencies = []
	while items:
		batch = set(item for value in items.values() for item in value) - set(items.keys())
		batch.update(key for key, value in items.items() if not value)
		resolvedDependencies.append(batch)
		items = dict(((key, value - batch) for key, value in items.items() if value))
	return resolvedDependencies
