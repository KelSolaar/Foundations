import foundations.globals.constants

from setuptools import setup
from setuptools import find_packages

def getLongDescription():
	"""
	This definition returns the Package long description.

	:return: Package long description. ( String )
	"""

	description = str()
	with open("README.rst") as file:
		for line in file:
			if ".. code:: python" in line:
				continue

			description += line
	return description

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
	install_requires=[],
	classifiers=["Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Intended Audience :: Developers",
				"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
				"Natural Language :: English",
				"Operating System :: OS Independent",
				"Programming Language :: Python :: 2.7",
				"Topic :: Utilities"])
