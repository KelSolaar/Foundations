#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**strings.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines various strings manipulation objects.

**Others:**

"""

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
from foundations.globals.constants import Constants

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
			"ASCII_CHARACTERS",
			"encode",
			"getNiceName",
			"getVersionRank",
			"getSplitextBasename",
			"getCommonAncestor",
			"getCommonPathsAncestor",
			"getWords",
			"filterWords",
			"replace",
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
def encode(data):
	"""
	This definition encodes given data to unicode using package default settings.

	Usage::

		>>> encode("myData")
		u'myData'
		>>> encode("汉字/漢字")
		u'\u6c49\u5b57/\u6f22\u5b57'

	:param data: Data to encode. ( String )
	:return: Encoded data. ( Unicode )
	"""

	encodedData = None
	if isinstance(data, unicode):
		encodedData = data
	else:
		try:
			encodedData = unicode(data, Constants.encodingFormat, Constants.encodingError)
		except TypeError:
			encodedData = unicode(data.__str__(), Constants.encodingFormat, Constants.encodingError)
	return encodedData

def getNiceName(name):
	"""
	This definition converts a string to nice string: **currentLogText** -> **Current Log Text**.

	Usage::

		>>> getNiceName("getMeANiceName")
		'Get Me A Nice Name'
		>>> getNiceName("__getMeANiceName")
		'__Get Me A Nice Name'

	:param name: Current string to be nicified. ( String )
	:return: Nicified string. ( String )
	"""

	chunks = re.sub(r"(.)([A-Z][a-z]+)", r"\1 \2", name)
	return " ".join(element.title() for element in re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", chunks).split())

def getVersionRank(version):
	"""
	This definition converts a version string to it's rank.

	Usage::

		>>> getVersionRank("4.2.8")
		4002008000000
		>>> getVersionRank("4.0")
		4000000000000
		>>> getVersionRank("4.2.8").__class__
		<type 'int'>

	:param version: Current version to calculate rank. ( String )
	:return: Rank. ( Integer )
	"""

	tokens = list(foundations.common.unpackDefault(filter(any, re.split("\.|-|,", version)), length=4, default=0))
	rank = sum((int(1000 ** i) * int(tokens[-i]) for i in range(len(tokens), 0, -1)))
	LOGGER.debug("> Rank: '{0}'.".format(rank))
	return rank

def getSplitextBasename(path):
	"""
	This definition gets the basename of a path without its extension.

	Usage::

		>>> getSplitextBasename("/Users/JohnDoe/Documents/Test.txt")
		'Test'

	:param path: Path to extract the basename without extension. ( String )
	:return: Splitext basename. ( String )
	"""

	basename = foundations.common.getFirstItem(os.path.splitext(os.path.basename(os.path.normpath(path))))
	LOGGER.debug("> Splitext basename: '{0}'.".format(basename))
	return basename

def getCommonAncestor(*args):
	"""
	This definition gets common ancestor of given iterables.

	Usage::

		>>> getCommonAncestor(("1", "2", "3"), ("1", "2", "0"), ("1", "2", "3", "4"))
		('1', '2')
		>>> getCommonAncestor("azerty", "azetty", "azello")
		'aze'

	:param \*args: Iterables to retrieve common ancestor from. ( Iterables )
	:return: Common ancestor. ( Iterable )
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
	This definition gets common paths ancestor of given paths.

	Usage::

		>>> getCommonPathsAncestor("/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt")
		'/Users/JohnDoe/Documents'

	:param \*args: Paths to retrieve common ancestor from. ( Strings )
	:return: Common path ancestor. ( String )
	"""

	pathAncestor = os.sep.join(getCommonAncestor(*[path.split(os.sep) for path in args]))
	LOGGER.debug("> Common Paths Ancestor: '{0}'".format(pathAncestor))
	return pathAncestor

def getWords(data):
	"""
	This method extracts the words from given string.

	Usage::

		>>> getWords("Users are: John Doe, Jane Doe, Z6PO.")
		['Users', 'are', 'John', 'Doe', 'Jane', 'Doe', 'Z6PO']

	:param data: Data to extract words from. ( String )
	:return: Words. ( List )
	"""

	words = re.findall(r"\w+", data)
	LOGGER.debug("> Words: '{0}'".format(", ".join(words)))
	return words

def filterWords(words, filtersIn=None, filtersOut=None, flags=0):
	"""
	This method filters the words using the given filters.

	Usage::

		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersIn=("John", "Doe"))
		['John', 'Doe', 'Doe']
		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersIn=("\w*r",))
		['Users', 'are']
		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersOut=("\w*o",))
		['Users', 'are', 'Jane', 'Z6PO']

	:param filtersIn: Regex filters in list. ( Tuple / List )
	:param filtersIn: Regex filters out list. ( Tuple / List )
	:param flags: Regex flags. ( Integer )
	:return: Filtered words. ( List )
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
	This definition replaces the data occurences in the string.

	Usage::

		>>> replace("Users are: John Doe, Jane Doe, Z6PO.", {"John" : "Luke", "Jane" : "Anakin", "Doe" : "Skywalker",
		 "Z6PO" : "R2D2"})
		'Users are: Luke Skywalker, Anakin Skywalker, R2D2.'

	:param string: String to manipulate. ( String )
	:param data: Replacement occurences. ( Dictionary )
	:return: Manipulated string. ( String )
	"""

	for old, new in data.iteritems():
		string = string.replace(old, new)
	return string

def removeStrip(string, pattern):
	"""
	This definition removes the pattern occurences in the string and strip the result.

	Usage::

		>>> replaceStrip("John Doe", "John")
		'Doe'

	:param string: String to manipulate. ( String )
	:param pattern: Replacement pattern. ( String )
	:return: Manipulated string. ( String )
	"""

	return string.replace(pattern, "").strip()

def toForwardSlashes(data):
	"""
	This definition converts backward slashes to forward slashes.

	Usage::

		>>> toForwardSlashes("To\Forward\Slashes")
		'To/Forward/Slashes'

	:param data: Data to convert. ( String )
	:return: Converted path. ( String )
	"""

	data = data.replace("\\", "/")
	LOGGER.debug("> Data: '{0}' to forward slashes.".format(data))
	return data

def toBackwardSlashes(data):
	"""
	This definition converts forward slashes to backward slashes.

	Usage::

		>>> toBackwardSlashes("/Users/JohnDoe/Documents")
		'\\Users\\JohnDoe\\Documents'

	:param data: Data to convert. ( String )
	:return: Converted path. ( String )
	"""

	data = data.replace("/", "\\")
	LOGGER.debug("> Data: '{0}' to backward slashes.".format(data))
	return data

def toPosixPath(path):
	"""
	This definition converts Windows path to Posix path while stripping drives letters and network server slashes.

	Usage::

		>>> toPosixPath("c:\\Users\\JohnDoe\\Documents")
		'/Users/JohnDoe/Documents'

	:param path: Windows path. ( String )
	:return: Path converted to Posix path. ( String )
	"""

	posixPath = posixpath.normpath(toForwardSlashes(re.sub(r"[a-zA-Z]:\\|\\\\", "/", os.path.normpath(path))))
	LOGGER.debug("> Stripped converted to Posix path: '{0}'.".format(posixPath))
	return posixPath

def getNormalizedPath(path):
	"""
	This definition normalizes a path, escaping slashes if needed on Windows.

	Usage::

		>>> getNormalizedPath("C:\Users\JohnDoe\Documents")
		'C:\\Users\\JohnDoe\\Documents'

	:param path: Path to normalize. ( String )
	:return: Normalized path. ( String )
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
	This definition returns a random sequence.
	
	Usage::

		>>> getRandomSequence()
		arGAqzf3

	:param length: Length of the sequence. ( Integer )
	:return: Random sequence. ( String )
	"""

	return str().join([random.choice(ASCII_CHARACTERS) for i in range(length)])

def isEmail(data):
	"""
	This definition check if given data string is an email.

	Usage::

		>>> isEmail("john.doe@domain.com")
		True
		>>> isEmail("john.doe:domain.com")
		False

	:param data: Data to check. ( String )
	:return: Is email. ( Boolean )
	"""

	if re.match(r"[\w.%+-]+@[\w.]+\.[a-zA-Z]{2,4}", data):
		LOGGER.debug("> {0}' is matched as email.".format(data))
		return True
	else:
		LOGGER.debug("> {0}' is not matched as email.".format(data))
		return False

def isWebsite(data):
	"""
	This definition check if given data string is a website.
	
	Usage::

		>>> isWebsite("http://www.domain.com")
		True
		>>> isWebsite("domain.com")
		False

	:param data: Data to check. ( String )
	:return: Is website. ( Boolean )
	"""

	if re.match(r"(http|ftp|https)://([\w\-\.]+)/?", data):
		LOGGER.debug("> {0}' is matched as website.".format(data))
		return True
	else:
		LOGGER.debug("> {0}' is not matched as website.".format(data))
		return False
