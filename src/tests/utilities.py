#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**utilities.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines tests suite logging configuration.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import sys

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
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

LOGGER = logging.getLogger(Constants.logger)

# Starting The Console Handler.
LOGGING_CONSOLE_HANDLER = logging.StreamHandler(sys.__stdout__)
LOGGING_CONSOLE_HANDLER.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
LOGGER.addHandler(LOGGING_CONSOLE_HANDLER)
