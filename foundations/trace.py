#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**trace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package trace objects.

**Others:**
	Portions of the code from echo.py by Thomas Guest: http://wordaligned.org/svn/etc/echo/echo.py.

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import ast
import functools
import inspect
import re
import sys
import itertools

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["REGISTERED_MODULES",
			"TRACER_SYMBOL",
			"UNTRACABLE_SYMBOL",
			"TRACER_HOOK",
			"UNTRACABLE_NAMES",
			"NULL_OBJECT_NAME",
			"TRACE_NAMES_CACHE",
			"TRACE_WALKER_CACHE",
			"isReadOnly",
			"setTracerHook",
			"getTracerHook",
			"isTraced",
			"isBaseTraced",
			"isUntracable",
			"setTraced",
			"setUntraced",
			"setUntracable",
			"traceWalker",
			"getObjectName",
			"getTraceName",
			"getMethodName",
			"isStaticMethod",
			"isClassMethod",
			"formatArgument",
			"validateTracer",
			"tracer",
			"untracer",
			"untracable",
			"traceFunction",
			"untraceFunction",
			"traceMethod",
			"untraceMethod",
			"traceProperty",
			"untraceProperty",
			"traceClass",
			"untraceClass",
			"traceModule",
			"untraceModule",
			"registerModule",
			"installTracer",
			"evaluateTraceRequest"]

REGISTERED_MODULES = set()

TRACER_SYMBOL = "_trace__tracer__"
UNTRACABLE_SYMBOL = "_trace__untracable__"

TRACER_HOOK = "_trace__hook__"

UNTRACABLE_NAMES = ("__str__", "__repr__")

NULL_OBJECT_NAME = "None"

TRACE_NAMES_CACHE = {}
TRACE_WALKER_CACHE = {}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def isReadOnly(object):
	"""
	Returns if given object is read only ( built-in or extension ).

	:param object: Object.
	:type object: object
	:return: Is object read only.
	:rtype: bool
	"""

	try:
		attribute = "_trace__read__"
		setattr(object, attribute, True)
		delattr(object, attribute)
		return False
	except (TypeError, AttributeError):
		return True

def setTracerHook(object, hook):
	"""
	Sets given object tracer hook on given object.

	:param hook: Tracer hook.
	:type hook: object
	:param object: Object.
	:type object: object
	:return: Definition success.
	:rtype: bool
	"""

	setattr(object, TRACER_HOOK, hook)
	return True

def getTracerHook(object):
	"""
	Returns given object tracer hook.

	:param object: Object.
	:type object: object
	:return: Object tracer hook.
	:rtype: object
	"""

	if hasattr(object, TRACER_HOOK):
		return getattr(object, TRACER_HOOK)

def isTraced(object):
	"""
	Returns if given object is traced.

	:param object: Object.
	:type object: object
	:return: Is object traced.
	:rtype: bool
	"""

	return hasattr(object, TRACER_SYMBOL)

def isBaseTraced(cls):
	"""
	Returns if given class has a traced base.

	:param cls: Class.
	:type cls: object
	:return: Is base traced.
	:rtype: bool
	"""

	for base in cls.mro()[1:]:
		if isTraced(base):
			return True
	return False

def isUntracable(object):
	"""
	Returns if given object is untracable.

	:param object: Object.
	:type object: object
	:return: Is object untracable.
	:rtype: bool
	"""

	return hasattr(object, UNTRACABLE_SYMBOL)

def setTraced(object):
	"""
	Sets given object as traced.

	:param object: Object.
	:type object: object
	:return: Definition success.
	:rtype: bool
	"""

	setattr(object, TRACER_SYMBOL, True)
	return True

def setUntraced(object):
	"""
	Sets given object as untraced.

	:param object: Object.
	:type object: object
	:return: Definition success.
	:rtype: bool
	"""

	if isTraced(object):
		delattr(object, TRACER_SYMBOL)
	return True

def setUntracable(object):
	"""
	Sets given object as untraced.

	:param object: Object.
	:type object: object
	:return: Definition success.
	:rtype: bool
	"""

	setattr(object, UNTRACABLE_SYMBOL, True)
	return True

def traceWalker(module):
	"""
	Defines a generator used to walk into modules.
	
	:param module: Module to walk.
	:type module: ModuleType
	:return: Class / Function / Method.
	:rtype: object or object
	"""

	for name, function in inspect.getmembers(module, inspect.isfunction):
		yield None, function

	for name, cls in inspect.getmembers(module, inspect.isclass):
		yield cls, None

		for name, method in inspect.getmembers(cls, inspect.ismethod):
			yield cls, method

		for name, function in inspect.getmembers(cls, inspect.isfunction):
			yield cls, function

		for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
			yield cls, accessor.fget
			yield cls, accessor.fset
			yield cls, accessor.fdel

