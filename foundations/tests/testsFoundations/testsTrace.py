#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsTrace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.trace` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.trace

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["GLOBAL_RETURN_VALUE",
		"Dummy",
		"dummy1",
		"dummy2",
		"SetTracerHookTestCase",
		"GetTracerHookTestCase",
		"IsTracedTestCase",
		"IsUntracableTestCase",
		"SetTracedTestCase",
		"SetUntracedTestCase",
		"GetObjectNameTestCase",
		"GetMethodNameTestCase",
		"IsClassMethodTestCase"]

GLOBAL_RETURN_VALUE = range(10)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Dummy(object):
	"""
	This class is a dummy class used to test :mod:`foundations.trace` module.
	"""

	def __init__(self):
		self.__attribute = GLOBAL_RETURN_VALUE

	@property
	def attribute(self):
		return self.__attribute

	@attribute.setter
	def attribute(self, value):
		self.__attribute = value

	@attribute.deleter
	def attribute(self):
		return

	def __str__(self):
		pass

	def __repr__(self):
		pass

	def __private(self):
		return self.__private.__name__

	def public(self):
		return self.public.__name__

	@foundations.trace.untracable
	def untracedPublic(self):
		return self.untracedPublic.__name__

	@staticmethod
	def static():
		return Dummy.static.__name__

	@classmethod
	def clsmethod(cls):
		return cls.clsmethod.__name__

def dummy1():
	return GLOBAL_RETURN_VALUE

def dummy2():
	return GLOBAL_RETURN_VALUE

class SetTracerHookTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.setTracerHook` class units tests methods.
	"""

	def testSetTracerHook(self):
		"""
		This method tests :func:`foundations.trace.setTracerHook` definition.
		"""

		object, hook = lambda: None, str()
		self.assertTrue(foundations.trace.setTracerHook(object, hook))
		self.assertTrue(hasattr(object, foundations.trace.TRACER_HOOK))

class GetTracerHookTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.getTracerHook` class units tests methods.
	"""

	def testGetTracerHook(self):
		"""
		This method tests :func:`foundations.trace.getTracerHook` definition.
		"""

		object, hook = lambda: None, str()
		foundations.trace.setTracerHook(object, hook),
		self.assertEqual(foundations.trace.getTracerHook(object), hook)

class IsTracedTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.isTraced` class units tests methods.
	"""

	def testIsTraced(self):
		"""
		This method tests :func:`foundations.trace.isTraced` definition.
		"""

		object = lambda: None
		foundations.trace.setTraced(object)
		self.assertTrue(foundations.trace.isTraced(object))
		self.assertFalse(foundations.trace.isTraced(lambda: None))

class IsUntracableTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.isUntracable` class units tests methods.
	"""

	def testIsUntracable(self):
		"""
		This method tests :func:`foundations.trace.isUntracable` definition.
		"""

		object = foundations.trace.untracable(lambda: None)
		self.assertTrue(foundations.trace.isUntracable(object))
		self.assertFalse(foundations.trace.isUntracable(lambda: None))

class SetTracedTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.setTraced` class units tests methods.
	"""

	def testSetTraced(self):
		"""
		This method tests :func:`foundations.trace.setTraced` definition.
		"""

		object = lambda: None
		self.assertTrue(foundations.trace.setTraced(object))
		self.assertTrue(hasattr(object, foundations.trace.TRACER_SYMBOL))

class SetUntracedTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.setUntraced` class units tests methods.
	"""

	def testSetTraced(self):
		"""
		This method tests :func:`foundations.trace.setUntraced` definition.
		"""

		object = lambda: None
		foundations.trace.setTraced(object)
		self.assertTrue(foundations.trace.setUntraced(object))
		self.assertFalse(hasattr(object, foundations.trace.TRACER_SYMBOL))

class SetUntracableTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.setUntracable` class units tests methods.
	"""

	def testSetUntracable(self):
		"""
		This method tests :func:`foundations.trace.setUntracable` definition.
		"""

		object = foundations.trace.untracable(lambda: None)
		self.assertTrue(hasattr(object, foundations.trace.UNTRACABLE_SYMBOL))

class GetObjectNameTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.getObjectName` class units tests methods.
	"""

	def testGetObjectName(self):
		"""
		This method tests :func:`foundations.trace.getObjectName` definition.
		"""

		self.assertEqual(foundations.trace.getObjectName(foundations.trace.getObjectName),
						foundations.trace.getObjectName.__name__)

class GetMethodNameTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.getMethodName` class units tests methods.
	"""

	def testGetMethodName(self):
		"""
		This method tests :func:`foundations.trace.getMethodName` definition.
		"""

		self.assertEqual(foundations.trace.getMethodName(Dummy.public), "public")
		self.assertEqual(foundations.trace.getMethodName(Dummy._Dummy__private), "_Dummy__private")

class IsClassMethodTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.isClassMethod` class units tests methods.
	"""

	def testIsClassMethod(self):
		"""
		This method tests :func:`foundations.trace.isClassMethod` definition.
		"""

		for key, value in {Dummy.clsmethod : True, Dummy.public : False, Dummy.static : False}.iteritems():
			self.assertEqual(foundations.trace.isClassMethod(key), value)

class FormatArgumentTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.formatArgument` class units tests methods.
	"""

	def testFormatArgument(self):
		"""
		This method tests :func:`foundations.trace.formatArgument` definition.
		"""

		self.assertEqual(foundations.trace.formatArgument(("x", range(3))), "x=[0, 1, 2]")

class TracerCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.tracer` class units tests methods.
	"""

	def testTracer(self):
		"""
		This method tests :func:`foundations.trace.tracer` definition.
		"""

		traced = foundations.trace.tracer(dummy)
		self.assertTrue(hasattr(traced, "_trace__hook__"))
		self.assertEqual(traced(), GLOBAL_RETURN_VALUE)

class TracerCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.tracer` class units tests methods.
	"""

	def testTracer(self):
		"""
		This method tests :func:`foundations.trace.tracer` definition.
		"""

		tracedFunction = foundations.trace.tracer(dummy1)
		self.assertTrue(hasattr(tracedFunction, "_trace__tracer__"))
		self.assertEqual(tracedFunction(), dummy1())

class untracableCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.untracable` class units tests methods.
	"""

	def testUntracer(self):
		"""
		This method tests :func:`foundations.trace.untracable` definition.
		"""

		untracedFunction = foundations.trace.untracable(dummy2)
		self.assertTrue(hasattr(untracedFunction, "_trace__untracable__"))
		self.assertEqual(untracedFunction(), dummy2())

		untracedFunction = foundations.trace.tracer(untracedFunction)
		self.assertFalse(hasattr(untracedFunction, "_trace__tracer__"))
		self.assertEqual(untracedFunction(), dummy2())

if __name__ == "__main__":
	unittest.main()
