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
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Constants Module.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import platform

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Constants():
	"""
	This Class Is The Constants Class.
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

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
