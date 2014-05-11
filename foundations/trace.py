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

from __future__ import unicode_literals

import ast
import functools
import inspect
import re
import sys
import itertools

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
            "is_read_only",
            "set_tracer_hook",
            "get_tracer_hook",
            "is_traced",
            "is_base_traced",
            "is_untracable",
            "set_traced",
            "set_untraced",
            "set_untracable",
            "trace_walker",
            "get_object_name",
            "get_trace_name",
            "get_method_name",
            "is_static_method",
            "is_class_method",
            "format_argument",
            "validate_tracer",
            "tracer",
            "untracer",
            "untracable",
            "trace_function",
            "untrace_function",
            "trace_method",
            "untrace_method",
            "trace_property",
            "untrace_property",
            "trace_class",
            "untrace_class",
            "trace_module",
            "untrace_module",
            "register_module",
            "install_tracer",
            "evaluate_trace_request"]

REGISTERED_MODULES = set()

TRACER_SYMBOL = "_trace__tracer__"
UNTRACABLE_SYMBOL = "_trace__untracable__"

TRACER_HOOK = "_trace__hook__"

UNTRACABLE_NAMES = ("__str__", "__repr__")

NULL_OBJECT_NAME = "None"

TRACE_NAMES_CACHE = {}
TRACE_WALKER_CACHE = {}

def is_read_only(object):
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

def set_tracer_hook(object, hook):
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

def get_tracer_hook(object):
    """
    Returns given object tracer hook.

    :param object: Object.
    :type object: object
    :return: Object tracer hook.
    :rtype: object
    """

    if hasattr(object, TRACER_HOOK):
        return getattr(object, TRACER_HOOK)

def is_traced(object):
    """
    Returns if given object is traced.

    :param object: Object.
    :type object: object
    :return: Is object traced.
    :rtype: bool
    """

    return hasattr(object, TRACER_SYMBOL)

def is_base_traced(cls):
    """
    Returns if given class has a traced base.

    :param cls: Class.
    :type cls: object
    :return: Is base traced.
    :rtype: bool
    """

    for base in cls.mro()[1:]:
        if is_traced(base):
            return True
    return False

def is_untracable(object):
    """
    Returns if given object is untracable.

    :param object: Object.
    :type object: object
    :return: Is object untracable.
    :rtype: bool
    """

    return hasattr(object, UNTRACABLE_SYMBOL)

def set_traced(object):
    """
    Sets given object as traced.

    :param object: Object.
    :type object: object
    :return: Definition success.
    :rtype: bool
    """

    setattr(object, TRACER_SYMBOL, True)
    return True

def set_untraced(object):
    """
    Sets given object as untraced.

    :param object: Object.
    :type object: object
    :return: Definition success.
    :rtype: bool
    """

    if is_traced(object):
        delattr(object, TRACER_SYMBOL)
    return True

def set_untracable(object):
    """
    Sets given object as untraced.

    :param object: Object.
    :type object: object
    :return: Definition success.
    :rtype: bool
    """

    setattr(object, UNTRACABLE_SYMBOL, True)
    return True

def trace_walker(module):
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

def get_object_name(object):
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

def get_trace_name(object):
    """
    Returns given object trace name.

    :param object: Object.
    :type object: object
    :return: Object trace name.
    :rtype: unicode
    """

    global TRACE_NAMES_CACHE
    global TRACE_WALKER_CACHE

    trace_name = TRACE_NAMES_CACHE.get(object)
    if trace_name is None:

        TRACE_NAMES_CACHE[object] = trace_name = get_object_name(object)

        if type(object) is property:
            object = object.fget

        module = inspect.getmodule(object)
        if module is None:
            return

        members = TRACE_WALKER_CACHE.get(module)
        if members is None:
            TRACE_WALKER_CACHE[module] = members = tuple(trace_walker(module))

        for (cls, member) in members:
            if object in (cls, untracer(member)):
                TRACE_NAMES_CACHE[object] = trace_name = \
                ".".join(map(get_object_name, filter(lambda x: x is not None, (module, cls, member))))
                break

    return trace_name

