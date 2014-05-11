#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**verbose.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package verbose and logging objects.

**Others:**

"""

from __future__ import unicode_literals

import functools
import hashlib
import inspect
import itertools
import logging
import sys
import threading
import tempfile

import foundations.trace
from foundations.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["THREADS_IDENTIFIERS",
		   "INDENT_LEVEL",
		   "to_string",
		   "LOGGER",
		   "LOGGING_DEFAULT_FORMATTER",
		   "LOGGING_EXTENDED_FORMATTER",
		   "LOGGING_STANDARD_FORMATTER",
		   "TRACER_LOGGING_FUNCTION",
		   "Streamer"
		   "StandardOutputStreamer",
		   "indent_message",
		   "tracer",
		   "install_logger",
		   "uninstall_logger",
		   "get_logging_console_handler",
		   "get_logging_file_handler",
		   "get_logging_stream_handler",
		   "remove_logging_handler",
		   "set_verbosity_level"]

THREADS_IDENTIFIERS = {}

INDENT_LEVEL = 0

def to_unicode(data, encoding=Constants.default_codec, errors=Constants.codec_error):
	"""
	Converts given data to unicode string using package default settings, fighting **The Hell**!

	Usage::

		>>> to_unicode("myData")
		u'myData'
		>>> to_unicode("汉字/漢字")
		u'\u6c49\u5b57/\u6f22\u5b57'

	:param data: Data to convert.
	:type data: object
	:param encoding: File encoding codec.
	:type encoding: unicode
	:param errors: File encoding errors handling.
	:type errors: unicode
	:return: Unicode data.
	:rtype: unicode
	"""

	if isinstance(data, type("")):
		return data
	else:
		try:
			return unicode(data, encoding, errors)
		except TypeError:
			return unicode(str(data), encoding, errors)

def _LogRecord__getattribute__(self, attribute):
	"""
	Overrides logging.LogRecord.__getattribute__ method
	in order to manipulate requested attributes values.

	:param attribute: Attribute name.
	:type attribute: unicode
	:return: Modified method.
	:rtype: object
	"""

	if attribute == "__dict__":
		thread_ident = threading.currentThread().ident
		if not thread_ident in THREADS_IDENTIFIERS:
			THREADS_IDENTIFIERS[thread_ident] = (threading.currentThread().name,
												hashlib.md5(threading.currentThread().name).hexdigest()[:8])
		object.__getattribute__(self, attribute)["threadName"] = THREADS_IDENTIFIERS[thread_ident][1]
		return object.__getattribute__(self, attribute)
	else:
		return object.__getattribute__(self, attribute)

logging.LogRecord.__getattribute__ = _LogRecord__getattribute__

def _LogRecord_msg():
	"""
	Overrides logging.LogRecord.msg attribute to ensure variable content is stored as unicode.
	"""

	def _LogRecord_msgProperty(self):
		return self.__msg

	def _LogRecord_msgSetter(self, value):
		self.__msg = to_unicode(value)

	logging.LogRecord.msg = property(_LogRecord_msgProperty, _LogRecord_msgSetter)

_LogRecord_msg()

LOGGER = logging.getLogger(Constants.logger)

LOGGING_DEFAULT_FORMATTER = logging.Formatter("%(levelname)-8s: %(message)s")
LOGGING_EXTENDED_FORMATTER = logging.Formatter("%(asctime)s - %(threadName)s - %(levelname)-8s: %(message)s")
LOGGING_STANDARD_FORMATTER = logging.Formatter()

TRACER_LOGGING_FUNCTION = LOGGER.info

class Streamer(object):
	"""
	Defines a stream object for :class:`logging.StreamHandler` logging handler.
	"""

	def __init__(self, stream=None):
		"""
		Initializes the class.

		:param stream: Stream object.
		:type stream: object
		"""

		self.__stream = []

	@property
	def stream(self):
		"""
		Property for **self.__stream** attribute.

		:return: self.__stream.
		:rtype: list
		"""

		return self.__stream

	@stream.setter
	def stream(self, value):
		"""
		Setter for **self.__stream** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("stream", value)
		self.__stream = value

	@stream.deleter
	def stream(self):
		"""
		Deleter for **self.__stream** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "stream"))

	def write(self, message):
		"""
		Provides write ability to the class.

		:param message: Current message.
		:type message: unicode
		"""

		self.__stream.append(message)

	def flush(self):
		"""
		Flushes the current stream.
		"""

		pass

class StandardOutputStreamer(object):
	"""
	| Defines a redirection object intented to be used for :data:`sys.stdout` and :data:`sys.stderr` streams.
	| Logging messages will be written to given logger handlers.
	"""

	def __init__(self, logger):
		"""
		Initializes the class.

		:param logger: Logger.
		:type logger: object
		"""

		self.__logger = logger

	@property
	def logger(self):
		"""
		Property for **self.__logger** attribute.

		:return: self.__logger.
		:rtype: Logger
		"""

		return self.__logger

	@logger.setter
	def logger(self, value):
		"""
		Setter for **self.__logger** attribute.

		:param value: Attribute value.
		:type value: Logger
		"""

		raise Exception("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "logger"))

	@logger.deleter
	def logger(self):
		"""
		Deleter for **self.__logger** attribute.
		"""

		raise Exception("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "logger"))

	def write(self, message):
		"""
		Writes given message to logger handlers.

		:param message: Message.
		:type message: unicode
		:return: Method success.
		:rtype: bool
		"""

		for handler in self.__logger.__dict__["handlers"]:
			handler.stream.write(message)
		return True

def indent_message(message):
	"""
	Idents given message using the attr`INDENT_LEVEL` attribute value.

	:param message: Message to indent.
	:type message: unicode
	:return: indented message.
	:rtype: unicode
	"""

	return "{0}{1}".format(" " * 4 * INDENT_LEVEL, message)

def tracer(object):
	"""
	| Traces execution.
	| Any method / definition decorated will have it's execution traced through debug messages.
	| Both object entry and exit are logged.

	Entering in an object::

		INFO    : ---> foundations.environment.get_user_application_data_directory() <<<---

	Exiting from an object::

		INFO   : <--- foundations.environment.get_system_application_data_directory() ^ '...' --->

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	@functools.partial(foundations.trace.validate_tracer, object)
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

		global INDENT_LEVEL

		trace_name = foundations.trace.get_trace_name(object)

		code = object.func_code
		args_count = code.co_argcount
		args_names = code.co_varnames[:args_count]
		function_defaults = object.func_defaults or list()
		args_defaults = dict(zip(args_names[-len(function_defaults):], function_defaults))

		positional_args = map(foundations.trace.format_argument, zip(args_names, args))
		defaulted_args = [foundations.trace.format_argument((name, args_defaults[name])) \
						 for name in args_names[len(args):] if name not in kwargs]
		nameless_args = map(repr, args[args_count:])
		keyword_args = map(foundations.trace.format_argument, kwargs.items())
		TRACER_LOGGING_FUNCTION(indent_message("---> {0}({1}) <---".format(trace_name,
																		  ", ".join(itertools.chain(positional_args,
																									defaulted_args,
																									nameless_args,
																									keyword_args)))))

		INDENT_LEVEL += 1
		value = object(*args, **kwargs)
		INDENT_LEVEL -= 1

		TRACER_LOGGING_FUNCTION(indent_message("<--- {0} ^ {1} --->".format(trace_name, repr(value))))

		return value

	return tracer_wrapper

