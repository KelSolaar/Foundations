#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsParser.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`foundations.parser` module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import unittest
from collections import OrderedDict

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.namespace as namespace
import foundations.parser
from foundations.parser import Parser

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
COMPONENT_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.rc")
IBL_SET_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ibl")
TEMPLATE_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.sIBLT")
DEFAULTS_FILE = os.path.join(RESOURCES_DIRECTORY, "defaults.rc")
STRIPPING_FILE = os.path.join(RESOURCES_DIRECTORY, "stripping.rc")
PARSING_ERRORS_FILE = os.path.join(RESOURCES_DIRECTORY, "parsingErrors.rc")
STANDARD_FILES = {"component" : COMPONENT_FILE,
		"iblSet" : IBL_SET_FILE,
		"template" : TEMPLATE_FILE}
STANDARD_FILES_RAW_SECTIONS = {"component" : None,
					"iblSet" : None,
					"template" : ("Script",)}
STANDARD_FILES_SECTIONS_AND_ATTRIBUTES = {"component" : OrderedDict([("Component", {"stripped" : ["Name", "Module", "Object", "Rank", "Version"],
																"namespaced" : ["Component|Name", "Component|Module", "Component|Object", "Component|Rank", "Component|Version"]}),
													("Informations", {"stripped" : ["Author", "Email", "Url", "Description"],
																"namespaced" : ["Informations|Author", "Informations|Email", "Informations|Url", "Informations|Description"]})]),
							"iblSet" : OrderedDict([("Header", {"stripped" : ["ICOfile", "Name", "Author", "Location", "Comment", "GEOlat", "GEOlong", "Link", "Date", "Time", "Height", "North"],
															"namespaced" : ["Header|ICOfile", "Header|Name", "Header|Author", "Header|Location", "Header|Comment", "Header|GEOlat", "Header|GEOlong", "Header|Link", "Header|Date", "Header|Time", "Header|Height", "Header|North"]}),
												("Background", {"stripped" : ["BGfile", "BGmap", "BGu", "BGv", "BGheight"],
															"namespaced" : ["Background|BGfile", "Background|BGmap", "Background|BGu", "Background|BGv", "Background|BGheight"]}),
												("Enviroment", {"stripped" : ["EVfile", "EVmap", "EVu", "EVv", "EVheight", "EVmulti", "EVgamma"],
															"namespaced" : ["Enviroment|EVfile", "Enviroment|EVmap", "Enviroment|EVu", "Enviroment|EVv", "Enviroment|EVheight", "Enviroment|EVmulti", "Enviroment|EVgamma"]}),
												("Reflection", {"stripped" : ["REFfile", "REFmap", "REFu", "REFv", "REFheight", "REFmulti", "REFgamma"],
															"namespaced" : ["Reflection|REFfile", "Reflection|REFmap", "Reflection|REFu", "Reflection|REFv", "Reflection|REFheight", "Reflection|REFmulti", "Reflection|REFgamma"]}),
												("Sun", {"stripped" : ["SUNcolor", "SUNmulti", "SUNu", "SUNv"],
															"namespaced" : ["Sun|SUNcolor", "Sun|SUNmulti", "Sun|SUNu", "Sun|SUNv"]}),
												("Light1", {"stripped" : ["LIGHTname", "LIGHTcolor", "LIGHTmulti", "LIGHTu", "LIGHTv"],
															"namespaced" : ["Light1|LIGHTname", "Light1|LIGHTcolor", "Light1|LIGHTmulti", "Light1|LIGHTu", "Light1|LIGHTv"]})]),
							"template" : OrderedDict([("Template", {"stripped" : ["Name", "Path", "HelpFile", "Release", "Date", "Author", "Email", "Url", "Software", "Version", "Renderer", "OutputScript", "Comment"],
																"namespaced" : ["Template|Name", "Template|Path", "Template|HelpFile", "Template|Release", "Template|Date", "Template|Author", "Template|Email", "Template|Url", "Template|Software", "Template|Version", "Template|Renderer", "Template|OutputScript", "Template|Comment"]}),
													("sIBL File Attributes", {"stripped" : ["Background|BGfile", "Background|BGheight", "Enviroment|EVfile", "Enviroment|EVmulti", "Enviroment|EVgamma", "Reflection|REFfile", "Reflection|REFmulti", "Reflection|REFgamma", "Sun|SUNu", "Sun|SUNv", "Sun|SUNcolor", "Sun|SUNmulti", "Header|Height", "Header|North", "Lights|DynamicLights"],
																"namespaced" : ["sIBL File Attributes|Background|BGfile", "sIBL File Attributes|Background|BGheight", "sIBL File Attributes|Enviroment|EVfile", "sIBL File Attributes|Enviroment|EVmulti", "sIBL File Attributes|Enviroment|EVgamma", "sIBL File Attributes|Reflection|REFfile", "sIBL File Attributes|Reflection|REFmulti", "sIBL File Attributes|Reflection|REFgamma", "sIBL File Attributes|Sun|SUNu", "sIBL File Attributes|Sun|SUNv", "sIBL File Attributes|Sun|SUNcolor", "sIBL File Attributes|Sun|SUNmulti", "sIBL File Attributes|Header|Height", "sIBL File Attributes|Header|North", "sIBL File Attributes|Lights|DynamicLights"]}),
													("Common Attributes", {"stripped" : ["createBackground", "createLighting", "createReflection", "createSun", "createLights"],
																"namespaced" : ["Common Attributes|createBackground", "Common Attributes|createLighting", "Common Attributes|createReflection", "Common Attributes|createSun", "Common Attributes|createLights"]}),
													("Additional Attributes", {"stripped" : ["preserveSessionSettings", "createFeedBack", "createGround", "shadowCatcher", "hideLights", "physicalSun", "activateFinalGather", "activateLinearWorkflow", "framebufferGamma", "photographicTonemapper", "showCamerasDialog"],
																"namespaced" : ["Additional Attributes|preserveSessionSettings", "Additional Attributes|createFeedBack", "Additional Attributes|createGround", "Additional Attributes|shadowCatcher", "Additional Attributes|hideLights", "Additional Attributes|physicalSun", "Additional Attributes|activateFinalGather", "Additional Attributes|activateLinearWorkflow", "Additional Attributes|framebufferGamma", "Additional Attributes|photographicTonemapper", "Additional Attributes|showCamerasDialog"]}),
													("Remote Connection", {"stripped" : ["ConnectionType", "ExecutionCommand", "DefaultAddress", "DefaultPort"],
																"namespaced" : ["Remote Connection|ConnectionType", "Remote Connection|ExecutionCommand", "Remote Connection|DefaultAddress", "Remote Connection|DefaultPort"]}),
													("Script", {"stripped" : ["_rawSectionContent"],
																"namespaced" : ["Script|_rawSectionContent"]})])}

