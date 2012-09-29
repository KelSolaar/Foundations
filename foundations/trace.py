import functools
import inspect
import sys

TRACED_MODULES = set()

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

def defaultTracer(fn):
	""" Echo calls to a function.

	Returns a decorated version of the input function which "tracees" calls
	made to it by writing out the function's name and the arguments it was
	called with.
	"""
	# Unpack function's arg count, arg names, arg defaults
	code = fn.func_code
	argcount = code.co_argcount
	argnames = code.co_varnames[:argcount]
	fn_defaults = fn.func_defaults or list()
	argdefs = dict(zip(argnames[-len(fn_defaults):], fn_defaults))

	@functools.wraps(fn)
	def wrapped(*v, **k):
		# Collect function arguments by chaining together positional,
		# defaulted, extra positional and keyword arguments.
		positional = map(formatArguments, zip(argnames, v))
		defaulted = [formatArguments((a, argdefs[a])) for a in argnames[len(v):] if a not in k]
		nameless = map(repr, v[argcount:])
		keyword = map(formatArguments, k.items())
		args = positional + defaulted + nameless + keyword
		print("%s(%s)" % (getName(fn), ", ".join(args)))
		return fn(*v, **k)
	return wrapped

def traceInstancemethod(cls, method, tracer=defaultTracer):
	""" Change an instancemethod so that calls to it are traceed.

	Replacing a classmethod is a little more tricky.
	See: http://www.python.org/doc/current/ref/types.html
	"""
	name = getMethodName(method)
	if name in ("__str__", "__repr__"):
		return

	if isClassMethod(method):
		setattr(cls, name, classmethod(tracer(method.im_func)))
	else:
		setattr(cls, name, tracer(method))

def traceClass(cls, tracer=defaultTracer):
	""" Echo calls to class methods and static functions
	"""
	for name, method in inspect.getmembers(cls, inspect.ismethod):
		traceInstancemethod(cls, method)
	for name, fn in inspect.getmembers(cls, inspect.isfunction):
		setattr(cls, getName(fn), staticmethod(tracer(fn)))
	for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
		setattr(cls, name, property(tracer(accessor.fget),
									tracer(accessor.fset),
									tracer(accessor.fdel)))

def traceModule(module, tracer=defaultTracer):
	""" Echo calls to functions and methods in a module.
	"""
	for fname, fn in inspect.getmembers(module, inspect.isfunction):
		setattr(module, fname, tracer(fn))
	for name, cls in inspect.getmembers(module, inspect.isclass):
		traceClass(cls)

def registerModule(module=None):
	global TRACED_MODULES
	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])
	TRACED_MODULES.add(module)

def installTracer():
	for module in TRACED_MODULES:
		if hasattr(module, "__trace__"):
			continue

		traceModule(module)
		module.__trace__ = True
