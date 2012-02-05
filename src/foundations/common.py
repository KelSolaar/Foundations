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
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import itertools
import logging
import os
import platform
import sys
import time

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.environment import Environment
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
			"getSystemApplicationDataDirectory",
			"getUserApplicationDataDirectory",
			"removeLoggingHandler",
			"exit",
			"wait",
			"uniqify",
			"orderedUniqify",
			"pathExists",
			"isBinaryFile"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getSystemApplicationDataDirectory():
	"""
	This definition returns the system Application data directory.
	
	Examples directories::

		- 'C:\Users\$USER\AppData\Roaming' on Windows 7.
		- 'C:\Documents and Settings\$USER\Application Data' on Windows XP.
		- '/Users/$USER/Library/Preferences' on Mac Os X.
		- '/home/$USER' on Linux.

	:return: User Application data directory. ( String )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		environmentVariable = Environment("APPDATA")
		return environmentVariable.getValue()

	elif platform.system() == "Darwin":
		environmentVariable = Environment("HOME")
		return os.path.join(environmentVariable.getValue(), "Library/Preferences")

	elif platform.system() == "Linux":
		environmentVariable = Environment("HOME")
		return environmentVariable.getValue()

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getUserApplicationDataDirectory():
	"""
	| This definition returns the user Application directory.
	| The difference between :func:`getSystemApplicationDataDirectory`
		and :func:`getSystemApplicationDataDirectory` definitions is that :func:`getUserApplicationDataDirectory` definition
		will append :attr:`foundations.globals.constants.Constants.providerDirectory`
		and :attr:`foundations.globals.constants.Constants.applicationDirectory` attributes values to the path returned.

	Examples directories::

		- 'C:\Users\$USER\AppData\Roaming\Provider\Application' on Windows 7.
		- 'C:\Documents and Settings\$USER\Application Data\Provider\Application' on Windows XP.
		- '/Users/$USER/Library/Preferences/Provider/Application' on Mac Os X.
		- '/home/$USER/.Provider/Application' on Linux.

	:return: User Application directory. ( String )
	"""

	return os.path.join(getSystemApplicationDataDirectory(), Constants.providerDirectory, Constants.applicationDirectory)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def removeLoggingHandler(logger, handler):
	"""
	This definition removes given logging handler from given logger.

	:param logger: Handler parent logger. ( Logger )
	:param handler: Handler. ( Handler )
	:return: Definition success. ( Boolean )
	"""

	len(logger.__dict__["handlers"]) and LOGGER.debug("> Stopping handler: '{0}'.".format(handler))
	logger.removeHandler(handler)
	return True

@core.executionTrace
def exit(exitCode=1):
	"""
	This definition shuts down current process logging, associated handlers and then exits to system.
	
	:param exitCode: System exit code. ( Integer / String / Object )

	:note: **exitCode** argument is passed to Python :func:`sys.exit` definition.
	"""

	LOGGER.debug("> {0} | Exiting current process!".format(core.getModule(exit).__name__))

	LOGGER.debug("> Stopping logging handlers and logger!")
	for handler in LOGGER.__dict__["handlers"]:
		removeLoggingHandler(LOGGER, handler)

	sys.exit(exitCode)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def wait(waitTime):
	"""
	This definition halts current process exection for an user defined time.

	:param waitTime: Current sleep time in seconds. ( Float )
	:return: Definition success. ( Boolean )
	"""

	LOGGER.debug("> Waiting '{0}' seconds!".format(waitTime))

	time.sleep(waitTime)
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def uniqify(sequence):
	"""
	This definition uniqifies the given sequence even if unhashable.

	:param sequence: Sequence. ( Object )
	:return: Uniqified sequence. ( List )
	
	:note: The sequence order is not maintained by this definition.
	"""

	return [key for key, group in itertools.groupby(sorted(sequence))]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def orderedUniqify(sequence):
	"""
	This definition uniqifies the given hashable sequence while preserving its order.

	:param sequence: Sequence. ( Object )
	:return: Uniqified sequence. ( List )
	"""

	items = set()
	return [key for key in sequence if key not in items and not items.add(key)]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def pathExists(path):
	"""
	This definition returns if given path exists.

	:param path: Path. ( String )
	:return: Path existence. ( Boolean )
	"""

	if not path:
		return
	else:
		return os.path.exists(path)

@core.executionTrace
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
