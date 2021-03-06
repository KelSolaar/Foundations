#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_data_structures.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.data_structures` module.

**Others:**

"""

from __future__ import unicode_literals

import pickle
import sys

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest

import foundations.data_structures

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestNestedAttribute",
           "TestStructure",
           "TestOrderedStructure",
           "TestLookup"]


class TestNestedAttribute(unittest.TestCase):
    """
    Defines :class:`foundations.data_structures.NestedAttribute` class units tests methods.
    """

    def test_nested_attribute(self):
        """
        Tests :class:`foundations.data_structures.NestedAttribute` class.
        """

        nest = foundations.data_structures.NestedAttribute()
        nest.my.deeply.nested.attribute = 64
        self.assertTrue(hasattr(nest, "nest.my.deeply.nested.attribute"))
        self.assertEqual(nest.my.deeply.nested.attribute, 64)


class TestStructure(unittest.TestCase):
    """
    Defines :class:`foundations.data_structures.Structure` class units tests methods.
    """

    def test_structure(self):
        """
        Tests :class:`foundations.data_structures.Structure` class.
        """

        structure = foundations.data_structures.Structure(John="Doe", Jane="Doe")
        self.assertIn("John", structure)
        self.assertTrue(hasattr(structure, "John"))
        setattr(structure, "John", "Nemo")
        self.assertEqual(structure["John"], "Nemo")
        structure["John"] = "Vador"
        self.assertEqual(structure["John"], "Vador")
        del (structure["John"])
        self.assertNotIn("John", structure)
        self.assertFalse(hasattr(structure, "John"))
        structure.John = "Doe"
        self.assertIn("John", structure)
        self.assertTrue(hasattr(structure, "John"))
        del (structure.John)
        self.assertNotIn("John", structure)
        self.assertFalse(hasattr(structure, "John"))
        structure = foundations.data_structures.Structure(John=None, Jane=None)
        self.assertIsNone(structure.John)
        self.assertIsNone(structure["John"])
        structure.update(**{"John": "Doe", "Jane": "Doe"})
        self.assertEqual(structure.John, "Doe")
        self.assertEqual(structure["John"], "Doe")

    def test_structure_pickle(self):
        """
        Tests :class:`foundations.data_structures.Structure` class pickling.
        """

        structure = foundations.data_structures.Structure(John="Doe", Jane="Doe")

        data = pickle.dumps(structure)
        data = pickle.loads(data)
        self.assertEqual(structure, data)

        data = pickle.dumps(structure, pickle.HIGHEST_PROTOCOL)
        data = pickle.loads(data)
        self.assertEqual(structure, data)


class TestOrderedStructure(unittest.TestCase):
    """
    Defines :class:`foundations.data_structures.OrderedStructure` class units tests methods.
    """

    def test_ordered_structure(self):
        """
        Tests :class:`foundations.data_structures.OrderedStructure` class.
        """

        structure = foundations.data_structures.OrderedStructure([("personA", "John"),
                                                                  ("personB", "Jane"),
                                                                  ("personC", "Luke")])
        self.assertIn("personA", structure)
        self.assertTrue(hasattr(structure, "personA"))
        self.assertListEqual(["personA", "personB", "personC"], structure.keys())
        structure["personA"] = "Anakin"
        self.assertEquals("Anakin", structure.personA)
        structure.personA = "John"
        self.assertEquals("John", structure["personA"])
        del (structure.personA)
        self.assertTrue("personA" not in structure)
        del (structure["personB"])
        self.assertTrue(not hasattr(structure, "personB"))


class TestLookup(unittest.TestCase):
    """
    Defines :class:`foundations.data_structures.Lookup` class units tests methods.
    """

    def test_get_first_key_from_value(self):
        """
        Tests :meth:`foundations.data_structures.Lookup.get_first_key_from_value` method.
        """

        lookup = foundations.data_structures.Lookup(firstName="Doe", lastName="John", gender="male")
        self.assertEqual("firstName", lookup.get_first_key_from_value("Doe"))

    def test_get_keys_from_value(self):
        """
        Tests :meth:`foundations.data_structures.Lookup.get_keys_from_value` method.
        """

        lookup = foundations.data_structures.Lookup(John="Doe", Jane="Doe", Luke="Skywalker")
        self.assertListEqual(["Jane", "John"], lookup.get_keys_from_value("Doe"))


if __name__ == "__main__":
    unittest.main()
