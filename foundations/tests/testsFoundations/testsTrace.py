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
from foundations.tests.testsFoundations.resources.dummy import dummy3

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["IsReadOnly",
		"SetTracerHookTestCase",
		"GetTracerHookTestCase",
		"IsTracedTestCase",
		"IsBaseTracedTestCase",
		"IsUntracableTestCase",
		"SetTracedTestCase",
		"SetUntracedTestCase",
		"TraceWalkerTestCase"
		"GetObjectNameTestCase",
		"GetTraceNameTestCase",
		"GetMethodNameTestCase",
		"IsStaticMethodTestCase",
		"IsClassMethodTestCase",
		"ValidateTracerTestCase"
		"TracerTestCase",
		"UntracerTestCase",
		"UntracableTestCase",
		"TraceFunctionTestCase",
		"UntraceFunctionTestCase",
		"TraceMethodTestCase",
		"UntraceMethodTestCase",
		"TracePropertyTestCase",
		"UntracePropertyTestCase",
		"TraceClassTestCase",
		"UntraceClassTestCase",
		"TraceModuleTestCase",
		"UntraceModuleTestCase",
		"RegisterModuleTestCase",
		"InstallTracerTestCase",
		"UninstallTracerTestCase",
		"EvaluateTraceRequestTestCase"]

TRACABLE_METHODS = {"_Dummy__privateMethod" : Dummy._Dummy__privateMethod,
					"publicMethod" : Dummy.publicMethod,
					"staticMethod" : Dummy.staticMethod,
					"clsMethod" : Dummy.clsMethod}
UNTRACABLE_METHODS = {"__str__" : Dummy.__str__,
					"__repr__" : Dummy.__repr__,
					"untracedPublic" : Dummy.untracedPublic}

TRACABLE_DEFINITIONS = {"dummy1" : dummy1,
						"dummy3" : dummy3}
UNTRACABLE_DEFINITIONS = {"dummy2" : dummy2}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class IsReadOnlyTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.isReadOnly` definition units tests methods.
	"""

	def testIsReadOnly(self):
		"""
		This method tests :func:`foundations.trace.isReadOnly` definition.
		"""

		self.assertTrue(foundations.trace.isReadOnly(str))
		self.assertTrue(foundations.trace.isReadOnly(str()))
		self.assertTrue(foundations.trace.isReadOnly(dict))
		self.assertTrue(foundations.trace.isReadOnly(dict()))

		class Writable(object):
			pass

		self.assertFalse(foundations.trace.isReadOnly(Writable))
		self.assertFalse(foundations.trace.isReadOnly(Writable()))

class SetTracerHookTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.setTracerHook` definition units tests methods.
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
	This class defines :func:`foundations.trace.getTracerHook` definition units tests methods.
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
	This class defines :func:`foundations.trace.isTraced` definition units tests methods.
	"""

	def testIsTraced(self):
		"""
		This method tests :func:`foundations.trace.isTraced` definition.
		"""

		object = lambda: None
		foundations.trace.setTraced(object)
		self.assertTrue(foundations.trace.isTraced(object))
		self.assertFalse(foundations.trace.isTraced(lambda: None))

class IsBaseTracedTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.isBaseTraced` definition units tests methods.
	"""

	def testIsBaseTraced(self):
		"""
		This method tests :func:`foundations.trace.isBaseTraced` definition.
		"""

		class Dummy2(Dummy):
			pass

		self.assertFalse(foundations.trace.isBaseTraced(Dummy2))

		foundations.trace.traceClass(Dummy)

		self.assertTrue(foundations.trace.isBaseTraced(Dummy2))

		foundations.trace.untraceClass(Dummy)

class IsUntracableTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.isUntracable` definition units tests methods.
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
	This class defines :func:`foundations.trace.setTraced` definition units tests methods.
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
	This class defines :func:`foundations.trace.setUntraced` definition units tests methods.
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
	This class defines :func:`foundations.trace.setUntracable` definition units tests methods.
	"""

	def testSetUntracable(self):
		"""
		This method tests :func:`foundations.trace.setUntracable` definition.
		"""

		object = foundations.trace.untracable(lambda: None)
		self.assertTrue(hasattr(object, foundations.trace.UNTRACABLE_SYMBOL))

class TraceWalkerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.traceWalker` definition units tests methods.
	"""

	def testTraceWalker(self):
		"""
		This method tests :func:`foundations.trace.traceWalker` definition.
		"""

		module = foundations.tests.testsFoundations.resources.dummy
		members = list(foundations.trace.traceWalker(module))

		for method in TRACABLE_METHODS.itervalues():
			self.assertIn((Dummy, method), members)

		for method in UNTRACABLE_METHODS.itervalues():
			self.assertIn((Dummy, method), members)

		for definition in TRACABLE_DEFINITIONS.itervalues():
			self.assertIn((None, definition), members)

		for definition in UNTRACABLE_DEFINITIONS.itervalues():
			self.assertIn((None, definition), members)

		for accessor in (Dummy.attribute.fget, Dummy.attribute.fset, Dummy.attribute.fdel):
			self.assertIn((Dummy, accessor), members)

class GetObjectNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.getObjectName` definition units tests methods.
	"""

	def testGetObjectName(self):
		"""
		This method tests :func:`foundations.trace.getObjectName` definition.
		"""

		self.assertEqual(foundations.trace.getObjectName(Dummy.attribute), "attribute")
		self.assertEqual(foundations.trace.getObjectName(foundations.trace.getObjectName),
						foundations.trace.getObjectName.__name__)
		self.assertEqual(foundations.trace.getObjectName(Dummy), "Dummy")
		self.assertEqual(foundations.trace.getObjectName(Dummy()), "Dummy")

class GetTraceNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.getTraceName` definition units tests methods.
	"""

	def testGetTraceName(self):
		"""
		This method tests :func:`foundations.trace.getTraceName` definition.
		"""

		self.assertEqual(foundations.trace.getTraceName(dummy1),
						"foundations.tests.testsFoundations.resources.dummy.dummy1")
		self.assertEqual(foundations.trace.getTraceName(Dummy.publicMethod),
						"foundations.tests.testsFoundations.resources.dummy.Dummy.publicMethod")
		self.assertEqual(foundations.trace.getTraceName(Dummy._Dummy__privateMethod),
						"foundations.tests.testsFoundations.resources.dummy.Dummy.__privateMethod")
		self.assertEqual(foundations.trace.getTraceName(Dummy.attribute),
						"foundations.tests.testsFoundations.resources.dummy.Dummy.attribute")

class GetMethodNameTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.getMethodName` definition units tests methods.
	"""

	def testGetMethodName(self):
		"""
		This method tests :func:`foundations.trace.getMethodName` definition.
		"""

		self.assertEqual(foundations.trace.getMethodName(Dummy.publicMethod), "publicMethod")
		self.assertEqual(foundations.trace.getMethodName(Dummy._Dummy__privateMethod), "_Dummy__privateMethod")

class IsStaticMethodTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.isStaticMethod` definition units tests methods.
	"""

	def testIsStaticMethod(self):
		"""
		This method tests :func:`foundations.trace.isStaticMethod` definition.
		"""

		self.assertTrue(foundations.trace.isStaticMethod(Dummy.staticMethod))
		self.assertFalse(foundations.trace.isStaticMethod(Dummy.publicMethod))

class IsClassMethodTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.isClassMethod` definition units tests methods.
	"""

	def testIsClassMethod(self):
		"""
		This method tests :func:`foundations.trace.isClassMethod` definition.
		"""

		for key, value in {Dummy.clsMethod : True, Dummy.publicMethod : False, Dummy.staticMethod : False}.iteritems():
			self.assertEqual(foundations.trace.isClassMethod(key), value)

class FormatArgumentTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.formatArgument` definition units tests methods.
	"""

	def testFormatArgument(self):
		"""
		This method tests :func:`foundations.trace.formatArgument` definition.
		"""

		self.assertEqual(foundations.trace.formatArgument(("x", range(3))), "x=[0, 1, 2]")

class ValidateTracerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.validateTracer` definition units tests methods.
	"""

	def testValidateTracer(self):
		"""
		This method tests :func:`foundations.trace.validateTracer` definition.
		"""

		wrapped = foundations.trace.validateTracer(dummy1, lambda x: x)
		self.assertTrue(hasattr(wrapped, foundations.trace.TRACER_HOOK))
		self.assertTrue(foundations.trace.isTraced(wrapped))

		wrapped = foundations.trace.validateTracer(dummy2, lambda x: x)
		self.assertFalse(hasattr(wrapped, foundations.trace.TRACER_HOOK))
		self.assertFalse(foundations.trace.isTraced(wrapped))
		self.assertEqual(wrapped, dummy2)

class TracerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.tracer` definition units tests methods.
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
	This class defines :func:`foundations.trace.untracer` definition units tests methods.
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
	This class defines :func:`foundations.trace.untracable` definition units tests methods.
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

class TraceFunctionTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.traceFunction` definition units tests functions.
	"""

	def testTraceFunction(self):
		"""
		This function tests :func:`foundations.trace.traceFunction` definition.
		"""

		module = foundations.tests.testsFoundations.resources.dummy
		for name, function in TRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.isTraced(function))
			self.assertTrue(foundations.trace.traceFunction(module, function))
			self.assertTrue(foundations.trace.isTraced(getattr(module, name)))
			foundations.trace.untraceFunction(module, getattr(module, name))

class UntraceFunctionTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.untraceFunction` definition units tests functions.
	"""

	def testUntraceFunction(self):
		"""
		This function tests :func:`foundations.trace.untraceFunction` definition.
		"""

		module = foundations.tests.testsFoundations.resources.dummy
		for name, function in TRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.isTraced(function))
			foundations.trace.traceFunction(module, function)
			self.assertTrue(foundations.trace.untraceFunction(module, getattr(module, name)))
			self.assertFalse(foundations.trace.isTraced(getattr(module, name)))
			self.assertEqual(function, getattr(module, name))

class TraceMethodTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.traceMethod` definition units tests methods.
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
	This class defines :func:`foundations.trace.untraceMethod` definition methods.
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
class TracePropertyTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.traceProperty` definition units tests propertys.
	"""

	def testTraceProperty(self):
		"""
		This property tests :func:`foundations.trace.traceProperty` definition.
		"""

		name, accessor = Dummy.attribute.fget.__name__, Dummy.attribute
		self.assertFalse(foundations.trace.isTraced(accessor))
		self.assertTrue(foundations.trace.traceProperty(Dummy, accessor))
		foundations.trace.untraceProperty(Dummy, getattr(Dummy, name))

class UntracePropertyTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.untraceProperty` definition units tests propertys.
	"""

	def testUntraceProperty(self):
		"""
		This property tests :func:`foundations.trace.untraceProperty` definition.
		"""

		name, accessor = Dummy.attribute.fget.__name__, Dummy.attribute
		fget, fset, fdel = accessor.fget, accessor.fset, accessor.fdel
		self.assertFalse(foundations.trace.isTraced(accessor))
		foundations.trace.traceProperty(Dummy, accessor)
		self.assertTrue(foundations.trace.untraceProperty(Dummy, getattr(Dummy, name)))
		self.assertEqual(getattr(Dummy, name).fget, fget)
		self.assertEqual(getattr(Dummy, name).fset, fset)
		self.assertEqual(getattr(Dummy, name).fdel, fdel)

class TraceClassTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.traceClass` definition units tests methods.
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

		self.assertTrue(foundations.trace.traceClass(Dummy, pattern=r"^publicMethod$"))
		self.assertTrue(foundations.trace.isTraced(getattr(Dummy, "publicMethod")))
		self.assertFalse(foundations.trace.isTraced(getattr(Dummy, "clsMethod")))

		foundations.trace.untraceClass(Dummy)

		self.assertTrue(foundations.trace.traceClass(Dummy, pattern=r"^(?:(?!publicMethod).)*$"))
		self.assertFalse(foundations.trace.isTraced(getattr(Dummy, "publicMethod")))
		self.assertTrue(foundations.trace.isTraced(getattr(Dummy, "clsMethod")))

		foundations.trace.untraceClass(Dummy)

class UntraceClassTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.untraceClass` definition units tests methods.
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
	This class defines :func:`foundations.trace.traceModule` definition units tests methods.
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

		self.assertTrue(foundations.trace.traceModule(module, pattern=r"^dummy1$"))
		self.assertTrue(foundations.trace.isTraced(getattr(module, dummy1.__name__)))
		self.assertFalse(foundations.trace.isTraced(getattr(module, dummy2.__name__)))

		foundations.trace.untraceModule(module)

		self.assertTrue(foundations.trace.traceModule(module, pattern=r"^(?:(?!dummy1).)*$"))
		self.assertFalse(foundations.trace.isTraced(getattr(module, dummy1.__name__)))
		self.assertTrue(foundations.trace.isTraced(getattr(module, dummy3.__name__)))

		foundations.trace.untraceModule(module)

class UntraceModuleTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.untraceModule` definition units tests methods.
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
	This class defines :func:`foundations.trace.registerModule` definition units tests methods.
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

class InstallTracerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.installTracer` definition units tests methods.
	"""

	def testInstallTracer(self):
		"""
		This method tests :func:`foundations.trace.installTracer` definition.
		"""

		registeredModules = foundations.trace.REGISTERED_MODULES
		foundations.trace.REGISTERED_MODULES = set()

		module = foundations.tests.testsFoundations.resources.dummy
		foundations.trace.registerModule(module)
		self.assertTrue(foundations.trace.installTracer(pattern=r"Nemo"))
		self.assertFalse(foundations.trace.isTraced(module))
		self.assertTrue(foundations.trace.installTracer(pattern=r"\w+ummy"))
		self.assertTrue(foundations.trace.isTraced(module))
		foundations.trace.uninstallTracer()

		foundations.trace.REGISTERED_MODULES = foundations.trace.REGISTERED_MODULES

class UninstallTracerTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.uninstallTracer` definition units tests methods.
	"""

	def testUninstallTracer(self):
		"""
		This method tests :func:`foundations.trace.uninstallTracer` definition.
		"""

		registeredModules = foundations.trace.REGISTERED_MODULES
		foundations.trace.REGISTERED_MODULES = set()

		module = foundations.tests.testsFoundations.resources.dummy
		foundations.trace.registerModule(module)
		foundations.trace.installTracer()
		self.assertTrue(foundations.trace.uninstallTracer(r"Nemo"))
		self.assertTrue(foundations.trace.isTraced(module))
		self.assertTrue(foundations.trace.uninstallTracer(r"\w+ummy"))
		self.assertFalse(foundations.trace.isTraced(module))

		foundations.trace.REGISTERED_MODULES = foundations.trace.REGISTERED_MODULES

class EvaluateTraceRequestTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.trace.evaluateTraceRequest` definition units tests methods.
	"""

	def testEvaluateTraceRequest(self):
		"""
		This method tests :func:`foundations.trace.evaluateTraceRequest` definition.
		"""

		module = foundations.tests.testsFoundations.resources.dummy

		self.assertTrue(foundations.trace.evaluateTraceRequest("'foundations.tests.testsFoundations.resources.dummy'"))
		self.assertTrue(foundations.trace.isTraced(module))

		foundations.trace.untraceModule(module)

		self.assertTrue(foundations.trace.evaluateTraceRequest("['foundations.tests.testsFoundations.resources.dummy']"))
		self.assertTrue(foundations.trace.isTraced(module))

		foundations.trace.untraceModule(module)

		self.assertTrue(foundations.trace.evaluateTraceRequest(
		"{'foundations.tests.testsFoundations.resources.dummy' : (r'.*', 0)}"))
		self.assertTrue(foundations.trace.isTraced(module))

		foundations.trace.untraceModule(module)

		self.assertTrue(foundations.trace.evaluateTraceRequest(
		"{'foundations.tests.testsFoundations.resources.dummy' : (r'^(?:(?!dummy1).)*$', 0)}"))
		self.assertTrue(foundations.trace.isTraced(module))
		self.assertFalse(foundations.trace.isTraced(getattr(module, "dummy1")))

		foundations.trace.untraceModule(module)

if __name__ == "__main__":
	unittest.main()
