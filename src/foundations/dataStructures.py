#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**dataStructures.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package data structures objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"NestedAttribute",
			"Structure",
			"OrderedStructure",
			"Lookup"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class NestedAttribute(object):
	"""
	This class is an helper object providing methods to manipulate nested attributes.
	
	Usage:
		
		>>> nest = NestedAttribute()
		>>> nest.my.nested.attribute = "Value"
		>>> nest.my.nested.attribute
		Value
		>>> nest.another.very.deeply.nested.attribute = 64
		>>> nest.another.very.deeply.nested.attribute
		64
	"""

	# @core.executionTrace
	def __getattr__(self, attribute):
		"""
		This method returns requested attribute.
	
		:param attribute: Attribute name. ( String )
		:return: Attribute. ( Object )
		"""

		self.__dict__[attribute] = NestedAttribute()
		return self.__dict__[attribute]

	# @core.executionTrace
	def __setattr__(self, attribute, value):
		"""
		This method sets given attribute with given value.
	
		:param attribute: Attribute name. ( String )
		:param name: Attribute value. ( Object )
		"""

		namespaces = attribute.split(".")
		object.__setattr__(reduce(object.__getattribute__, namespaces[:-1], self), namespaces[-1], value)

	# @core.executionTrace
	def __delattr__(self, attribute):
		"""
		This method deletes given attribute with.
	
		:param attribute: Attribute name. ( String )
		"""

		namespaces = attribute.split(".")
		object.__delattr__(reduce(object.__getattribute__, namespaces[:-1], self), namespaces[-1])

class Structure(dict):
	"""
	This class creates an object similar to C/C++ structured type.
	
	Usage:
		
		>>> person = Structure(firstName="Doe", lastName="John", gender="male")
		>>> person.firstName
		'Doe'
		>>> person.keys()
		['gender', 'firstName', 'lastName']
		>>> person["gender"]
		'male'
		>>> del(person["gender"])
		>>> person["gender"]
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		KeyError: 'gender'
		>>> person.gender
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		AttributeError: 'Structure' object has no attribute 'gender'
	"""

	@core.executionTrace
	def __init__(self, *args, **kwargs):
		"""
		This method initializes the class.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		dict.__init__(self, **kwargs)
		self.__dict__.update(**kwargs)

	# @core.executionTrace
	def __getattr__(self, attribute):
		"""
		This method returns given attribute value.

		:return: Attribute value. ( Object )
		"""

		return self[attribute]

	# @core.executionTrace
	def __setattr__(self, attribute, value):
		"""
		This method sets both key and sibling attribute with given value.

		:param attribute.: Attribute. ( Object )
		:param value.: Value. ( Object )
		"""

		dict.__setitem__(self, attribute, value)
		object.__setattr__(self, attribute, value)

	__setitem__ = __setattr__

	# @core.executionTrace
	def __delattr__(self, attribute):
		"""
		This method deletes both key and sibling attribute.

		:param attribute.: Attribute. ( Object )
		"""

		dict.__delitem__(self, attribute)
		object.__delattr__(self, attribute)

	__delitem__ = __delattr__

	# @core.executionTrace
	def update(self, *args, **kwargs):
		"""
		This method reimplements the :meth:`Dict.update` method.
		
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		dict.update(self, *args, **kwargs)
		self.__dict__.update(*args, **kwargs)

class OrderedStructure(OrderedDict):
	"""
	| This class creates an object similar to C/C++ structured type.
	| Contrary to the :class:`Structure` since this class inherits from :class:`collections.OrderedDict`,
		its content is ordered.

	Usage:

		>>> people = OrderedStructure([("personA", "John"), ("personB", "Jane"), ("personC", "Luke")])
		>>> people
		OrderedStructure([('personA', 'John'), ('personB', 'Jane'), ('personC', 'Luke')])
		>>> people.keys()
		['personA', 'personB', 'personC']
		>>> people.personA
		'John'
		>>> del(people["personA"])
		>>> people["personA"]
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		KeyError: 'personA'
		>>> people.personA
		Traceback (most recent call last):
		  File "<console>", line 1, in <module>
		AttributeError: 'OrderedStructure' object has no attribute 'personA'
		>>> people.personB = "Kate"
		>>> people["personB"]
		'Kate'
		>>> people.personB
		'Kate'
	"""

	@core.executionTrace
	def __init__(self, *args, **kwargs):
		"""
		This method initializes the class.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		OrderedDict.__init__(self, *args, **kwargs)

	# @core.executionTrace
	def __setitem__(self, key, value, *args, **kwargs):
		"""
		This method sets a key and sibling attribute with given value.

		:param key.: Key. ( Object )
		:param value.: Value. ( Object )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		OrderedDict.__setitem__(self, key, value, *args, **kwargs)
		OrderedDict.__setattr__(self, key, value)

	# @core.executionTrace
	def __delitem__(self, key, *args, **kwargs):
		"""
		This method deletes both key and sibling attribute.

		:param key.: Key. ( Object )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Key / Value pairs. ( Key / Value pairs )
		"""

		OrderedDict.__delitem__(self, key, *args, **kwargs)
		OrderedDict.__delattr__(self, key)

	# @core.executionTrace
	def __setattr__(self, attribute, value):
		"""
		This method sets both key and sibling attribute with given value.

		:param attribute.: Attribute. ( Object )
		:param value.: Value. ( Object )
		"""

		if hasattr(self, "_OrderedDict__root") and hasattr(self, "_OrderedDict__map"):
			if self._OrderedDict__root:
				OrderedDict.__setitem__(self, attribute, value)
		OrderedDict.__setattr__(self, attribute, value)

	# @core.executionTrace
	def __delattr__(self, attribute):
		"""
		This method deletes both key and sibling attribute.

		:param attribute.: Attribute. ( Object )
		"""

		if hasattr(self, "_OrderedDict__root") and hasattr(self, "_OrderedDict__map"):
			if self._OrderedDict__root:
				OrderedDict.__delitem__(self, attribute)
		OrderedDict.__delattr__(self, attribute)

class Lookup(dict):
	"""
	This class extend dict type to provide a lookup by value(s).

	Usage:

		>>> person = Lookup(firstName="Doe", lastName="John", gender="male")
		>>> person.getFirstKeyFromValue("Doe")
		'firstName'
		>>> persons = foundations.foundations.dataStructures.Lookup(John="Doe", Jane="Doe", Luke="Skywalker")
		>>> persons.getKeysFromValue("Doe")
		['Jane', 'John']
	"""

	# @core.executionTrace
	def getFirstKeyFromValue(self, value):
		"""
		This method gets the first key from given value.

		:param value.: Value. ( Object )
		:return: Key. ( Object )
		"""

		for key, data in self.iteritems():
			if data == value:
				return key

	# @core.executionTrace
	def getKeysFromValue(self, value):
		"""
		This method gets the keys from given value.

		:param value.: Value. ( Object )
		:return: Keys. ( Object )
		"""

		return [key for key, data in self.iteritems() if data == value]