def getObjectName(object):
	"""
	Returns given object name.

	:param object: Object to retrieve the name.
	:type object: object
	:return: Object name.
	:rtype: unicode
	"""

	if type(object) is property:
		return object.fget.__name__
	elif hasattr(object, "__name__"):
		return object.__name__
	elif hasattr(object, "__class__"):
		return object.__class__.__name__
	else:
		return NULL_OBJECT_NAME

def getTraceName(object):
	"""
	Returns given object trace name.
	
	:param object: Object.
	:type object: object
	:return: Object trace name.
	:rtype: unicode
	"""

	global TRACE_NAMES_CACHE
	global TRACE_WALKER_CACHE

	traceName = TRACE_NAMES_CACHE.get(object)
	if traceName is None:

		TRACE_NAMES_CACHE[object] = traceName = getObjectName(object)

		if type(object) is property:
			object = object.fget

		module = inspect.getmodule(object)
		if module is None:
			return

		members = TRACE_WALKER_CACHE.get(module)
		if members is None:
			TRACE_WALKER_CACHE[module] = members = tuple(traceWalker(module))

		for (cls, member) in members:
			if object in (cls, untracer(member)):
				TRACE_NAMES_CACHE[object] = traceName = \
				".".join(map(getObjectName, filter(lambda x: x is not None, (module, cls, member))))
				break

	return traceName

def getMethodName(method):
	"""
	Returns given method name.

	:param method: Method to retrieve the name.
	:type method: object
	:return: Method name.
	:rtype: unicode
	"""

	name = getObjectName(method)
	if name.startswith("__") and not name.endswith("__"):
		name = "_{0}{1}".format(getObjectName(method.im_class), name)
	return name

def isStaticMethod(method):
	"""
	Returns if given method is a static method.

	:param method: Method.
	:type method: object
	:return: Is static method.
	:rtype: bool
	"""

	return type(method) is type(lambda x: None)

def isClassMethod(method):
	"""
	Returns if given method is a class method.

	:param method: Method.
	:type method: object
	:return: Is class method.
	:rtype: bool
	"""

	if isStaticMethod(method):
		return False

	return method.im_self is not None

def formatArgument(argumentValue):
	"""
	Returns a string representing an argument / value pair.

	Usage::
	
		>>> formatArgument(('x', (0, 1, 2)))
		u'x=(0, 1, 2)'
	
	:param argumentValue: Argument / value pair.
	:type argumentValue: tuple
	:return: Formatted .argument / value pair.
	:rtype: unicode
	"""

	return "{0}={1!r}".format(*argumentValue)

def validateTracer(*args):
	"""
	Validate and finishes a tracer by adding mandatory extra attributes.

	:param \*args: Arguments.
	:type \*args: \*
	:return: Validated wrapped object.
	:rtype: object
	"""

	object, wrapped = args
	if isTraced(object) or isUntracable(object) or getObjectName(object) in UNTRACABLE_NAMES:
		return object

	setTracerHook(wrapped, object)
	setTraced(wrapped)

	return wrapped

def tracer(object):
	"""
	| Traces execution.
	| Any method / definition decorated will have it's execution traced.
	
	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	@functools.partial(validateTracer, object)
	def tracerWrapper(*args, **kwargs):
		"""
		Traces execution.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		code = object.func_code
		argsCount = code.co_argcount
		argsNames = code.co_varnames[:argsCount]
		functionDefaults = object.func_defaults or list()
		argsDefaults = dict(zip(argsNames[-len(functionDefaults):], functionDefaults))

		positionalArgs = map(formatArgument, zip(argsNames, args))
		defaultedArgs = [formatArgument((name, argsDefaults[name])) for name in argsNames[len(args):] if name not in kwargs]
		namelessArgs = map(repr, args[argsCount:])
		keywordArgs = map(formatArgument, kwargs.items())
		sys.stdout.write("{0}({1})\n".format(getTraceName(object),
											", ".join(itertools.chain(positionalArgs,
																	defaultedArgs,
																	namelessArgs,
																	keywordArgs))))
		return object(*args, **kwargs)

	return tracerWrapper

def untracer(object):
	"""
	Object is used to untrace given object.
	
	:param object: Object to untrace.
	:type object: object
	:return: Untraced object.
	:rtype: object
	"""

	if isTraced(object):
		return getTracerHook(object)
	return object

