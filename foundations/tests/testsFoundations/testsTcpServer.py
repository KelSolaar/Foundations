#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**testsTCPServer.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.tcpServer` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import socket
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from foundations.tcpServer import TCPServer
from foundations.tcpServer import EchoRequestsHandler

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TCPServerTestCase", "EchoRequestsHandlerTestCase"]


#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TCPServerTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.tcpServer.TCPServer` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("address", "port", "handler", "online")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(TCPServer))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("start", "stop")

		for method in requiredMethods:
			self.assertIn(method, dir(TCPServer))

	def testStart(self):
		"""
		This method tests :meth:`foundations.tcpServer.TCPServer.start` method.
		"""

		tcpServer = TCPServer("127.0.0.1", 16384)
		self.assertTrue(tcpServer.start())
		self.assertEqual(tcpServer.online, True)
		tcpServer.stop()

	def testStop(self):
		"""
		This method tests :meth:`foundations.tcpServer.TCPServer.stop` method.
		"""

		tcpServer = TCPServer("127.0.0.1", 16384)
		tcpServer.start()
		self.assertTrue(tcpServer.stop())
		self.assertEqual(tcpServer.online, False)

class EchoRequestsHandlerTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.tcpServer.EchoRequestsHandler` class units tests methods.
	"""

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		requiredMethods = ("handle",)

		for method in requiredMethods:
			self.assertIn(method, dir(EchoRequestsHandler))

	def testHandle(self):
		"""
		This method tests :meth:`foundations.tcpServer.TCPServer.handle` method.
		"""

		tcpServer = TCPServer("127.0.0.1", 16384)
		tcpServer.start()
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.connect(("127.0.0.1", 16384))
		data = "Hello World!"
		connection.send(data)
		self.assertEqual(connection.recv(1024), data)
		connection.close()
		tcpServer.stop()

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
