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

from __future__ import unicode_literals

import foundations.common
import foundations.verbose
from foundations.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "NAMESPACE_SPLITTER",
           "set_namespace",
           "get_namespace",
           "remove_namespace",
           "get_root",
           "get_leaf"]

LOGGER = foundations.verbose.install_logger()

NAMESPACE_SPLITTER = "|"


def set_namespace(namespace, attribute, namespace_splitter=NAMESPACE_SPLITTER):
    """
    Sets given namespace to given attribute.

    Usage::

        >>> set_namespace("parent", "child")
        u'parent|child'

    :param namespace: Namespace.
    :type namespace: unicode
    :param attribute: Attribute.
    :type attribute: unicode
    :param namespace_splitter: Namespace splitter character.
    :type namespace_splitter: unicode
    :return: Namespaced attribute.
    :rtype: unicode
    """

    long_name = "{0}{1}{2}".format(namespace, namespace_splitter, attribute)
    LOGGER.debug("> Namespace: '{0}', attribute: '{1}', long name: '{2}'.".format(namespace, attribute, long_name))
    return long_name


def get_namespace(attribute, namespace_splitter=NAMESPACE_SPLITTER, root_only=False):
    """
    Returns given attribute foundations.namespace.

    Usage::

        >>> get_namespace("grandParent|parent|child")
        u'grandParent|parent'
        >>> get_namespace("grandParent|parent|child", root_only=True)
        u'grandParent'

    :param attribute: Attribute.
    :type attribute: unicode
    :param namespace_splitter: Namespace splitter character.
    :type namespace_splitter: unicode
    :param root_only: Return only root foundations.namespace.
    :type root_only: bool
    :return: Attribute foundations.namespace.
    :rtype: unicode
    """

    attribute_tokens = attribute.split(namespace_splitter)
    if len(attribute_tokens) == 1:
        LOGGER.debug("> Attribute: '{0}', namespace: '{1}'.".format(attribute, Constants.null_object))
    else:
        namespace = foundations.common.get_first_item(attribute_tokens) if root_only else \
            namespace_splitter.join(attribute_tokens[0:-1])
        LOGGER.debug("> Attribute: '{0}', namespace: '{1}'.".format(attribute, namespace))
        return namespace


def remove_namespace(attribute, namespace_splitter=NAMESPACE_SPLITTER, root_only=False):
    """
    Returns attribute with stripped foundations.namespace.

    Usage::

        >>> remove_namespace("grandParent|parent|child")
        u'child'
        >>> remove_namespace("grandParent|parent|child", root_only=True)
        u'parent|child'

    :param attribute: Attribute.
    :type attribute: unicode
    :param namespace_splitter: Namespace splitter character.
    :type namespace_splitter: unicode
    :param root_only: Remove only root foundations.namespace.
    :type root_only: bool
    :return: Attribute without foundations.namespace.
    :rtype: unicode
    """

    attribute_tokens = attribute.split(namespace_splitter)
    stripped_attribute = root_only and namespace_splitter.join(attribute_tokens[1:]) or \
                         attribute_tokens[len(attribute_tokens) - 1]
    LOGGER.debug("> Attribute: '{0}', stripped attribute: '{1}'.".format(attribute, stripped_attribute))
    return stripped_attribute


def get_root(attribute, namespace_splitter=NAMESPACE_SPLITTER):
    """
    Returns given attribute root.

    Usage::

        >>> get_root("grandParent|parent|child")
        u'grandParent'

    :param attribute: Attribute.
    :type attribute: unicode
    :param namespace_splitter: Namespace splitter character.
    :type namespace_splitter: unicode
    :return: Attribute foundations.namespace.
    :rtype: unicode
    """

    return get_namespace(attribute, namespace_splitter, root_only=True)


def get_leaf(attribute, namespace_splitter=NAMESPACE_SPLITTER):
    """
    Returns given attribute leaf.

    Usage::

        >>> get_leaf("grandParent|parent|child")
        u'child'

    :param attribute: Attribute.
    :type attribute: unicode
    :param namespace_splitter: Namespace splitter character.
    :type namespace_splitter: unicode
    :return: Attribute foundations.namespace.
    :rtype: unicode
    """

    return foundations.common.get_last_item(attribute.split(namespace_splitter))