def untracable(object):
	"""
	Marks decorated object as non tracable.
	
	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def untracableWrapper(*args, **kwargs):
		"""
		Marks decorated object as non tracable.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		return object(*args, **kwargs)

	setUntracable(untracableWrapper)

	return untracableWrapper

def traceFunction(module, function, tracer=tracer):
	"""
	Traces given module function using given tracer.

	:param module: Module of the function.
	:type module: object
	:param function: Function to trace.
	:type function: object
	:param tracer: Tracer.
	:type tracer: object
	:return: Definition success.
	:rtype: bool
	"""

	if isTraced(function):
		return False

	name = getObjectName(function)
	if isUntracable(function) or name in UNTRACABLE_NAMES:
		return False

	setattr(module, name, tracer(function))
	return True

def untraceFunction(module, function):
	"""
	Untraces given module function.

	:param module: Module of the function.
	:type module: object
	:param function: Function to untrace.
	:type function: object
	:return: Definition success.
	:rtype: bool
	"""

	if not isTraced(function):
		return False

	name = getObjectName(function)
	setattr(module, name, untracer(function))
	return True

def traceMethod(cls, method, tracer=tracer):
	"""
	Traces given class method using given tracer.

	:param cls: Class of the method.
	:type cls: object
	:param method: Method to trace.
	:type method: object
	:param tracer: Tracer.
	:type tracer: object
	:return: Definition success.
	:rtype: bool
	"""

	if isTraced(method):
		return False

	name = getMethodName(method)
	if isUntracable(method) or name in UNTRACABLE_NAMES:
		return False

	if isClassMethod(method):
		setattr(cls, name, classmethod(tracer(method.im_func)))
	elif isStaticMethod(method):
		setattr(cls, name, staticmethod(tracer(method)))
	else:
		setattr(cls, name, tracer(method))
	return True

def untraceMethod(cls, method):
	"""
	Untraces given class method.

	:param cls: Class of the method.
	:type cls: object
	:param method: Method to untrace.
	:type method: object
	:return: Definition success.
	:rtype: bool
	"""

	if not isTraced(method):
		return False

	name = getMethodName(method)
	if isClassMethod(method):
		setattr(cls, name, classmethod(untracer(method)))
	elif isStaticMethod(method):
		setattr(cls, name, staticmethod(untracer(method)))
	else:
		setattr(cls, name, untracer(method))
	return True

def traceProperty(cls, accessor, tracer=tracer):
	"""
	Traces given class property using given tracer.

	:param cls: Class of the property.
	:type cls: object
	:param accessor: Property to trace.
	:type accessor: property
	:param tracer: Tracer.
	:type tracer: object
	:return: Definition success.
	:rtype: bool
	"""

	if isTraced(accessor.fget) and isTraced(accessor.fset) and isTraced(accessor.fdel):
		return False

	name = getMethodName(accessor)
	setattr(cls, name, property(tracer(accessor.fget),
								tracer(accessor.fset),
								tracer(accessor.fdel)))
	return True

def untraceProperty(cls, accessor):
	"""
	Untraces given class property.

	:param cls: Class of the property.
	:type cls: object
	:param accessor: Property to untrace.
	:type accessor: property
	:return: Definition success.
	:rtype: bool
	"""

	if not isTraced(accessor.fget) or not isTraced(accessor.fset) or not isTraced(accessor.fdel):
		return False

	name = getMethodName(accessor)
	setattr(cls, name, property(untracer(accessor.fget),
								untracer(accessor.fset),
								untracer(accessor.fdel)))
	return True

def traceClass(cls, tracer=tracer, pattern=r".*", flags=0):
	"""
	Traces given class using given tracer.

	:param cls: Class to trace.
	:type cls: object
	:param tracer: Tracer.
	:type tracer: object
	:param pattern: Matching pattern.
	:type pattern: unicode
	:param flags: Matching regex flags.
	:type flags: int
	:return: Definition success.
	:rtype: bool
	"""

	if not isBaseTraced(cls) and (isTraced(cls) or isReadOnly(cls)):
		return False

	for name, method in inspect.getmembers(cls, inspect.ismethod):
		if not re.search(pattern, name, flags=flags):
			continue

		traceMethod(cls, method, tracer)

	for name, function in inspect.getmembers(cls, inspect.isfunction):
		if not re.search(pattern, name, flags=flags):
			continue

		traceMethod(cls, function, tracer)

	for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
		if not re.search(pattern, name, flags=flags):
			continue

		traceProperty(cls, accessor, tracer)

	setTraced(cls)

	return True