def install_logger(logger=None, module=None):
	"""
	Installs given logger in given module or default logger in caller introspected module.

	:param logger: Logger to install.
	:type logger: Logger
	:param module: Module.
	:type module: ModuleType
	:return: Logger.
	:rtype: Logger
	"""

	logger = logging.getLogger(Constants.logger) if logger is None else logger
	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])
	setattr(module, "LOGGER", logger)

	foundations.trace.register_module(module)

	return logger

def uninstall_logger(logger=None, module=None):
	"""
	Uninstalls given logger in given module or default logger in caller introspected module.

	:param logger: Logger to uninstall.
	:type logger: Logger
	:param module: Module.
	:type module: ModuleType
	:return: Definition success.
	:rtype: bool
	"""

	logger = logging.getLogger(Constants.logger) if logger is None else logger
	if module is None:
		# Note: inspect.getmodule() can return the wrong module if it has been imported with different relatives paths.
		module = sys.modules.get(inspect.currentframe().f_back.f_globals["__name__"])
	hasattr(module, "LOGGER") and delattr(module, "LOGGER")
	return True

def get_logging_console_handler(logger=None, formatter=LOGGING_DEFAULT_FORMATTER):
	"""
	Adds a logging console handler to given logger or default logger.

	:param logger: Logger to add the handler to.
	:type logger: Logger
	:param formatter: Handler formatter.
	:type formatter: Formatter
	:return: Added handler.
	:rtype: Handler
	"""

	logger = LOGGER if logger is None else logger
	logging_console_handler = logging.StreamHandler(sys.__stdout__)
	logging_console_handler.setFormatter(formatter)
	logger.addHandler(logging_console_handler)
	return logging_console_handler

