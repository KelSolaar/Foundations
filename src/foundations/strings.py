#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**strings.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Strings Module.

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
	This definition converts a string to nice string: currentLogText -> current log text.

	@param name: Current string to be nicified. ( String )
	@return: Nicified string. ( String )
	"""

	niceName = ""
	for index in range(len(name)):
		if index == 0:
			niceName += name[index].upper()
		else:
			if name[index].upper() == name[index]:
				if index + 1 < len(name):
					if name[index + 1].upper() != name[index + 1]:
						niceName += " " + name[index]
					else:
						LOGGER.debug("> '{0}' to '{1}'.".format(name, name))
						return name
				else:
					niceName += name[index]
			else:
				niceName += name[index]
	LOGGER.debug("> '{0}' to '{1}'.".format(name, niceName))
	return niceName

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getVersionRank(version):
	"""
	This definition converts a version string to it's rank.

	@param version: Current version to calculate rank. ( String )
	@return: Rank. ( Integer )
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

	@param path: Path to extract the basename without extension. ( String )
	@return: Splitext basename. ( String )
	"""

	basename = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
	LOGGER.debug("> Splitext basename: '{0}'.".format(basename))
	return basename

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getWords(datas):
	"""
	This method extracts the words from provided string.

	@param datas: Datas to extract words from. ( String )
	@return: Words. ( List )
	"""

	words = re.findall("\w+", datas)
	LOGGER.debug("> Words: '{0}'".format(", ".join(words)))
	return words

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def filterWords(words, filtersIn=None, filtersOut=None, flags=0):
	"""
	This method filters the words using the provided filters.

	@param filtersIn: Regex filters in list. ( List / Tuple )
	@param filtersIn: Regex filters out list. ( List / Tuple )
	@param flags: Regex flags. ( Object )
	@return: Filtered words. ( List )
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
	@param string: String to manipulate. ( String )
	@param datas: Replacement occurences. ( Dictionary )
	@return: Manipulated string. ( String )
	"""

	for old, new in datas.items():
		string = string.replace(old, new)
	return string

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def toForwardSlashes(datas):
	"""
	This definition converts backward slashes to forward slashes.

	@param datas: Datas to convert. ( String )
	@return: Converted path. ( String )
	"""

	datas = datas.replace("\\", "/")
	LOGGER.debug("> Datas: '{0}' to forward slashes.".format(datas))
	return datas

@core.executionTrace
def toBackwardSlashes(datas):
	"""
	This definition converts forward slashes to backward slashes.

	@param datas: Datas to convert. ( String )
	@return: Converted path. ( String )
	"""

	datas = datas.replace("/", "\\")
	LOGGER.debug("> Datas: '{0}' to backward slashes.".format(datas))
	return datas

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def toPosixPath(path):
	"""
	This definition converts Windows path to Posix path while stripping drives letters and network server slashes.

	@param path: Windows path. ( String )
	@return: Path converted to Posix path. ( String )
	"""

	posixPath = posixpath.normpath(toForwardSlashes(re.sub("[a-zA-Z]:\\\\|\\\\\\\\", "/", os.path.normpath(path))))
	LOGGER.debug("> Stripped converted to Posix path: '{0}'.".format(posixPath))
	return posixPath

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getNormalizedPath(path):
	"""
	This definition normalizes a path, escaping slashes if needed on Windows.

	@param path: Path to normalize. ( String )
	@return: Normalized path. ( String )
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

	@param datas: Datas to check. ( String )
	@return: Is email. ( Boolean )
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

	@param datas: Datas to check. ( String )
	@return: Is website. ( Boolean )
	"""

	if re.match("(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?", datas):
		LOGGER.debug("> {0}' is matched as website.".format(datas))
		return True
	else:
		LOGGER.debug("> {0}' is not matched as website.".format(datas))
		return False

