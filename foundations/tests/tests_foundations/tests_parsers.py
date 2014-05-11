#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tests_parsers.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines units tests for :mod:`foundations.parsers` module.

**Others:**

"""

from __future__ import unicode_literals

import datetime
import os
import tempfile
import sys

if sys.version_info[:2] <= (2, 6):
    import unittest2 as unittest
    from ordereddict import OrderedDict
else:
    import unittest
    from collections import OrderedDict

import foundations.namespace
import foundations.parsers
import foundations.walkers
from foundations.parsers import PlistFileParser
from foundations.parsers import SectionsFileParser

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
           "COMPONENT_FILE",
           "IBL_SET_FILE",
           "TEMPLATE_FILE",
           "DEFAULTS_FILE",
           "STRIPPING_FILE",
           "PARSING_ERRORS_FILE",
           "STANDARD_FILES",
           "STANDARD_FILES_RAW_SECTIONS",
           "STANDARD_FILES_SECTIONS_AND_ATTRIBUTES",
           "DEFAULTS_FILE_SECTIONS_AND_ATTRIBUTES",
           "STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED",
           "STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED",
           "PARSING_ERRORS_LINES_AND_VALUES",
           "RANDOM_ATTRIBUTES",
           "RANDOM_COMMENTS",
           "SCRIPT_RAW_SECTION",
           "CHINESE_IBL_SET_FILE",
           "CHINESE_IBL_SET_FILE_RANDOM_ATTRIBUTES",
           "TestSectionsFileParser",
           "TestPlistFileParser",
           "TestGetAttributeCompound"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
COMPONENT_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.rc")
IBL_SET_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ibl")
TEMPLATE_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.sIBLT")
DEFAULTS_FILE = os.path.join(RESOURCES_DIRECTORY, "defaults.rc")
STRIPPING_FILE = os.path.join(RESOURCES_DIRECTORY, "stripping.rc")
PARSING_ERRORS_FILE = os.path.join(RESOURCES_DIRECTORY, "parsing_errors.rc")
PLIST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.plist")
STANDARD_FILES = {"component": COMPONENT_FILE,
                  "ibl_set": IBL_SET_FILE,
                  "template": TEMPLATE_FILE}
STANDARD_FILES_RAW_SECTIONS = {"component": None,
                               "ibl_set": None,
                               "template": ("Script",)}
STANDARD_FILES_SECTIONS_AND_ATTRIBUTES = {"component": OrderedDict([("Component",
                                                                     {"stripped": ["Name",
                                                                                   "Title",
                                                                                   "Module",
                                                                                   "Object",
                                                                                   "Rank",
                                                                                   "Version"],
                                                                      "namespaced": ["Component|Name",
                                                                                     "Component|Title",
                                                                                     "Component|Module",
                                                                                     "Component|Object",
                                                                                     "Component|Rank",
                                                                                     "Component|Version"]}),
                                                                    ("Informations",
                                                                     {"stripped": ["Author",
                                                                                   "Email",
                                                                                   "Url",
                                                                                   "Description"],
                                                                      "namespaced": ["Informations|Author",
                                                                                     "Informations|Email",
                                                                                     "Informations|Url",
                                                                                     "Informations|Description"]})]),
                                          "ibl_set": OrderedDict([("Header",
                                                                  {"stripped": ["ICOfile",
                                                                                "Name",
                                                                                "Author",
                                                                                "Location",
                                                                                "Comment",
                                                                                "GEOlat",
                                                                                "GEOlong",
                                                                                "Link",
                                                                                "Date",
                                                                                "Time",
                                                                                "Height",
                                                                                "North"],
                                                                   "namespaced": ["Header|ICOfile",
                                                                                  "Header|Name",
                                                                                  "Header|Author",
                                                                                  "Header|Location",
                                                                                  "Header|Comment",
                                                                                  "Header|GEOlat",
                                                                                  "Header|GEOlong",
                                                                                  "Header|Link",
                                                                                  "Header|Date",
                                                                                  "Header|Time",
                                                                                  "Header|Height",
                                                                                  "Header|North"]}),
                                                                 ("Background",
                                                                  {"stripped": ["BGfile",
                                                                                "BGmap",
                                                                                "BGu",
                                                                                "BGv",
                                                                                "BGheight"],
                                                                   "namespaced": ["Background|BGfile",
                                                                                  "Background|BGmap",
                                                                                  "Background|BGu",
                                                                                  "Background|BGv",
                                                                                  "Background|BGheight"]}),
                                                                 ("Enviroment",
                                                                  {"stripped": ["EVfile",
                                                                                "EVmap",
                                                                                "EVu",
                                                                                "EVv",
                                                                                "EVheight",
                                                                                "EVmulti",
                                                                                "EVgamma"],
                                                                   "namespaced": ["Enviroment|EVfile",
                                                                                  "Enviroment|EVmap",
                                                                                  "Enviroment|EVu",
                                                                                  "Enviroment|EVv",
                                                                                  "Enviroment|EVheight",
                                                                                  "Enviroment|EVmulti",
                                                                                  "Enviroment|EVgamma"]}),
                                                                 ("Reflection",
                                                                  {"stripped": ["REFfile",
                                                                                "REFmap",
                                                                                "REFu",
                                                                                "REFv",
                                                                                "REFheight",
                                                                                "REFmulti",
                                                                                "REFgamma"],
                                                                   "namespaced": ["Reflection|REFfile",
                                                                                  "Reflection|REFmap",
                                                                                  "Reflection|REFu",
                                                                                  "Reflection|REFv",
                                                                                  "Reflection|REFheight",
                                                                                  "Reflection|REFmulti",
                                                                                  "Reflection|REFgamma"]}),
                                                                 ("Sun",
                                                                  {"stripped": ["SUNcolor",
                                                                                "SUNmulti",
                                                                                "SUNu",
                                                                                "SUNv"],
                                                                   "namespaced": ["Sun|SUNcolor",
                                                                                  "Sun|SUNmulti",
                                                                                  "Sun|SUNu",
                                                                                  "Sun|SUNv"]}),
                                                                 ("Light1",
                                                                  {"stripped": ["LIGHTname",
                                                                                "LIGHTcolor",
                                                                                "LIGHTmulti",
                                                                                "LIGHTu",
                                                                                "LIGHTv"],
                                                                   "namespaced": ["Light1|LIGHTname",
                                                                                  "Light1|LIGHTcolor",
                                                                                  "Light1|LIGHTmulti",
                                                                                  "Light1|LIGHTu",
                                                                                  "Light1|LIGHTv"]})]),
                                          "template": OrderedDict([("Template",
                                                                    {"stripped": ["Name",
                                                                                  "Path",
                                                                                  "HelpFile",
                                                                                  "Release",
                                                                                  "Date",
                                                                                  "Author",
                                                                                  "Email",
                                                                                  "Url",
                                                                                  "Software",
                                                                                  "Version",
                                                                                  "Renderer",
                                                                                  "OutputScript",
                                                                                  "Comment"],
                                                                     "namespaced": ["Template|Name",
                                                                                    "Template|Path",
                                                                                    "Template|HelpFile",
                                                                                    "Template|Release",
                                                                                    "Template|Date",
                                                                                    "Template|Author",
                                                                                    "Template|Email",
                                                                                    "Template|Url",
                                                                                    "Template|Software",
                                                                                    "Template|Version",
                                                                                    "Template|Renderer",
                                                                                    "Template|OutputScript",
                                                                                    "Template|Comment"]}),
                                                                   ("sIBL File Attributes",
                                                                    {"stripped": ["Background|BGfile",
                                                                                  "Background|BGheight",
                                                                                  "Enviroment|EVfile",
                                                                                  "Enviroment|EVmulti",
                                                                                  "Enviroment|EVgamma",
                                                                                  "Reflection|REFfile",
                                                                                  "Reflection|REFmulti",
                                                                                  "Reflection|REFgamma",
                                                                                  "Sun|SUNu", "Sun|SUNv",
                                                                                  "Sun|SUNcolor",
                                                                                  "Sun|SUNmulti",
                                                                                  "Header|Height",
                                                                                  "Header|North",
                                                                                  "Lights|DynamicLights"],
                                                                     "namespaced": [
                                                                         "sIBL File Attributes|Background|BGfile",
                                                                         "sIBL File Attributes|Background|BGheight",
                                                                         "sIBL File Attributes|Enviroment|EVfile",
                                                                         "sIBL File Attributes|Enviroment|EVmulti",
                                                                         "sIBL File Attributes|Enviroment|EVgamma",
                                                                         "sIBL File Attributes|Reflection|REFfile",
                                                                         "sIBL File Attributes|Reflection|REFmulti",
                                                                         "sIBL File Attributes|Reflection|REFgamma",
                                                                         "sIBL File Attributes|Sun|SUNu",
                                                                         "sIBL File Attributes|Sun|SUNv",
                                                                         "sIBL File Attributes|Sun|SUNcolor",
                                                                         "sIBL File Attributes|Sun|SUNmulti",
                                                                         "sIBL File Attributes|Header|Height",
                                                                         "sIBL File Attributes|Header|North",
                                                                         "sIBL File Attributes|Lights|DynamicLights"]}),
                                                                   ("Common Attributes",
                                                                    {"stripped": ["createBackground",
                                                                                  "createLighting",
                                                                                  "createReflection",
                                                                                  "createSun",
                                                                                  "createLights"],
                                                                     "namespaced": [
                                                                         "Common Attributes|createBackground",
                                                                         "Common Attributes|createLighting",
                                                                         "Common Attributes|createReflection",
                                                                         "Common Attributes|createSun",
                                                                         "Common Attributes|createLights"]}),
                                                                   ("Additional Attributes",
                                                                    {"stripped": ["preserveSessionSettings",
                                                                                  "createFeedBack",
                                                                                  "createGround",
                                                                                  "shadowCatcher",
                                                                                  "hideLights",
                                                                                  "physicalSun",
                                                                                  "activateFinalGather",
                                                                                  "activateLinearWorkflow",
                                                                                  "framebufferGamma",
                                                                                  "photographicTonemapper",
                                                                                  "showCamerasDialog"],
                                                                     "namespaced": [
                                                                         "Additional Attributes|preserveSessionSettings",
                                                                         "Additional Attributes|createFeedBack",
                                                                         "Additional Attributes|createGround",
                                                                         "Additional Attributes|shadowCatcher",
                                                                         "Additional Attributes|hideLights",
                                                                         "Additional Attributes|physicalSun",
                                                                         "Additional Attributes|activateFinalGather",
                                                                         "Additional Attributes|activateLinearWorkflow",
                                                                         "Additional Attributes|framebufferGamma",
                                                                         "Additional Attributes|photographicTonemapper",
                                                                         "Additional Attributes|showCamerasDialog"]}),
                                                                   ("Remote Connection",
                                                                    {"stripped": ["ConnectionType",
                                                                                  "ExecutionCommand",
                                                                                  "DefaultAddress",
                                                                                  "DefaultPort"],
                                                                     "namespaced": ["Remote Connection|ConnectionType",
                                                                                    "Remote Connection|ExecutionCommand",
                                                                                    "Remote Connection|DefaultAddress",
                                                                                    "Remote Connection|DefaultPort"]}),
                                                                   ("Script",
                                                                    {"stripped": ["__raw__"],
                                                                     "namespaced": ["__raw__"]})])}

DEFAULTS_FILE_SECTIONS_AND_ATTRIBUTES = {"_defaults": {"_defaults|Default A": "Attribute 'Default A' value",
                                                       "_defaults|Default B": "Attribute 'Default B' value"},
                                         "Options A": {"Options A|John Doe": "Unknown"},
                                         "Options B": {"Options B|Jane Doe": "Unknown"}}

STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED = {"Stripping A": {"Stripping A|John Doe": "\"Unknown\""},
                                                   "Stripping B": {"Stripping B|Jane Doe": "\"Unknown\""}}

STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED = {"	Stripping A	": {"	Stripping A	|	John Doe	":
                                                                                   "	\"Unknown\"	"},
                                                       " Stripping B ": {" Stripping B | Jane Doe ": " \"Unknown\" "}}

PARSING_ERRORS_LINES_AND_VALUES = {3: "Attribute structure is invalid: {0}".format(
    "This statement will produce the line nº '3' parsing error.\n"),
                                   6: "Attribute structure is invalid: {0}".format(
                                       "This statement will produce the line nº '6' parsing error.\n"),
                                   12: "Attribute structure is invalid: {0}".format(
                                       "This statement will produce the line nº '12' parsing error.\n")}

RANDOM_ATTRIBUTES = {"component": {"Component|Name": "core.database",
                                   "Component|Module": "database",
                                   "Informations|Author": "Thomas Mansencal",
                                   "Informations|Email": "thomas.mansencal@gmail.com"},
                     "ibl_set": {"Header|ICOfile": "Icon.jpg",
                                "Header|Name": "Standard",
                                "Header|Comment": "Testing Foundations with units tests = fun!",
                                "Background|BGfile": "Standard_Background.jpg",
                                "Background|BGmap": "1",
                                "Enviroment|EVfile": "Standard_Lighting.jpg",
                                "Enviroment|EVmap": "1",
                                "Reflection|REFfile": "Standard_Reflection.jpg",
                                "Reflection|REFmap": "1",
                                "Sun|SUNcolor": "240,250,255",
                                "Sun|SUNmulti": "1.0",
                                "Light1|LIGHTcolor": "250,220,190",
                                "Light1|LIGHTmulti": "0.75"},
                     "template": {"Template|Name": "@Name | Standard | String | Template Name",
                                  "Template|Path": "@Path | | String | Template Path",
                                  "sIBL File Attributes|Background|BGfile": "@BGfile",
                                  "sIBL File Attributes|Background|BGheight": "@BGheight",
                                  "Common Attributes|createBackground": "@createBackground | 1 | Boolean | Create Background",
                                  "Common Attributes|createLighting": "@createLighting | 1 | Boolean | Create Lighting",
                                  "Additional Attributes|preserveSessionSettings":
                                      "@preserveSessionSettings | 1 | Boolean | Preserve Session Settings",
                                  "Additional Attributes|createFeedBack":
                                      "@createFeedBack | 1 | Boolean | Create Feedback",
                                  "Remote Connection|ConnectionType": "@ConnectionType | Socket | String | Connection Type",
                                  "Remote Connection|ExecutionCommand":
                                      "@ExecutionCommand | source \"$loaderScriptPath\"; | String | ExecutionCommand"}}

RANDOM_COMMENTS = {"component": {"Component|#0": {"content": "Component comment for tests purpose.", "id": 0},
                                 "Informations|#1": {"content": "Informations comment for tests purpose.", "id": 1}},
                   "ibl_set": {"Header|#0": {"content": "Header comment for tests purpose.", "id": 0},
                              "Header|#1": {"content": "Additional header comment for tests purpose.", "id": 1}},
                   "template": {"Template|#0": {"content": "Template comment for tests purpose.", "id": 0},
                                "sIBL File Attributes|#1": {"content":
                                                                "sIBL File Attributes comment for tests purpose.",
                                                            "id": 1}}}

SCRIPT_RAW_SECTION = ["// @OutputScript - @Release for @Software @Version\n",
                      "// Author: @Author\n",
                      "// EMail: @Email\n",
                      "// Homepage: @Url\n",
                      "// Template path: @Path\n",
                      "// Template last modified: @Date\n",
                      "// sIBL_GUI\n",
                      "string $backgroundFilePath = \"@BGfile\";\n",
                      "int $backgroundWidth = @BGheight*2;\n",
                      "string $lightingFilePath = \"@EVfile\";\n"]

CHINESE_IBL_SET_FILE = os.path.join(RESOURCES_DIRECTORY, "标准.ibl")
CHINESE_IBL_SET_FILE_RANDOM_ATTRIBUTES = {"Header|Name": "标准",
                                          "Header|Comment": "秎穾籺 飣偓啅 鋧鋓頠 踄 岪弨",
                                          "Header|Date": "2011:01:01",
                                          "Light1|LIGHTv": "0.85"}

PLIST_FILE_CONTENT = {"Dictionary A": {"String C": "My Value C", "String B": "My Value B"},
                      "Number A": 123456789,
                      "Array A": ["My Value A", "My Value B", "My Value C"],
                      "String A": "My Value A",
                      "Date A": datetime.datetime(2000, 1, 1, 0, 0),
                      "Boolean A": True,
                      "Data A": "My Value B"}

class TestSectionsFileParser(unittest.TestCase):
    """
    Defines :class:`foundations.parsers.SectionsFileParser` class units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("path",
                              "content",
                              "splitters",
                              "namespace_splitter",
                              "comment_limiters",
                              "comment_marker",
                              "quotation_markers",
                              "raw_section_content_identifier",
                              "defaults_section",
                              "sections",
                              "comments",
                              "parsing_errors",
                              "preserve_order")

        for attribute in required_attributes:
            self.assertIn(attribute, dir(SectionsFileParser))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ("parse",
                           "section_exists",
                           "attribute_exists",
                           "get_attributes",
                           "get_all_attributes",
                           "get_value",
                           "set_value",
                           "write")

        for method in required_methods:
            self.assertIn(method, dir(SectionsFileParser))

    def test__getitem__(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.__getitem__` method.
        """

        sections_file_parser = SectionsFileParser(IBL_SET_FILE)
        sections_file_parser.parse()
        self.assertListEqual(sections_file_parser["Header"].keys(),
                            STANDARD_FILES_SECTIONS_AND_ATTRIBUTES.get("ibl_set").get("Header").get("namespaced"))

    def test__setitem__(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.__setitem__` method.
        """

        sections_file_parser = SectionsFileParser()
        section = {"Attribute A" : "Value A"}
        sections_file_parser["Header"] = section
        self.assertEqual(sections_file_parser["Header"], sections_file_parser.sections["Header"])

    def test__iter__(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.__iter__` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            for key, value in sections_file_parser:
                self.assertIn(key, STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys())

    def test__contains__(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.__contains__` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            for key in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys():
                self.assertTrue(key in sections_file_parser)

    def test__len__(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.__len__` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertEqual(len(sections_file_parser), len(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys()))

    def test_parse(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.parse` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.read()
            parseSuccess = sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertTrue(parseSuccess)

            self.assertIsInstance(sections_file_parser.sections, OrderedDict)
            self.assertIsInstance(sections_file_parser.comments, OrderedDict)
            sections_file_parser.preserve_order = False
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertIsInstance(sections_file_parser.sections, dict)
            self.assertIsInstance(sections_file_parser.comments, dict)

    def test_parse_international(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.parse` in international specific context.
        """

        sections_file_parser = SectionsFileParser(CHINESE_IBL_SET_FILE)
        sections_file_parser.parse()
        for attribute, value in CHINESE_IBL_SET_FILE_RANDOM_ATTRIBUTES.iteritems():
            self.assertEqual(value, sections_file_parser.get_value(foundations.namespace.get_leaf(attribute),
                                                                foundations.namespace.get_root(attribute)))

    def test_sections(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class sections consistencies.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertListEqual(sections_file_parser.sections.keys(),
                                 STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys())
            sections_file_parser.preserve_order = False
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
                self.assertIn(section, sections_file_parser.sections)

    def test_raw_sections(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class raw sections consistencies.
        """

        sections_file_parser = SectionsFileParser(TEMPLATE_FILE)
        sections_file_parser.parse(raw_sections=("Script",))
        self.assertListEqual(sections_file_parser.sections["Script"]["__raw__"][0:10], SCRIPT_RAW_SECTION)

    def test_comments(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class comments consistencies.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertEqual(sections_file_parser.comments, OrderedDict())
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type], strip_comments=False)
            for comment, value in RANDOM_COMMENTS[type].iteritems():
                self.assertIn(comment, sections_file_parser.comments)
                self.assertEqual(value["id"], sections_file_parser.comments[comment]["id"])

    def test_defaults_section(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class default section consistency.
        """

        sections_file_parser = SectionsFileParser(DEFAULTS_FILE)
        sections_file_parser.parse()
        for section in DEFAULTS_FILE_SECTIONS_AND_ATTRIBUTES:
            self.assertIn(section, sections_file_parser.sections)

    def test_namespaces(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class namespaces consistencies.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type],
                                                                   namespaces=False)
            for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
                for attribute in sections_file_parser.sections[section]:
                    self.assertIn(attribute, STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["stripped"])

    def test_strip_whitespaces(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class whitespaces consistencies.
        """

        sections_file_parser = SectionsFileParser(STRIPPING_FILE)
        sections_file_parser.parse(strip_whitespaces=False)
        for section in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED:
            self.assertIn(section, sections_file_parser.sections)
            for attribute, value in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED[section].iteritems():
                self.assertIn(attribute, sections_file_parser.sections[section])
                self.assertIn(value, sections_file_parser.sections[section].itervalues())

    def test_strip_quotation_markers(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class quotation markers consistencies.
        """

        sections_file_parser = SectionsFileParser(STRIPPING_FILE)
        sections_file_parser.parse(strip_quotation_markers=False)
        for section in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED:
            self.assertIn(section, sections_file_parser.sections)
            for attribute, value in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED[section].iteritems():
                self.assertIn(attribute, sections_file_parser.sections[section])
                self.assertIn(value, sections_file_parser.sections[section].itervalues())

    def test_parsing_errors(self):
        """
        Tests :class:`foundations.parsers.SectionsFileParser` class parsing errors consistencies.
        """

        sections_file_parser = SectionsFileParser(PARSING_ERRORS_FILE)
        sections_file_parser.parse(raise_parsing_errors=False)
        for exception in sections_file_parser.parsing_errors:
            self.assertIn(exception.line, PARSING_ERRORS_LINES_AND_VALUES)
            self.assertEqual(exception.value, PARSING_ERRORS_LINES_AND_VALUES[exception.line])

    def test_section_exists(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.section_exists` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertTrue(sections_file_parser.section_exists(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys()[0]))
            self.assertFalse(sections_file_parser.section_exists("Unknown"))

    def test_attribute_exists(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.attribute_exists` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file, preserve_order=False)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            for attribute in RANDOM_ATTRIBUTES[type]:
                self.assertTrue(
                    sections_file_parser.attribute_exists(attribute, foundations.namespace.get_namespace(attribute,
                                                                                                     root_only=True)))
                self.assertFalse(
                    sections_file_parser.attribute_exists("Unknown", foundations.namespace.get_namespace(attribute,
                                                                                                     root_only=True)))

    def test_get_attributes(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.get_attributes` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
                self.assertListEqual(sections_file_parser.get_attributes(section,
                                                                      strip_namespaces=True).keys(),
                                     STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["stripped"])
                self.assertListEqual(sections_file_parser.get_attributes(section).keys(),
                                     STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["namespaced"])

    def test_get_all_attributes(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.get_all_attributes` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            attributes = sections_file_parser.get_all_attributes()
            tests_attributes = []
            for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
                tests_attributes.extend(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["namespaced"])
            self.assertListEqual(attributes.keys(), tests_attributes)

    def test_get_value(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.get_value` method.
        """

        for type, file in STANDARD_FILES.iteritems():
            sections_file_parser = SectionsFileParser(file, preserve_order=False)
            sections_file_parser.parse(raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            for attribute, value in RANDOM_ATTRIBUTES[type].iteritems():
                self.assertEqual(sections_file_parser.get_value(attribute, foundations.namespace.get_namespace(attribute,
                                                                                                           root_only=True)),
                                 value)
            self.assertEqual(sections_file_parser.get_value("attribute", "section", default=None), None)
            self.assertEqual(sections_file_parser.get_value("attribute", "section", default=list()), list())

    def test_set_value(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.set_value` method.
        """

        sections_file_parser = SectionsFileParser()
        sections_file_parser.set_value("Attribute A", "Section A", "Value A")
        self.assertEqual(sections_file_parser["Section A"]["Attribute A"], "Value A")
        sections_file_parser.set_value("Attribute A", "Section A", "Value Alternate")
        self.assertEqual(sections_file_parser["Section A"]["Attribute A"], "Value Alternate")
        sections_file_parser.set_value("Attribute B", "Section B", "Value B")
        self.assertEqual(sections_file_parser["Section B"]["Attribute B"], "Value B")

    def test_write(self):
        """
        Tests :meth:`foundations.parsers.SectionsFileParser.write` method.
        """

        # Standard sections files.
        for type, file in STANDARD_FILES.iteritems():
            read_sections_file_parser = SectionsFileParser(file)
            read_sections_file_parser.parse(strip_comments=False, raw_sections=STANDARD_FILES_RAW_SECTIONS[type])

            file_descriptor, path = tempfile.mkstemp()
            write_sections_file_parser = SectionsFileParser(unicode(path))
            write_sections_file_parser.sections = read_sections_file_parser.sections
            write_sections_file_parser.comments = read_sections_file_parser.comments
            write_sections_file_parser.write()

            checking_sections_file_parser = SectionsFileParser(write_sections_file_parser.path)
            checking_sections_file_parser.parse(strip_comments=False, raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertDictEqual(read_sections_file_parser.sections, checking_sections_file_parser.sections)
            os.close(file_descriptor)

        # Standard sections files with namespaces.
        for type, file in STANDARD_FILES.iteritems():
            read_sections_file_parser = SectionsFileParser(file)
            read_sections_file_parser.parse(namespaces=True,
                                        strip_comments=False,
                                        raw_sections=STANDARD_FILES_RAW_SECTIONS[type])

            file_descriptor, path = tempfile.mkstemp()
            write_sections_file_parser = SectionsFileParser(unicode(path))
            write_sections_file_parser.sections = read_sections_file_parser.sections
            write_sections_file_parser.comments = read_sections_file_parser.comments
            write_sections_file_parser.write(namespaces=True)

            checking_sections_file_parser = SectionsFileParser(write_sections_file_parser.path)
            checking_sections_file_parser.parse(namespaces=False,
                                            strip_comments=False,
                                            raw_sections=STANDARD_FILES_RAW_SECTIONS[type])
            self.assertDictEqual(read_sections_file_parser.sections, checking_sections_file_parser.sections)
            os.close(file_descriptor)

        # Default section file.
        read_sections_file_parser = SectionsFileParser(DEFAULTS_FILE)
        read_sections_file_parser.parse()

        file_descriptor, path = tempfile.mkstemp()
        write_sections_file_parser = SectionsFileParser(unicode(path))
        write_sections_file_parser.sections = read_sections_file_parser.sections
        write_sections_file_parser.comments = read_sections_file_parser.comments
        write_sections_file_parser.write()

        checking_sections_file_parser = SectionsFileParser(write_sections_file_parser.path)
        checking_sections_file_parser.parse()
        os.close(file_descriptor)

class TestPlistFileParser(unittest.TestCase):
    """
    Defines :class:`foundations.parsers.PlistFileParser` class units tests methods.
    """

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ("path",
                              "content",
                              "elements",
                              "parsing_errors",
                              "unserializers")

        for attribute in required_attributes:
            self.assertIn(attribute, dir(PlistFileParser))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ("parse",
                           "element_exists",
                           "filter_values",
                           "get_value")

        for method in required_methods:
            self.assertIn(method, dir(PlistFileParser))

    def test_parse(self):
        """
        Tests :meth:`foundations.parsers.PlistFileParser.parse` method.
        """

        plist_file_parser = PlistFileParser(PLIST_FILE)
        self.assertTrue(plist_file_parser.parse())
        self.assertDictEqual(plist_file_parser.elements, PLIST_FILE_CONTENT)

    def test_element_exists(self):
        """
        Tests :meth:`foundations.parsers.PlistFileParser.element_exists` method.
        """

        plist_file_parser = PlistFileParser(PLIST_FILE)
        plist_file_parser.parse()
        self.assertTrue(plist_file_parser.element_exists("String A"))
        self.assertFalse(plist_file_parser.element_exists("String Nemo"))

    def test_filter_values(self):
        """
        Tests :meth:`foundations.parsers.PlistFileParser.filter_values` method.
        """

        plist_file_parser = PlistFileParser(PLIST_FILE)
        plist_file_parser.parse()
        self.assertEqual(plist_file_parser.filter_values(r"String A"), [PLIST_FILE_CONTENT["String A"]])
        self.assertEqual(sorted(plist_file_parser.filter_values(r"String.*")), sorted([PLIST_FILE_CONTENT["String A"],
                                                                                    PLIST_FILE_CONTENT["Dictionary A"][
                                                                                        "String B"],
                                                                                    PLIST_FILE_CONTENT["Dictionary A"][
                                                                                        "String C"]]))
        self.assertEqual(plist_file_parser.filter_values(r"Date A"), [PLIST_FILE_CONTENT["Date A"]])

    def test_get_value(self):
        """
        Tests :meth:`foundations.parsers.PlistFileParser.get_value` method.
        """

        plist_file_parser = PlistFileParser(PLIST_FILE)
        plist_file_parser.parse()
        for item in foundations.walkers.dictionaries_walker(PLIST_FILE_CONTENT):
            path, element, value = item
            self.assertEqual(value, plist_file_parser.get_value(element))

class TestGetAttributeCompound(unittest.TestCase):
    """
    Defines :func:`foundations.parsers.get_attribute_compound` definition units tests methods.
    """

    def test_get_attribute_compound(self):
        """
        Tests :func:`foundations.parsers.get_attribute_compound` definition.
        """

        self.assertIsInstance(foundations.parsers.get_attribute_compound("Attribute", "Value"),
                              foundations.parsers.AttributeCompound)

        self.assertEqual(None, foundations.parsers.get_attribute_compound("Attribute").value)

        compound = foundations.parsers.AttributeCompound(name="Attribute",
                                                         value="Value",
                                                         link="@Link",
                                                         type="Boolean",
                                                         alias="Link Parameter")
        data = "@Link | Value | Boolean | Link Parameter"
        self.assertEqual(compound.name, foundations.parsers.get_attribute_compound("Attribute", data).name)
        self.assertEqual(compound.value, foundations.parsers.get_attribute_compound("Attribute", data).value)
        self.assertEqual(compound.link, foundations.parsers.get_attribute_compound("Attribute", data).link)
        self.assertEqual(compound.type, foundations.parsers.get_attribute_compound("Attribute", data).type)
        self.assertEqual(compound.alias, foundations.parsers.get_attribute_compound("Attribute", data).alias)

        data = "@Link"
        self.assertEqual(compound.link, foundations.parsers.get_attribute_compound("Attribute", data).link)

if __name__ == "__main__":
    import foundations.tests.utilities

    unittest.main()
