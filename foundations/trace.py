import functools
import inspect
import re
import sys

REGISTERED_MODULES = set()

TRACER_SYMBOL = "_trace__tracer__"
UNTRACER_SYMBOL = "_trace__untracer__"

def getName(item):
	" Return an item's name. "
	return item.__name__

def isClassMethod(method):
	" Determine if an instancemethod is a classmethod. "
	return method.im_self is not None

def getMethodName(method):
	""" Return a method's name.
	
	This function returns the name the method is accessed by from
	outside the class (i.e. it prefixes "private" methods appropriately).
	"""
	name = getName(method)
	if name.startswith("__") and not name.endswith("__"):
		name = "_%s%s" % (getName(method.im_class), name)
	return name

def formatArguments(arg_val):
	""" Return a string representing a (name, value) pair.

	>>> formatArguments(('x', (1, 2, 3)))
	'x=(1, 2, 3)'
	"""
	arg, val = arg_val
	return "%s=%r" % (arg, val)

def tracer(function):
	""" Echo calls to a function.

	Returns a decorated version of the input function which "tracees" calls
	made to it by writing out the function's name and the arguments it was
	called with.
	"""

	@functools.wraps(function)
	def wrapped(*args, **kwargs):
		# print inspect.currentframe().f_back.f_code.co_name

		code = function.func_code
		argsCount = code.co_argcount
		argsNames = code.co_varnames[:argsCount]
		functionDefaults = function.func_defaults or list()
		argsDefaults = dict(zip(argsNames[-len(functionDefaults):], functionDefaults))

		positionalArgs = map(formatArguments, zip(argsNames, args))
		defaultedArgs = [formatArguments((name, argsDefaults[name])) for name in argsNames[len(args):] if name not in kwargs]
		namelessArgs = map(repr, args[argsCount:])
		keywordArgs = map(formatArguments, kwargs.items())
		sys.stdout.write("{0}.({1})\n".format(getName(function),
											", ".join(positionalArgs + defaultedArgs + namelessArgs + keywordArgs)))
		return function(*args, **kwargs)
	return wrapped

def untracer(function):
	@functools.wraps(function)
	def wrapped(*args, **kwargs):
		return function(*args, **kwargs)
	setattr(wrapped, UNTRACER_SYMBOL, True)
	return wrapped

def traceInstancemethod(cls, method, tracer=tracer):
	""" Change an instancemethod so that calls to it are traceed.

	Replacing a classmethod is a little more tricky.
	See: http://www.python.org/doc/current/ref/types.html
	"""
	name = getMethodName(method)
	if name in ("__str__", "__repr__") or method.__dict__.get(UNTRACER_SYMBOL):
		return

	if isClassMethod(method):
		setattr(cls, name, classmethod(tracer(method.im_func)))
	else:
		setattr(cls, name, tracer(method))

def traceClass(cls, tracer=tracer):
	""" Echo calls to class methods and static functions
	"""
	for name, method in inspect.getmembers(cls, inspect.ismethod):
		if method.__dict__.get(UNTRACER_SYMBOL):
			continue

		traceInstancemethod(cls, method)

	for name, function in inspect.getmembers(cls, inspect.isfunction):
		if function.__dict__.get(UNTRACER_SYMBOL):
			continue

		setattr(cls, getName(function), staticmethod(tracer(function)))

	for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
		if accessor.fget.__dict__.get(UNTRACER_SYMBOL) or \
		accessor.fset.__dict__.get(UNTRACER_SYMBOL) or \
		accessor.fdel.__dict__.get(UNTRACER_SYMBOL):
			continue

		setattr(cls, name, property(tracer(accessor.fget),
									tracer(accessor.fset),
									tracer(accessor.fdel)))

def traceModule(module, tracer=tracer):
	""" Echo calls to functions and methods in a module.
	"""
	for name, function in inspect.getmembers(module, inspect.isfunction):
		if function.__dict__.get(UNTRACER_SYMBOL):
			continue

		setattr(module, name, tracer(function))

	for name, cls in inspect.getmembers(module, inspect.isclass):
		traceClass(cls)

def registerModule(module=None):
	global REGISTERED_MODULES
	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])
	REGISTERED_MODULES.add(module)

def installTracer(pattern=r".*", flags=0):
	for module in REGISTERED_MODULES:
		if hasattr(module, TRACER_SYMBOL):
			continue

		if not re.search(pattern, module.__name__, flags=flags):
			continue

		traceModule(module)
		setattr(module, TRACER_SYMBOL, True)
