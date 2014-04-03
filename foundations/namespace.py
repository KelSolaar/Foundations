#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**namespace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Provides simple strings namespace manipulation objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.verbose
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Sets given namespace to given attribute.

	Usage::
		
		>>> setNamespace("parent", "child")
		u'parent|child'
		
	:param namespace: Namespace.
	:type namespace: unicode
	:param attribute: Attribute.
	:type attribute: unicode
	:param namespaceSplitter: Namespace splitter character.
	:type namespaceSplitter: unicode
	:return: Namespaced attribute.
	:rtype: unicode
	"""

	longName = "{0}{1}{2}".format(namespace, namespaceSplitter, attribute)
	LOGGER.debug("> Namespace: '{0}', attribute: '{1}', long name: '{2}'.".format(namespace, attribute, longName))
	return longName

def getNamespace(attribute, namespaceSplitter=NAMESPACE_SPLITTER, rootOnly=False):
	"""
	Returns given attribute foundations.namespace.

	Usage::
		
		>>> getNamespace("grandParent|parent|child")
		u'grandParent|parent'
		>>> getNamespace("grandParent|parent|child", rootOnly=True)
		u'grandParent'

	:param attribute: Attribute.
	:type attribute: unicode
	:param namespaceSplitter: Namespace splitter character.
	:type namespaceSplitter: unicode
	:param rootOnly: Return only root foundations.namespace.
	:type rootOnly: bool
	:return: Attribute foundations.namespace.
	:rtype: unicode
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
	Returns attribute with stripped foundations.namespace.

	Usage::
		
		>>> removeNamespace("grandParent|parent|child")
		u'child'
		>>> removeNamespace("grandParent|parent|child", rootOnly=True)
		u'parent|child'

	:param attribute: Attribute.
	:type attribute: unicode
	:param namespaceSplitter: Namespace splitter character.
	:type namespaceSplitter: unicode
	:param rootOnly: Remove only root foundations.namespace.
	:type rootOnly: bool
	:return: Attribute without foundations.namespace.
	:rtype: unicode
	"""

	attributeTokens = attribute.split(namespaceSplitter)
	strippedAttribute = rootOnly and namespaceSplitter.join(attributeTokens[1:]) or \
						attributeTokens[len(attributeTokens) - 1]
	LOGGER.debug("> Attribute: '{0}', stripped attribute: '{1}'.".format(attribute, strippedAttribute))
	return strippedAttribute

def getRoot(attribute, namespaceSplitter=NAMESPACE_SPLITTER):
	"""
	Returns given attribute root.

	Usage::
		
		>>> getRoot("grandParent|parent|child")
		u'grandParent'

	:param attribute: Attribute.
	:type attribute: unicode
	:param namespaceSplitter: Namespace splitter character.
	:type namespaceSplitter: unicode
	:return: Attribute foundations.namespace.
	:rtype: unicode
	"""

	return getNamespace(attribute, namespaceSplitter, rootOnly=True)

def getLeaf(attribute, namespaceSplitter=NAMESPACE_SPLITTER):
	"""
	Returns given attribute leaf.

	Usage::
		
		>>> getLeaf("grandParent|parent|child")
		u'child'

	:param attribute: Attribute.
	:type attribute: unicode
	:param namespaceSplitter: Namespace splitter character.
	:type namespaceSplitter: unicode
	:return: Attribute foundations.namespace.
	:rtype: unicode
	"""

	return foundations.common.getLastItem(attribute.split(namespaceSplitter))