def get_method_name(method):
    """
    Returns given method name.

    :param method: Method to retrieve the name.
    :type method: object
    :return: Method name.
    :rtype: unicode
    """

    name = get_object_name(method)
    if name.startswith("__") and not name.endswith("__"):
        name = "_{0}{1}".format(get_object_name(method.im_class), name)
    return name

def is_static_method(method):
    """
    Returns if given method is a static method.

    :param method: Method.
    :type method: object
    :return: Is static method.
    :rtype: bool
    """

    return type(method) is type(lambda x: None)

def is_class_method(method):
    """
    Returns if given method is a class method.

    :param method: Method.
    :type method: object
    :return: Is class method.
    :rtype: bool
    """

    if is_static_method(method):
        return False

    return method.im_self is not None

def format_argument(argumentValue):
    """
    Returns a string representing an argument / value pair.

    Usage::

        >>> format_argument(('x', (0, 1, 2)))
        u'x=(0, 1, 2)'

    :param argumentValue: Argument / value pair.
    :type argumentValue: tuple
    :return: Formatted .argument / value pair.
    :rtype: unicode
    """

    return "{0}={1!r}".format(*argumentValue)

def validate_tracer(*args):
    """
    Validate and finishes a tracer by adding mandatory extra attributes.

    :param \*args: Arguments.
    :type \*args: \*
    :return: Validated wrapped object.
    :rtype: object
    """

    object, wrapped = args
    if is_traced(object) or is_untracable(object) or get_object_name(object) in UNTRACABLE_NAMES:
        return object

    set_tracer_hook(wrapped, object)
    set_traced(wrapped)

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
    @functools.partial(validate_tracer, object)
    def tracer_wrapper(*args, **kwargs):
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
        args_count = code.co_argcount
        args_names = code.co_varnames[:args_count]
        function_defaults = object.func_defaults or list()
        args_defaults = dict(zip(args_names[-len(function_defaults):], function_defaults))

        positional_args = map(format_argument, zip(args_names, args))
        defaulted_args = [format_argument((name, args_defaults[name])) for name in args_names[len(args):] if name not in kwargs]
        nameless_args = map(repr, args[args_count:])
        keyword_args = map(format_argument, kwargs.items())
        sys.stdout.write("{0}({1})\n".format(get_trace_name(object),
                                            ", ".join(itertools.chain(positional_args,
                                                                    defaulted_args,
                                                                    nameless_args,
                                                                    keyword_args))))
        return object(*args, **kwargs)

    return tracer_wrapper

def untracer(object):
    """
    Object is used to untrace given object.

    :param object: Object to untrace.
    :type object: object
    :return: Untraced object.
    :rtype: object
    """

    if is_traced(object):
        return get_tracer_hook(object)
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

    set_untracable(untracableWrapper)

    return untracableWrapper

def trace_function(module, function, tracer=tracer):
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

    if is_traced(function):
        return False

    name = get_object_name(function)
    if is_untracable(function) or name in UNTRACABLE_NAMES:
        return False

    setattr(module, name, tracer(function))
    return True

def untrace_function(module, function):
    """
    Untraces given module function.

    :param module: Module of the function.
    :type module: object
    :param function: Function to untrace.
    :type function: object
    :return: Definition success.
    :rtype: bool
    """

    if not is_traced(function):
        return False

    name = get_object_name(function)
    setattr(module, name, untracer(function))
    return True

def trace_method(cls, method, tracer=tracer):
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

    if is_traced(method):
        return False

    name = get_method_name(method)
    if is_untracable(method) or name in UNTRACABLE_NAMES:
        return False

    if is_class_method(method):
        setattr(cls, name, classmethod(tracer(method.im_func)))
    elif is_static_method(method):
        setattr(cls, name, staticmethod(tracer(method)))
    else:
        setattr(cls, name, tracer(method))
    return True

