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
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Common Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

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
#***	Overall variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getSystemApplicationDatasDirectory():
	"""
	This definition gets the system Application datas directory.

	@return: User Application datas directory. ( String )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		environmentVariable = Environment("APPDATA")
		return environmentVariable.getPath()

	elif platform.system() == "Darwin":
		environmentVariable = Environment("HOME")
		return os.path.join(environmentVariable.getPath(), "Library/Preferences")

	elif platform.system() == "Linux":
		environmentVariable = Environment("HOME")
		return environmentVariable.getPath()

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getUserApplicationDatasDirectory():
	"""
	This definition gets the user Application directory.

	@return: User Application directory. ( String )
	"""

	return os.path.join(getSystemApplicationDatasDirectory(), Constants.providerDirectory, Constants.applicationDirectory)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def closeHandler(logger, handler):
	"""
	This definition shuts down the provided handler.

	@param logger: Current logger. ( Object )
	@param handler: Current handler. ( Object )
	@return: Definition success. ( Boolean )
	"""

	len(logger.__dict__["handlers"]) and LOGGER.debug("> Stopping handler: '{0}'.".format(handler))
	logger.removeHandler(handler)
	return True

@core.executionTrace
def exit(exitCode, logger, handlers):
	"""
	This definition shuts down the logging and exit the current process.

	@param exitCode: Current exit code. ( Integer )
	@param logger: Current logger. ( Object )
	@param handlers: Handlers. ( Object )
	"""

	LOGGER.debug("> {0} | Exiting current process!".format(core.getModule(exit).__name__))

	LOGGER.debug("> Stopping logging handlers and logger, then exiting.")

	for handler in handlers:
		handler and closeHandler(logger, handler)

	sys.exit(exitCode)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def wait(waitTime):
	"""
	This definition is a wait timer.

	@param waitTime: Current sleep time in seconds. ( Integer )
	@return: Definition success. ( Boolean )
	"""

	LOGGER.debug("> Waiting '{0}' seconds!".format(waitTime))

	time.sleep(waitTime)
	return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
