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

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import platform
import posixpath
import re
import string

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

	chunks = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
	return " ".join(element.title() for element in re.sub('([a-z0-9])([A-Z])', r'\1 \2', chunks).split())

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getVersionRank(version):
	"""
	This definition converts a version string to it's rank.

	Usage::

		>>> getVersionRank("4.2.8")
		428
		>>> print getVersionRank("4.2.8").__class__
		<type 'int'>

	:param version: Current version to calculate rank. ( String )
	:return: Rank. ( Integer )
	"""

	tokens = version.split(".")
	rank = sum((int(10 ** (i - 1)) * int(tokens[-i]) for i in range(len(tokens), 0, -1)))
	LOGGER.debug("> Rank: '{0}'.".format(rank))
	return rank

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getSplitextBasename(path):
	"""
	This definition get the basename of a path without its extension.

	Usage::

		>>> getSplitextBasename("/Users/JohnDoe/Documents/Test.txt")
		'Test'

	:param path: Path to extract the basename without extension. ( String )
	:return: Splitext basename. ( String )
	"""

	basename = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
	LOGGER.debug("> Splitext basename: '{0}'.".format(basename))
	return basename

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getWords(datas):
	"""
	This method extracts the words from provided string.

	Usage::

		>>> getWords("Users are: John Doe, Jane Doe, Z6PO.")
		['Users', 'are', 'John', 'Doe', 'Jane', 'Doe', 'Z6PO']

	:param datas: Datas to extract words from. ( String )
	:return: Words. ( List )
	"""

	words = re.findall("\w+", datas)
	LOGGER.debug("> Words: '{0}'".format(", ".join(words)))
	return words

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def filterWords(words, filtersIn=None, filtersOut=None, flags=0):
	"""
	This method filters the words using the provided filters.

	Usage::

		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersIn=("John", "Doe"))
		['John', 'Doe', 'Doe']
		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersIn=("[\w]*r",))
		['Users', 'are']
		>>> filterWords(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filtersOut=("[\w]*o",))
		['Users', 'are', 'Jane', 'Z6PO']

	:param filtersIn: Regex filters in list. ( List / Tuple )
	:param filtersIn: Regex filters out list. ( List / Tuple )
	:param flags: Regex flags. ( Object )
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def replace(string, datas):
	"""
	This definition replaces the datas occurences in the string.

	Usage::

		>>> replace("Users are: John Doe, Jane Doe, Z6PO.", {"John" : "Luke", "Jane" : "Anakin", "Doe" : "Skywalker", "Z6PO" : "R2D2"})
		'Users are: Luke Skywalker, Anakin Skywalker, R2D2.'

	:param string: String to manipulate. ( String )
	:param datas: Replacement occurences. ( Dictionary )
	:return: Manipulated string. ( String )
	"""

	for old, new in datas.items():
		string = string.replace(old, new)
	return string

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def toForwardSlashes(datas):
	"""
	This definition converts backward slashes to forward slashes.

	Usage::

		>>> toForwardSlashes("To\Forward\Slashes")
		'To/Forward/Slashes'

	:param datas: Datas to convert. ( String )
	:return: Converted path. ( String )
	"""

	datas = datas.replace("\\", "/")
	LOGGER.debug("> Datas: '{0}' to forward slashes.".format(datas))
	return datas

@core.executionTrace
def toBackwardSlashes(datas):
	"""
	This definition converts forward slashes to backward slashes.

	Usage::

		>>> toBackwardSlashes("/Users/JohnDoe/Documents")
		'\\Users\\JohnDoe\\Documents'

	:param datas: Datas to convert. ( String )
	:return: Converted path. ( String )
	"""

	datas = datas.replace("/", "\\")
	LOGGER.debug("> Datas: '{0}' to backward slashes.".format(datas))
	return datas

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def isEmail(datas):
	"""
	This definition check if provided datas string is an email.

	Usage::

		>>> isEmail("john.doe@domain.com")
		True
		>>> isEmail("john.doe:domain.com")
		False

	:param datas: Datas to check. ( String )
	:return: Is email. ( Boolean )
	"""

	if re.match("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}", datas):
		LOGGER.debug("> {0}' is matched as email.".format(datas))
		return True
	else:
		LOGGER.debug("> {0}' is not matched as email.".format(datas))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def isWebsite(datas):
	"""
	This definition check if provided datas string is a website.
	
	Usage::

		>>> isWebsite("http://www.domain.com")
		True
		>>> isWebsite("domain.com")
		False

	:param datas: Datas to check. ( String )
	:return: Is website. ( Boolean )
	"""

	if re.match("(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?", datas):
		LOGGER.debug("> {0}' is matched as website.".format(datas))
		return True
	else:
		LOGGER.debug("> {0}' is not matched as website.".format(datas))
		return False
