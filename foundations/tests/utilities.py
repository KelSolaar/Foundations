#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**utilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines tests suite logging configuration.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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

__all__ = ["LOGGER"]

LOGGER = foundations.verbose.installLogger()
foundations.verbose.getLoggingConsoleHandler()
