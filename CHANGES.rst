Foundations - 2.0.8 - Stable
============================

.. .changes

Changes
=======

2.0.8 - Stable
--------------

**Foundations** 2.0.8 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=6&state=closed

-  Implement unicode support.

2.0.7 - Stable
--------------

**Foundations** 2.0.7 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=5&state=closed

-  Fixed **socket** module related exceptions in **foundations.common.isInternetAvailable** definition.
-  Handled non existing files and directories in **foundations.pkzip.Pkzip.extract** method.

2.0.6 - Stable
--------------

**Foundations** 2.0.6 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=4&state=closed

-  Implemented a better version rank calculation definition allowing to properly compare various version formats.

2.0.5 - Stable
--------------

**Foundations** 2.0.5 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=3&state=closed

-  Prevented exception in **foundations.tcpServer.TCPServer.start** method when the requested address is not available.

2.0.4 - Stable
--------------

**Foundations** 2.0.4 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=2&state=closed

-  Refactored exceptions handling code in **foundations.exceptions** module.
-  Refactored execution tracing code through new **foundations.trace** module.
-  Refactored verbose logging code through new **foundations.verbose** module.
-  Generic purpose decorators have been moved to dedicated **foundations.decorators** module.
-  **foundations.io.File** class now supports online resources.
-  Added **foundations.common.dependencyResolver** definition.

2.0.3 - Stable
--------------

**Foundations** 2.0.3 - Stable - https://github.com/KelSolaar/Foundations/issues?milestone=1&state=closed

-  Added support for **Python 2.6**.

2.0.2 - Stable
--------------

-  Updated package directory structure to be compliant with **Python Package Index**.
-  Added documentation / Api files.
-  Added TCP server implementation through **foundations.tcpServer** module.
-  **foundations.walkers.FilesWalker** class has been refactored to **foundations.walkers.filesWalker** generator definition.

2.0.1 - Stable
--------------

-  Prevented memory leak in **foundations.dataStuctures.Structure** class.

2.0.0 - Stable
--------------

-  Major package refactor.
-  Added **cache**, **dag**, **dataStructures** modules and associated units tests module.

1.0.4 - Stable
--------------

-  Reorganize package directories structure.
-  Added **rotatingBackup** module and associated **testsRotatingBackup** units tests module.

1.0.3 - Stable
--------------

-  Ensured that the parser will split attributes only one time.
-  Added **toPosixPath** method to **strings** module and associated units tests.

1.0.2 - Stable
--------------

-  Added **getWords** and **filterWords** methods to **strings** module and associated units tests.
-  Implemented **filterWords** in **walkers** module.
-  Added **getSplitextBasename** definition to **strings** module and associated units tests to **testsStrings** module.
-  Replaced list comprehension expressions by generators.

1.0.1 - Stable
--------------

-  Added **namespace** module and associated **testsGlobals** units tests module.

1.0.0 - Stable
--------------

-  Initial release of Foundations.

.. .about

About
-----

| **Foundations** by Thomas Mansencal – 2008 - 2013
| Copyright© 2008 - 2013 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_