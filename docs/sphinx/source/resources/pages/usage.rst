_`Usage`
========

Given the large spectrum of the objects defined in **Foundations** package, please refer to `Foundations - Api <http://thomasmansencal.com/Sharing/Foundations/Support/Documentation/Api/index.html>`_ for precise usage examples about each modules. Here are listed a few non exhaustive usage examples.

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

-  foundations.walkers.filesWalker:

.. code:: python

	>>> for file in filesWalker("./foundations/tests/testsFoundations/../standard/level_0"):
	...     print(file)
	...
	./foundations/tests/testsFoundations/../standard/level_0/level_1/level_2/standard.sIBLT
	./foundations/tests/testsFoundations/../standard/level_0/level_1/loremIpsum.txt
	./foundations/tests/testsFoundations/../standard/level_0/level_1/standard.rc
	./foundations/tests/testsFoundations/../standard/level_0/standard.ibl		
	>>> for file in filesWalker("./foundations/tests/testsFoundations/../standard/level_0", ("\.sIBLT",)):
	...     print(file)
	...
	./foundations/tests/testsFoundations/../standard/level_0/level_1/level_2/standard.sIBLT

.. raw:: html

    <br/>

