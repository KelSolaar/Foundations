#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**strings.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines various strings manipulation objects.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
import posixpath
import random
import re

import foundations.common
import foundations.verbose

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "ASCII_CHARACTERS",
           "to_string",
           "get_nice_name",
           "get_version_rank",
           "get_splitext_basename",
           "get_common_ancestor",
           "get_common_paths_ancestor",
           "get_words",
           "filter_words",
           "replace",
           "remove_strip",
           "to_forward_slashes",
           "to_backward_slashes",
           "to_posix_path",
           "get_normalized_path",
           "get_random_sequence",
           "is_email",
           "is_website"]

LOGGER = foundations.verbose.install_logger()

ASCII_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

to_string = foundations.verbose.to_unicode


def get_nice_name(name):
    """
    Converts a string to nice string: **currentLogText** -> **Current Log Text**.

    Usage::

        >>> get_nice_name("getMeANiceName")
        u'Get Me A Nice Name'
        >>> get_nice_name("__getMeANiceName")
        u'__Get Me A Nice Name'

    :param name: Current string to be nicified.
    :type name: unicode
    :return: Nicified string.
    :rtype: unicode
    """

    chunks = re.sub(r"(.)([A-Z][a-z]+)", r"\1 \2", name)
    return " ".join(element.title() for element in re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", chunks).split())


def get_version_rank(version):
    """
    Converts a version string to it's rank.

    Usage::

        >>> get_version_rank("4.2.8")
        4002008000000
        >>> get_version_rank("4.0")
        4000000000000
        >>> get_version_rank("4.2.8").__class__
        <type 'int'>

    :param version: Current version to calculate rank.
    :type version: unicode
    :return: Rank.
    :rtype: int
    """

    tokens = list(foundations.common.unpack_default(filter(any, re.split("\.|-|,", version)), length=4, default=0))
    rank = sum((int(1000 ** i) * int(tokens[-i]) for i in range(len(tokens), 0, -1)))
    LOGGER.debug("> Rank: '{0}'.".format(rank))
    return rank


def get_splitext_basename(path):
    """
    Gets the basename of a path without its extension.

    Usage::

        >>> get_splitext_basename("/Users/JohnDoe/Documents/Test.txt")
        u'Test'

    :param path: Path to extract the basename without extension.
    :type path: unicode
    :return: Splitext basename.
    :rtype: unicode
    """

    basename = foundations.common.get_first_item(os.path.splitext(os.path.basename(os.path.normpath(path))))
    LOGGER.debug("> Splitext basename: '{0}'.".format(basename))
    return basename


def get_common_ancestor(*args):
    """
    Gets common ancestor of given iterables.

    Usage::

        >>> get_common_ancestor(("1", "2", "3"), ("1", "2", "0"), ("1", "2", "3", "4"))
        (u'1', u'2')
        >>> get_common_ancestor("azerty", "azetty", "azello")
        u'aze'

    :param \*args: Iterables to retrieve common ancestor from.
    :type \*args: [iterable]
    :return: Common ancestor.
    :rtype: iterable
    """

    array = map(set, zip(*args))
    divergence = filter(lambda i: len(i) > 1, array)
    if divergence:
        ancestor = foundations.common.get_first_item(args)[:array.index(foundations.common.get_first_item(divergence))]
    else:
        ancestor = min(args)
    LOGGER.debug("> Common Ancestor: '{0}'".format(ancestor))
    return ancestor


def get_common_paths_ancestor(*args):
    """
    Gets common paths ancestor of given paths.

    Usage::

        >>> get_common_paths_ancestor("/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt")
        u'/Users/JohnDoe/Documents'

    :param \*args: Paths to retrieve common ancestor from.
    :type \*args: [unicode]
    :return: Common path ancestor.
    :rtype: unicode
    """

    path_ancestor = os.sep.join(get_common_ancestor(*[path.split(os.sep) for path in args]))
    LOGGER.debug("> Common Paths Ancestor: '{0}'".format(path_ancestor))
    return path_ancestor


def get_words(data):
    """
    Extracts the words from given string.

    Usage::

        >>> get_words("Users are: John Doe, Jane Doe, Z6PO.")
        [u'Users', u'are', u'John', u'Doe', u'Jane', u'Doe', u'Z6PO']

    :param data: Data to extract words from.
    :type data: unicode
    :return: Words.
    :rtype: list
    """

    words = re.findall(r"\w+", data)
    LOGGER.debug("> Words: '{0}'".format(", ".join(words)))
    return words


def filter_words(words, filters_in=None, filters_out=None, flags=0):
    """
    Filters the words using the given filters.

    Usage::

        >>> filter_words(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filters_in=("John", "Doe"))
        [u'John', u'Doe', u'Doe']
        >>> filter_words(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filters_in=("\w*r",))
        [u'Users', u'are']
        >>> filter_words(["Users", "are", "John", "Doe", "Jane", "Doe", "Z6PO"], filters_out=("\w*o",))
        [u'Users', u'are', u'Jane', u'Z6PO']

    :param filters_in: Regex filters in list.
    :type filters_in: tuple or list
    :param filters_in: Regex filters out list.
    :type filters_in: tuple or list
    :param flags: Regex flags.
    :type flags: int
    :return: Filtered words.
    :rtype: list
    """

    filtered_words = []
    for word in words:
        if filters_in:
            filter_matched = False
            for filter in filters_in:
                if not re.search(filter, word, flags):
                    LOGGER.debug("> '{0}' word skipped, filter in '{1}' not matched!".format(word, filter))
                else:
                    filter_matched = True
                    break
            if not filter_matched:
                continue

        if filters_out:
            filter_matched = False
            for filter in filters_out:
                if re.search(filter, word, flags):
                    LOGGER.debug("> '{0}' word skipped, filter out '{1}' matched!".format(word, filter))
                    filter_matched = True
                    break
            if filter_matched:
                continue
        filtered_words.append(word)
    LOGGER.debug("> Filtered words: '{0}'".format(", ".join(filtered_words)))
    return filtered_words


def replace(string, data):
    """
    Replaces the data occurrences in the string.

    Usage::

        >>> replace("Users are: John Doe, Jane Doe, Z6PO.", {"John" : "Luke", "Jane" : "Anakin", "Doe" : "Skywalker",
         "Z6PO" : "R2D2"})
        u'Users are: Luke Skywalker, Anakin Skywalker, R2D2.'

    :param string: String to manipulate.
    :type string: unicode
    :param data: Replacement occurrences.
    :type data: dict
    :return: Manipulated string.
    :rtype: unicode
    """

    for old, new in data.iteritems():
        string = string.replace(old, new)
    return string


def remove_strip(string, pattern):
    """
    Removes the pattern occurrences in the string and strip the result.

    Usage::

        >>> remove_strip("John Doe", "John")
        u'Doe'

    :param string: String to manipulate.
    :type string: unicode
    :param pattern: Replacement pattern.
    :type pattern: unicode
    :return: Manipulated string.
    :rtype: unicode
    """

    return string.replace(pattern, "").strip()


def to_forward_slashes(data):
    """
    Converts backward slashes to forward slashes.

    Usage::

        >>> to_forward_slashes("To\Forward\Slashes")
        u'To/Forward/Slashes'

    :param data: Data to convert.
    :type data: unicode
    :return: Converted path.
    :rtype: unicode
    """

    data = data.replace("\\", "/")
    LOGGER.debug("> Data: '{0}' to forward slashes.".format(data))
    return data


def to_backward_slashes(data):
    """
    Converts forward slashes to backward slashes.

    Usage::

        >>> to_backward_slashes("/Users/JohnDoe/Documents")
        u'\\Users\\JohnDoe\\Documents'

    :param data: Data to convert.
    :type data: unicode
    :return: Converted path.
    :rtype: unicode
    """

    data = data.replace("/", "\\")
    LOGGER.debug("> Data: '{0}' to backward slashes.".format(data))
    return data


def to_posix_path(path):
    """
    Converts Windows path to Posix path while stripping drives letters and network server slashes.

    Usage::

        >>> to_posix_path("c:\\Users\\JohnDoe\\Documents")
        u'/Users/JohnDoe/Documents'

    :param path: Windows path.
    :type path: unicode
    :return: Path converted to Posix path.
    :rtype: unicode
    """

    posix_path = posixpath.normpath(to_forward_slashes(re.sub(r"[a-zA-Z]:\\|\\\\", "/", os.path.normpath(path))))
    LOGGER.debug("> Stripped converted to Posix path: '{0}'.".format(posix_path))
    return posix_path


def get_normalized_path(path):
    """
    Normalizes a path, escaping slashes if needed on Windows.

    Usage::

        >>> get_normalized_path("C:\\Users/johnDoe\\Documents")
        u'C:\\Users\\JohnDoe\\Documents'

    :param path: Path to normalize.
    :type path: unicode
    :return: Normalized path.
    :rtype: unicode
    """

    if platform.system() == "Windows" or platform.system() == "Microsoft":
        path = os.path.normpath(path).replace("\\", "\\\\")
        LOGGER.debug("> Path: '{0}', normalized path.".format(path))
        return path
    else:
        path = os.path.normpath(path)
        LOGGER.debug("> Path: '{0}', normalized path.".format(path))
        return path


def get_random_sequence(length=8):
    """
    Returns a random sequence.

    Usage::

        >>> get_random_sequence()
        u'N_mYO7g5'

    :param length: Length of the sequence.
    :type length: int
    :return: Random sequence.
    :rtype: unicode
    """

    return "".join([random.choice(ASCII_CHARACTERS) for i in range(length)])


def is_email(data):
    """
    Check if given data string is an email.

    Usage::

        >>> is_email("john.doe@domain.com")
        True
        >>> is_email("john.doe:domain.com")
        False

    :param data: Data to check.
    :type data: unicode
    :return: Is email.
    :rtype: bool
    """

    if re.match(r"[\w.%+-]+@[\w.]+\.[a-zA-Z]{2,4}", data):
        LOGGER.debug("> {0}' is matched as email.".format(data))
        return True
    else:
        LOGGER.debug("> {0}' is not matched as email.".format(data))
        return False


def is_website(url):
    """
    Check if given url string is a website.

    Usage::

        >>> is_website("http://www.domain.com")
        True
        >>> is_website("domain.com")
        False

    :param data: Data to check.
    :type data: unicode
    :return: Is website.
    :rtype: bool
    """

    if re.match(r"(http|ftp|https)://([\w\-\.]+)/?", url):
        LOGGER.debug("> {0}' is matched as website.".format(url))
        return True
    else:
        LOGGER.debug("> {0}' is not matched as website.".format(url))
        return False
