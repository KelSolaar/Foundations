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
		"execution_time",
		"memoize",
		"system_exit"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def execution_time(object):
	"""
	| Implements execution timing.
	| Any method / definition decorated will have it's execution timed through information messages.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def execution_time_wrapper(*args, **kwargs):
		"""
		Implements execution timing.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		start_time = time.time()

		value = object(*args, **kwargs)

		end_time = time.time()

		sys.stdout.write("{0} | '{1}' object processed during '{2:f}' ms!\n".format(__name__,
																				object.__name__,
																				(end_time - start_time) * 1000.0))

		return value

	return execution_time_wrapper

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

	def memoize_decorator(object):
		"""
		Implements method / definition memoization.

		:param object: Object to decorate.
		:type object: object
		:return: Object.
		:rtype: object
		"""

		@functools.wraps(object)
		def memoize_wrapper(*args, **kwargs):
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

		return memoize_wrapper

	return memoize_decorator

def system_exit(object):
	"""
	Handles proper system exit in case of critical exception.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def system_exit_wrapper(*args, **kwargs):
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
			sys.stderr.write("\n".join(foundations.exceptions.format_exception(*sys.exc_info())))
			foundations.core.exit(1)

	return system_exit_wrapper
