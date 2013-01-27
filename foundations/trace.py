#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**trace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package trace objects.

**Others:**
	Portions of the code from echo.py by Thomas Guest: http://wordaligned.org/svn/etc/echo/echo.py.

"""

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
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
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
			"setUntracable"
			"traceWalker",
			"getObjectName",
			"getTraceName",
			"getMethodName",
			"isStaticMethod",
			"isClassMethod",
			"formatArgument",
			"validateTracer",
			"tracer",
			"untracer"
			"untracable",
			"wrapped",
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

NULL_OBJECT_NAME = str(None)

TRACE_NAMES_CACHE = {}
TRACE_WALKER_CACHE = {}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def isReadOnly(object):
	"""
	This definition returns if given object is read only ( built-in or extension ).

	:param object: Object. ( Object )
	:return: Is object read only. ( Boolean )
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
	This definition sets given object tracer hook on given object.

	:param hook: Tracer hook. ( Object )
	:param object: Object. ( Object )
	:return: Definition success. ( Boolean )
	"""

	setattr(object, TRACER_HOOK, hook)
	return True

def getTracerHook(object):
	"""
	This definition returns given object tracer hook.

	:param object: Object. ( Object )
	:return: Object tracer hook. ( Object )
	"""

	if hasattr(object, TRACER_HOOK):
		return getattr(object, TRACER_HOOK)

def isTraced(object):
	"""
	This definition returns if given object is traced.

	:param object: Object. ( Object )
	:return: Is object traced. ( Boolean )
	"""

	return hasattr(object, TRACER_SYMBOL)

def isBaseTraced(cls):
	"""
	This definition returns if given class has a traced base.

	:param cls: Class. ( Object )
	:return: Is base traced. ( Boolean )
	"""

	for base in cls.mro()[1:]:
		if isTraced(base):
			return True
	return False

def isUntracable(object):
	"""
	This definition returns if given object is untracable.

	:param object: Object. ( Object )
	:return: Is object untracable. ( Boolean )
	"""

	return hasattr(object, UNTRACABLE_SYMBOL)

def setTraced(object):
	"""
	This definition sets given object as traced.

	:param object: Object. ( Object )
	:return: Definition success. ( Boolean )
	"""

	setattr(object, TRACER_SYMBOL, True)
	return True

def setUntraced(object):
	"""
	This definition sets given object as untraced.

	:param object: Object. ( Object )
	:return: Definition success. ( Boolean )
	"""

	if isTraced(object):
		delattr(object, TRACER_SYMBOL)
	return True

def setUntracable(object):
	"""
	This definition sets given object as untraced.

	:param object: Object. ( Object )
	:return: Definition success. ( Boolean )
	"""

	setattr(object, UNTRACABLE_SYMBOL, True)
	return True

def traceWalker(module):
	"""
	This definition is a generator used to walk into modules.
	
	:param module: Module to walk. ( Module )
	:return: Class / Function / Method. ( Object / Object )
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
	This definition returns given object name.

	:param object: Object to retrieve the name. ( Object )
	:return: Object name. ( String )
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
	This definition returns given object trace name.
	
	:param object: Object. ( Object )
	:return: Object trace name. ( String )
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
	This definition returns given method name.

	:param method: Method to retrieve the name. ( Object )
	:return: Method name. ( String )
	"""

	name = getObjectName(method)
	if name.startswith("__") and not name.endswith("__"):
		name = "_{0}{1}".format(getObjectName(method.im_class), name)
	return name

def isStaticMethod(method):
	"""
	This definition returns if given method is a static method.

	:param method: Method. ( Object )
	:return: Is static method. ( Boolean )
	"""

	return type(method) is type(lambda x: None)

def isClassMethod(method):
	"""
	This definition returns if given method is a class method.

	:param method: Method. ( Object )
	:return: Is class method. ( Boolean )
	"""

	if isStaticMethod(method):
		return False

	return method.im_self is not None

def formatArgument(argumentValue):
	"""
	This definition returns a string representing an argument / value pair.

	Usage::
	
		>>> formatArgument(('x', (0, 1, 2)))
		'x=(0, 1, 2)'
	
	:param argumentValue: Argument / value pair. ( Tuple )
	:return: Formatted .argument / value pair. ( String )
	"""

	return "{0}={1!r}".format(*argumentValue)

def validateTracer(*args):
	"""
	This definition is used to validate and finish a tracer by adding mandatory extra attributes.

	:param \*args: Arguments. ( \* )
	:return: Validated wrapped object. ( Object )
	"""

	object, wrapped = args
	if isTraced(object) or isUntracable(object) or getObjectName(object) in UNTRACABLE_NAMES:
		return object

	setTracerHook(wrapped, object)
	setTraced(wrapped)

	return wrapped

def tracer(object):
	"""
	| This decorator object is used for execution tracing.
	| Any method / definition decorated will have it's execution traced.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	@functools.partial(validateTracer, object)
	def tracerWrapper(*args, **kwargs):
		"""
		This decorator is used for execution tracing.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
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
	This definition object is used to untrace given object.
	
	:param object: Object to untrace. ( Object )
	:return: Untraced object. ( Object )
	"""

	if isTraced(object):
		return getTracerHook(object)
	return object

