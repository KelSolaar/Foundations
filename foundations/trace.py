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
import functools
import inspect
import re
import sys

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["REGISTERED_MODULES",
			"TRACER_SYMBOL",
			"UNTRACABLE_SYMBOL",
			"TRACER_HOOK",
			"setTracerHook",
			"getTracerHook",
			"isTraced",
			"isUntracable",
			"setTraced",
			"setUntraced",
			"setUntracable"
			"getObjectName",
			"getMethodName",
			"isClassMethod",
			"formatArgument",
			"tracer",
			"untracer"
			"tracerWrapped",
			"untracable",
			"wrapped",
			"traceMethod",
			"untraceMethod",
			"traceClass",
			"untraceClass",
			"traceModule",
			"untraceModule",
			"registerModule",
			"installTracer"]

REGISTERED_MODULES = set()

TRACER_SYMBOL = "_trace__tracer__"
UNTRACABLE_SYMBOL = "_trace__untracable__"

TRACER_HOOK = "_trace__hook__"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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

def isUntracable(object):
	"""
	This definition returns if given object is untraced.

	:param object: Object. ( Object )
	:return: Is object untraced. ( Boolean )
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

def getObjectName(object):
	"""
	This definition returns given object name.

	:param object: Object to retrieve the name. ( Object )
	:return: Object name. ( String )
	"""

	return object.__name__

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

def isClassMethod(method):
	"""
	This definition returns if given method is a class method.

	:param method: Method. ( Object )
	:return: Is class method. ( Boolean )
	"""

	if type(method) is type(lambda x: None):
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

def tracer(object):
	"""
	| This decorator object is used for execution tracing.
	| Any method / definition decorated will have it's execution traced.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	if isUntracable(object):
		return object

	@functools.wraps(object)
	def tracerWrapped(*args, **kwargs):
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
		sys.stdout.write("{0}({1})\n".format(getObjectName(object),
											", ".join(positionalArgs + defaultedArgs + namelessArgs + keywordArgs)))
		return object(*args, **kwargs)

	setTracerHook(tracerWrapped, object)
	setTraced(tracerWrapped)

	return tracerWrapped

def untracer(object):
	"""
	This definition object is used to untrace given object.
	
	:param object: Object to untrace. ( Object )
	:return: Untraced object. ( Object )
	"""

	if isTraced(object):
		tracerHook = getTracerHook(object)
		setUntraced(tracerHook)
		return tracerHook
	return object

def untracable(function):
	"""
	This decorator object is used to mark decorated object as non tracable.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(function)
	def wrapped(*args, **kwargs):
		"""
		This decorator object is used to mark decorated object as non tracable.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
		"""

		return function(*args, **kwargs)

	setUntracable(wrapped)

	return wrapped

def traceMethod(cls, method, tracer=tracer):
	"""
	This definition traces given method using given tracer.

	:param cls: Class of the method. ( Object )
	:param method: Method to trace. ( Object )
	:param tracer: Tracer. ( Object )
	:return: Definition success. ( Boolean )
	"""

	name = getMethodName(method)
	if name in ("__str__", "__repr__"):
		return False

	if isClassMethod(method):
		setattr(cls, name, classmethod(tracer(method.im_func)))
	else:
		setattr(cls, name, tracer(method))
	return True

def untraceMethod(cls, method):
	"""
	This definition untraces given method.

	:param cls: Class of the method. ( Object )
	:param method: Method to untrace. ( Object )
	:return: Definition success. ( Boolean )
	"""

	name = getMethodName(method)
	if name in ("__str__", "__repr__"):
		return False

	if isClassMethod(method):
		setattr(cls, name, classmethod(untracer(method)))
	else:
		setattr(cls, name, untracer(method))
	return True

def traceClass(cls, tracer=tracer):
	"""
	This definition traces given class using given tracer.

	:param cls: Class to trace. ( Object )
	:param tracer: Tracer. ( Object )
	:return: Definition success. ( Boolean )
	"""

	for name, method in inspect.getmembers(cls, inspect.ismethod):
		traceMethod(cls, method)

	for name, function in inspect.getmembers(cls, inspect.isfunction):
		setattr(cls, getObjectName(function), staticmethod(tracer(function)))

	for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
		setattr(cls, name, property(tracer(accessor.fget),
									tracer(accessor.fset),
									tracer(accessor.fdel)))

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
		if not isTraced(function):
			continue

		setattr(cls, getObjectName(function), staticmethod(untracer(function)))

	for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
		if not isTraced(accessor.fget) or not isTraced(accessor.fset) or not isTraced(accessor.fdel):
			continue

		setattr(cls, name, property(untracer(accessor.fget),
									untracer(accessor.fset),
									untracer(accessor.fdel)))

	setUntraced(cls)

	return True

def traceModule(module, tracer=tracer):
	"""
	This definition traces given module using given tracer.

	:param module: Module to trace. ( Module )
	:param tracer: Tracer. ( Object )
	:return: Definition success. ( Boolean )
	"""

	global REGISTERED_MODULES

	for name, function in inspect.getmembers(module, inspect.isfunction):
		setattr(module, name, tracer(function))

	for name, cls in inspect.getmembers(module, inspect.isclass):
		traceClass(cls)

	REGISTERED_MODULES.add(module)

	setTraced(module)

	return True

def untraceModule(module):
	"""
	This definition untraces given module.

	:param module: Module to untrace. ( Module )
	:return: Definition success. ( Boolean )
	"""

	for name, function in inspect.getmembers(module, inspect.isfunction):
		setattr(module, name, untracer(function))

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
		if isTraced(module):
			continue

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