DEFAULTS_FILE_SECTIONS_AND_ATTRIBUTES = {"_defaults" : {"_defaults|Default A" : "Attribute 'Default A' value", "_defaults|Default B" : "Attribute 'Default B' value"},
									"Options A" : {"Options A|John Doe" : "Unknown"},
									"Options B" : {"Options B|Jane Doe" : "Unknown"}}

STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED = {"Stripping A" : {"Stripping A|John Doe" : "\"Unknown\""},
													"Stripping B" : {"Stripping B|Jane Doe" : "\"Unknown\""}}

STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED = {"	Stripping A	" : {"	Stripping A	|	John Doe	" : "	\"Unknown\"	"},
													" Stripping B " : {" Stripping B | Jane Doe " : " \"Unknown\" "}}

PARSING_ERRORS_LINES_AND_VALUES = {3 : "Attribute structure is invalid: {}".format("This statement will produce the line nº '3' parsing error.\n"),
									6 : "Attribute structure is invalid: {}".format("This statement will produce the line nº '6' parsing error.\n"),
									12 : "Attribute structure is invalid: {}".format("This statement will produce the line nº '12' parsing error.\n")}

RANDOM_ATTRIBUTES = {"component" : {"Component|Name" : "core.db", "Component|Module" : "db", "Informations|Author" : "Thomas Mansencal", "Informations|Email" : "thomas.mansencal@gmail.com"},
					"iblSet" : {"Header|ICOfile" : "Icon.jpg", "Header|Name" : "Standard", "Header|Comment" : "Testing Foundations with units tests = fun!", "Background|BGfile" : "Standard_Background.jpg", "Background|BGmap" : "1", "Enviroment|EVfile" : "Standard_Lighting.jpg", "Enviroment|EVmap" : "1", "Reflection|REFfile" : "Standard_Reflection.jpg", "Reflection|REFmap" : "1", "Sun|SUNcolor" : "240,250,255", "Sun|SUNmulti" : "1.0", "Light1|LIGHTcolor" : "250,220,190", "Light1|LIGHTmulti" : "0.75"},
					"template" : {"Template|Name" : "@Name | Standard | String | Template Name", "Template|Path" : "@Path | | String | Template Path", "sIBL File Attributes|Background|BGfile" : "@BGfile", "sIBL File Attributes|Background|BGheight" : "@BGheight", "Common Attributes|createBackground" : "@createBackground | 1 | Boolean | Create Background", "Common Attributes|createLighting" : "@createLighting | 1 | Boolean | Create Lighting", "Additional Attributes|preserveSessionSettings" : "@preserveSessionSettings | 1 | Boolean | Preserve Session Settings", "Additional Attributes|createFeedBack" : "@createFeedBack | 1 | Boolean | Create Feedback", "Remote Connection|ConnectionType" : "@ConnectionType | Socket | String | Connection Type", "Remote Connection|ExecutionCommand" : "@ExecutionCommand | source \"$loaderScriptPath\"; | String | ExecutionCommand"}}

