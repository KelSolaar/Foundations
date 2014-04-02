Foundations
===========

..  image:: https://secure.travis-ci.org/KelSolaar/Foundations.png?branch=master
..  image:: https://gemnasium.com/KelSolaar/Foundations.png  

Introduction
------------

**Foundations** is the core package of `Oncilla <http://github.com/KelSolaar/Oncilla>`_, `Color <http://github.com/KelSolaar/Color>`_, `Manager <http://github.com/KelSolaar/Manager>`_, `Umbra <http://github.com/KelSolaar/Umbra>`_, `sIBL_GUI <http://github.com/KelSolaar/sIBL_GUI>`_, `sIBL_Reporter <http://github.com/KelSolaar/sIBL_Reporter>`_.It provides modules defining various utilities objects used in those packages.

Installation
------------

The following dependencies are needed:

-  **Python 2.6.7** or **Python 2.7.3**: http://www.python.org/
-  **PyQt**: http://www.riverbankcomputing.co.uk/

To install **Foundations** from the `Python Package Index <http://pypi.python.org/pypi/Foundations>`_ you can issue this command in a shell::

	pip install Foundations

or this alternative command::

	easy_install Foundations

You can also directly install from `Github <http://github.com/KelSolaar/Foundations>`_ source repository::

	git clone git://github.com/KelSolaar/Foundations.git
	cd Foundations
	python setup.py install

If you want to build the documentation you will also need:

-  **Tidy** http://tidy.sourceforge.net/

Usage
-----

Given the large spectrum of the objects defined in **Foundations** package, please refer to `Foundations - Api <http://thomasmansencal.com/Sharing/Foundations/Support/Documentation/Api/index.html>`_ for precise usage examples about each modules. Here are listed a few non exhaustive usage examples.

-  **foundations.dataStructures.Structure**:

.. code:: python

	>>> person = Structure(firstName="Doe", lastName="John", gender="male")
	>>> person.firstName
	'Doe'
	>>> person.keys()
	['gender', 'firstName', 'lastName']
	>>> person["gender"]
	'male'
	>>> del(person["gender"])
	>>> person["gender"]
	Traceback (most recent call last):
	  File "<console>", line 1, in <module>
	KeyError: 'gender'
	>>> person.gender
	Traceback (most recent call last):
	  File "<console>", line 1, in <module>
	AttributeError: 'Structure' object has no attribute 'gender'

-  **foundations.dataStructures.Lookup**:

.. code:: python

	>>> person = Lookup(firstName="Doe", lastName="John", gender="male")
	>>> person.getFirstKeyFromValue("Doe")
	'firstName'
	>>> persons = foundations.foundations.dataStructures.Lookup(John="Doe", Jane="Doe", Luke="Skywalker")
	>>> persons.getKeysFromValue("Doe")
	['Jane', 'John']

-  **foundations.environment.Environment**:

.. code:: python

	>>> environment = Environment(JOHN="DOE", DOE="JOHN")
	>>> environment.setValues()
	True
	>>> import os
	>>> os.environ["JOHN"]
	'DOE'
	>>> os.environ["DOE"]
	'JOHN'

- **foundations.strings.getNiceName**:

.. code:: python

	>>> getNiceName("getMeANiceName")
	'Get Me A Nice Name'
	>>> getNiceName("__getMeANiceName")
	'__Get Me A Nice Name'

- **foundations.strings.getSplitextBasename**:

.. code:: python

	>>> getSplitextBasename("/Users/JohnDoe/Documents/Test.txt")
	'Test'

- **foundations.strings.getCommonPathsAncestor**:

.. code:: python

	>>> getCommonPathsAncestor("/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt")
	'/Users/JohnDoe/Documents'

-  **foundations.walkers.filesWalker**:

.. code:: python

	>>> for file in filesWalker("./foundations/tests/testsFoundations/resources/standard/level_0"):
	...     print(file)
	...
	./foundations/tests/testsFoundations/resources/standard/level_0/level_1/level_2/standard.sIBLT
	./foundations/tests/testsFoundations/resources/standard/level_0/level_1/loremIpsum.txt
	./foundations/tests/testsFoundations/resources/standard/level_0/level_1/standard.rc
	./foundations/tests/testsFoundations/resources/standard/level_0/standard.ibl		
	>>> for file in filesWalker("./foundations/tests/testsFoundations/resources/standard/level_0", ("\.sIBLT",)):
	...     print(file)
	...
	./foundations/tests/testsFoundations/resources/standard/level_0/level_1/level_2/standard.sIBLT

About
-----

| **Foundations** by Thomas Mansencal – 2008 - 2014
| Copyright © 2008 - 2014 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_