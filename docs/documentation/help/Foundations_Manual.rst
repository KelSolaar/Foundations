Foundations - Manual - Help File
================================

.. raw:: html

    <br/>

Table Of Content
=================

.. .tocTree

-  `Introduction`_
-  `Installation`_
-  `Usage`_
-  `Changes`_
-  `Api`_
-  `About`_

.. raw:: html

    <br/>

.. .introduction

_`Introduction`
===============

Foundations is the core package of `Umbra <http://github.com/KelSolaar/Umbra>`_, `sIBL_GUI <http://github.com/KelSolaar/sIBL_GUI>`_, `sIBL_Reporter <http://github.com/KelSolaar/sIBL_Reporter>`_ and others tools.

.. raw:: html

    <br/>

.. .installation

_`Installation`
===============

.. raw:: html

    <br/>

.. .usage

_`Usage`
========

Given the large spectrum of the objects defined in **Foundations** package, please refer to the Api ( `Foundations - Api <index.html>`_ ) for precise usage examples about each modules. Here are listed a few non exhaustive usage examples.

-  foundations.dataStructures.Structure:

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

-  foundations.dataStructures.Lookup:

.. code:: python

	>>> person = Lookup(firstName="Doe", lastName="John", gender="male")
	>>> person.getFirstKeyFromValue("Doe")
	'firstName'
	>>> persons = foundations.foundations.dataStructures.Lookup(John="Doe", Jane="Doe", Luke="Skywalker")
	>>> persons.getKeysFromValue("Doe")
	['Jane', 'John']

-  foundations.environment.Environment:

.. code:: python

	>>> environment = Environment(JOHN="DOE", DOE="JOHN")
	>>> environment.setValues()
	True
	>>> import os
	>>> os.environ["JOHN"]
	'DOE'
	>>> os.environ["DOE"]
	'JOHN'

- foundations.strings.getNiceName:

.. code:: python

	>>> getNiceName("getMeANiceName")
	'Get Me A Nice Name'
	>>> getNiceName("__getMeANiceName")
	'__Get Me A Nice Name'

- foundations.strings.getSplitextBasename:

.. code:: python

	>>> getSplitextBasename("/Users/JohnDoe/Documents/Test.txt")
	'Test'

- foundations.strings.getCommonPathsAncestor:

.. code:: python

	>>> getCommonPathsAncestor("/Users/JohnDoe/Documents", "/Users/JohnDoe/Documents/Test.txt")
	'/Users/JohnDoe/Documents'

-  foundations.walkers.FilesWalker:

.. code:: python

	>>> filesWalker = FilesWalker("./Foundations/src/tests/testsFoundations/resources/standard/level_0")
	>>> filesWalker.walk().keys()
	['standard|0d24f027', 'standard|407ed3b2', 'standard|20efaeaf', 'loremIpsum|ddf30259']
	>>> filesWalker.walk(filtersIn=("\.sIBLT$",))
	{'standard|20efaeaf': './Foundations/src/tests/testsFoundations/resources/standard/level_0/level_1/level_2/standard.sIBLT'}
	>>> filesWalker.walk(filtersOut=("\.sIBLT$", "\.rc$", "\.ibl$")).values()
	['./Foundations/src/tests/testsFoundations/resources/standard/level_0/level_1/loremIpsum.txt']

.. raw:: html

    <br/>

.. .api

_`Api`
======

*Foundations* Api documentation is available here: `Foundations - Api <index.html>`_

.. raw:: html

    <br/>

.. .changes

_`Changes`
==========

**Foundations - Changes**: Change_Log.html

.. raw:: html

    <br/>

.. .about

_`About`
========

| *Foundations* by Thomas Mansencal - 2008 - 2012
| Copyright© 2008 - 2012 - Thomas Mansencal - `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| http://www.thomasmansencal.com/