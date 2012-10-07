#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**core.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package core objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import linecache
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
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"extractStack",
			"exit",
			"wait"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def extractStack(frame, stackTraceFrameTag="__stackTraceFrameTag__"):
	"""
	| This definition extracts the stack from provided frame.
	| The code is similar to :func:`traceback.extract_stack` except that it allows frames to be excluded
		from the stack if the given stack trace frame tag is found in the frame locals and set **True**.
	
	:param frame: Frame. ( Frame )
	:param stackTraceFrameTag: Stack trace frame tag. ( String )
	:return: Stack. ( List )
	"""

	stack = []
	while frame is not None:
		skipFrame = frame.f_locals.get(stackTraceFrameTag)
		if not skipFrame:
			lineNumber = frame.f_lineno
			code = frame.f_code
			codeName = code.co_name
			filename = code.co_filename
			linecache.checkcache(filename)
			line = linecache.getline(filename, lineNumber, frame.f_globals)
			line = line and line.strip() or None
			stack.append((filename, lineNumber, codeName, line))
		frame = frame.f_back
	stack.reverse()

	return stack

def exit(exitCode=1):
	"""
	This definition shuts down current process logging, associated handlers and then exits to system.
	
	:param exitCode: System exit code. ( Integer / String / Object )

	:note: **exitCode** argument is passed to Python :func:`sys.exit` definition.
	"""

	LOGGER.debug("> {0} | Exiting current process!".format(__name__))

	LOGGER.debug("> Stopping logging handlers and logger!")
	for handler in LOGGER.handlers:
		foundations.verbose.removeLoggingHandler(handler)

	sys.exit(exitCode)

def wait(waitTime):
	"""
	This definition halts current process exection for an user defined time.

	:param waitTime: Current sleep time in seconds. ( Float )
	:return: Definition success. ( Boolean )
	"""

	LOGGER.debug("> Waiting '{0}' seconds!".format(waitTime))

	time.sleep(waitTime)
	return True
