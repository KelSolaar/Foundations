#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package default constants through the :class:`Constants` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines **Foundations** package default constants.
	"""

	applicationName = "Foundations"
	"""Package Application name: '**Foundations**' ( String )"""
	majorVersion = "2"
	"""Package major version: '**2**' ( String )"""
	minorVersion = "1"
	"""Package minor version: '**1**' ( String )"""
	changeVersion = "0"
	"""Package change version: '**0**' ( String )"""
	releaseVersion = ".".join((majorVersion, minorVersion, changeVersion))
	"""Package release version: '**2.1.0**' ( String )"""

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

	defaultCodec = foundations.DEFAULT_CODEC
	"""Default codec: '**utf-8**' ( String )"""
	codecError = foundations.CODEC_ERROR
	"""Default codec error behavior: '**ignore**' ( String )"""

	applicationDirectory = os.sep.join(("Foundations", ".".join((majorVersion, minorVersion))))
	"""Package Application directory: '**Foundations**' ( String )"""
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""

	nullObject = "None"
	"""Default null object string: '**None**' ( String )"""
