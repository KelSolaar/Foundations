#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**core.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package core objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
import time

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
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
			"exit",
			"wait"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def exit(exitCode=0):
	"""
	Shuts down current process logging, associated handlers and then exits to system.
	
	:param exitCode: System exit code.
	:type exitCode: Integer or String or Object

	:note: **exitCode** argument is passed to Python :func:`sys.exit` definition.
	"""

	LOGGER.debug("> {0} | Exiting current process!".format(__name__))

	LOGGER.debug("> Stopping logging handlers and logger!")
	for handler in LOGGER.handlers:
		foundations.verbose.removeLoggingHandler(handler)

	sys.exit(exitCode)

def wait(waitTime):
	"""
	Halts current process exection for an user defined time.

	:param waitTime: Current sleep time in seconds.
	:type waitTime: float
	:return: Definition success.
	:rtype: bool
	"""

	LOGGER.debug("> Waiting '{0}' seconds!".format(waitTime))

	time.sleep(waitTime)
	return True
