#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**strings.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines various strings manipulation objects.

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
import platform
import posixpath
import random
import re

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
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

__all__ = ["LOGGER",
			"ASCII_CHARACTERS",
			"toString",
			"getNiceName",
			"getVersionRank",
			"getSplitextBasename",
			"getCommonAncestor",
			"getCommonPathsAncestor",
			"getWords",
			"filterWords",
			"replace",
			"removeStrip",
			"toForwardSlashes",
			"toBackwardSlashes",
			"toPosixPath",
			"getNormalizedPath",
			"getRandomSequence",
			"isEmail",
			"isWebsite"]

LOGGER = foundations.verbose.installLogger()

ASCII_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
toString = foundations.verbose.toUnicode

def getNiceName(name):
	"""
	Converts a string to nice string: **currentLogText** -> **Current Log Text**.

	Usage::

		>>> getNiceName("getMeANiceName")
		u'Get Me A Nice Name'
		>>> getNiceName("__getMeANiceName")
		u'__Get Me A Nice Name'

	:param name: Current string to be nicified.
	:type name: unicode
	:return: Nicified string.
	:rtype: unicode
	"""

	chunks = re.sub(r"(.)([A-Z][a-z]+)", r"\1 \2", name)
	return " ".join(element.title() for element in re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", chunks).split())

def getVersionRank(version):
	"""
	Converts a version string to it's rank.

	Usage::

		>>> getVersionRank("4.2.8")
		4002008000000
		>>> getVersionRank("4.0")
		4000000000000
		>>> getVersionRank("4.2.8").__class__
		<type 'int'>

	:param version: Current version to calculate rank.
	:type version: unicode
	:return: Rank.
	:rtype: int
	"""

	tokens = list(foundations.common.unpackDefault(filter(any, re.split("\.|-|,", version)), length=4, default=0))
	rank = sum((int(1000 ** i) * int(tokens[-i]) for i in range(len(tokens), 0, -1)))
	LOGGER.debug("> Rank: '{0}'.".format(rank))
	return rank

def getSplitextBasename(path):
	"""
	Gets the basename of a path without its extension.

	Usage::

		>>> getSplitextBasename("/Users/JohnDoe/Documents/Test.txt")
		u'Test'

	:param path: Path to extract the basename without extension.
	:type path: unicode
	:return: Splitext basename.
	:rtype: unicode
	"""

	basename = foundations.common.getFirstItem(os.path.splitext(os.path.basename(os.path.normpath(path))))
	LOGGER.debug("> Splitext basename: '{0}'.".format(basename))
	return basename

def getCommonAncestor(*args):
	"""
	Gets common ancestor of given iterables.

	Usage::

		>>> getCommonAncestor(("1", "2", "3"), ("1", "2", "0"), ("1", "2", "3", "4"))
		(u'1', u'2')
		>>> getCommonAncestor("azerty", "azetty", "azello")
		u'aze'

	:param \*args: Iterables to retrieve common ancestor from.
	:type \*args: [iterable]
	:return: Common ancestor.
	:rtype: iterable
	"""

	array = map(set, zip(*args))
	divergence = filter(lambda i: len(i) > 1, array)
	if divergence:
		ancestor = foundations.common.getFirstItem(args)[:array.index(foundations.common.getFirstItem(divergence))]
	else:
		ancestor = min(args)
	LOGGER.debug("> Common Ancestor: '{0}'".format(ancestor))
	return ancestor

def getCommonPathsAncestor(*args):
	"""
	Gets common paths ancestor of given paths.

	Usage::

		>>> getCommonPathsAncestor("/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt")
		u'/Users/JohnDoe/Documents'

	:param \*args: Paths to retrieve common ancestor from.
	:type \*args: [unicode]
	:return: Common path ancestor.
	:rtype: unicode
	"""

	pathAncestor = os.sep.join(getCommonAncestor(*[path.split(os.sep) for path in args]))
	LOGGER.debug("> Common Paths Ancestor: '{0}'".format(pathAncestor))
	return pathAncestor

def getWords(data):
	"""
	Extracts the words from given string.

	Usage::

		>>> getWords("Users are: John Doe, Jane Doe, Z6PO.")
		[u'Users', u'are', u'John', u'Doe', u'Jane', u'Doe', u'Z6PO']

	:param data: Data to extract words from.
	:type data: unicode
	:return: Words.
	:rtype: list
	"""

	words = re.findall(r"\w+", data)
	LOGGER.debug("> Words: '{0}'".format(", ".join(words)))
	return words

def filterWords(words, filtersIn=None, filtersOut=None, flags=0):
	"""
	Filters the words using the given filters.

	Usage::

		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersIn=("John", "Doe"))
		[u'John', u'Doe', u'Doe']
		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersIn=("\w*r",))
		[u'Users', u'are']
		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersOut=("\w*o",))
		[u'Users', u'are', u'Jane', u'Z6PO']

	:param filtersIn: Regex filters in list.
	:type filtersIn: tuple or list
	:param filtersIn: Regex filters out list.
	:type filtersIn: tuple or list
	:param flags: Regex flags.
	:type flags: int
	:return: Filtered words.
	:rtype: list
	"""

	filteredWords = []
	for word in words:
		if filtersIn:
			filterMatched = False
			for filter in filtersIn:
				if not re.search(filter, word, flags):
					LOGGER.debug("> '{0}' word skipped, filter in '{1}' not matched!".format(word, filter))
				else:
					filterMatched = True
					break
			if not filterMatched:
				continue

		if filtersOut:
			filterMatched = False
			for filter in filtersOut:
				if re.search(filter, word, flags):
					LOGGER.debug("> '{0}' word skipped, filter out '{1}' matched!".format(word, filter))
					filterMatched = True
					break
			if filterMatched:
				continue
		filteredWords.append(word)
	LOGGER.debug("> Filtered words: '{0}'".format(", ".join(filteredWords)))
	return filteredWords

def replace(string, data):
	"""
	Replaces the data occurrences in the string.

	Usage::

		>>> replace("Users are: John Doe, Jane Doe, Z6PO.", {"John" : "Luke", "Jane" : "Anakin", "Doe" : "Skywalker",
		 "Z6PO" : "R2D2"})
		u'Users are: Luke Skywalker, Anakin Skywalker, R2D2.'

	:param string: String to manipulate.
	:type string: unicode
	:param data: Replacement occurrences.
	:type data: dict
	:return: Manipulated string.
	:rtype: unicode
	"""

	for old, new in data.iteritems():
		string = string.replace(old, new)
	return string

def removeStrip(string, pattern):
	"""
	Removes the pattern occurrences in the string and strip the result.

	Usage::

		>>> removeStrip("John Doe", "John")
		u'Doe'

	:param string: String to manipulate.
	:type string: unicode
	:param pattern: Replacement pattern.
	:type pattern: unicode
	:return: Manipulated string.
	:rtype: unicode
	"""

	return string.replace(pattern, "").strip()

def toForwardSlashes(data):
	"""
	Converts backward slashes to forward slashes.

	Usage::

		>>> toForwardSlashes("To\Forward\Slashes")
		u'To/Forward/Slashes'

	:param data: Data to convert.
	:type data: unicode
	:return: Converted path.
	:rtype: unicode
	"""

	data = data.replace("\\", "/")
	LOGGER.debug("> Data: '{0}' to forward slashes.".format(data))
	return data

def toBackwardSlashes(data):
	"""
	Converts forward slashes to backward slashes.

	Usage::

		>>> toBackwardSlashes("/Users/JohnDoe/Documents")
		u'\\Users\\JohnDoe\\Documents'

	:param data: Data to convert.
	:type data: unicode
	:return: Converted path.
	:rtype: unicode
	"""

	data = data.replace("/", "\\")
	LOGGER.debug("> Data: '{0}' to backward slashes.".format(data))
	return data

def toPosixPath(path):
	"""
	Converts Windows path to Posix path while stripping drives letters and network server slashes.

	Usage::

		>>> toPosixPath("c:\\Users\\JohnDoe\\Documents")
		u'/Users/JohnDoe/Documents'

	:param path: Windows path.
	:type path: unicode
	:return: Path converted to Posix path.
	:rtype: unicode
	"""

	posixPath = posixpath.normpath(toForwardSlashes(re.sub(r"[a-zA-Z]:\\|\\\\", "/", os.path.normpath(path))))
	LOGGER.debug("> Stripped converted to Posix path: '{0}'.".format(posixPath))
	return posixPath

def getNormalizedPath(path):
	"""
	Normalizes a path, escaping slashes if needed on Windows.

	Usage::

		>>> getNormalizedPath("C:\\Users/johnDoe\\Documents")
		u'C:\\Users\\JohnDoe\\Documents'

	:param path: Path to normalize.
	:type path: unicode
	:return: Normalized path.
	:rtype: unicode
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		path = os.path.normpath(path).replace("\\", "\\\\")
		LOGGER.debug("> Path: '{0}', normalized path.".format(path))
		return path
	else:
		path = os.path.normpath(path)
		LOGGER.debug("> Path: '{0}', normalized path.".format(path))
		return path

def getRandomSequence(length=8):
	"""
	Returns a random sequence.

	Usage::

		>>> getRandomSequence()
		u'N_mYO7g5'

	:param length: Length of the sequence.
	:type length: int
	:return: Random sequence.
	:rtype: unicode
	"""

	return "".join([random.choice(ASCII_CHARACTERS) for i in range(length)])

def isEmail(data):
	"""
	Check if given data string is an email.

	Usage::

		>>> isEmail("john.doe@domain.com")
		True
		>>> isEmail("john.doe:domain.com")
		False

	:param data: Data to check.
	:type data: unicode
	:return: Is email.
	:rtype: bool
	"""

	if re.match(r"[\w.%+-]+@[\w.]+\.[a-zA-Z]{2,4}", data):
		LOGGER.debug("> {0}' is matched as email.".format(data))
		return True
	else:
		LOGGER.debug("> {0}' is not matched as email.".format(data))
		return False

def isWebsite(url):
	"""
	Check if given url string is a website.

	Usage::

		>>> isWebsite("http://www.domain.com")
		True
		>>> isWebsite("domain.com")
		False

	:param data: Data to check.
	:type data: unicode
	:return: Is website.
	:rtype: bool
	"""

	if re.match(r"(http|ftp|https)://([\w\-\.]+)/?", url):
		LOGGER.debug("> {0}' is matched as website.".format(url))
		return True
	else:
		LOGGER.debug("> {0}' is not matched as website.".format(url))
		return False
