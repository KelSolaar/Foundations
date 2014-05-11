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

from __future__ import unicode_literals

import sys
import time

import foundations.verbose

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "exit",
           "wait"]

LOGGER = foundations.verbose.install_logger()


def exit(exit_code=0):
    """
    Shuts down current process logging, associated handlers and then exits to system.

    :param exit_code: System exit code.
    :type exit_code: Integer or String or Object

    :note: **exit_code** argument is passed to Python :func:`sys.exit` definition.
    """

    LOGGER.debug("> {0} | Exiting current process!".format(__name__))

    LOGGER.debug("> Stopping logging handlers and logger!")
    for handler in LOGGER.handlers:
        foundations.verbose.remove_logging_handler(handler)

    sys.exit(exit_code)


def wait(wait_time):
    """
    Halts current process exection for an user defined time.

    :param wait_time: Current sleep time in seconds.
    :type wait_time: float
    :return: Definition success.
    :rtype: bool
    """

    LOGGER.debug("> Waiting '{0}' seconds!".format(wait_time))

    time.sleep(wait_time)
    return True
