#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package default constants through the :class:`Constants` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["Constants"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Constants():
	"""
	This class provides **Foundations** package default constants.
	"""

	applicationName = "Foundations"
	"""Package Application name: '**Foundations**' ( String )"""
	majorVersion = "2"
	"""Package major version: '**2**' ( String )"""
	minorVersion = "0"
	"""Package minor version: '**0**' ( String )"""
	changeVersion = "7"
	"""Package change version: '**7**' ( String )"""
	releaseVersion = ".".join((majorVersion, minorVersion, changeVersion))
	"""Package release version: '**2.0.7**' ( String )"""

	logger = "Foundations_Logger"
	"""Package logger name: '**Foundations_Logger**' ( String )"""
	verbosityLevel = 3
	"""Default logging verbosity level: '**3**' ( Integer )"""
	verbosityLabels = ("Critical", "Error", "Warning", "Info", "Debug")
	"""Logging verbosity labels: ('**Critical**', '**Error**', '**Warning**', '**Info**', '**Debug**') ( Tuple )"""
	loggingDefaultFormatter = "Default"
	"""Default logging formatter name: '**Default**' ( String )"""
	loggingSeparators = "*" * 96
	"""Logging separators: '*' * 96 ( String )"""

	encodingFormat = "utf-8"
	"""Default encoding format: '**utf-8**' ( String )"""
	encodingError = "ignore"
	"""Default encoding error behavior: '**ignore**' ( String )"""

	applicationDirectory = os.sep.join(("Foundations", ".".join((majorVersion, minorVersion))))
	"""Package Application directory: '**Foundations**' ( String )"""
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""

	nullObject = str(None)
	"""Default null object string: '**None**' ( String )"""
