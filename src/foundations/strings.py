#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
************************************************************************************************
***	strings.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Strings Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import os
import platform
import posixpath
import re

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
import foundations.exceptions
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getNiceName(name):
	"""
	This Definition Converts A String To Nice String: currentLogText -> Current Log Text.

	@param name: Current String To Be Nicified. ( String )
	@return: Nicified String. ( String )
	"""

	niceName = ""
	for index in range(len(name)):
		if index == 0:
			niceName += name[ index ].upper()
		else:
			if name[ index ].upper() == name[ index ]:
				if index + 1 < len(name):
					if  name[ index + 1 ].upper() != name[ index + 1 ]:
						niceName += " " + name[ index ]
					else:
						LOGGER.debug("> '{0}' To '{1}'.".format(name, name))
						return name
				else:
					niceName += name[ index ]
			else:
				niceName += name[ index ]
	LOGGER.debug("> '{0}' To '{1}'.".format(name, niceName))
	return niceName

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getVersionRank(version):
	"""
	This Definition Converts A Version String To It's Rank.

	@param version: Current Version To Calculate Rank. ( String )
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
	This Definition Get The Basename Of A Path Without Its Extension.

	@param path: Path To Extract The Basename Without Extension. ( String )
	@return: Splitext Basename. ( String )
	"""

	basename = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
	LOGGER.debug("> Splitext Basename: '{0}'.".format(basename))
	return basename

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getWords(datas):
	"""
	This Method Extracts The Words From Provided String.
	
	@param datas: Datas To Extract Words From. ( String )
	@return: Words. ( List )
	"""

	words = re.findall("\w+", datas)
	LOGGER.debug("> Words: '{0}'".format(", ".join(words)))
	return words

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def filterWords(words, filtersIn=None, filtersOut=None, flags=0):
	"""
	This Method Filters The Words Using The Provided Filters.
	
	@param filtersIn: Regex filtersIn List. ( List / Tuple )
	@param filtersIn: Regex filtersOut List. ( List / Tuple )
	@param flags: Regex Flags. ( Object )
	@return: Filtered Words. ( List )
	"""

	filteredWords = []
	for word in words:
		if filtersIn:
			filterMatched = False
			for filter in filtersIn:
				if not re.search(filter, word, flags):
					LOGGER.debug("> '{0}' Word Skipped, Filter In '{1}' Not Matched!".format(word, filter))
				else:
					filterMatched = True
					break
			if not filterMatched:
				continue

		if filtersOut:
			filterMatched = False
			for filter in filtersOut:
				if re.search(filter, word, flags):
					LOGGER.debug("> '{0}' Word Skipped, Filter Out '{1}' Matched!".format(word, filter))
					filterMatched = True
					break
			if filterMatched:
				continue
		filteredWords.append(word)
	LOGGER.debug("> Filtered Words: '{0}'".format(", ".join(filteredWords)))
	return filteredWords

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def replace(string, datas):
	"""
	This Definition Replaces The Datas Occurences In The String.
	@param string: String To Manipulate. ( String )
	@param datas: Replacement Occurences. ( Dictionary )
	@return: Manipulated String. ( String )
	"""

	for old, new in datas.items():
		string = string.replace(old, new)
	return string

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def toForwardSlashes(datas):
	"""
	This Definition Converts Backward Slashes To Forward Slashes.

	@param datas: Datas To Convert. ( String )	
	@return: Converted Path. ( String )
	"""

	datas = datas.replace("\\", "/")
	LOGGER.debug("> Datas: '{0}' To Forward Slashes.".format(datas))
	return datas

@core.executionTrace
def toBackwardSlashes(datas):
	"""
	This Definition Converts Forward Slashes To Backward Slashes.

	@param datas: Datas To Convert. ( String )	
	@return: Converted Path. ( String )
	"""

	datas = datas.replace("/", "\\")
	LOGGER.debug("> Datas: '{0}' To Backward Slashes.".format(datas))
	return datas

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def toPosixPath(path):
	"""
	This Definition Converts Windows Path To Posix Path While Stripping Drives Letters And Network Server Slashes.
	
	@param path: Windows Path. ( String )
	@return: Path Converted To Posix Path. ( String )
	"""

	posixPath = posixpath.normpath(toForwardSlashes(re.sub("[a-zA-Z]:\\\\|\\\\\\\\", "/", os.path.normpath(path))))
	LOGGER.debug("> Stripped Converted To Posix Path: '{0}'.".format(posixPath))
	return posixPath

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getNormalizedPath(path):
	"""
	This Definition Normalizes A Path, Escaping Slashes If Needed On Windows.

	@param path: Path To Normalize. ( String )
	@return: Normalized Path. ( String )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		path = os.path.normpath(path).replace("\\", "\\\\")
		LOGGER.debug("> Path: '{0}', Normalized Path.".format(path))
		return path
	else:
		path = os.path.normpath(path)
		LOGGER.debug("> Path: '{0}', Normalized Path.".format(path))
		return path

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def isEmail(datas):
	"""
	This Definition Check If Provided Datas String Is An Email.

	@param datas: Datas To Check. ( String )	
	@return: Is Email. ( Boolean )
	"""

	if re.match("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}", datas):
		LOGGER.debug("> {0}' Is Matched As Email.".format(datas))
		return True
	else:
		LOGGER.debug("> {0}' Is Not Matched As Email.".format(datas))
		return False

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def isWebsite(datas):
	"""
	This Definition Check If Provided Datas String Is A Website.

	@param datas: Datas To Check. ( String )	
	@return: Is Website. ( Boolean )
	"""

	if re.match("(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?", datas):
		LOGGER.debug("> {0}' Is Matched As Website.".format(datas))
		return True
	else:
		LOGGER.debug("> {0}' Is Not Matched As Website.".format(datas))
		return False

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
