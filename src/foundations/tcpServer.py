#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcpServer.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`TcpServer`class and other helpers objects needed to run a **Python** socket server.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import SocketServer
import logging
import socket
import threading

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "EchoRequestsHandler", "TcpServer"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EchoRequestsHandler(SocketServer.BaseRequestHandler):
	"""
	This class represents the default requests handler.
	"""

	@core.executionTrace
	def handle(self):
		"""
		This method reimplements the :meth:`SocketServer.BaseRequestHandler.handle` method.
	
		:return: Method success. ( Boolean )
		"""

		while True:
			data = self.request.recv(1024)
			if not data:
				break

			self.request.send(data)
		return True

class TcpServer(object):
	"""
	This class defines a TCP server.
	"""

	@core.executionTrace
	def __init__(self, address, port, handler=EchoRequestsHandler):
		"""
		This method initializes the class.
		
		Usage::
			
			>>> tcpServer = TcpServer("127.0.0.1", 16384)
			>>> tcpServer.start()
			True
			>>> tcpServer.stop()
			True

		:param address: Server address. ( String )
		:param port: Server port list. ( Integer )
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
		This method is the property for **self.__address** attribute.

		:return: self.__address. ( String )
		"""

		return self.__address

	@address.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def address(self, value):
		"""
		This method is the setter method for **self.__address** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"address", value)
		self.__address = value

	@address.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def address(self):
		"""
		This method is the deleter method for **self.__address** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "address"))

	@property
	def port(self):
		"""
		This method is the property for **self.__port** attribute.

		:return: self.__port. ( Integer )
		"""

		return self.__port

	@port.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def port(self, value):
		"""
		This method is the setter method for **self.__port** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format(
			"port", value)
			assert type(value) >= 0 and type(value) >= 65535, \
			"'{0}' attribute: '{1}' value must be in 0-65535 range!".format("port", value)
		self.__port = value

	@port.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def port(self):
		"""
		This method is the deleter method for **self.__port** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "port"))

	@property
	def handler(self):
		"""
		This method is the property for **self.__handler** attribute.

		:return: self.__handler. ( String )
		"""

		return self.__handler

	@handler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def handler(self, value):
		"""
		This method is the setter method for **self.__handler** attribute.

		:param value: Attribute value. ( SocketServer.BaseRequestHandler )
		"""

		if value is not None:
			assert issubclass(value, SocketServer.BaseRequestHandler), \
			"'{0}' attribute: '{1}' is not 'SocketServer.BaseRequestHandler' subclass!".format("handler", value)
		self.__handler = value

	@handler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def handler(self):
		"""
		This method is the deleter method for **self.__handler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "handler"))

	@property
	def online(self):
		"""
		This method is the property for **self.__online** attribute.

		:return: self.__online. ( String )
		"""

		return self.__online

	@online.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def online(self, value):
		"""
		This method is the setter method for **self.__online** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "online"))

	@online.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def online(self):
		"""
		This method is the deleter method for **self.__online** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "online"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ServerOperationError)
	def start(self):
		"""
		This method  starts the TCP server.

		:return: Method success. ( Boolean )
		"""

		if self.__online:
			raise foundations.exceptions.ServerOperationError(
			"{0} | '{1}' server is already online!".format(self.__class__.__name__, self))

		try:
			self.__server = SocketServer.TCPServer((self.__address, self.__port), self.__handler)
			self.__worker = threading.Thread(target=self.__server.serve_forever)
			self.__worker.setDaemon(True)
			self.__worker.start()
			self.__online = True
			LOGGER.info(
			"{0} | Server successfully started on '{1}' address and '{2}' port using '{3}' requests handler!".format(
			self.__class__.__name__, self.__address, self.__port, self.__handler.__name__))
			return True
		except socket.error as error:
			if error.errno == 10048:
				LOGGER.warning(
				"{0} | Cannot start server, a connection is already opened on port '{2}'!".format(
				self.__class__.__name__, self, self.__port))
			else:
				raise error

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ServerOperationError)
	def stop(self):
		"""
		This method stops the TCP server.

		:return: Method success. ( Boolean )
		"""

		if not self.__online:
			raise foundations.exceptions.ServerOperationError(
			"{0} | '{1}' server is not online!".format(self.__class__.__name__, self))

		self.__server.shutdown()
		self.__server = None
		self.__worker = None
		self.__online = False
		LOGGER.info("{0} | Server successfully stopped!".format(self.__class__.__name__))
		return True
