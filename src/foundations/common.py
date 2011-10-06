#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package common utilities objects that don't fall in any specific category.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import platform
import sys
import time

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.environment import Environment
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

__all__ = ["LOGGER", "getSystemApplicationDatasDirectory", "getUserApplicationDatasDirectory", "removeLoggingHandler", "exit", "wait"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getSystemApplicationDatasDirectory():
	"""
	This definition gets system Application datas directory.
	
	Examples directories::

		- 'C:\Users\$USER\AppData\Roaming' on Windows 7.
		- 'C:\Documents and Settings\$USER\Application Data' on Windows XP.
		- '/Users/$USER/Library/Preferences' on Mac Os X.
		- '/home/$USER' on Linux.

	:return: User Application datas directory. ( String )
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
def getUserApplicationDatasDirectory():
	"""
	| This definition gets user Application directory.
	| The difference between :func:`getSystemApplicationDatasDirectory` and :func:`getSystemApplicationDatasDirectory` definitions is that :func:`getUserApplicationDatasDirectory` definition will append :attr:`foundations.globals.constants.Constants.providerDirectory` and :attr:`foundations.globals.constants.Constants.applicationDirectory` attributes values to the path returned.

	Examples directories::

		- 'C:\Users\$USER\AppData\Roaming\Provider\Application' on Windows 7.
		- 'C:\Documents and Settings\$USER\Application Data\Provider\Application' on Windows XP.
		- '/Users/$USER/Library/Preferences/Provider/Application' on Mac Os X.
		- '/home/$USER/.Provider/Application' on Linux.

	:return: User Application directory. ( String )
	"""

	return os.path.join(getSystemApplicationDatasDirectory(), Constants.providerDirectory, Constants.applicationDirectory)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def removeLoggingHandler(logger, handler):
	"""
	This definition removes provided logging handler from provided logger.

	:param logger: Handler parent logger. ( Logger )
	:param handler: Handler. ( Handler )
	:return: Definition success. ( Boolean )
	"""

	len(logger.__dict__["handlers"]) and LOGGER.debug("> Stopping handler: '{0}'.".format(handler))
	logger.removeHandler(handler)
	return True

@core.executionTrace
def exit(exitCode, logger, handlers):
	"""
	This definition shuts down current process logging, associated handlers and then exits to system.
	
	:param exitCode: System exit code. ( Integer / String / Object )
	:param logger: Current logger. ( Object )
	:param handlers: Handlers. ( List )

	:note: **exitCode** argument is passed to Python :func:`sys.exit` definition.
	"""

	LOGGER.debug("> {0} | Exiting current process!".format(core.getModule(exit).__name__))

	LOGGER.debug("> Stopping logging handlers and logger, then exiting.")

	for handler in handlers:
		handler and removeLoggingHandler(logger, handler)

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
