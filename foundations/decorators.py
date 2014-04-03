#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**decorators.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package generic decorators objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import sys
import time

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core
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
		"executionTime",
		"memoize",
		"systemExit"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def executionTime(object):
	"""
	| Implements execution timing.
	| Any method / definition decorated will have it's execution timed through information messages.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def executionTimeWrapper(*args, **kwargs):
		"""
		Implements execution timing.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		startTime = time.time()

		value = object(*args, **kwargs)

		endTime = time.time()

		sys.stdout.write("{0} | '{1}' object processed during '{2:f}' ms!\n".format(__name__,
																				object.__name__,
																				(endTime - startTime) * 1000.0))

		return value

	return executionTimeWrapper

def memoize(cache=None):
	"""
	| Implements method / definition memoization.
	| Any method / definition decorated will get its return value cached and restored whenever called with the same arguments.

	:param cache: Alternate cache.
	:type cache: dict
	:return: Object.
	:rtype: object
	"""

	if cache is None:
		cache = {}

	def memoizeDecorator(object):
		"""
		Implements method / definition memoization.

		:param object: Object to decorate.
		:type object: object
		:return: Object.
		:rtype: object
		"""

		@functools.wraps(object)
		def memoizeWrapper(*args, **kwargs):
			"""
			Implements method / definition memoization.

			:param \*args: Arguments.
			:type \*args: \*
			:param \*\*kwargs: Keywords arguments.
			:type \*\*kwargs: \*\*
			:return: Object.
			:rtype: object
			"""

			if kwargs:
				key = args, frozenset(kwargs.iteritems())
			else:
				key = args

			if key not in cache:
				cache[key] = object(*args, **kwargs)

			return cache[key]

		return memoizeWrapper

	return memoizeDecorator

def systemExit(object):
	"""
	Handles proper system exit in case of critical exception.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def systemExitWrapper(*args, **kwargs):
		"""
		Handles proper system exit in case of critical exception.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		try:
			if object(*args, **kwargs):
				foundations.core.exit(0)
		except Exception as error:
			sys.stderr.write("\n".join(foundations.exceptions.formatException(*sys.exc_info())))
			foundations.core.exit(1)

	return systemExitWrapper
