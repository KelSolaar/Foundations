#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_trace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.trace` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
import foundations.tests.tests_foundations.resources.dummy
from foundations.tests.tests_foundations.resources.dummy import Dummy
from foundations.tests.tests_foundations.resources.dummy import dummy1
from foundations.tests.tests_foundations.resources.dummy import dummy2
from foundations.tests.tests_foundations.resources.dummy import dummy3

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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

TRACABLE_METHODS = {"_Dummy__private_method" : Dummy._Dummy__private_method,
					"public_method" : Dummy.public_method,
					"static_method" : Dummy.static_method,
					"class_method" : Dummy.class_method}
UNTRACABLE_METHODS = {"__str__" : Dummy.__str__,
					"__repr__" : Dummy.__repr__,
					"untraced_public" : Dummy.untraced_public}

TRACABLE_DEFINITIONS = {"dummy1" : dummy1,
						"dummy3" : dummy3}
UNTRACABLE_DEFINITIONS = {"dummy2" : dummy2}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class IsReadOnlyTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.is_read_only` definition units tests methods.
	"""

	def test_is_read_only(self):
		"""
		Tests :func:`foundations.trace.is_read_only` definition.
		"""

		self.assertTrue(foundations.trace.is_read_only(unicode))
		self.assertTrue(foundations.trace.is_read_only(""))
		self.assertTrue(foundations.trace.is_read_only(dict))
		self.assertTrue(foundations.trace.is_read_only(dict()))

		class Writable(object):
			pass

		self.assertFalse(foundations.trace.is_read_only(Writable))
		self.assertFalse(foundations.trace.is_read_only(Writable()))

class SetTracerHookTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.set_tracer_hook` definition units tests methods.
	"""

	def test_set_tracer_hook(self):
		"""
		Tests :func:`foundations.trace.set_tracer_hook` definition.
		"""

		object, hook = lambda: None, ""
		self.assertTrue(foundations.trace.set_tracer_hook(object, hook))
		self.assertTrue(hasattr(object, foundations.trace.TRACER_HOOK))

class GetTracerHookTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.get_tracer_hook` definition units tests methods.
	"""

	def test_get_tracer_hook(self):
		"""
		Tests :func:`foundations.trace.get_tracer_hook` definition.
		"""

		object, hook = lambda: None, ""
		foundations.trace.set_tracer_hook(object, hook),
		self.assertEqual(foundations.trace.get_tracer_hook(object), hook)

class IsTracedTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.is_traced` definition units tests methods.
	"""

	def test_is_traced(self):
		"""
		Tests :func:`foundations.trace.is_traced` definition.
		"""

		object = lambda: None
		foundations.trace.set_traced(object)
		self.assertTrue(foundations.trace.is_traced(object))
		self.assertFalse(foundations.trace.is_traced(lambda: None))

class IsBaseTracedTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.is_base_traced` definition units tests methods.
	"""

	def test_is_base_traced(self):
		"""
		Tests :func:`foundations.trace.is_base_traced` definition.
		"""

		class Dummy2(Dummy):
			pass

		self.assertFalse(foundations.trace.is_base_traced(Dummy2))

		foundations.trace.trace_class(Dummy)

		self.assertTrue(foundations.trace.is_base_traced(Dummy2))

		foundations.trace.untrace_class(Dummy)

class IsUntracableTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.is_untracable` definition units tests methods.
	"""

	def test_is_untracable(self):
		"""
		Tests :func:`foundations.trace.is_untracable` definition.
		"""

		object = foundations.trace.untracable(lambda: None)
		self.assertTrue(foundations.trace.is_untracable(object))
		self.assertFalse(foundations.trace.is_untracable(lambda: None))

class SetTracedTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.set_traced` definition units tests methods.
	"""

	def test_set_traced(self):
		"""
		Tests :func:`foundations.trace.set_traced` definition.
		"""

		object = lambda: None
		self.assertTrue(foundations.trace.set_traced(object))
		self.assertTrue(hasattr(object, foundations.trace.TRACER_SYMBOL))

class SetUntracedTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.set_untraced` definition units tests methods.
	"""

	def test_set_traced(self):
		"""
		Tests :func:`foundations.trace.set_untraced` definition.
		"""

		object = lambda: None
		foundations.trace.set_traced(object)
		self.assertTrue(foundations.trace.set_untraced(object))
		self.assertFalse(hasattr(object, foundations.trace.TRACER_SYMBOL))

class SetUntracableTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.set_untracable` definition units tests methods.
	"""

	def test_set_untracable(self):
		"""
		Tests :func:`foundations.trace.set_untracable` definition.
		"""

		object = foundations.trace.untracable(lambda: None)
		self.assertTrue(hasattr(object, foundations.trace.UNTRACABLE_SYMBOL))

class TraceWalkerTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.trace_walker` definition units tests methods.
	"""

	def test_trace_walker(self):
		"""
		Tests :func:`foundations.trace.trace_walker` definition.
		"""

		module = foundations.tests.tests_foundations.resources.dummy
		members = list(foundations.trace.trace_walker(module))

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
	Defines :func:`foundations.trace.get_object_name` definition units tests methods.
	"""

	def test_get_object_name(self):
		"""
		Tests :func:`foundations.trace.get_object_name` definition.
		"""

		self.assertEqual(foundations.trace.get_object_name(Dummy.attribute), "attribute")
		self.assertEqual(foundations.trace.get_object_name(foundations.trace.get_object_name),
						foundations.trace.get_object_name.__name__)
		self.assertEqual(foundations.trace.get_object_name(Dummy), "Dummy")
		self.assertEqual(foundations.trace.get_object_name(Dummy()), "Dummy")

class GetTraceNameTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.get_trace_name` definition units tests methods.
	"""

	def test_get_trace_name(self):
		"""
		Tests :func:`foundations.trace.get_trace_name` definition.
		"""

		self.assertEqual(foundations.trace.get_trace_name(dummy1),
						"foundations.tests.tests_foundations.resources.dummy.dummy1")
		self.assertEqual(foundations.trace.get_trace_name(Dummy.public_method),
						"foundations.tests.tests_foundations.resources.dummy.Dummy.public_method")
		self.assertEqual(foundations.trace.get_trace_name(Dummy._Dummy__private_method),
						"foundations.tests.tests_foundations.resources.dummy.Dummy.__private_method")
		self.assertEqual(foundations.trace.get_trace_name(Dummy.attribute),
						"foundations.tests.tests_foundations.resources.dummy.Dummy.attribute")

class GetMethodNameTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.get_method_name` definition units tests methods.
	"""

	def test_get_method_name(self):
		"""
		Tests :func:`foundations.trace.get_method_name` definition.
		"""

		self.assertEqual(foundations.trace.get_method_name(Dummy.public_method), "public_method")
		self.assertEqual(foundations.trace.get_method_name(Dummy._Dummy__private_method), "_Dummy__private_method")

class IsStaticMethodTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.is_static_method` definition units tests methods.
	"""

	def test_is_static_method(self):
		"""
		Tests :func:`foundations.trace.is_static_method` definition.
		"""

		self.assertTrue(foundations.trace.is_static_method(Dummy.static_method))
		self.assertFalse(foundations.trace.is_static_method(Dummy.public_method))

class IsClassMethodTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.is_class_method` definition units tests methods.
	"""

	def test_is_class_method(self):
		"""
		Tests :func:`foundations.trace.is_class_method` definition.
		"""

		for key, value in {Dummy.class_method : True, Dummy.public_method : False, Dummy.static_method : False}.iteritems():
			self.assertEqual(foundations.trace.is_class_method(key), value)

class FormatArgumentTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.format_argument` definition units tests methods.
	"""

	def test_format_argument(self):
		"""
		Tests :func:`foundations.trace.format_argument` definition.
		"""

		self.assertEqual(foundations.trace.format_argument(("x", range(3))), "x=[0, 1, 2]")

class ValidateTracerTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.validate_tracer` definition units tests methods.
	"""

	def test_validate_tracer(self):
		"""
		Tests :func:`foundations.trace.validate_tracer` definition.
		"""

		wrapped = foundations.trace.validate_tracer(dummy1, lambda x: x)
		self.assertTrue(hasattr(wrapped, foundations.trace.TRACER_HOOK))
		self.assertTrue(foundations.trace.is_traced(wrapped))

		wrapped = foundations.trace.validate_tracer(dummy2, lambda x: x)
		self.assertFalse(hasattr(wrapped, foundations.trace.TRACER_HOOK))
		self.assertFalse(foundations.trace.is_traced(wrapped))
		self.assertEqual(wrapped, dummy2)

class TracerTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.tracer` definition units tests methods.
	"""

	def test_tracer(self):
		"""
		Tests :func:`foundations.trace.tracer` definition.
		"""

		object = foundations.trace.tracer(dummy1)
		self.assertTrue(foundations.trace.is_traced(object))
		self.assertEqual(object(), foundations.tests.tests_foundations.resources.dummy.GLOBAL_RETURN_VALUE)

class UntracerTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.untracer` definition units tests methods.
	"""

	def test_untracer(self):
		"""
		Tests :func:`foundations.trace.untracer` definition.
		"""

		object = foundations.trace.tracer(dummy1)
		self.assertEqual(foundations.trace.untracer(object), dummy1)
		self.assertEqual(foundations.trace.untracer(dummy1), dummy1)

class UntracableTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.untracable` definition units tests methods.
	"""

	def test_untracable(self):
		"""
		Tests :func:`foundations.trace.untracable` definition.
		"""

		object = foundations.trace.untracable(dummy2)
		self.assertTrue(foundations.trace.is_untracable(object))
		self.assertEqual(object(), dummy2())

		object = foundations.trace.tracer(object)
		self.assertFalse(foundations.trace.is_traced(object))
		self.assertEqual(object(), dummy2())

class TraceFunctionTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.trace_function` definition units tests functions.
	"""

	def test_trace_function(self):
		"""
		This function tests :func:`foundations.trace.trace_function` definition.
		"""

		module = foundations.tests.tests_foundations.resources.dummy
		for name, function in TRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.is_traced(function))
			self.assertTrue(foundations.trace.trace_function(module, function))
			self.assertTrue(foundations.trace.is_traced(getattr(module, name)))
			foundations.trace.untrace_function(module, getattr(module, name))

class UntraceFunctionTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.untrace_function` definition units tests functions.
	"""

	def test_untrace_function(self):
		"""
		This function tests :func:`foundations.trace.untrace_function` definition.
		"""

		module = foundations.tests.tests_foundations.resources.dummy
		for name, function in TRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.is_traced(function))
			foundations.trace.trace_function(module, function)
			self.assertTrue(foundations.trace.untrace_function(module, getattr(module, name)))
			self.assertFalse(foundations.trace.is_traced(getattr(module, name)))
			self.assertEqual(function, getattr(module, name))

class TraceMethodTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.trace_method` definition units tests methods.
	"""

	def test_trace_method(self):
		"""
		Tests :func:`foundations.trace.trace_method` definition.
		"""

		for name, method in TRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.is_traced(method))
			self.assertTrue(foundations.trace.trace_method(Dummy, method))
			self.assertTrue(foundations.trace.is_traced(getattr(Dummy, name)))
			foundations.trace.untrace_method(Dummy, getattr(Dummy, name))

		for name, method in UNTRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.is_traced(method))
			self.assertFalse(foundations.trace.trace_method(Dummy, getattr(Dummy, name)))
			self.assertFalse(foundations.trace.is_traced(getattr(Dummy, name)))

class UntraceMethodTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.untrace_method` definition methods.
	"""

	def test_untrace_method(self):
		"""
		Tests :func:`foundations.trace.untrace_method` definition.
		"""

		for name, method in TRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.is_traced(method))
			foundations.trace.trace_method(Dummy, method)
			self.assertTrue(foundations.trace.untrace_method(Dummy, getattr(Dummy, name)))
			self.assertFalse(foundations.trace.is_traced(getattr(Dummy, name)))
			self.assertEqual(method, getattr(Dummy, name))

		for name, method in UNTRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.is_traced(method))
			foundations.trace.trace_method(Dummy, method)
			self.assertFalse(foundations.trace.untrace_method(Dummy, getattr(Dummy, name)))
			self.assertFalse(foundations.trace.is_traced(getattr(Dummy, name)))
			self.assertEqual(method, getattr(Dummy, name))
class TracePropertyTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.trace_property` definition units tests propertys.
	"""

	def test_trace_property(self):
		"""
		This property tests :func:`foundations.trace.trace_property` definition.
		"""

		name, accessor = Dummy.attribute.fget.__name__, Dummy.attribute
		self.assertFalse(foundations.trace.is_traced(accessor))
		self.assertTrue(foundations.trace.trace_property(Dummy, accessor))
		foundations.trace.untrace_property(Dummy, getattr(Dummy, name))

class UntracePropertyTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.untrace_property` definition units tests propertys.
	"""

	def test_untrace_property(self):
		"""
		This property tests :func:`foundations.trace.untrace_property` definition.
		"""

		name, accessor = Dummy.attribute.fget.__name__, Dummy.attribute
		fget, fset, fdel = accessor.fget, accessor.fset, accessor.fdel
		self.assertFalse(foundations.trace.is_traced(accessor))
		foundations.trace.trace_property(Dummy, accessor)
		self.assertTrue(foundations.trace.untrace_property(Dummy, getattr(Dummy, name)))
		self.assertEqual(getattr(Dummy, name).fget, fget)
		self.assertEqual(getattr(Dummy, name).fset, fset)
		self.assertEqual(getattr(Dummy, name).fdel, fdel)

class TraceClassTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.trace_class` definition units tests methods.
	"""

	def test_trace_class(self):
		"""
		Tests :func:`foundations.trace.trace_class` definition.
		"""

		self.assertFalse(foundations.trace.is_traced(Dummy))
		self.assertTrue(foundations.trace.trace_class(Dummy))
		self.assertTrue(foundations.trace.is_traced(Dummy))

		for method in TRACABLE_METHODS.iterkeys():
			self.assertTrue(foundations.trace.is_traced(getattr(Dummy, method)))

		for method in UNTRACABLE_METHODS.iterkeys():
			self.assertFalse(foundations.trace.is_traced(getattr(Dummy, method)))

		for name, accessor in inspect.getmembers(Dummy, lambda x: type(x) is property):
			self.assertTrue(foundations.trace.is_traced(accessor.fget))
			self.assertTrue(foundations.trace.is_traced(accessor.fset))
			self.assertTrue(foundations.trace.is_traced(accessor.fdel))

		foundations.trace.untrace_class(Dummy)

		self.assertTrue(foundations.trace.trace_class(Dummy, pattern=r"^public_method$"))
		self.assertTrue(foundations.trace.is_traced(getattr(Dummy, "public_method")))
		self.assertFalse(foundations.trace.is_traced(getattr(Dummy, "class_method")))

		foundations.trace.untrace_class(Dummy)

		self.assertTrue(foundations.trace.trace_class(Dummy, pattern=r"^(?:(?!public_method).)*$"))
		self.assertFalse(foundations.trace.is_traced(getattr(Dummy, "public_method")))
		self.assertTrue(foundations.trace.is_traced(getattr(Dummy, "class_method")))

		foundations.trace.untrace_class(Dummy)

class UntraceClassTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.untrace_class` definition units tests methods.
	"""

	def test_untrace_class(self):
		"""
		Tests :func:`foundations.trace.untrace_class` definition.
		"""

		foundations.trace.trace_class(Dummy)
		self.assertTrue(foundations.trace.untrace_class(Dummy))
		self.assertFalse(foundations.trace.is_traced(Dummy))

		for name, method in TRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.is_traced(method))
			self.assertEqual(method, getattr(Dummy, name))

		for name, method in UNTRACABLE_METHODS.iteritems():
			self.assertFalse(foundations.trace.is_traced(method))
			self.assertEqual(method, getattr(Dummy, name))

		for name, accessor in inspect.getmembers(Dummy, lambda x: type(x) is property):
			self.assertFalse(foundations.trace.is_traced(accessor.fget))
			self.assertFalse(foundations.trace.is_traced(accessor.fset))
			self.assertFalse(foundations.trace.is_traced(accessor.fdel))

class TraceModuleTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.trace_module` definition units tests methods.
	"""

	def test_trace_module(self):
		"""
		Tests :func:`foundations.trace.trace_module` definition.
		"""

		module = foundations.tests.tests_foundations.resources.dummy
		self.assertTrue(foundations.trace.trace_module(module))
		self.assertTrue(foundations.trace.is_traced(module))

		for name, definition in TRACABLE_DEFINITIONS.iteritems():
			self.assertTrue(foundations.trace.is_traced(getattr(module, name)))

		for name, definition in UNTRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.is_traced(getattr(module, name)))

		self.assertIn(module, foundations.trace.REGISTERED_MODULES)

		foundations.trace.untrace_module(module)

		self.assertTrue(foundations.trace.trace_module(module, pattern=r"^dummy1$"))
		self.assertTrue(foundations.trace.is_traced(getattr(module, dummy1.__name__)))
		self.assertFalse(foundations.trace.is_traced(getattr(module, dummy2.__name__)))

		foundations.trace.untrace_module(module)

		self.assertTrue(foundations.trace.trace_module(module, pattern=r"^(?:(?!dummy1).)*$"))
		self.assertFalse(foundations.trace.is_traced(getattr(module, dummy1.__name__)))
		self.assertTrue(foundations.trace.is_traced(getattr(module, dummy3.__name__)))

		foundations.trace.untrace_module(module)

class UntraceModuleTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.untrace_module` definition units tests methods.
	"""

	def test_untrace_module(self):
		"""
		Tests :func:`foundations.trace.untrace_module` definition.
		"""

		module = foundations.tests.tests_foundations.resources.dummy
		foundations.trace.trace_module(module)
		self.assertTrue(foundations.trace.untrace_module(module))

		for name, definition in TRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.is_traced(getattr(module, name)))
			self.assertEqual(definition, getattr(module, name))

		for name, definition in UNTRACABLE_DEFINITIONS.iteritems():
			self.assertFalse(foundations.trace.is_traced(getattr(module, name)))
			self.assertEqual(definition, getattr(module, name))

class RegisterModuleTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.register_module` definition units tests methods.
	"""

	def test_register_module(self):
		"""
		Tests :func:`foundations.trace.register_module` definition.
		"""

		registered_modules = foundations.trace.REGISTERED_MODULES
		foundations.trace.REGISTERED_MODULES = set()

		module = foundations.tests.tests_foundations.resources.dummy
		self.assertTrue(foundations.trace.register_module(module))
		self.assertIn(module, foundations.trace.REGISTERED_MODULES)

		self.assertTrue(foundations.trace.register_module())
		self.assertIn(sys.modules[__name__], foundations.trace.REGISTERED_MODULES)

		foundations.trace.REGISTERED_MODULES = foundations.trace.REGISTERED_MODULES

class InstallTracerTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.install_tracer` definition units tests methods.
	"""

	def test_install_tracer(self):
		"""
		Tests :func:`foundations.trace.install_tracer` definition.
		"""

		registered_modules = foundations.trace.REGISTERED_MODULES
		foundations.trace.REGISTERED_MODULES = set()

		module = foundations.tests.tests_foundations.resources.dummy
		foundations.trace.register_module(module)
		self.assertTrue(foundations.trace.install_tracer(pattern=r"Nemo"))
		self.assertFalse(foundations.trace.is_traced(module))
		self.assertTrue(foundations.trace.install_tracer(pattern=r"\w+ummy"))
		self.assertTrue(foundations.trace.is_traced(module))
		foundations.trace.uninstall_tracer()

		foundations.trace.REGISTERED_MODULES = foundations.trace.REGISTERED_MODULES

class UninstallTracerTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.uninstall_tracer` definition units tests methods.
	"""

	def test_uninstall_tracer(self):
		"""
		Tests :func:`foundations.trace.uninstall_tracer` definition.
		"""

		registered_modules = foundations.trace.REGISTERED_MODULES
		foundations.trace.REGISTERED_MODULES = set()

		module = foundations.tests.tests_foundations.resources.dummy
		foundations.trace.register_module(module)
		foundations.trace.install_tracer()
		self.assertTrue(foundations.trace.uninstall_tracer(r"Nemo"))
		self.assertTrue(foundations.trace.is_traced(module))
		self.assertTrue(foundations.trace.uninstall_tracer(r"\w+ummy"))
		self.assertFalse(foundations.trace.is_traced(module))

		foundations.trace.REGISTERED_MODULES = foundations.trace.REGISTERED_MODULES

class EvaluateTraceRequestTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.trace.evaluate_trace_request` definition units tests methods.
	"""

	def test_evaluate_trace_request(self):
		"""
		Tests :func:`foundations.trace.evaluate_trace_request` definition.
		"""

		module = foundations.tests.tests_foundations.resources.dummy

		self.assertTrue(foundations.trace.evaluate_trace_request("'foundations.tests.tests_foundations.resources.dummy'"))
		self.assertTrue(foundations.trace.is_traced(module))

		foundations.trace.untrace_module(module)

		self.assertTrue(foundations.trace.evaluate_trace_request("['foundations.tests.tests_foundations.resources.dummy']"))
		self.assertTrue(foundations.trace.is_traced(module))

		foundations.trace.untrace_module(module)

		self.assertTrue(foundations.trace.evaluate_trace_request(
		"{'foundations.tests.tests_foundations.resources.dummy' : (r'.*', 0)}"))
		self.assertTrue(foundations.trace.is_traced(module))

		foundations.trace.untrace_module(module)

		self.assertTrue(foundations.trace.evaluate_trace_request(
		"{'foundations.tests.tests_foundations.resources.dummy' : (r'^(?:(?!dummy1).)*$', 0)}"))
		self.assertTrue(foundations.trace.is_traced(module))
		self.assertFalse(foundations.trace.is_traced(getattr(module, "dummy1")))

		foundations.trace.untrace_module(module)

if __name__ == "__main__":
	unittest.main()
