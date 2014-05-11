#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**guerilla.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines various guerilla / monkey patching objects.

**Others:**
    Portions of the code by Guido Van Rossum: http://mail.python.org/pipermail/python-dev/2008-January/076194.html
"""

from __future__ import unicode_literals

import foundations.common

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "attribute_warfare", "base_warfare"]


def attribute_warfare(object):
    """
    Alterates object attributes using guerilla / monkey patching.

    :param object: Object to alterate.
    :type object: object
    :return: Object.
    :rtype: object
    """

    def attribute_warfare_wrapper(attribute):
        """
        Alterates object attributes using guerilla / monkey patching.

        :param attribute: Attribute to alterate.
        :type attribute: object
        :return: Object.
        :rtype: object
        """

        setattr(object, attribute.__name__, attribute)
        return attribute

    return attribute_warfare_wrapper


def base_warfare(name, bases, attributes):
    """
    Adds any number of attributes to an existing class.

    :param name: Name.
    :type name: unicode
    :param bases: Bases.
    :type bases: list
    :param attributes: Attributes.
    :type attributes: dict
    :return: Base.
    :rtype: object
    """

    assert len(bases) == 1, "{0} | '{1}' object has multiple bases!".format(__name__, name)

    base = foundations.common.get_first_item(bases)
    for name, value in attributes.iteritems():
        if name != "__metaclass__":
            setattr(base, name, value)
    return base
