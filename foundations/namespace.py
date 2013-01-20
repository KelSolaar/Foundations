#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**namespace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module provides simple strings namespace manipulation objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.verbose
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"NAMESPACE_SPLITTER",
			"setNamespace",
			"getNamespace",
			"removeNamespace",
			"getRoot",
			"getLeaf"]

LOGGER = foundations.verbose.installLogger()

NAMESPACE_SPLITTER = "|"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def setNamespace(namespace, attribute, namespaceSplitter=NAMESPACE_SPLITTER):
	"""
	This definition sets given namespace to given attribute.

	Usage::
		
		>>> setNamespace("parent", "child")
		'parent|child'
		
	:param namespace: Namespace. ( String )
	:param attribute: Attribute. ( String )
	:param namespaceSplitter: Namespace splitter character. ( String )
	:return: Namespaced attribute. ( String )
	"""

	longName = "{0}{1}{2}".format(namespace, namespaceSplitter, attribute)
	LOGGER.debug("> Namespace: '{0}', attribute: '{1}', long name: '{2}'.".format(namespace, attribute, longName))
	return longName

def getNamespace(attribute, namespaceSplitter=NAMESPACE_SPLITTER, rootOnly=False):
	"""
	This definition returns given attribute foundations.namespace.

	Usage::
		
		>>> getNamespace("grandParent|parent|child")
		'grandParent|parent'
		>>> getNamespace("grandParent|parent|child", rootOnly=True)
		'grandParent'

	:param attribute: Attribute. ( String )
	:param namespaceSplitter: Namespace splitter character. ( String )
	:param rootOnly: Return only root foundations.namespace. ( Boolean )
	:return: Attribute foundations.namespace. ( String )
	"""

	attributeTokens = attribute.split(namespaceSplitter)
	if len(attributeTokens) == 1:
		LOGGER.debug("> Attribute: '{0}', namespace: '{1}'.".format(attribute, Constants.nullObject))
	else:
		namespace = foundations.common.getFirstItem(attributeTokens) if rootOnly else \
		namespaceSplitter.join(attributeTokens[0:-1])
		LOGGER.debug("> Attribute: '{0}', namespace: '{1}'.".format(attribute, namespace))
		return namespace

def removeNamespace(attribute, namespaceSplitter=NAMESPACE_SPLITTER, rootOnly=False):
	"""
	This definition returns attribute with stripped foundations.namespace.

	Usage::
		
		>>> removeNamespace("grandParent|parent|child")
		'child'
		>>> removeNamespace("grandParent|parent|child", rootOnly=True)
		'parent|child'

	:param attribute: Attribute. ( String )
	:param namespaceSplitter: Namespace splitter character. ( String )
	:param rootOnly: Remove only root foundations.namespace. ( Boolean )
	:return: Attribute without foundations.namespace. ( String )
	"""

	attributeTokens = attribute.split(namespaceSplitter)
	strippedAttribute = rootOnly and namespaceSplitter.join(attributeTokens[1:]) or \
						attributeTokens[len(attributeTokens) - 1]
	LOGGER.debug("> Attribute: '{0}', stripped attribute: '{1}'.".format(attribute, strippedAttribute))
	return strippedAttribute

def getRoot(attribute, namespaceSplitter=NAMESPACE_SPLITTER):
	"""
	This definition returns given attribute root.

	Usage::
		
		>>> getNamespace("grandParent|parent|child")
		'grandParent|parent'
		>>> getNamespace("grandParent|parent|child", rootOnly=True)
		'grandParent'

	:param attribute: Attribute. ( String )
	:param namespaceSplitter: Namespace splitter character. ( String )
	:return: Attribute foundations.namespace. ( String )
	"""

	return getNamespace(attribute, namespaceSplitter, rootOnly=True)

def getLeaf(attribute, namespaceSplitter=NAMESPACE_SPLITTER):
	"""
	This definition returns given attribute leaf.

	Usage::
		
		>>> getNamespace("grandParent|parent|child")
		'grandParent|parent'
		>>> getNamespace("grandParent|parent|child", rootOnly=True)
		'grandParent'

	:param attribute: Attribute. ( String )
	:param namespaceSplitter: Namespace splitter character. ( String )
	:return: Attribute foundations.namespace. ( String )
	"""

	return foundations.common.getLastItem(attribute.split(namespaceSplitter))
