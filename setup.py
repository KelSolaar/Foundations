import re
from setuptools import setup
from setuptools import find_packages

import foundations.globals.constants

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
	description="Foundations is the core package of Umbra, sIBL_GUI, sIBL_Reporter.",
	long_description=getLongDescription(),
	install_requires=["ordereddict>=1.1", "sphinx>=1.1.3", "unittest2>=0.5.1"],
	classifiers=["Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
				"Natural Language :: English",
				"Operating System :: OS Independent",
				"Programming Language :: Python :: 2.7",
				"Topic :: Utilities"])
