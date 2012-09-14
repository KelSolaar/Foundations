import foundations.globals.constants

from setuptools import setup
from setuptools import find_packages

setup(name=foundations.globals.constants.Constants.applicationName,
	version=foundations.globals.constants.Constants.releaseVersion,
	author=foundations.globals.constants.__author__,
	author_email=foundations.globals.constants.__email__,
	packages=find_packages(),
	scripts=[],
	url="https://github.com/KelSolaar/Foundations",
	license="GPL v3",
	description="Foundations is the core package of Umbra, sIBL_GUI, sIBL_Reporter.",
	long_description=open("README.rst").read(),
	install_requires=[],
	include_package_data=True)
