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
import inspect
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.trace
import foundations.tests.testsFoundations.resources.dummy
from foundations.tests.testsFoundations.resources.dummy import Dummy
from foundations.tests.testsFoundations.resources.dummy import dummy1
from foundations.tests.testsFoundations.resources.dummy import dummy2

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["SetTracerHookTestCase",
		"GetTracerHookTestCase",
		"IsTracedTestCase",
		"IsUntracableTestCase",
		"SetTracedTestCase",
		"SetUntracedTestCase",
		"GetObjectNameTestCase",
		"GetMethodNameTestCase",
		"IsStaticMethodTestCase",
		"IsClassMethodTestCase",
		"TracerTestCase",
		"UntracerTestCase",
		"UntracableTestCase",
		"TraceMethodTestCase",
		"UntraceMethodTestCase",
		"TraceClassTestCase",
		"UntraceClassTestCase",
		"TraceModuleTestCase",
		"UntraceModuleTestCase"]

TRACABLE_METHODS = {"_Dummy__privateMethod" : Dummy._Dummy__privateMethod,
					"publicMethod" : Dummy.publicMethod,
					"staticMethod" : Dummy.staticMethod,
					"clsMethod" : Dummy.clsMethod}
UNTRACABLE_METHODS = {"__str__" : Dummy.__str__,
					"__repr__" : Dummy.__repr__,
					"untracedPublic" : Dummy.untracedPublic}

TRACABLE_DEFINITIONS = {"dummy1" : dummy1}
UNTRACABLE_DEFINITIONS = {"dummy2" : dummy2}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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

		self.assertEqual(foundations.trace.getMethodName(Dummy.publicMethod), "publicMethod")
		self.assertEqual(foundations.trace.getMethodName(Dummy._Dummy__privateMethod), "_Dummy__privateMethod")

class IsStaticMethodTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.isStaticMethod` class units tests methods.
	"""

	def testIsStaticMethod(self):
		"""
		This method tests :func:`foundations.trace.isStaticMethod` definition.
		"""

		self.assertTrue(foundations.trace.isStaticMethod(Dummy.staticMethod))
		self.assertFalse(foundations.trace.isStaticMethod(Dummy.publicMethod))

class IsClassMethodTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.isClassMethod` class units tests methods.
	"""

	def testIsClassMethod(self):
		"""
		This method tests :func:`foundations.trace.isClassMethod` definition.
		"""

		for key, value in {Dummy.clsMethod : True, Dummy.publicMethod : False, Dummy.staticMethod : False}.iteritems():
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

class TracerTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.tracer` class units tests methods.
	"""

	def testTracer(self):
		"""
		This method tests :func:`foundations.trace.tracer` definition.
		"""

		object = foundations.trace.tracer(dummy1)
		self.assertTrue(foundations.trace.isTraced(object))
		self.assertEqual(object(), foundations.tests.testsFoundations.resources.dummy.GLOBAL_RETURN_VALUE)

class UntracerTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.untracer` class units tests methods.
	"""

	def testUntracer(self):
		"""
		This method tests :func:`foundations.trace.untracer` definition.
		"""

		object = foundations.trace.tracer(dummy1)
		self.assertEqual(foundations.trace.untracer(object), dummy1)
		self.assertEqual(foundations.trace.untracer(dummy1), dummy1)

class UntracableTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.untracable` class units tests methods.
	"""

	def testUntracable(self):
		"""
		This method tests :func:`foundations.trace.untracable` definition.
		"""

		object = foundations.trace.untracable(dummy2)
		self.assertTrue(foundations.trace.isUntracable(object))
		self.assertEqual(object(), dummy2())

		object = foundations.trace.tracer(object)
		self.assertFalse(foundations.trace.isTraced(object))
		self.assertEqual(object(), dummy2())

class TraceMethodTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.traceMethod` class units tests methods.
	"""

	def testTraceMethod(self):
		"""
		This method tests :func:`foundations.trace.traceMethod` definition.
		"""

		for name, method in TRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.isTraced(method))
			self.assertTrue(foundations.trace.traceMethod(Dummy, method))
			self.assertTrue(foundations.trace.isTraced(getattr(Dummy, name)))
			foundations.trace.untraceMethod(Dummy, getattr(Dummy, name))

		for name, method in UNTRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.isTraced(method))
			self.assertFalse(foundations.trace.traceMethod(Dummy, getattr(Dummy, name)))
			self.assertFalse(foundations.trace.isTraced(getattr(Dummy, name)))

class UntraceMethodTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.untraceMethod` class units tests methods.
	"""

	def testUntraceMethod(self):
		"""
		This method tests :func:`foundations.trace.untraceMethod` definition.
		"""

		for name, method in TRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.isTraced(method))
			foundations.trace.traceMethod(Dummy, method)
			self.assertTrue(foundations.trace.untraceMethod(Dummy, getattr(Dummy, name)))
			self.assertFalse(foundations.trace.isTraced(getattr(Dummy, name)))
			self.assertEqual(method, getattr(Dummy, name))

		for name, method in UNTRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.isTraced(method))
			foundations.trace.traceMethod(Dummy, method)
			self.assertFalse(foundations.trace.untraceMethod(Dummy, getattr(Dummy, name)))
			self.assertFalse(foundations.trace.isTraced(getattr(Dummy, name)))
			self.assertEqual(method, getattr(Dummy, name))

class TraceClassTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.traceClass` class units tests methods.
	"""

	def testTraceClass(self):
		"""
		This method tests :func:`foundations.trace.traceClass` definition.
		"""

		self.assertFalse(foundations.trace.isTraced(Dummy))
		self.assertTrue(foundations.trace.traceClass(Dummy))
		self.assertTrue(foundations.trace.isTraced(Dummy))

		for method in TRACABLE_METHODS.iterkeys():
			self.assertTrue(foundations.trace.isTraced(getattr(Dummy, method)))

		for method in UNTRACABLE_METHODS.iterkeys():
			self.assertFalse(foundations.trace.isTraced(getattr(Dummy, method)))

		for name, accessor in inspect.getmembers(Dummy, lambda x: type(x) is property):
			self.assertTrue(foundations.trace.isTraced(accessor.fget))
			self.assertTrue(foundations.trace.isTraced(accessor.fset))
			self.assertTrue(foundations.trace.isTraced(accessor.fdel))

		foundations.trace.untraceClass(Dummy)

class UntraceClassTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.untraceClass` class units tests methods.
	"""

	def testUntraceClass(self):
		"""
		This method tests :func:`foundations.trace.untraceClass` definition.
		"""

		foundations.trace.traceClass(Dummy)
		self.assertTrue(foundations.trace.untraceClass(Dummy))
		self.assertFalse(foundations.trace.isTraced(Dummy))

		for name, method in TRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.isTraced(method))
			self.assertEqual(method, getattr(Dummy, name))

		for name, method in UNTRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.isTraced(method))
			self.assertEqual(method, getattr(Dummy, name))

		for name, accessor in inspect.getmembers(Dummy, lambda x: type(x) is property):
			self.assertFalse(foundations.trace.isTraced(accessor.fget))
			self.assertFalse(foundations.trace.isTraced(accessor.fset))
			self.assertFalse(foundations.trace.isTraced(accessor.fdel))

class TraceModuleTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.traceModule` class units tests methods.
	"""

	def testTraceModule(self):
		"""
		This method tests :func:`foundations.trace.traceModule` definition.
		"""

		module = foundations.tests.testsFoundations.resources.dummy
		self.assertTrue(foundations.trace.traceModule(module))
		self.assertTrue(foundations.trace.isTraced(module))

		for name, definition in TRACABLE_DEFINITIONS.iteritems():
			self.assertTrue(foundations.trace.isTraced(getattr(module, name)))

		for name, definition in UNTRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.isTraced(getattr(module, name)))

		self.assertIn(module, foundations.trace.REGISTERED_MODULES)

		foundations.trace.untraceModule(module)

class UntraceModuleTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.untraceModule` class units tests methods.
	"""

	def testUntraceModule(self):
		"""
		This method tests :func:`foundations.trace.untraceModule` definition.
		"""

		module = foundations.tests.testsFoundations.resources.dummy
		foundations.trace.traceModule(module)
		self.assertTrue(foundations.trace.untraceModule(module))

		for name, definition in TRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.isTraced(getattr(module, name)))
			self.assertEqual(definition, getattr(module, name))

		for name, definition in UNTRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.isTraced(getattr(module, name)))
			self.assertEqual(definition, getattr(module, name))

class RegisterModuleTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.trace.registerModule` class units tests methods.
	"""

	def testRegisterModule(self):
		"""
		This method tests :func:`foundations.trace.registerModule` definition.
		"""

		registeredModules = foundations.trace.REGISTERED_MODULES
		foundations.trace.REGISTERED_MODULES = set()

		module = foundations.tests.testsFoundations.resources.dummy
		self.assertTrue(foundations.trace.registerModule(module))
		self.assertIn(module, foundations.trace.REGISTERED_MODULES)

		self.assertTrue(foundations.trace.registerModule())
		self.assertIn(sys.modules[__name__], foundations.trace.REGISTERED_MODULES)

		foundations.trace.REGISTERED_MODULES = foundations.trace.REGISTERED_MODULES

if __name__ == "__main__":
	unittest.main()
