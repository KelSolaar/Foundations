#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**dataStructures.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package data structures objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

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

__all__ = ["LOGGER",
			"NestedAttribute",
			"Structure",
			"OrderedStructure",
			"Lookup"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class NestedAttribute(object):
	"""
	Defines an helper object providing methods to manipulate nested attributes.
	
	Usage:
		
		>>> nest = NestedAttribute()
		>>> nest.my.nested.attribute = "Value"
		>>> nest.my.nested.attribute
		Value
		>>> nest.another.very.deeply.nested.attribute = 64
		>>> nest.another.very.deeply.nested.attribute
		64
	"""

	def __getattr__(self, attribute):
		"""
		Returns requested attribute.
	
		:param attribute: Attribute name.
		:type attribute: unicode
		:return: Attribute.
		:rtype: object
		"""

		self.__dict__[attribute] = NestedAttribute()
		return self.__dict__[attribute]

	def __setattr__(self, attribute, value):
		"""
		Sets given attribute with given value.
	
		:param attribute: Attribute name.
		:type attribute: unicode
		:param name: Attribute value.
		:type name: object
		"""

		namespaces = attribute.split(".")
		object.__setattr__(reduce(object.__getattribute__, namespaces[:-1], self), namespaces[-1], value)

	def __delattr__(self, attribute):
		"""
		Deletes given attribute with.
	
		:param attribute: Attribute name.
		:type attribute: unicode
		"""

		namespaces = attribute.split(".")
		object.__delattr__(reduce(object.__getattribute__, namespaces[:-1], self), namespaces[-1])

class Structure(dict):
	"""
	Defines an object similar to C/C++ structured type.
	
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

	def __init__(self, *args, **kwargs):
		"""
		Initializes the class.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Key / Value pairs.
		:type \*\*kwargs: dict
		"""

		dict.__init__(self, **kwargs)
		self.__dict__.update(**kwargs)

	def __getattr__(self, attribute):
		"""
		Returns given attribute value.

		:return: Attribute value.
		:rtype: object
		"""

		try:
			return dict.__getitem__(self, attribute)
		except KeyError:
			raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, attribute))

	def __setattr__(self, attribute, value):
		"""
		Sets both key and sibling attribute with given value.

		:param attribute: Attribute.
		:type attribute: object
		:param value: Value.
		:type value: object
		"""

		dict.__setitem__(self, attribute, value)
		object.__setattr__(self, attribute, value)

	__setitem__ = __setattr__

	def __delattr__(self, attribute):
		"""
		Deletes both key and sibling attribute.

		:param attribute: Attribute.
		:type attribute: object
		"""

		dict.__delitem__(self, attribute)
		object.__delattr__(self, attribute)

	__delitem__ = __delattr__

	def update(self, *args, **kwargs):
		"""
		Reimplements the :meth:`Dict.update` method.
		
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		dict.update(self, *args, **kwargs)
		self.__dict__.update(*args, **kwargs)

class OrderedStructure(OrderedDict):
	"""
	| Defines an object similar to C/C++ structured type.
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

	def __init__(self, *args, **kwargs):
		"""
		Initializes the class.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Key / Value pairs.
		:type \*\*kwargs: dict
		"""

		OrderedDict.__init__(self, *args, **kwargs)

	def __setitem__(self, key, value, *args, **kwargs):
		"""
		Sets a key and sibling attribute with given value.

		:param key: Key.
		:type key: object
		:param value: Value.
		:type value: object
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Key / Value pairs.
		:type \*\*kwargs: dict
		"""

		OrderedDict.__setitem__(self, key, value, *args, **kwargs)
		OrderedDict.__setattr__(self, key, value)

	def __delitem__(self, key, *args, **kwargs):
		"""
		Deletes both key and sibling attribute.

		:param key: Key.
		:type key: object
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Key / Value pairs.
		:type \*\*kwargs: dict
		"""

		OrderedDict.__delitem__(self, key, *args, **kwargs)
		OrderedDict.__delattr__(self, key)

	def __setattr__(self, attribute, value):
		"""
		Sets both key and sibling attribute with given value.

		:param attribute: Attribute.
		:type attribute: object
		:param value: Value.
		:type value: object
		"""

		if sys.version_info[:2] <= (2, 6):
			if not attribute in ("_OrderedDict__map", "_OrderedDict__end"):
				OrderedDict.__setitem__(self, attribute, value)
		else:
			if hasattr(self, "_OrderedDict__root") and hasattr(self, "_OrderedDict__map"):
				if self._OrderedDict__root:
					OrderedDict.__setitem__(self, attribute, value)
		OrderedDict.__setattr__(self, attribute, value)

	def __delattr__(self, attribute):
		"""
		Deletes both key and sibling attribute.

		:param attribute: Attribute.
		:type attribute: object
		"""

		if sys.version_info[:2] <= (2, 6):
			if not attribute in ("_OrderedDict__map", "_OrderedDict__end"):
				OrderedDict.__delitem__(self, attribute)
		else:
			if hasattr(self, "_OrderedDict__root") and hasattr(self, "_OrderedDict__map"):
				if self._OrderedDict__root:
					OrderedDict.__delitem__(self, attribute)
		OrderedDict.__delattr__(self, attribute)

class Lookup(dict):
	"""
	Extends dict type to provide a lookup by value(s).

	Usage:

		>>> person = Lookup(firstName="Doe", lastName="John", gender="male")
		>>> person.getFirstKeyFromValue("Doe")
		'firstName'
		>>> persons = foundations.dataStructures.Lookup(John="Doe", Jane="Doe", Luke="Skywalker")
		>>> persons.getKeysFromValue("Doe")
		['Jane', 'John']
	"""

	def getFirstKeyFromValue(self, value):
		"""
		Gets the first key from given value.

		:param value: Value.
		:type value: object
		:return: Key.
		:rtype: object
		"""

		for key, data in self.iteritems():
			if data == value:
				return key

	def getKeysFromValue(self, value):
		"""
		Gets the keys from given value.

		:param value: Value.
		:type value: object
		:return: Keys.
		:rtype: object
		"""

		return [key for key, data in self.iteritems() if data == value]
