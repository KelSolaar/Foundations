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
import os
import socket
import urllib2

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"CONNECTION_IP",
		"DEFAULT_HOST_IP",
		"wait",
		"uniqify",
		"unpackDefault",
		"orderedUniqify",
		"pathExists",
		"getFirstItem",
		"getLastItem",
		"isBinaryFile",
		"repeat",
		"dependencyResolver",
		"isInternetAvailable",
		"getHostAddress"]

LOGGER = foundations.verbose.installLogger()

CONNECTION_IP = "www.google.com"
DEFAULT_HOST_IP = "127.0.0.1"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def uniqify(sequence):
	"""
	This definition uniqifies the given sequence even if unhashable.

	:param sequence: Sequence. ( Object )
	:return: Uniqified sequence. ( List )
	
	:note: The sequence order is not maintained by this definition.
	"""

	return [key for key, group in itertools.groupby(sorted(sequence))]

def orderedUniqify(sequence):
	"""
	This definition uniqifies the given hashable sequence while preserving its order.

	:param sequence: Sequence. ( Object )
	:return: Uniqified sequence. ( List )
	"""

	items = set()
	return [key for key in sequence if key not in items and not items.add(key)]

def unpackDefault(iterable, length=3, default=None):
	"""
	This definition unpacks given iterable maintaining given length and filling missing entries with given default.

	:param iterable: iterable. ( Object )
	:param length: Iterable length. ( Integer )
	:param default: Filling default object. ( Object )
	:return: Unpacked iterable. ( Object )
	"""

	return itertools.islice(itertools.chain(iter(iterable), itertools.repeat(default)), length)

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

def repeat(object, iterations=1):
	"""
	This definition repeats given object iterations times.

	:param object: Object to repeat. ( Object )
	:param iterations: Repetitions number. ( Integer )
	:return: Object return values. ( List )
	"""

	return [object() for i in range(iterations)]

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

def isInternetAvailable(ip=CONNECTION_IP, timeout=1.5):
	"""
	This definition returns if an internet connection is available.

	:param ip: Alternative address ip to check against. ( String )
	:param timeout: Timeout in seconds. ( Integer )
	:return: Is internet available. ( Boolean )
	"""

	try:
		urllib2.urlopen("http://{0}".format(ip), timeout=timeout)
		return True
	except (urllib2.URLError, socket.error) as error:
		return False

def getHostAddress(host=None, defaultAddress=DEFAULT_HOST_IP):
	"""
	This definition returns the given host address.

	:param host: Host to retrieve the address. ( String )
	:param defaultAddress: Default address if the host is unreachable. ( String )
	:return: Host address. ( String )
	"""

	try:
		return socket.gethostbyname(host or socket.gethostname())
	except Exception as error:
		return defaultAddress