def get_logging_file_handler(logger=None, file=None, formatter=LOGGING_DEFAULT_FORMATTER):
	"""
	Adds a logging file handler to given logger or default logger using given file.

	:param logger: Logger to add the handler to.
	:type logger: Logger
	:param file: File to verbose into.
	:type file: unicode
	:param formatter: Handler formatter.
	:type formatter: Formatter
	:return: Added handler.
	:rtype: Handler
	"""

	logger = LOGGER if logger is None else logger
	file = tempfile.NamedTemporaryFile().name if file is None else file
	logging_file_handler = logging.FileHandler(file)
	logging_file_handler.setFormatter(formatter)
	logger.addHandler(logging_file_handler)
	return logging_file_handler

def get_logging_stream_handler(logger=None, formatter=LOGGING_DEFAULT_FORMATTER):
	"""
	Adds a logging stream handler to given logger or default logger using given file.

	:param logger: Logger to add the handler to.
	:type logger: Logger
	:param file: File to verbose into.
	:type file: unicode
	:param formatter: Handler formatter.
	:type formatter: Formatter
	:return: Added handler.
	:rtype: Handler
	"""

	logger = LOGGER if logger is None else logger
	logging_stream_handler = logging.StreamHandler(Streamer())
	logging_stream_handler.setFormatter(formatter)
	logger.addHandler(logging_stream_handler)
	return logging_stream_handler

def remove_logging_handler(handler, logger=None):
	"""
	Removes given logging handler from given logger.

	:param handler: Handler.
	:type handler: Handler
	:param logger: Handler logger.
	:type logger: Logger
	:return: Definition success.
	:rtype: bool
	"""

	logger = LOGGER if logger is None else logger
	logger.handlers and LOGGER.debug("> Stopping handler: '{0}'.".format(handler))
	logger.removeHandler(handler)
	return True

def set_verbosity_level(verbosity_level=3, logger=None):
	"""
	Defines logging verbosity level.

	Available verbosity levels::

		0: Critical.
		1: Error.
		2: Warning.
		3: Info.
		4: Debug.

	:param verbosity_level: Verbosity level.
	:type verbosity_level: int
	:param logger: Logger to set the verbosity level to.
	:type logger: Logger
	:return: Definition success.
	:rtype: bool
	"""

	logger = LOGGER if logger is None else logger
	if verbosity_level == 0:
		logger.setLevel(logging.CRITICAL)
		logging.disable(logging.ERROR)
	elif verbosity_level == 1:
		logger.setLevel(logging.ERROR)
		logging.disable(logging.WARNING)
	elif verbosity_level == 2:
		logger.setLevel(logging.WARNING)
		logging.disable(logging.INFO)
	elif verbosity_level == 3:
		logger.setLevel(logging.INFO)
		logging.disable(logging.DEBUG)
	elif verbosity_level == 4:
		logger.setLevel(logging.DEBUG)
		logging.disable(logging.NOTSET)
	return True
