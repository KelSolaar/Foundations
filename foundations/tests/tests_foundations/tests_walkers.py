#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**tests_walkers.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.walkers` module.

**Others:**

"""

from __future__ import unicode_literals

import os
import re
import sys

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
else:
    import unittest

import foundations.strings
import foundations.walkers
from foundations.nodes import AbstractCompositeNode

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
           "ROOT_DIRECTORY",
           "FILES_TREE_HIERARCHY",
           "TREE_HIERARCHY",
           "CHINESE_ROOT_DIRECTORY",
           "CHINESE_FILES_TREE_HIERARCHY",
           "CHINESE_TREE_HIERARCHY",
           "TestFilesWalker",
           "TestDepthWalker",
           "TestDictionariesWalker",
           "TestNodesWalker"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
ROOT_DIRECTORY = "standard"
FILES_TREE_HIERARCHY = ("lorem_ipsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT",
                        "level_0/standard.ibl",
                        "level_0/level_1/lorem_ipsum.txt", "level_0/level_1/standard.rc",
                        "level_0/level_1/level_2/standard.sIBLT")
TREE_HIERARCHY = ((["level_0"], ["lorem_ipsum.txt", "standard.ibl", "standard.rc", "standard.sIBLT"]),
                  (["level_1"], ["standard.ibl"]),
                  (["level_2"], ["lorem_ipsum.txt", "standard.rc"]),
                  ([], ["standard.sIBLT"]))
CHINESE_ROOT_DIRECTORY = "标准"
CHINESE_FILES_TREE_HIERARCHY = ("内容.txt",
                                "0级/无效.txt",
                                "0级/1级/空虚.txt",
                                "0级/1级/2级/内容.txt", "0级/1级/2级/物.txt")
CHINESE_TREE_HIERARCHY = ((["0级"], ["内容.txt"]),
                          (["1级"], ["无效.txt"]),
                          (["2级"], ["空虚.txt"]),
                          ([], ["内容.txt", "物.txt"]))


class TestFilesWalker(unittest.TestCase):
    """
    Defines :func:`foundations.walkers.files_walker` definition units tests methods.
    """

    def test_files_walker(self):
        """
        Tests :func:`foundations.walkers.files_walker` definition.
        """

        root_directory = os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY)
        for path in foundations.walkers.files_walker(root_directory):
            self.assertTrue(os.path.exists(path))

        reference_paths = [foundations.strings.replace(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY, path),
                                                       {"/": "|", "\\": "|"}) for path in FILES_TREE_HIERARCHY]
        walker_files = \
            [foundations.strings.replace(path, {"/": "|", "\\": "|"})
             for path in foundations.walkers.files_walker(root_directory)]
        for item in reference_paths:
            self.assertIn(item, walker_files)

        walker_files = \
            [foundations.strings.replace(path, {"/": "|", "\\": "|"})
             for path in foundations.walkers.files_walker(root_directory, filters_out=("\.rc$",))]
        for item in walker_files:
            self.assertTrue(not re.search(r"\.rc$", item))

        walker_files = \
            [foundations.strings.replace(path, {"/": "|", "\\": "|"})
             for path in
             foundations.walkers.files_walker(root_directory, filters_out=("\.ibl", "\.rc$", "\.sIBLT$", "\.txt$"))]
        self.assertTrue(not walker_files)

    def test_files_walker_international(self):
        """
        Tests :func:`foundations.walkers.files_walker` definition in international specific context.
        """

        root_directory = os.path.join(RESOURCES_DIRECTORY, CHINESE_ROOT_DIRECTORY)
        for path in foundations.walkers.files_walker(root_directory):
            self.assertTrue(os.path.exists(path))

        reference_paths = [foundations.strings.replace(os.path.join(RESOURCES_DIRECTORY, CHINESE_ROOT_DIRECTORY, path),
                                                       {"/": "|", "\\": "|"}) for path in CHINESE_FILES_TREE_HIERARCHY]
        walker_files = \
            [foundations.strings.replace(path, {"/": "|", "\\": "|"})
             for path in foundations.walkers.files_walker(root_directory)]
        for item in reference_paths:
            self.assertIn(item, walker_files)

        walker_files = \
            [foundations.strings.replace(path, {"/": "|", "\\": "|"})
             for path in foundations.walkers.files_walker(root_directory, filters_out=("\.rc$",))]
        for item in walker_files:
            self.assertTrue(not re.search(r"\.rc$", item))

        walker_files = \
            [foundations.strings.replace(path, {"/": "|", "\\": "|"})
             for path in
             foundations.walkers.files_walker(root_directory, filters_out=("\.ibl", "\.rc$", "\.sIBLT$", "\.txt$"))]
        self.assertTrue(not walker_files)


class TestDepthWalker(unittest.TestCase):
    """
    Defines :func:`foundations.walkers.depth_walker` definition units tests methods.
    """

    def test_depth_walker(self):
        """
        Tests :func:`foundations.walkers.depth_walker` definition.
        """

        for i, value in \
                enumerate(foundations.walkers.depth_walker(os.path.join(RESOURCES_DIRECTORY, ROOT_DIRECTORY),
                                                           maximum_depth=2)):
            parent_directory, directories, files = value
            self.assertEqual((directories, sorted(files)), (TREE_HIERARCHY[i][0], sorted(TREE_HIERARCHY[i][1])))

    def test_depth_walkerInternational(self):
        """
        Tests :func:`foundations.walkers.depth_walker` definition in international specific context.
        """

        for i, value in \
                enumerate(foundations.walkers.depth_walker(os.path.join(RESOURCES_DIRECTORY, CHINESE_ROOT_DIRECTORY),
                                                           maximum_depth=2)):
            parent_directory, directories, files = value
            self.assertEqual(
                (directories, sorted(files)), (CHINESE_TREE_HIERARCHY[i][0], sorted(CHINESE_TREE_HIERARCHY[i][1])))


class TestDictionariesWalker(unittest.TestCase):
    """
    Defines :func:`foundations.walkers.dictionaries_walker` definition units tests methods.
    """

    def test_dictionaries_walker(self):
        """
        Tests :func:`foundations.walkers.dictionaries_walker` definition.
        """

        nested_dictionary = {"Level 1A": {"Level 2A": {"Level 3A": "Higher Level"}},
                             "Level 1B": "Lower level", "Level 1C": {}}
        yielded_values = ((("Level 1A", "Level 2A"), "Level 3A", "Higher Level"), ((), "Level 1B", "Lower level"))
        for value in foundations.walkers.dictionaries_walker(nested_dictionary):
            self.assertIsInstance(value, tuple)
            self.assertIn(value, yielded_values)
        for path, key, value in foundations.walkers.dictionaries_walker(nested_dictionary):
            self.assertIsInstance(path, tuple)
            self.assertIsInstance(key, unicode)
            self.assertIsInstance(value, unicode)


class TestNodesWalker(unittest.TestCase):
    """
    Defines :func:`foundations.walkers.nodes_walker` definition units tests methods.
    """

    def test_nodes_walker(self):
        """
        Tests :func:`foundations.walkers.nodes_walker` definition.
        """

        node_a = AbstractCompositeNode("MyNodeA")
        node_b = AbstractCompositeNode("MyNodeB", node_a)
        node_c = AbstractCompositeNode("MyNodeC", node_a)
        node_d = AbstractCompositeNode("MyNodeD", node_b)
        node_e = AbstractCompositeNode("MyNodeE", node_b)
        node_f = AbstractCompositeNode("MyNodeF", node_d)
        node_g = AbstractCompositeNode("MyNodeG", node_f)
        node_h = AbstractCompositeNode("MyNodeH", node_g)
        values = [node_b, node_c, node_d, node_e, node_f, node_g, node_h]
        for node in values:
            self.assertIn(node, list(foundations.walkers.nodes_walker(node_a)))

        values = [node_g, node_f, node_d, node_b, node_a]
        self.assertEquals(list(foundations.walkers.nodes_walker(node_h, ascendants=True)), values)


if __name__ == "__main__":
    import foundations.tests.utilities

    unittest.main()
