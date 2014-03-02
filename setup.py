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

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Encoding manipulations.
#**********************************************************************************************************************
import sys

def _setEncoding():
	"""
	This definition sets the Application encoding.
	"""

	reload(sys)
	sys.setdefaultencoding("utf-8")

_setEncoding()

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re
from setuptools import setup
from setuptools import find_packages

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.globals.constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["getLongDescription"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getLongDescription():
	"""
	This definition returns the Package long description.

	:return: Package long description. ( String )
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

setup(name=foundations.globals.constants.Constants.applicationName,
	version=foundations.globals.constants.Constants.releaseVersion,
	author=foundations.globals.constants.__author__,
	author_email=foundations.globals.constants.__email__,
	include_package_data=True,
	packages=find_packages(),
	scripts=[],
	url="https://github.com/KelSolaar/Foundations",
	license="GPLv3",
	description="Foundations is the core package of Umbra, sIBL_GUI and sIBL_Reporter.",
	long_description=getLongDescription(),
	install_requires=["ordereddict>=1.1", "sphinx>=1.2.1", "sphinx-rtd-theme>=0.1.5", "unittest2>=0.5.1"] \
					if sys.version_info[:2] <= (2, 6) else \
					["sphinx>=1.1.3", "sphinx-rtd-theme>=0.1.5", "unittest2>=0.5.1"],
	classifiers=["Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
				"Natural Language :: English",
				"Operating System :: OS Independent",
				"Programming Language :: Python :: 2.7",
				"Topic :: Utilities"])
