#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2010 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************s************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
************************************************************************************************
***	namespace.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Namespace Module.
***
***	Others:
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import core
from globals.constants import Constants

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)
NAMESPACE_SPLITTER = "|"

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
def setNamespace(namespace, attribute, namespaceSplitter=NAMESPACE_SPLITTER):
	"""
	This Definition Returns The Compounded Attribute And Compounded Namespace.

	@param namespace: Namespace. ( String )
	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace Splitter Character. ( String )
	@return: Namespaced Attribute. ( String )
	"""

	longName = str(namespace + namespaceSplitter + attribute)
	LOGGER.debug("> Namespace: '{0}', Attribute: '{1}', Long Name: '{2}'.".format(namespace, attribute, longName))
	return longName

@core.executionTrace
def getNamespace(attribute, namespaceSplitter=NAMESPACE_SPLITTER, rootOnly=False):
	"""
	This Definition Returns The Attribute Namespace.

	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace Splitter Character. ( String )
	@param rootOnly: Return Only Root Namespace. ( Boolean )
	@return: Attribute Namespace. ( String )
	"""

	attributeTokens = attribute.split(namespaceSplitter)
	if len(attributeTokens) == 1:
		LOGGER.debug("> Attribute: '{0}', Namespace: '{1}'.".format(attribute, Constants.nullObject))
		return None
	else:
		namespace = rootOnly and attributeTokens[0] or namespaceSplitter.join(attributeTokens[0:-1])
		LOGGER.debug("> Attribute: '{0}', Namespace: '{1}'.".format(attribute, namespace))
		return namespace

@core.executionTrace
def removeNamespace(attribute, namespaceSplitter=NAMESPACE_SPLITTER, rootOnly=False):
	"""
	This Definition Returns The Attribute Without Namespace.

	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace Splitter Character. ( String )
	@param rootOnly: Remove Only Root Namespace. ( Boolean )
	@return: Attribute Without Namespace. ( String )
	"""

	attributeTokens = attribute.split(namespaceSplitter)
	strippedAttribute = rootOnly and namespaceSplitter.join(attributeTokens[1:]) or attributeTokens[len(attributeTokens) - 1]
	LOGGER.debug("> Attribute: '{0}', Stripped Attribute: '{1}'.".format(attribute, strippedAttribute))
	return strippedAttribute

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