def untracable(object):
	"""
	This decorator object is used to mark decorated object as non tracable.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	def untracableWrapper(*args, **kwargs):
		"""
		This decorator object is used to mark decorated object as non tracable.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
		"""

		return object(*args, **kwargs)

	setUntracable(untracableWrapper)

	return untracableWrapper

def traceFunction(module, function, tracer=tracer):
	"""
	This definition traces given module function using given tracer.

	:param module: Module of the function. ( Object )
	:param function: Function to trace. ( Object )
	:param tracer: Tracer. ( Object )
	:return: Definition success. ( Boolean )
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
	This definition untraces given module function.

	:param module: Module of the function. ( Object )
	:param function: Function to untrace. ( Object )
	:return: Definition success. ( Boolean )
	"""

	if not isTraced(function):
		return False

	name = getObjectName(function)
	setattr(module, name, untracer(function))
	return True

def traceMethod(cls, method, tracer=tracer):
	"""
	This definition traces given class method using given tracer.

	:param cls: Class of the method. ( Object )
	:param method: Method to trace. ( Object )
	:param tracer: Tracer. ( Object )
	:return: Definition success. ( Boolean )
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
	This definition untraces given class method.

	:param cls: Class of the method. ( Object )
	:param method: Method to untrace. ( Object )
	:return: Definition success. ( Boolean )
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
	This definition traces given class property using given tracer.

	:param cls: Class of the property. ( Object )
	:param accessor: Property to trace. ( Property )
	:param tracer: Tracer. ( Object )
	:return: Definition success. ( Boolean )
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
	This definition untraces given class property.

	:param cls: Class of the property. ( Object )
	:param accessor: Property to untrace. ( Property )
	:return: Definition success. ( Boolean )
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
	This definition traces given class using given tracer.

	:param cls: Class to trace. ( Object )
	:param tracer: Tracer. ( Object )
	:param pattern: Matching pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:return: Definition success. ( Boolean )
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
	This definition untraces given class.

	:param cls: Class to untrace. ( Object )
	:return: Definition success. ( Boolean )
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
	This definition traces given module members using given tracer.

	:param module: Module to trace. ( Module )
	:param tracer: Tracer. ( Object )
	:param pattern: Matching pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:return: Definition success. ( Boolean )
	
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
	This definition untraces given module members.

	:param module: Module to untrace. ( Module )
	:return: Definition success. ( Boolean )
	"""

	for name, function in inspect.getmembers(module, inspect.isfunction):
		untraceFunction(module, function)

	for name, cls in inspect.getmembers(module, inspect.isclass):
		untraceClass(cls)

	setUntraced(module)

	return True

def registerModule(module=None):
	"""
	This definition registers given module or caller introspected module in the candidates modules for tracing.

	:param module: Module to register. ( Module )
	:return: Definition success. ( Boolean )
	"""

	global REGISTERED_MODULES

	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])

	REGISTERED_MODULES.add(module)
	return True

def installTracer(tracer=tracer, pattern=r".*", flags=0):
	"""
	This definition installs given tracer in the candidates modules for tracing matching given pattern.

	:param tracer: Tracer. ( Object )
	:param pattern: Matching pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:return: Definition success. ( Boolean )
	"""

	for module in REGISTERED_MODULES:
		if not re.search(pattern, module.__name__, flags=flags):
			continue

		traceModule(module, tracer)
	return True

def uninstallTracer(pattern=r".*", flags=0):
	"""
	This definition installs the tracer in the candidates modules for tracing matching given pattern.

	:param pattern: Matching pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:return: Definition success. ( Boolean )
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
	This definition evaluate given string trace request.

	Usage::

		Umbra -t "{'umbra.engine' : ('.*', 0), 'umbra.preferences' : (r'.*', 0)}"
		Umbra -t "['umbra.engine', 'umbra.preferences']"
		Umbra -t "'umbra.engine, umbra.preferences"
		
	:param data: Trace request. ( String )
	:param tracer: Tracer. ( Object )
	:return: Definition success. ( Boolean )
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

