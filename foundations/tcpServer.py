#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcpServer.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`TCPServer` class and other helpers objects needed to run a **Python** socket server.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import errno
import SocketServer
import socket
import threading

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "EchoRequestsHandler", "TCPServer"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EchoRequestsHandler(SocketServer.BaseRequestHandler):
	"""
	Defines the default echo requests handler.
	"""

	def handle(self):
		"""
		Reimplements the :meth:`SocketServer.BaseRequestHandler.handle` method.
	
		:return: Method success.
		:rtype: bool
		"""

		while True:
			data = self.request.recv(1024)
			if not data:
				break

			self.request.send(data)
		return True

class TCPServer(object):
	"""
	Defines a TCP server.
	"""

	def __init__(self, address, port, handler=EchoRequestsHandler):
		"""
		Initializes the class.
		
		Usage::
			
			>>> tcpServer = TCPServer("127.0.0.1", 16384)
			>>> tcpServer.start()
			True
			>>> tcpServer.stop()
			True

		:param address: Server address.
		:type address: unicode
		:param port: Server port list.
		:type port: int
		:param handler: Request handler. ( SocketServer.BaseRequestHandler )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		self.__address = None
		self.address = address
		self.__port = None
		self.port = port
		self.__handler = None
		self.handler = handler

		self.__server = None
		self.__worker = None
		self.__online = False

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def address(self):
		"""
		Property for **self.__address** attribute.

		:return: self.__address.
		:rtype: unicode
		"""

		return self.__address

	@address.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def address(self, value):
		"""
		Setter for **self.__address** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"address", value)
		self.__address = value

	@address.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def address(self):
		"""
		Deleter for **self.__address** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "address"))

	@property
	def port(self):
		"""
		Property for **self.__port** attribute.

		:return: self.__port.
		:rtype: int
		"""

		return self.__port

	@port.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def port(self, value):
		"""
		Setter for **self.__port** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format(
			"port", value)
			assert type(value) >= 0 and type(value) >= 65535, \
			"'{0}' attribute: '{1}' value must be in 0-65535 range!".format("port", value)
		self.__port = value

	@port.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def port(self):
		"""
		Deleter for **self.__port** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "port"))

	@property
	def handler(self):
		"""
		Property for **self.__handler** attribute.

		:return: self.__handler.
		:rtype: unicode
		"""

		return self.__handler

	@handler.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def handler(self, value):
		"""
		Setter for **self.__handler** attribute.

		:param value: Attribute value. ( SocketServer.BaseRequestHandler )
		"""

		if value is not None:
			assert issubclass(value, SocketServer.BaseRequestHandler), \
			"'{0}' attribute: '{1}' is not 'SocketServer.BaseRequestHandler' subclass!".format("handler", value)
		self.__handler = value
		self.__handler.container = self

	@handler.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def handler(self):
		"""
		Deleter for **self.__handler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "handler"))

	@property
	def online(self):
		"""
		Property for **self.__online** attribute.

		:return: self.__online.
		:rtype: unicode
		"""

		return self.__online

	@online.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def online(self, value):
		"""
		Setter for **self.__online** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "online"))

	@online.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def online(self):
		"""
		Deleter for **self.__online** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "online"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.handleExceptions(foundations.exceptions.ServerOperationError)
	def start(self):
		"""
		Starts the TCP server.

		:return: Method success.
		:rtype: bool
		"""

		if self.__online:
			raise foundations.exceptions.ServerOperationError(
			"{0} | '{1}' TCP Server is already online!".format(self.__class__.__name__, self))

		try:
			self.__server = SocketServer.TCPServer((self.__address, self.__port), self.__handler)
			self.__worker = threading.Thread(target=self.__server.serve_forever)
			self.__worker.setDaemon(True)
			self.__worker.start()
			self.__online = True
			LOGGER.info(
			"{0} | TCP Server successfully started with '{1}' address on '{2}' port using '{3}' requests handler!".format(
			self.__class__.__name__, self.__address, self.__port, self.__handler.__name__))
			return True
		except socket.error as error:
			if error.errno in (errno.EADDRINUSE, errno.EADDRNOTAVAIL):
				LOGGER.warning(
				"!> {0} | Cannot start TCP Server, address is already in use on port '{1}'!".format(
				self.__class__.__name__, self.__port))
			else:
				raise error

	@foundations.exceptions.handleExceptions(foundations.exceptions.ServerOperationError)
	def stop(self, terminate=False):
		"""
		Stops the TCP server.

		:return: Method success.
		:rtype: bool
		"""

		if not self.__online:
			raise foundations.exceptions.ServerOperationError(
			"{0} | '{1}' TCP Server is not online!".format(self.__class__.__name__, self))

		if not terminate:
			self.__server.shutdown()
		else:
			self.__server._BaseServer__shutdown_request = True

		self.__server = None
		self.__worker = None
		self.__online = False

		LOGGER.info("{0} | TCP Server successfully stopped!".format(self.__class__.__name__))
		return True
