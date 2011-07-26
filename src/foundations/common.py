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
	This Definition Gets The System Application Datas Directory.

	@return: User Application Datas Directory. ( String )
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
	This Definition Gets The User Application Directory.

	@return: User Application Directory. ( String )
	"""

	return os.path.join(getSystemApplicationDatasDirectory(), Constants.providerDirectory, Constants.applicationDirectory)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def closeHandler(logger, handler):
	"""
	This Definition Shuts Down The Provided Handler.

	@param logger: Current Logger. ( Object )
	@param handler: Current Handler. ( Object )
	@return: Definition Success. ( Boolean )
	"""

	len(logger.__dict__["handlers"]) and LOGGER.debug("> Stopping Handler: '{0}'.".format(handler))
	logger.removeHandler(handler)
	return True

@core.executionTrace
def exit(exitCode, logger, handlers):
	"""
	This Definition Shuts Down The Logging And Exit The Current Process.

	@param exitCode: Current Exit Code. ( Integer )
	@param logger: Current Logger. ( Object )
	@param handlers: Handlers. ( Object )
	"""

	LOGGER.debug("> {0} | Exiting Current Process!".format(core.getModule(exit).__name__))

	LOGGER.debug("> Stopping Logging Handlers And Logger, Then Exiting.")

	for handler in handlers:
		handler and closeHandler(logger, handler)

	sys.exit(exitCode)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def wait(waitTime):
	"""
	This Definition Is A Wait Timer.

	@param waitTime: Current Sleep Time In Seconds. ( Integer )
	@return: Definition Success. ( Boolean )
	"""

	LOGGER.debug("> Waiting '{0}' Seconds!".format(waitTime))

	time.sleep(waitTime)
	return True

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
