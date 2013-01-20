#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**cache.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines caching related classes.

**Others:**

"""

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

__all__ = ["LOGGER", "Cache"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Cache(dict):
	"""
	This class defines the cache object and provides various methods to interact with its content.
	
	Usage:
		
	"""

	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		dict.__init__(self, **kwargs)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def addContent(self, **content):
		"""
		This method adds given content to the cache.

		Usage::
		
			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache
			{'Luke': 'Skywalker', 'John': 'Doe'}

		:param \*\*content: Content to add. ( \*\* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' content to the cache.".format(self.__class__.__name__, content))

		self.update(**content)
		return True

	def removeContent(self, *keys):
		"""
		This method removes given content from the cache.

		Usage::
			
			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache.removeContent("Luke", "John")
			True
			>>> cache
			{}			
			
		:param \*keys: Content to remove. ( \* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing '{0}' content from the cache.".format(self.__class__.__name__, keys))

		for key in keys:
			if not key in self:
				raise KeyError("{0} | '{1}' key doesn't exists in cache content!".format(self.__class__.__name__, key))

			del self[key]
		return True

	def getContent(self, key):
		"""
		This method gets given content from the cache.

		Usage::

			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache.getContent("Luke")
			'Skywalker'
			
		:param key: Content to retrieve. ( Object )
		:return: Content. ( Object )
		"""

		LOGGER.debug("> Retrieving '{0}' content from the cache.".format(self.__class__.__name__, key))

		return self.get(key)

	def flushContent(self):
		"""
		This method flushes the cache content.

		Usage::

			>>> cache = Cache()
			>>> cache.addContent(John="Doe", Luke="Skywalker")
			True
			>>> cache.flushContent()
			True
			>>> cache
			{}
			
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Flushing cache content.".format(self.__class__.__name__))

		self.clear()
		return True
