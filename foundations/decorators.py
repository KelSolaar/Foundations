#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**decorators.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package generic decorators objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
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
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"executionTime",
		"memoize"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def executionTime(object):
	"""
	| This decorator is used for execution timing.
	| Any method / definition decorated will have it's execution timed through information messages.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	def executionTimeWrapper(*args, **kwargs):
		"""
		This decorator is used for execution timing.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
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
	| This decorator is used for method / definition memoization.
	| Any method / definition decorated will get its return value cached and restored whenever called
		with the same arguments.
	
	:param cache: Alternate cache. ( Dictionary )
	:return: Object. ( Object )
	"""

	if cache is None:
		cache = {}

	def memoizeDecorator(object):
		"""
		This decorator is used for object memoization.

		:param object: Object to decorate. ( Object )
		:return: Object. ( Object )
		"""

		@functools.wraps(object)
		def memoizeWrapper(*args, **kwargs):
			"""
			This decorator is used for object memoization.
	
			:param \*args: Arguments. ( \* )
			:param \*\*kwargs: Keywords arguments. ( \*\* )
			:return: Object. ( Object )
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