def untraceClass(cls):
	"""
	Untraces given class.

	:param cls: Class to untrace.
	:type cls: object
	:return: Definition success.
	:rtype: bool
	"""

	for name, method in inspect.getmembers(cls, inspect.ismethod):
		untraceMethod(cls, method)

	for name, function in inspect.getmembers(cls, inspect.isfunction):
		untraceMethod(cls, function)

	for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
		untraceProperty(cls, accessor)

	setUntraced(cls)

	return True

def traceModule(module, tracer=tracer, pattern=r".*", flags=0):
	"""
	Traces given module members using given tracer.

	:param module: Module to trace.
	:type module: ModuleType
	:param tracer: Tracer.
	:type tracer: object
	:param pattern: Matching pattern.
	:type pattern: unicode
	:param flags: Matching regex flags.
	:type flags: int
	:return: Definition success.
	:rtype: bool
	
	:note: Only members exported by **__all__** attribute will be traced.
	"""

	if isTraced(module):
		return False

	global REGISTERED_MODULES

	for name, function in inspect.getmembers(module, inspect.isfunction):
		if name not in module.__all__ or not re.search(pattern, name, flags=flags):
			continue

		traceFunction(module, function, tracer)

	for name, cls in inspect.getmembers(module, inspect.isclass):
		if name not in module.__all__ or not re.search(pattern, name, flags=flags):
			continue

		traceClass(cls, tracer, pattern, flags)

	REGISTERED_MODULES.add(module)

	setTraced(module)

	return True

def untraceModule(module):
	"""
	Untraces given module members.

	:param module: Module to untrace.
	:type module: ModuleType
	:return: Definition success.
	:rtype: bool
	"""

	for name, function in inspect.getmembers(module, inspect.isfunction):
		untraceFunction(module, function)

	for name, cls in inspect.getmembers(module, inspect.isclass):
		untraceClass(cls)

	setUntraced(module)

	return True

def registerModule(module=None):
	"""
	Registers given module or caller introspected module in the candidates modules for tracing.

	:param module: Module to register.
	:type module: ModuleType
	:return: Definition success.
	:rtype: bool
	"""

	global REGISTERED_MODULES

	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])

	REGISTERED_MODULES.add(module)
	return True

def installTracer(tracer=tracer, pattern=r".*", flags=0):
	"""
	Installs given tracer in the candidates modules for tracing matching given pattern.

	:param tracer: Tracer.
	:type tracer: object
	:param pattern: Matching pattern.
	:type pattern: unicode
	:param flags: Matching regex flags.
	:type flags: int
	:return: Definition success.
	:rtype: bool
	"""

	for module in REGISTERED_MODULES:
		if not re.search(pattern, module.__name__, flags=flags):
			continue

		traceModule(module, tracer)
	return True

def uninstallTracer(pattern=r".*", flags=0):
	"""
	Installs the tracer in the candidates modules for tracing matching given pattern.

	:param pattern: Matching pattern.
	:type pattern: unicode
	:param flags: Matching regex flags.
	:type flags: int
	:return: Definition success.
	:rtype: bool
	"""

	for module in REGISTERED_MODULES:
		if not isTraced(module):
			continue

		if not re.search(pattern, module.__name__, flags=flags):
			continue

		untraceModule(module)
	return True

def evaluateTraceRequest(data, tracer=tracer):
	"""
	Evaluate given string trace request.

	Usage::

		Umbra -t "{'umbra.engine' : ('.*', 0), 'umbra.preferences' : (r'.*', 0)}"
		Umbra -t "['umbra.engine', 'umbra.preferences']"
		Umbra -t "'umbra.engine, umbra.preferences"
		
	:param data: Trace request.
	:type data: unicode
	:param tracer: Tracer.
	:type tracer: object
	:return: Definition success.
	:rtype: bool
	"""

	data = ast.literal_eval(data)

	if isinstance(data, str):
		modules = dict.fromkeys(map(lambda x: x.strip(), data.split(",")), (None, None))
	elif isinstance(data, list):
		modules = dict.fromkeys(data, (None, None))
	elif isinstance(data, dict):
		modules = data

	for module, (pattern, flags) in modules.iteritems():
		__import__(module)
		pattern = pattern if pattern is not None else r".*"
		flags = flags if flags is not None else re.IGNORECASE
		traceModule(sys.modules[module], tracer, pattern, flags)
	return True
