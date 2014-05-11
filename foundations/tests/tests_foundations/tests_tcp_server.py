#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**testsTCPServer.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.tcp_server` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
from foundations.tcp_server import TCPServer
from foundations.tcp_server import EchoRequestsHandler

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestTCPServer", "TestEchoRequestsHandler"]


#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TestTCPServer(unittest.TestCase):
	"""
	Defines :class:`foundations.tcp_server.TCPServer` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("address", "port", "handler", "online")

		for attribute in required_attributes:
			self.assertIn(attribute, dir(TCPServer))

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("start", "stop")

		for method in required_methods:
			self.assertIn(method, dir(TCPServer))

	def test_start(self):
		"""
		Tests :meth:`foundations.tcp_server.TCPServer.start` method.
		"""

		tcp_server = TCPServer("127.0.0.1", 16384)
		self.assertTrue(tcp_server.start())
		self.assertEqual(tcp_server.online, True)
		tcp_server.stop()

	def test_stop(self):
		"""
		Tests :meth:`foundations.tcp_server.TCPServer.stop` method.
		"""

		tcp_server = TCPServer("127.0.0.1", 16384)
		tcp_server.start()
		self.assertTrue(tcp_server.stop())
		self.assertEqual(tcp_server.online, False)

class TestEchoRequestsHandler(unittest.TestCase):
	"""
	Defines :class:`foundations.tcp_server.EchoRequestsHandler` class units tests methods.
	"""

	def test_required_methods(self):
		"""
		Tests presence of required methods.
		"""

		required_methods = ("handle",)

		for method in required_methods:
			self.assertIn(method, dir(EchoRequestsHandler))

	def test_handle(self):
		"""
		Tests :meth:`foundations.tcp_server.TCPServer.handle` method.
		"""

		tcp_server = TCPServer("127.0.0.1", 16384)
		tcp_server.start()
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.connect(("127.0.0.1", 16384))
		data = "Hello World!"
		connection.send(data)
		self.assertEqual(connection.recv(1024), data)
		connection.close()
		tcp_server.stop()

if __name__ == "__main__":
	import foundations.tests.utilities
	unittest.main()
