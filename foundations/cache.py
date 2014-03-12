#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**cache.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines caching related classes.

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

__all__ = ["LOGGER", "Cache"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Cache(dict):
	"""
	Defines the cache object and provides various methods to interact with its content.
	
	Usage:
		
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: Key / Value pairs.
		:type \*\*kwargs: dict
		"""

		dict.__init__(self, **kwargs)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def addContent(self, **content):
		"""
		Adds given content to the cache.

		Usage::
		
			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache
			{'Luke': 'Skywalker', 'John': 'Doe'}

		:param \*\*content: Content to add.
		:type \*\*content: \*\*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		self.update(**content)
		return True

	def removeContent(self, *keys):
		"""
		Removes given content from the cache.

		Usage::
			
			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache.removeContent("Luke", "John")
			True
			>>> cache
			{}			
			
		:param \*keys: Content to remove.
		:type \*keys: \*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' content from the cache.".format(self.__class__.__name__, keys))

		for key in keys:
			if not key in self:
				raise KeyError("{0} | '{1}' key doesn't exists in cache content!".format(self.__class__.__name__, key))

			del self[key]
		return True

	def getContent(self, key):
		"""
		Gets given content from the cache.

		Usage::

			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache.getContent("Luke")
			'Skywalker'
			
		:param key: Content to retrieve.
		:type key: object
		:return: Content.
		:rtype: object
		"""

		LOGGER.debug("> Retrieving '{0}' content from the cache.".format(self.__class__.__name__, key))

		return self.get(key)

	def flushContent(self):
		"""
		Flushes the cache content.

		Usage::

			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache.flushContent()
			True
			>>> cache
			{}
			
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Flushing cache content.".format(self.__class__.__name__))

		self.clear()
		return True