def untrace_method(cls, method):
    """
    Untraces given class method.

    :param cls: Class of the method.
    :type cls: object
    :param method: Method to untrace.
    :type method: object
    :return: Definition success.
    :rtype: bool
    """

    if not is_traced(method):
        return False

    name = get_method_name(method)
    if is_class_method(method):
        setattr(cls, name, classmethod(untracer(method)))
    elif is_static_method(method):
        setattr(cls, name, staticmethod(untracer(method)))
    else:
        setattr(cls, name, untracer(method))
    return True

def trace_property(cls, accessor, tracer=tracer):
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

    if is_traced(accessor.fget) and is_traced(accessor.fset) and is_traced(accessor.fdel):
        return False

    name = get_method_name(accessor)
    setattr(cls, name, property(tracer(accessor.fget),
                                tracer(accessor.fset),
                                tracer(accessor.fdel)))
    return True

def untrace_property(cls, accessor):
    """
    Untraces given class property.

    :param cls: Class of the property.
    :type cls: object
    :param accessor: Property to untrace.
    :type accessor: property
    :return: Definition success.
    :rtype: bool
    """

    if not is_traced(accessor.fget) or not is_traced(accessor.fset) or not is_traced(accessor.fdel):
        return False

    name = get_method_name(accessor)
    setattr(cls, name, property(untracer(accessor.fget),
                                untracer(accessor.fset),
                                untracer(accessor.fdel)))
    return True

def trace_class(cls, tracer=tracer, pattern=r".*", flags=0):
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

    if not is_base_traced(cls) and (is_traced(cls) or is_read_only(cls)):
        return False

    for name, method in inspect.getmembers(cls, inspect.ismethod):
        if not re.search(pattern, name, flags=flags):
            continue

        trace_method(cls, method, tracer)

    for name, function in inspect.getmembers(cls, inspect.isfunction):
        if not re.search(pattern, name, flags=flags):
            continue

        trace_method(cls, function, tracer)

    for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
        if not re.search(pattern, name, flags=flags):
            continue

        trace_property(cls, accessor, tracer)

    set_traced(cls)

    return True

def untrace_class(cls):
    """
    Untraces given class.

    :param cls: Class to untrace.
    :type cls: object
    :return: Definition success.
    :rtype: bool
    """

    for name, method in inspect.getmembers(cls, inspect.ismethod):
        untrace_method(cls, method)

    for name, function in inspect.getmembers(cls, inspect.isfunction):
        untrace_method(cls, function)

    for name, accessor in inspect.getmembers(cls, lambda x: type(x) is property):
        untrace_property(cls, accessor)

    set_untraced(cls)

    return True

def trace_module(module, tracer=tracer, pattern=r".*", flags=0):
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

    if is_traced(module):
        return False

    global REGISTERED_MODULES

    for name, function in inspect.getmembers(module, inspect.isfunction):
        if name not in module.__all__ or not re.search(pattern, name, flags=flags):
            continue

        trace_function(module, function, tracer)

    for name, cls in inspect.getmembers(module, inspect.isclass):
        if name not in module.__all__ or not re.search(pattern, name, flags=flags):
            continue

        trace_class(cls, tracer, pattern, flags)

    REGISTERED_MODULES.add(module)

    set_traced(module)

    return True

def untrace_module(module):
    """
    Untraces given module members.

    :param module: Module to untrace.
    :type module: ModuleType
    :return: Definition success.
    :rtype: bool
    """

    for name, function in inspect.getmembers(module, inspect.isfunction):
        untrace_function(module, function)

    for name, cls in inspect.getmembers(module, inspect.isclass):
        untrace_class(cls)

    set_untraced(module)

    return True

def register_module(module=None):
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

def install_tracer(tracer=tracer, pattern=r".*", flags=0):
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

        trace_module(module, tracer)
    return True

def uninstall_tracer(pattern=r".*", flags=0):
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
        if not is_traced(module):
            continue

        if not re.search(pattern, module.__name__, flags=flags):
            continue

        untrace_module(module)
    return True

def evaluate_trace_request(data, tracer=tracer):
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
        trace_module(sys.modules[module], tracer, pattern, flags)
    return True
