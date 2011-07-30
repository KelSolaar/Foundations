#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Constants Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import platform

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Constants():
	"""
	This class is the Constants class.
	"""

	applicationName = "Foundations"

	logger = "Foundations_Logger"
	verbosityLevel = 3
	verbosityLabels = ("Critical", "Error", "Warning", "Info", "Debug")
	loggingDefaultFormatter = "Default"
	loggingSeparators = "*" * 96

	encodingFormat = "utf-8"
	encodingError = "ignore"

	applicationDirectory = "Foundations"
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"

	nullObject = "None"

