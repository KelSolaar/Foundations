#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsParsers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`foundations.parsers` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.namespace
import foundations.parsers
import foundations.walkers
from foundations.parsers import PlistFileParser
from foundations.parsers import SectionsFileParser

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
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
		   "SectionsFileParserTestCase",
		   "PlistFileParserTestCase",
		   "GetAttributeCompoundTestCase"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
COMPONENT_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.rc")
IBL_SET_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ibl")
TEMPLATE_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.sIBLT")
DEFAULTS_FILE = os.path.join(RESOURCES_DIRECTORY, "defaults.rc")
STRIPPING_FILE = os.path.join(RESOURCES_DIRECTORY, "stripping.rc")
PARSING_ERRORS_FILE = os.path.join(RESOURCES_DIRECTORY, "parsingErrors.rc")
PLIST_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.plist")
STANDARD_FILES = {"component": COMPONENT_FILE,
				  "iblSet": IBL_SET_FILE,
				  "template": TEMPLATE_FILE}
STANDARD_FILES_RAW_SECTIONS = {"component": None,
							   "iblSet": None,
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
										  "iblSet": OrderedDict([("Header",
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
					 "iblSet": {"Header|ICOfile": "Icon.jpg",
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
				   "iblSet": {"Header|#0": {"content": "Header comment for tests purpose.", "id": 0},
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

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SectionsFileParserTestCase(unittest.TestCase):
	"""
	Defines :class:`foundations.parsers.SectionsFileParser` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		Tests presence of required attributes.
		"""

		requiredAttributes = ("path",
							  "content",
							  "splitters",
							  "namespaceSplitter",
							  "commentLimiters",
							  "commentMarker",
							  "quotationMarkers",
							  "rawSectionContentIdentifier",
							  "defaultsSection",
							  "sections",
							  "comments",
							  "parsingErrors",
							  "preserveOrder")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(SectionsFileParser))

	def testRequiredMethods(self):
		"""
		Tests presence of required methods.
		"""

		requiredMethods = ("parse",
						   "sectionExists",
						   "attributeExists",
						   "getAttributes",
						   "getAllAttributes",
						   "getValue",
						   "setValue",
						   "write")

		for method in requiredMethods:
			self.assertIn(method, dir(SectionsFileParser))

	def test__getitem__(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.__getitem__` method.
		"""

		sectionsFileParser = SectionsFileParser(IBL_SET_FILE)
		sectionsFileParser.parse()
		self.assertListEqual(sectionsFileParser["Header"].keys(),
							STANDARD_FILES_SECTIONS_AND_ATTRIBUTES.get("iblSet").get("Header").get("namespaced"))

	def test__setitem__(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.__setitem__` method.
		"""

		sectionsFileParser = SectionsFileParser()
		section = {"Attribute A" : "Value A"}
		sectionsFileParser["Header"] = section
		self.assertEqual(sectionsFileParser["Header"], sectionsFileParser.sections["Header"])

	def test__iter__(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.__iter__` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for key, value in sectionsFileParser:
				self.assertIn(key, STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys())

	def test__contains__(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.__contains__` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for key in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys():
				self.assertTrue(key in sectionsFileParser)

	def test__len__(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.__len__` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertEqual(len(sectionsFileParser), len(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys()))

	def testParse(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.parse` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.read()
			parseSuccess = sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertTrue(parseSuccess)

			self.assertIsInstance(sectionsFileParser.sections, OrderedDict)
			self.assertIsInstance(sectionsFileParser.comments, OrderedDict)
			sectionsFileParser.preserveOrder = False
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertIsInstance(sectionsFileParser.sections, dict)
			self.assertIsInstance(sectionsFileParser.comments, dict)

	def testParseInternational(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.parse` in international specific context.
		"""

		sectionsFileParser = SectionsFileParser(CHINESE_IBL_SET_FILE)
		sectionsFileParser.parse()
		for attribute, value in CHINESE_IBL_SET_FILE_RANDOM_ATTRIBUTES.iteritems():
			self.assertEqual(value, sectionsFileParser.getValue(foundations.namespace.getLeaf(attribute),
																foundations.namespace.getRoot(attribute)))

	def testSections(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class sections consistencies.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertListEqual(sectionsFileParser.sections.keys(),
								 STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys())
			sectionsFileParser.preserveOrder = False
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
				self.assertIn(section, sectionsFileParser.sections)

	def testRawSections(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class raw sections consistencies.
		"""

		sectionsFileParser = SectionsFileParser(TEMPLATE_FILE)
		sectionsFileParser.parse(rawSections=("Script",))
		self.assertListEqual(sectionsFileParser.sections["Script"]["__raw__"][0:10], SCRIPT_RAW_SECTION)

	def testComments(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class comments consistencies.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertEqual(sectionsFileParser.comments, OrderedDict())
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type], stripComments=False)
			for comment, value in RANDOM_COMMENTS[type].iteritems():
				self.assertIn(comment, sectionsFileParser.comments)
				self.assertEqual(value["id"], sectionsFileParser.comments[comment]["id"])

	def testDefaultsSection(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class default section consistency.
		"""

		sectionsFileParser = SectionsFileParser(DEFAULTS_FILE)
		sectionsFileParser.parse()
		for section in DEFAULTS_FILE_SECTIONS_AND_ATTRIBUTES:
			self.assertIn(section, sectionsFileParser.sections)

	def testNamespaces(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class namespaces consistencies.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type],
																   namespaces=False)
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
				for attribute in sectionsFileParser.sections[section]:
					self.assertIn(attribute, STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["stripped"])

	def testStripWhitespaces(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class whitespaces consistencies.
		"""

		sectionsFileParser = SectionsFileParser(STRIPPING_FILE)
		sectionsFileParser.parse(stripWhitespaces=False)
		for section in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED:
			self.assertIn(section, sectionsFileParser.sections)
			for attribute, value in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED[section].iteritems():
				self.assertIn(attribute, sectionsFileParser.sections[section])
				self.assertIn(value, sectionsFileParser.sections[section].itervalues())

	def testStripQuotationMarkers(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class quotation markers consistencies.
		"""

		sectionsFileParser = SectionsFileParser(STRIPPING_FILE)
		sectionsFileParser.parse(stripQuotationMarkers=False)
		for section in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED:
			self.assertIn(section, sectionsFileParser.sections)
			for attribute, value in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED[section].iteritems():
				self.assertIn(attribute, sectionsFileParser.sections[section])
				self.assertIn(value, sectionsFileParser.sections[section].itervalues())

	def testParsingErrors(self):
		"""
		Tests :class:`foundations.parsers.SectionsFileParser` class parsing errors consistencies.
		"""

		sectionsFileParser = SectionsFileParser(PARSING_ERRORS_FILE)
		sectionsFileParser.parse(raiseParsingErrors=False)
		for exception in sectionsFileParser.parsingErrors:
			self.assertIn(exception.line, PARSING_ERRORS_LINES_AND_VALUES)
			self.assertEqual(exception.value, PARSING_ERRORS_LINES_AND_VALUES[exception.line])

	def testSectionExists(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.sectionExists` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertTrue(sectionsFileParser.sectionExists(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys()[0]))
			self.assertFalse(sectionsFileParser.sectionExists("Unknown"))

	def testAttributeExists(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.attributeExists` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file, preserveOrder=False)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for attribute in RANDOM_ATTRIBUTES[type]:
				self.assertTrue(
					sectionsFileParser.attributeExists(attribute, foundations.namespace.getNamespace(attribute,
																									 rootOnly=True)))
				self.assertFalse(
					sectionsFileParser.attributeExists("Unknown", foundations.namespace.getNamespace(attribute,
																									 rootOnly=True)))

	def testGetAttributes(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.getAttributes` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
				self.assertListEqual(sectionsFileParser.getAttributes(section,
																	  stripNamespaces=True).keys(),
									 STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["stripped"])
				self.assertListEqual(sectionsFileParser.getAttributes(section).keys(),
									 STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["namespaced"])

	def testGetAllAttributes(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.getAllAttributes` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			attributes = sectionsFileParser.getAllAttributes()
			testsAttributes = []
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
				testsAttributes.extend(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["namespaced"])
			self.assertListEqual(attributes.keys(), testsAttributes)

	def testGetValue(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.getValue` method.
		"""

		for type, file in STANDARD_FILES.iteritems():
			sectionsFileParser = SectionsFileParser(file, preserveOrder=False)
			sectionsFileParser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for attribute, value in RANDOM_ATTRIBUTES[type].iteritems():
				self.assertEqual(sectionsFileParser.getValue(attribute, foundations.namespace.getNamespace(attribute,
																										   rootOnly=True)),
								 value)
			self.assertEqual(sectionsFileParser.getValue("attribute", "section", default=None), None)
			self.assertEqual(sectionsFileParser.getValue("attribute", "section", default=list()), list())

	def testSetValue(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.setValue` method.
		"""

		sectionsFileParser = SectionsFileParser()
		sectionsFileParser.setValue("Attribute A", "Section A", "Value A")
		self.assertEqual(sectionsFileParser["Section A"]["Attribute A"], "Value A")
		sectionsFileParser.setValue("Attribute A", "Section A", "Value Alternate")
		self.assertEqual(sectionsFileParser["Section A"]["Attribute A"], "Value Alternate")
		sectionsFileParser.setValue("Attribute B", "Section B", "Value B")
		self.assertEqual(sectionsFileParser["Section B"]["Attribute B"], "Value B")

	def testWrite(self):
		"""
		Tests :meth:`foundations.parsers.SectionsFileParser.write` method.
		"""

		# Standard sections files.
		for type, file in STANDARD_FILES.iteritems():
			readSectionsFileParser = SectionsFileParser(file)
			readSectionsFileParser.parse(stripComments=False, rawSections=STANDARD_FILES_RAW_SECTIONS[type])

			fileDescriptor, path = tempfile.mkstemp()
			writeSectionsFileParser = SectionsFileParser(unicode(path))
			writeSectionsFileParser.sections = readSectionsFileParser.sections
			writeSectionsFileParser.comments = readSectionsFileParser.comments
			writeSectionsFileParser.write()

			checkingSectionsFileParser = SectionsFileParser(writeSectionsFileParser.path)
			checkingSectionsFileParser.parse(stripComments=False, rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertDictEqual(readSectionsFileParser.sections, checkingSectionsFileParser.sections)
			os.close(fileDescriptor)

		# Standard sections files with namespaces.
		for type, file in STANDARD_FILES.iteritems():
			readSectionsFileParser = SectionsFileParser(file)
			readSectionsFileParser.parse(namespaces=True,
										stripComments=False,
										rawSections=STANDARD_FILES_RAW_SECTIONS[type])

			fileDescriptor, path = tempfile.mkstemp()
			writeSectionsFileParser = SectionsFileParser(unicode(path))
			writeSectionsFileParser.sections = readSectionsFileParser.sections
			writeSectionsFileParser.comments = readSectionsFileParser.comments
			writeSectionsFileParser.write(namespaces=True)

			checkingSectionsFileParser = SectionsFileParser(writeSectionsFileParser.path)
			checkingSectionsFileParser.parse(namespaces=False,
											stripComments=False,
											rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertDictEqual(readSectionsFileParser.sections, checkingSectionsFileParser.sections)
			os.close(fileDescriptor)

		# Default section file.
		readSectionsFileParser = SectionsFileParser(DEFAULTS_FILE)
		readSectionsFileParser.parse()

		fileDescriptor, path = tempfile.mkstemp()
		writeSectionsFileParser = SectionsFileParser(unicode(path))
		writeSectionsFileParser.sections = readSectionsFileParser.sections
		writeSectionsFileParser.comments = readSectionsFileParser.comments
		writeSectionsFileParser.write()

		checkingSectionsFileParser = SectionsFileParser(writeSectionsFileParser.path)
		checkingSectionsFileParser.parse()
		os.close(fileDescriptor)

class PlistFileParserTestCase(unittest.TestCase):
	"""
	Defines :class:`foundations.parsers.PlistFileParser` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		Tests presence of required attributes.
		"""

		requiredAttributes = ("path",
							  "content",
							  "elements",
							  "parsingErrors",
							  "unserializers")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(PlistFileParser))

	def testRequiredMethods(self):
		"""
		Tests presence of required methods.
		"""

		requiredMethods = ("parse",
						   "elementExists",
						   "filterValues",
						   "getValue")

		for method in requiredMethods:
			self.assertIn(method, dir(PlistFileParser))

	def testParse(self):
		"""
		Tests :meth:`foundations.parsers.PlistFileParser.parse` method.
		"""

		plistFileParser = PlistFileParser(PLIST_FILE)
		self.assertTrue(plistFileParser.parse())
		self.assertDictEqual(plistFileParser.elements, PLIST_FILE_CONTENT)

	def testElementExists(self):
		"""
		Tests :meth:`foundations.parsers.PlistFileParser.elementExists` method.
		"""

		plistFileParser = PlistFileParser(PLIST_FILE)
		plistFileParser.parse()
		self.assertTrue(plistFileParser.elementExists("String A"))
		self.assertFalse(plistFileParser.elementExists("String Nemo"))

	def testFilterValues(self):
		"""
		Tests :meth:`foundations.parsers.PlistFileParser.filterValues` method.
		"""

		plistFileParser = PlistFileParser(PLIST_FILE)
		plistFileParser.parse()
		self.assertEqual(plistFileParser.filterValues(r"String A"), [PLIST_FILE_CONTENT["String A"]])
		self.assertEqual(sorted(plistFileParser.filterValues(r"String.*")), sorted([PLIST_FILE_CONTENT["String A"],
																					PLIST_FILE_CONTENT["Dictionary A"][
																						"String B"],
																					PLIST_FILE_CONTENT["Dictionary A"][
																						"String C"]]))
		self.assertEqual(plistFileParser.filterValues(r"Date A"), [PLIST_FILE_CONTENT["Date A"]])

	def testGetValue(self):
		"""
		Tests :meth:`foundations.parsers.PlistFileParser.getValue` method.
		"""

		plistFileParser = PlistFileParser(PLIST_FILE)
		plistFileParser.parse()
		for item in foundations.walkers.dictionariesWalker(PLIST_FILE_CONTENT):
			path, element, value = item
			self.assertEqual(value, plistFileParser.getValue(element))

class GetAttributeCompoundTestCase(unittest.TestCase):
	"""
	Defines :func:`foundations.parsers.getAttributeCompound` definition units tests methods.
	"""

	def testGetAttributeCompound(self):
		"""
		Tests :func:`foundations.parsers.getAttributeCompound` definition.
		"""

		self.assertIsInstance(foundations.parsers.getAttributeCompound("Attribute", "Value"),
							  foundations.parsers.AttributeCompound)

		self.assertEqual(None, foundations.parsers.getAttributeCompound("Attribute").value)

		compound = foundations.parsers.AttributeCompound(name="Attribute",
														 value="Value",
														 link="@Link",
														 type="Boolean",
														 alias="Link Parameter")
		data = "@Link | Value | Boolean | Link Parameter"
		self.assertEqual(compound.name, foundations.parsers.getAttributeCompound("Attribute", data).name)
		self.assertEqual(compound.value, foundations.parsers.getAttributeCompound("Attribute", data).value)
		self.assertEqual(compound.link, foundations.parsers.getAttributeCompound("Attribute", data).link)
		self.assertEqual(compound.type, foundations.parsers.getAttributeCompound("Attribute", data).type)
		self.assertEqual(compound.alias, foundations.parsers.getAttributeCompound("Attribute", data).alias)

		data = "@Link"
		self.assertEqual(compound.link, foundations.parsers.getAttributeCompound("Attribute", data).link)

if __name__ == "__main__":
	import foundations.tests.utilities

	unittest.main()