RANDOM_COMMENTS = {"component" : {"Component|#0" : {"content" : "Component comment for tests purpose.", "id" : 0}, "Informations|#1" : {"content" : "Informations comment for tests purpose.", "id" : 1}},
					"iblSet" : {"Header|#0" : {"content" : "Header comment for tests purpose.", "id" : 0}, "Header|#1" : {"content" : "Additional header comment for tests purpose.", "id" : 1}},
					"template" : {"Template|#0" : {"content" : "Template comment for tests purpose.", "id" : 0}, "sIBL File Attributes|#1" : {"content" : "sIBL File Attributes comment for tests purpose.", "id" : 1}}}

SCRIPT_RAW_SECTION = [ "// @OutputScript - @Release for @Software @Version\n",
						"// Author: @Author\n",
						"// EMail: @Email\n",
						"// Homepage: @Url\n",
						"// Template path: @Path\n",
						"// Template last modified: @Date\n",
						"// sIBL_GUI\n",
						"string $backgroundFilePath = \"@BGfile\";\n",
						"int $backgroundWidth = @BGheight*2;\n",
						"string $lightingFilePath = \"@EVfile\";\n" ]

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class ParserTestCase(unittest.TestCase):
	"""
	This class defines :class:`foundations.parser.Parser` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		parser = Parser(IBL_SET_FILE)
		requiredAttributes = ("file",
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
								"parsingErrors")

		for attribute in requiredAttributes:
			self.assertIn(attribute, dir(parser))

	def testRequiredMethods(self):
		"""
		This method tests presence of required methods.
		"""

		parser = Parser(IBL_SET_FILE)
		requiredMethods = ("parse",
							"sectionExists",
							"attributeExists",
							"getAttributes",
							"getValue")

		for method in requiredMethods:
			self.assertIn(method, dir(parser))

	def testParse(self):
		"""
		This method tests :meth:`foundations.parser.Parser.parse` method.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parseSuccess = parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertTrue(parseSuccess)

			self.assertIsInstance(parser.sections, OrderedDict)
			self.assertIsInstance(parser.comments, OrderedDict)
			parser.parse(orderedDictionary=False, rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertIsInstance(parser.sections, dict)
			self.assertIsInstance(parser.comments, dict)

	def testSections(self):
		"""
		This method tests :class:`foundations.parser.Parser` class sections consistencies.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertListEqual(parser.sections.keys(), STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys())
			parser.parse(orderedDictionary=False, rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
				self.assertIn(section, parser.sections.keys())

	def testRawSections(self):
		"""
		This method tests :class:`foundations.parser.Parser` class raw sections consistencies.
		"""

		parser = Parser(TEMPLATE_FILE)
		parser.read()
		parser.parse(rawSections=("Script",))
		self.assertListEqual(parser.sections["Script"]["Script|_rawSectionContent"][0:10], SCRIPT_RAW_SECTION)

	def testComments(self):
		"""
		This method tests :class:`foundations.parser.Parser` class comments consistencies.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertEqual(parser.comments, OrderedDict())
			parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type], stripComments=False)
			for comment, value in RANDOM_COMMENTS[type].items():
				self.assertIn(comment, parser.comments)
				self.assertEqual(value["id"], parser.comments[comment]["id"])

	def testDefaultsSection(self):
		"""
		This method tests :class:`foundations.parser.Parser` class default section consistency.
		"""

		parser = Parser(DEFAULTS_FILE)
		parser.read() and parser.parse()
		for section in DEFAULTS_FILE_SECTIONS_AND_ATTRIBUTES.keys():
			self.assertIn(section, parser.sections.keys())

	def testNamespaces(self):
		"""
		This method tests :class:`foundations.parser.Parser` class namespaces consistencies.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type], namespaces=False)
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
					for attribute in parser.sections[section]:
						self.assertIn(attribute, STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["stripped"])

	def testStripWhitespaces(self):
		"""
		This method tests :class:`foundations.parser.Parser` class whitespaces consistencies.
		"""

		parser = Parser(STRIPPING_FILE)
		parser.read() and parser.parse(stripWhitespaces=False)
		for section in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED.keys():
			self.assertIn(section, parser.sections.keys())
			for attribute, value in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_NON_STRIPPED[section].items():
				self.assertIn(attribute, parser.sections[section].keys())
				self.assertIn(value, parser.sections[section].values())

	def testStripQuotationMarkers(self):
		"""
		This method tests :class:`foundations.parser.Parser` class quotation markers consistencies.
		"""

		parser = Parser(STRIPPING_FILE)
		parser.read() and parser.parse(stripQuotationMarkers=False)
		for section in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED.keys():
			self.assertIn(section, parser.sections.keys())
			for attribute, value in STRIPPING_FILE_SECTIONS_AND_ATTRIBUTES_STRIPPED[section].items():
				self.assertIn(attribute, parser.sections[section].keys())
				self.assertIn(value, parser.sections[section].values())

	def testParsingErrors(self):
		"""
		This method tests :class:`foundations.parser.Parser` class parsing errors consistencies.
		"""

		parser = Parser(PARSING_ERRORS_FILE)
		parser.read() and parser.parse(raiseParsingErrors=False)
		for exception in parser.parsingErrors:
			self.assertIn(exception.line, PARSING_ERRORS_LINES_AND_VALUES.keys())
			self.assertEqual(exception.value, PARSING_ERRORS_LINES_AND_VALUES[exception.line])

	def testSectionExists(self):
		"""
		This method tests :meth:`foundations.parser.Parser.sectionExists` method.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			self.assertTrue(parser.sectionExists(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type].keys()[0]))
			self.assertFalse(parser.sectionExists("Unknown"))

	def testAttributeExists(self):
		"""
		This method tests :meth:`foundations.parser.Parser.attributeExists` method.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(False, rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for attribute in RANDOM_ATTRIBUTES[type].keys():
				self.assertTrue(parser.attributeExists(attribute, namespace.getNamespace(attribute, rootOnly=True)))
				self.assertFalse(parser.attributeExists("Unknown", namespace.getNamespace(attribute, rootOnly=True)))

	def testGetAttributes(self):
		"""
		This method tests :meth:`foundations.parser.Parser.getAttributes` method.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
					self.assertListEqual(parser.getAttributes(section, orderedDictionary=True, stripNamespaces=True).keys(), STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["stripped"])
					self.assertListEqual(parser.getAttributes(section).keys(), STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["namespaced"])

	def testGetAllAttributes(self):
		"""
		This method tests :meth:`foundations.parser.Parser.getAllAttributes` method.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			attributes = parser.getAllAttributes()
			testsAttributes = []
			for section in STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type]:
					testsAttributes.extend(STANDARD_FILES_SECTIONS_AND_ATTRIBUTES[type][section]["namespaced"])
			self.assertListEqual(attributes.keys(), testsAttributes)

	def testGetValue(self):
		"""
		This method tests :meth:`foundations.parser.Parser.getValue` method.
		"""

		for type, file in STANDARD_FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(False, rawSections=STANDARD_FILES_RAW_SECTIONS[type])
			for attribute, value in RANDOM_ATTRIBUTES[type].items():
				self.assertIsInstance(parser.getValue(attribute, namespace.getNamespace(attribute, rootOnly=True)), str)
				self.assertIsInstance(parser.getValue(attribute, namespace.getNamespace(attribute, rootOnly=True), encode=True), unicode)
				self.assertEqual(parser.getValue(attribute, namespace.getNamespace(attribute, rootOnly=True)), value)

class GetAttributeCompoundTestCase(unittest.TestCase):
	"""
	This class defines :func:`foundations.parser.getAttributeCompound` definition units tests methods.
	"""

	def testGetAttributeCompound(self):
		"""
		This method tests :func:`foundations.parser.getAttributeCompound` definition.
		"""

		self.assertIsInstance(foundations.parser.getAttributeCompound("Attribute", "Value"), foundations.parser.AttributeCompound)

		self.assertEqual(None, foundations.parser.getAttributeCompound("Attribute").value)

		compound = foundations.parser.AttributeCompound(name="Attribute", value="Value", link="@Link", type="Boolean", alias="Link Parameter")
		datas = "@Link | Value | Boolean | Link Parameter"
		self.assertEqual(compound.name, foundations.parser.getAttributeCompound("Attribute", datas).name)
		self.assertEqual(compound.value, foundations.parser.getAttributeCompound("Attribute", datas).value)
		self.assertEqual(compound.link, foundations.parser.getAttributeCompound("Attribute", datas).link)
		self.assertEqual(compound.type, foundations.parser.getAttributeCompound("Attribute", datas).type)
		self.assertEqual(compound.alias, foundations.parser.getAttributeCompound("Attribute", datas).alias)

		datas = "@Link"
		self.assertEqual(compound.link, foundations.parser.getAttributeCompound("Attribute", datas).link)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()
