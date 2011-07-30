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
#***********************************************************************************************
#
# The following code is protected by GNU GPL V3 Licence.
#
#***********************************************************************************************

"""
**namespace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Namespace Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)
NAMESPACE_SPLITTER = "|"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
def setNamespace(namespace, attribute, namespaceSplitter=NAMESPACE_SPLITTER):
	"""
	This definition returns the compounded attribute and compounded namespace.

	@param namespace: Namespace. ( String )
	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace splitter character. ( String )
	@return: Namespaced attribute. ( String )
	"""

	longName = str(namespace + namespaceSplitter + attribute)
	LOGGER.debug("> Namespace: '{0}', attribute: '{1}', long name: '{2}'.".format(namespace, attribute, longName))
	return longName

@core.executionTrace
def getNamespace(attribute, namespaceSplitter=NAMESPACE_SPLITTER, rootOnly=False):
	"""
	This definition returns the attribute namespace.

	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace splitter character. ( String )
	@param rootOnly: Return only root namespace. ( Boolean )
	@return: Attribute namespace. ( String )
	"""

	attributeTokens = attribute.split(namespaceSplitter)
	if len(attributeTokens) == 1:
		LOGGER.debug("> Attribute: '{0}', namespace: '{1}'.".format(attribute, Constants.nullObject))
	else:
		namespace = rootOnly and attributeTokens[0] or namespaceSplitter.join(attributeTokens[0:-1])
		LOGGER.debug("> Attribute: '{0}', namespace: '{1}'.".format(attribute, namespace))
		return namespace

@core.executionTrace
def removeNamespace(attribute, namespaceSplitter=NAMESPACE_SPLITTER, rootOnly=False):
	"""
	This definition returns the attribute without namespace.

	@param attribute: Attribute. ( String )
	@param namespaceSplitter: Namespace splitter character. ( String )
	@param rootOnly: Remove only root namespace. ( Boolean )
	@return: Attribute without namespace. ( String )
	"""

	attributeTokens = attribute.split(namespaceSplitter)
	strippedAttribute = rootOnly and namespaceSplitter.join(attributeTokens[1:]) or attributeTokens[len(attributeTokens) - 1]
	LOGGER.debug("> Attribute: '{0}', stripped attribute: '{1}'.".format(attribute, strippedAttribute))
	return strippedAttribute

