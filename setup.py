#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**setup.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    `https://pypi.python.org/pypi/Foundations <https://pypi.python.org/pypi/Foundations>`_ package setup file.

**Others:**

"""

from __future__ import unicode_literals

import re
import sys
from setuptools import setup
from setuptools import find_packages

import foundations.globals.constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["get_long_description"]


def get_long_description():
    """
    Returns the Package long description.

    :return: Package long description.
    :rtype: unicode
    """

    description = []
    with open("README.rst") as file:
        for line in file:
            if ".. code:: python" in line and len(description) >= 2:
                blockLine = description[-2]
                if re.search(r":$", blockLine) and not re.search(r"::$", blockLine):
                    description[-2] = "::".join(blockLine.rsplit(":", 1))
                continue

            description.append(line)
    return "".join(description)


setup(name=foundations.globals.constants.Constants.application_name,
      version=foundations.globals.constants.Constants.version,
      author=foundations.globals.constants.__author__,
      author_email=foundations.globals.constants.__email__,
      include_package_data=True,
      packages=find_packages(),
      scripts=[],
      url="https://github.com/KelSolaar/Foundations",
      license="GPLv3",
      description="Foundations is the core package of Oncilla, Manager, Umbra, sIBL_GUI and sIBL_Reporter.",
      long_description=get_long_description(),
      install_requires=["ordereddict>=1.1", "unittest2>=0.5.1", "Oncilla>=0.1.0"]
      if sys.version_info[:2] <= (2, 6) else
      ["unittest2>=0.5.1", "Oncilla>=0.1.0"],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Environment :: Console",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.7",
                   "Topic :: Utilities"])
