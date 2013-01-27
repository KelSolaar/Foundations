#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**parsers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`SectionsFileParser` class, :class:`PlistFileParser` class
	and others parsing related objects.

**Others:**
	Portions of the code from Fredrik Lundh: http://effbot.org/zone/element-iterparse.htm
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import base64
import datetime
import re
import sys
from xml.etree import ElementTree
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.dataStructures
import foundations.exceptions
import foundations.io
import foundations.namespace
import foundations.strings
import foundations.verbose
import foundations.walkers

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "AttributeCompound", "SectionsFileParser", "PlistFileParser", "getAttributeCompound"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class AttributeCompound(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for attributes compounds usually encountered in
	`sIBL_GUI <https://github.com/KelSolaar/sIBL_GUI>`_ Templates files.

	Some attributes compounds:

		- Name = @Name | Standard | String | Template Name
		- Background|BGfile = @BGfile
		- showCamerasDialog = @showCamerasDialog | 0 | Boolean | Cameras Selection Dialog

	"""

	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		Usage::

			AttributeCompound(name="showCamerasDialog", 
							value="0", 
							link="@showCamerasDialog", 
							type="Boolean", 
							alias="Cameras Selection Dialog")

		:param \*\*kwargs: name, value, link, type, alias. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class SectionsFileParser(foundations.io.File):
	"""
	This class provides methods to parse sections file format files,
	an alternative configuration file parser is available directly with Python: :class:`ConfigParser.ConfigParser`.

	The parser given by this class has some major differences with Python :class:`ConfigParser.ConfigParser`:

		- | Sections and attributes are stored in their appearance order by default.
			( Using Python :class:`collections.OrderedDict` )
		- | A default section ( **_default** ) will store orphans attributes 
			( Attributes appearing before any declared section ).
		- File comments are stored inside the :obj:`SectionsFileParser.comments` class property. 
		- | Sections, attributes and values are whitespaces stripped by default
			but can also be stored with their leading and trailing whitespaces. 
		- | Values are quotations markers stripped by default
			but can also be stored with their leading and trailing quotations markers. 
		- Attributes are namespaced by default allowing sections merge without keys collisions. 

	"""

	def __init__(self,
				file=None,
				splitters=("=", ":"),
				namespaceSplitter="|",
				commentLimiters=(";", "#"),
				commentMarker="#",
				quotationMarkers=("\"", "'", "`"),
				rawSectionContentIdentifier="_rawSectionContent",
				defaultsSection="_defaults"):
		"""
		This method initializes the class.
		
		Usage::
		
			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse(stripComments=False)
			True
			>>> sectionsFileParser.sections.keys()
			['Section A', 'Section B']
			>>> sectionsFileParser.comments 
			OrderedDict([('Section A|#0', {'content': 'Comment.', 'id': 0})])

		:param file: Current file path. ( String )
		:param splitters: Splitter characters.  ( Tuple / List )
		:param namespaceSplitter: Namespace splitters character. ( String )
		:param commentLimiters: Comment limiters characters. ( Tuple / List )
		:param commentMarker: Character use to prefix extracted comments idientifiers. ( String )
		:param quotationMarkers: Quotation markers characters. ( Tuple / List )
		:param rawSectionContentIdentifier: Raw section content identifier. ( String )
		:param defaultsSection: Default section name. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.io.File.__init__(self, file)

		# --- Setting class attributes. ---
		self.__splitters = None
		self.splitters = splitters
		self.__namespaceSplitter = None
		self.namespaceSplitter = namespaceSplitter
		self.__commentLimiters = None
		self.commentLimiters = commentLimiters
		self.__commentMarker = None
		self.commentMarker = commentMarker
		self.__quotationMarkers = None
		self.quotationMarkers = quotationMarkers
		self.__rawSectionContentIdentifier = None
		self.rawSectionContentIdentifier = rawSectionContentIdentifier
		self.__defaultsSection = None
		self.defaultsSection = defaultsSection

		self.__sections = None
		self.__comments = None
		self.__parsingErrors = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def splitters(self):
		"""
		This method is the property for **self.__splitters** attribute.

		:return: self.__splitters. ( Tuple / List )
		"""

		return self.__splitters

	@splitters.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def splitters(self, value):
		"""
		This method is the setter method for **self.__splitters** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"splitters", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"splitters", element)
				assert len(element) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("splitter", element)
				assert not re.search(r"\w", element), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"splitter", element)
		self.__splitters = value

	@splitters.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def splitters(self):
		"""
		This method is the deleter method for **self.__splitters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "splitters"))

	@property
	def namespaceSplitter(self):
		"""
		This method is the property for **self.__namespaceSplitter** attribute.

		:return: self.__namespaceSplitter. ( String )
		"""

		return self.__namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def namespaceSplitter(self, value):
		"""
		This method is the setter method for **self.__namespaceSplitter** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"namespaceSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespaceSplitter", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"namespaceSplitter", value)
		self.__namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def namespaceSplitter(self):
		"""
		This method is the deleter method for **self.__namespaceSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespaceSplitter"))

	@property
	def commentLimiters(self):
		"""
		This method is the property for **self.__commentLimiters** attribute.

		:return: self.__commentLimiters. ( Tuple / List )
		"""

		return self.__commentLimiters

	@commentLimiters.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def commentLimiters(self, value):
		"""
		This method is the setter method for **self.__commentLimiters** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"commentLimiters", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"commentLimiters", element)
		self.__commentLimiters = value

	@commentLimiters.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def commentLimiters(self):
		"""
		This method is the deleter method for **self.__commentLimiters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commentLimiters"))

	@property
	def commentMarker(self):
		"""
		This method is the property for **self.__commentMarker** attribute.

		:return: self.__commentMarker. ( String )
		"""

		return self.__commentMarker

	@commentMarker.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def commentMarker(self, value):
		"""
		This method is the setter method for **self.__commentMarker** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"commentMarker", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"commentMarker", value)
		self.__commentMarker = value

	@commentMarker.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def commentMarker(self):
		"""
		This method is the deleter method for **self.__commentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commentMarker"))

	@property
	def quotationMarkers(self):
		"""
		This method is the property for **self.__quotationMarkers** attribute.

		:return: self.__quotationMarkers. ( Tuple / List )
		"""

		return self.__quotationMarkers

	@quotationMarkers.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def quotationMarkers(self, value):
		"""
		This method is the setter method for **self.__quotationMarkers** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"quotationMarkers", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"quotationMarkers", element)
				assert len(element) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("quotationMarkers",
				 																					element)
				assert not re.search(r"\w", element), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"quotationMarkers", element)
		self.__quotationMarkers = value

	@quotationMarkers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def quotationMarkers(self):
		"""
		This method is the deleter method for **self.__quotationMarkers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "quotationMarkers"))

	@property
	def rawSectionContentIdentifier(self):
		"""
		This method is the property for **self.__rawSectionContentIdentifier** attribute.

		:return: self.__rawSectionContentIdentifier. ( String )
		"""

		return self.__rawSectionContentIdentifier

	@rawSectionContentIdentifier.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def rawSectionContentIdentifier(self, value):
		"""
		This method is the setter method for **self.__rawSectionContentIdentifier** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"rawSectionContentIdentifier", value)
		self.__rawSectionContentIdentifier = value

	@rawSectionContentIdentifier.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def rawSectionContentIdentifier(self):
		"""
		This method is the deleter method for **self.__rawSectionContentIdentifier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rawSectionContentIdentifier"))

	@property
	def defaultsSection(self):
		"""
		This method is the property for **self.__defaultsSection** attribute.

		:return: self.__defaultsSection. ( String )
		"""

		return self.__defaultsSection

	@defaultsSection.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def defaultsSection(self, value):
		"""
		This method is the setter method for **self.__defaultsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"defaultsSection", value)
		self.__defaultsSection = value

	@defaultsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultsSection(self):
		"""
		This method is the deleter method for **self.__defaultsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultsSection"))

	@property
	def sections(self):
		"""
		This method is the property for **self.__sections** attribute.

		:return: self.__sections. ( OrderedDict / Dictionary )
		"""

		return self.__sections

	@sections.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def sections(self, value):
		"""
		This method is the setter method for **self.__sections** attribute.

		:param value: Attribute value. ( OrderedDict / Dictionary )
		"""

		if value is not None:
			assert type(value) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
			'OrderedDict' or 'dict'!".format("sections", value)
			for key, element in value.iteritems():
				assert type(key) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"sections", key)
				assert type(element) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
				'OrderedDict' or 'dict'!".format("sections", key)
		self.__sections = value

	@sections.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def sections(self):
		"""
		This method is the deleter method for **self.__sections** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "sections"))

	@property
	def comments(self):
		"""
		This method is the property for **self.__comments** attribute.

		:return: self.__comments. ( OrderedDict / Dictionary )
		"""

		return self.__comments

	@comments.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def comments(self, value):
		"""
		This method is the setter method for **self.__comments** attribute.

		:param value: Attribute value. ( OrderedDict / Dictionary )
		"""

		if value is not None:
			assert type(value) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
			'OrderedDict' or 'dict'!".format("comments", value)
			for key, element in value.iteritems():
				assert type(key) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"comments", key)
				assert type(element) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
				'OrderedDict' or 'dict'!".format("comments", key)
		self.__comments = value

	@comments.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def comments(self):
		"""
		This method is the deleter method for **self.__comments** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "comments"))

	@property
	def parsingErrors(self):
		"""
		This method is the property for **self.__parsingErrors** attribute.

		:return: self.__parsingErrors. ( List )
		"""

		return self.__parsingErrors

	@parsingErrors.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def parsingErrors(self, value):
		"""
		This method is the setter method for **self.__parsingErrors** attribute.

		:param value: Attribute value. ( List )
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("parsingErrors", value)
			for element in value:
				assert issubclass(element.__class__, foundations.exceptions.AbstractParsingError), \
				"'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
				"parsingErrors", element, foundations.exceptions.AbstractParsingError.__class__.__name__)
		self.__parsingErrors = value

	@parsingErrors.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def parsingErrors(self):
		"""
		This method is the deleter method for **self.__parsingErrors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parsingErrors"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.handleExceptions(foundations.exceptions.FileStructureParsingError)
	def parse(self,
			orderedDictionary=True,
			rawSections=None,
			namespaces=True,
			stripComments=True,
			stripWhitespaces=True,
			stripQuotationMarkers=True,
			raiseParsingErrors=True):
		"""
		This method process the file content and extract the sections / attributes
			as nested :class:`collections.OrderedDict` dictionaries or dictionaries.

		Usage::

			>>> content = ["; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse(stripComments=False)
			True
			>>> sectionsFileParser.sections.keys()
			['_defaults']
			>>> sectionsFileParser.sections["_defaults"].values()
			['Value A', 'Value B']
			>>> sectionsFileParser.parse(stripQuotationMarkers=False)
			True
			>>> sectionsFileParser.sections["_defaults"].values()
			['"Value A"', '"Value B"']
			>>> sectionsFileParser.comments 
			OrderedDict([('_defaults|#0', {'content': 'Comment.', 'id': 0})])
			>>> sectionsFileParser.parse()
			True
			>>> sectionsFileParser.sections["_defaults"]
			OrderedDict([('_defaults|Attribute 1', 'Value A'), ('_defaults|Attribute 2', 'Value B')])
			>>> sectionsFileParser.parse(namespaces=False)
			OrderedDict([('Attribute 1', 'Value A'), ('Attribute 2', 'Value B')])

		:param orderedDictionary: SectionsFileParser data is stored
			in :class:`collections.OrderedDict` dictionaries. ( Boolean )
		:param rawSections: Ignored raw sections. ( Tuple / List )
		:param namespaces: Attributes and comments are namespaced. ( Boolean )
		:param stripComments: Comments are stripped. ( Boolean )
		:param stripWhitespaces: Whitespaces are stripped. ( Boolean )
		:param stripQuotationMarkers: Attributes values quotation markers are stripped. ( Boolean )
		:param raiseParsingErrors: Raise parsing errors. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Reading sections from: '{0}'.".format(self.path))

		if not self.content:
			return False

		if not orderedDictionary:
			self.__sections = {}
			self.__comments = {}
			attributes = {}
		else:
			self.__sections = OrderedDict()
			self.__comments = OrderedDict()
			attributes = OrderedDict()
		section = self.__defaultsSection
		rawSections = rawSections or []
		self.__parsingErrors = []

		commentId = 0
		for i, line in enumerate(self.content):
			# Comments matching.
			search = re.search(r"^\s*[{0}](?P<comment>.+)$".format("".join(self.__commentLimiters)), line)
			if search:
				if not stripComments:
					comment = namespaces and foundations.namespace.setNamespace(section, "{0}{1}".format(
							self.__commentMarker, commentId), self.__namespaceSplitter) or \
							"{0}{1}".format(self.__commentMarker, commentId)
					self.__comments[comment] = {"id" : commentId, "content" : stripWhitespaces and \
												search.group("comment").strip() or search.group("comment")}
					commentId += 1
				continue

			# Sections matching.
			search = re.search(r"^\s*\[(?P<section>.+)\]\s*$", line)
			if search:
				section = stripWhitespaces and search.group("section").strip() or search.group("section")
				if not orderedDictionary:
					attributes = {}
				else:
					attributes = OrderedDict()
				rawContent = []
				continue

			if section in rawSections:
				rawContent.append(line)
				attributes[self.__rawSectionContentIdentifier] = rawContent
			else:
				# Empty line matching.
				search = re.search(r"^\s*$", line)
				if search:
					continue

				# Attributes matching.
				search = re.search(r"^(?P<attribute>.+?)[{0}](?P<value>.+)$".format("".join(self.__splitters)), line)
				if search:
					attribute = stripWhitespaces and search.group("attribute").strip() or search.group("attribute")
					attribute = namespaces and foundations.namespace.setNamespace(section,
																				attribute,
																				self.__namespaceSplitter) or attribute
					value = stripWhitespaces and search.group("value").strip() or search.group("value")
					attributes[attribute] = stripQuotationMarkers and value.strip("".join(self.__quotationMarkers)) or value
				else:
					self.__parsingErrors.append(foundations.exceptions.AttributeStructureParsingError(
					"Attribute structure is invalid: {0}".format(line), i + 1))

			self.__sections[section] = attributes

		LOGGER.debug("> Sections: '{0}'.".format(self.__sections))
		LOGGER.debug("> '{0}' file parsing done!".format(self.path))

		if self.__parsingErrors and raiseParsingErrors:
			raise foundations.exceptions.FileStructureParsingError(
			"{0} | '{1}' structure is invalid, parsing exceptions occured!".format(self.__class__.__name__, self.path))

		return True

	def sectionExists(self, section):
		"""
		This method checks if given section exists.
		
		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			True
			>>> sectionsFileParser.sectionExists("Section A")
			True
			>>> sectionsFileParser.sectionExists("Section C")
			False

		:param section: Section to check existence. ( String )
		:return: Section existence. ( Boolean )
		"""

		if not self.__sections:
			return False

		if section in self.__sections:
			LOGGER.debug("> '{0}' section exists in '{1}'.".format(section, self))
			return True
		else:
			LOGGER.debug("> '{0}' section doesn't exists in '{1}'.".format(section, self))
			return False

	def attributeExists(self, attribute, section):
		"""
		This method checks if given attribute exists.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			True
			>>> sectionsFileParser.attributeExists("Attribute 1", "Section A")
			True
			>>> sectionsFileParser.attributeExists("Attribute 2", "Section A")
			False

		:param attribute: Attribute to check existence. ( String )
		:param section: Section to search attribute into. ( String )
		:return: Attribute existence. ( Boolean )
		"""

		if not self.__sections:
			return False

		if foundations.namespace.removeNamespace(attribute, rootOnly=True) in self.getAttributes(section,
																					orderedDictionary=True,
																					stripNamespaces=True):
			LOGGER.debug("> '{0}' attribute exists in '{1}' section.".format(attribute, section))
			return True
		else:
			LOGGER.debug("> '{0}' attribute doesn't exists in '{1}' section.".format(attribute, section))
			return False

	def getAttributes(self, section, orderedDictionary=True, stripNamespaces=False):
		"""
		This method returns given section attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			True
			>>> sectionsFileParser.getAttributes("Section A")
			OrderedDict([('Section A|Attribute 1', 'Value A')])
			>>> sectionsFileParser.getAttributes("Section A", orderedDictionary=False)
			{'Section A|Attribute 1': 'Value A'}
			>>> sectionsFileParser.getAttributes("Section A", stripNamespaces=True)
			OrderedDict([('Attribute 1', 'Value A')])

		:param section: Section containing the requested attributes. ( String )
		:param orderedDictionary: Use an :class:`collections.OrderedDict` dictionary to store the attributes. ( String )
		:param stripNamespaces: Strip namespaces while retrieving attributes. ( Boolean )
		:return: Attributes. ( OrderedDict / Dictionary )
		"""

		LOGGER.debug("> Getting section '{0}' attributes.".format(section))
		dictionary = orderedDictionary and OrderedDict or dict
		attributes = dictionary()
		if not self.sectionExists(section):
			return attributes

		if stripNamespaces:
			for attribute, value in self.__sections[section].iteritems():
				attributes[foundations.namespace.removeNamespace(attribute, rootOnly=True)] = value
		else:
			attributes.update(self.__sections[section])
		LOGGER.debug("> Attributes: '{0}'.".format(attributes))
		return attributes

	def getAllAttributes(self, orderedDictionary=True):
		"""
		This method returns all sections attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			True
			>>> sectionsFileParser.getAllAttributes()
			OrderedDict([('Section A|Attribute 1', 'Value A'), ('Section B|Attribute 2', 'Value B')])
			>>> sectionsFileParser.getAllAttributes(orderedDictionary=False)
			{'Section B|Attribute 2': 'Value B', 'Section A|Attribute 1': 'Value A'}

		:param orderedDictionary: Use an :class:`collections.OrderedDict` dictionary to store the attributes. ( String )
		:return: All sections / files attributes. ( OrderedDict / Dictionary )
		"""

		dictionary = orderedDictionary and OrderedDict or dict
		allAttributes = dictionary()
		if not self.__sections:
			return allAttributes

		for attributes in self.__sections.itervalues():
			for attribute, value in attributes.iteritems():
				allAttributes[attribute] = value
		return allAttributes

	def getValue(self, attribute, section, encode=False, default=str()):
		"""
		This method returns requested attribute value.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			True
			>>> sectionsFileParser.getValue("Attribute 1", "Section A")
			Value A

		:param attribute: Attribute name. ( String )
		:param section: Section containing the searched attribute. ( String )
		:param encode: Encode value to unicode. ( Boolean )
		:param default: Default return value. ( Object )
		:return: Attribute value. ( String )
		"""

		if not self.__sections:
			return default

		if not self.attributeExists(attribute, section):
			return default

		if attribute in self.__sections[section]:
			value = self.__sections[section][attribute]
		elif foundations.namespace.setNamespace(section, attribute) in self.__sections[section]:
			value = self.__sections[section][foundations.namespace.setNamespace(section, attribute)]
		LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))
		value = foundations.strings.encode(value) if encode else value
		return value

	def write(self,
			namespaces=False,
			splitter="=",
			commentLimiter=(";"),
			spacesAroundSplitter=True,
			spaceAfterCommentLimiter=True):
		"""
		This method writes defined file using :obj:`SectionsFileParser.sections` and
			:obj:`SectionsFileParser.comments` class properties content.

		Usage::

			>>> sections = {"Section A": {"Section A|Attribute 1": "Value A"}, \
"Section B": {"Section B|Attribute 2": "Value B"}}
			>>> sectionsFileParser = SectionsFileParser("SectionsFile.rc")
			>>> sectionsFileParser.sections = sections
			>>> sectionsFileParser.write()
			True
			>>> sectionsFileParser.read()
			True
			>>> print sectionsFileParser.content[0:5]
			['[Section A]\\n', 'Attribute 1 = Value A\\n', '\\n', '[Section B]\\n', 'Attribute 2 = Value B\\n', '\\n']

		:param namespaces: Attributes are namespaced. ( Boolean )
		:param splitter: Splitter character. ( String )
		:param commentLimiter: Comment limiter character. ( String )
		:param spacesAroundSplitter: Spaces around attributes and value splitters. ( Boolean )
		:param spaceAfterCommentLimiter: Space after comments limiter. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.__sections:
			return False

		LOGGER.debug("> Setting '{0}' file content.".format(self.path))
		attributeTemplate = spacesAroundSplitter and "{{0}} {0} {{1}}\n".format(splitter) or \
							"{{0}} {0} {{1}}\n".format(splitter)
		attributeTemplate = foundations.strings.replace(attributeTemplate, {"{{" : "{", "}}" : "}"})
		commentTemplate = spaceAfterCommentLimiter and "{0} {{0}}\n".format(commentLimiter) or \
							"{0}{{0}}\n".format(commentLimiter)
		if self.__defaultsSection in self.__sections:
			LOGGER.debug("> Appending '{0}' default section.".format(self.__defaultsSection))
			if self.__comments:
				for comment, value in self.__comments.iteritems():
					if self.__defaultsSection in comment:
						value = value["content"] or ""
						LOGGER.debug("> Appending '{0}' comment with '{1}' value.".format(comment, value))
						self.content.append(commentTemplate.format(value))
			for attribute, value in self.__sections[self.__defaultsSection].iteritems():
				attribute = namespaces and attribute or foundations.namespace.removeNamespace(attribute,
																							self.__namespaceSplitter,
																							rootOnly=True)
				value = value or ""
				LOGGER.debug("> Appending '{0}' attribute with '{1}' value.".format(attribute, value))
				self.content.append(attributeTemplate.format(attribute, value))
			self.content.append("\n")

		for i, section in enumerate(self.__sections):
			LOGGER.debug("> Appending '{0}' section.".format(section))
			self.content.append("[{0}]\n".format(section))
			if self.__comments:
				for comment, value in self.__comments.iteritems():
					if section in comment:
						value = value["content"] or ""
						LOGGER.debug("> Appending '{0}' comment with '{1}' value.".format(comment, value))
						self.content.append(commentTemplate.format(value))
			for attribute, value in self.__sections[section].iteritems():
				if foundations.namespace.removeNamespace(attribute) == self.__rawSectionContentIdentifier:
					LOGGER.debug("> Appending '{0}' raw section content.".format(section))
					for line in value:
						self.content.append(line)
				else:
					LOGGER.debug("> Appending '{0}' section.".format(section))
					attribute = namespaces and attribute or foundations.namespace.removeNamespace(attribute,
																								self.__namespaceSplitter,
																								rootOnly=True)
					value = value or ""
					LOGGER.debug("> Appending '{0}' attribute with '{1}' value.".format(attribute, value))
					self.content.append(attributeTemplate.format(attribute, value))
			if i != len(self.__sections) - 1:
				self.content.append("\n")
		foundations.io.File.write(self)
		return True

class PlistFileParser(foundations.io.File):
	"""
	This class provides methods to parse plist files.
	"""

	def __init__(self, file=None):
		"""
		This method initializes the class.
		
		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.elements.keys()
			['Dictionary A', 'Number A', 'Array A', 'String A', 'Date A', 'Boolean A', 'Data A']
			>>> plistFileParser.elements["Dictionary A"]
			{'String C': 'My Value C', 'String B': 'My Value B'}

		:param file: Current file path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.io.File.__init__(self, file)

		# --- Setting class attributes. ---
		self.__elements = None
		self.__parsingErrors = None

		self.__unserializers = {"array": lambda x: [value.text for value in x],
								"dict": lambda x: dict((x[i].text, x[i + 1].text) for i in range(0, len(x), 2)),
								"key": lambda x: x.text or unicode(),
								"string": lambda x: x.text or unicode(),
								"data": lambda x: base64.decodestring(x.text or unicode()),
								"date": lambda x: datetime.datetime(*map(int, re.findall("\d+", x.text))),
								"true": lambda x: True,
								"false": lambda x: False,
								"real": lambda x: float(x.text),
								"integer": lambda x: int(x.text)}

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def elements(self):
		"""
		This method is the property for **self.__elements** attribute.

		:return: self.__elements. ( OrderedDict / Dictionary )
		"""

		return self.__elements

	@elements.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def elements(self, value):
		"""
		This method is the setter method for **self.__elements** attribute.

		:param value: Attribute value. ( OrderedDict / Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not  dict'!".format("elements", value)
		self.__elements = value

	@elements.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def elements(self):
		"""
		This method is the deleter method for **self.__elements** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "elements"))

	@property
	def parsingErrors(self):
		"""
		This method is the property for **self.__parsingErrors** attribute.

		:return: self.__parsingErrors. ( List )
		"""

		return self.__parsingErrors

	@parsingErrors.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def parsingErrors(self, value):
		"""
		This method is the setter method for **self.__parsingErrors** attribute.

		:param value: Attribute value. ( List )
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("parsingErrors", value)
			for element in value:
				assert issubclass(element.__class__, foundations.exceptions.AbstractParsingError), \
				"'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
				"parsingErrors", element, foundations.exceptions.AbstractParsingError.__class__.__name__)
		self.__parsingErrors = value

	@parsingErrors.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def parsingErrors(self):
		"""
		This method is the deleter method for **self.__parsingErrors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parsingErrors"))

	@property
	def unserializers(self):
		"""
		This method is the property for **self.__unserializers** attribute.

		:return: self.__unserializers. ( Dictionary )
		"""

		return self.__unserializers

	@unserializers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unserializers(self, value):
		"""
		This method is the setter method for **self.__unserializers** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "unserializers"))

	@unserializers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unserializers(self):
		"""
		This method is the deleter method for **self.__unserializers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unserializers"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.handleExceptions(foundations.exceptions.FileStructureParsingError)
	def parse(self, raiseParsingErrors=True):
		"""
		This method process the file content.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.elements.keys()
			['Dictionary A', 'Number A', 'Array A', 'String A', 'Date A', 'Boolean A', 'Data A']

		:param raiseParsingErrors: Raise parsing errors. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Reading elements from: '{0}'.".format(self.path))

		elementTreeParser = ElementTree.iterparse(self.path)

		self.__parsingErrors = []
		for action, element in elementTreeParser:
			unmarshal = self.__unserializers.get(element.tag)
			if unmarshal:
				data = unmarshal(element)
				element.clear()
				element.text = data
			elif element.tag != "plist":
				self.__parsingErrors.append(foundations.exceptions.FileStructureParsingError(
				"Unknown element: {0}".format(element.tag)))

		if self.__parsingErrors:
			if raiseParsingErrors:
				raise foundations.exceptions.FileStructureParsingError(
				"{0} | '{1}' structure is invalid, parsing exceptions occured!".format(self.__class__.__name__, self.path))
		else:
			self.__elements = foundations.common.getFirstItem(elementTreeParser.root).text
			return True

	def elementExists(self, element):
		"""
		This method checks if given element exists.

		Usage::
			
			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.elementExists("String A")
			True
			>>> plistFileParser.elementExists("String Nemo")
			False

		:param element: Element to check existence. ( String )
		:return: Element existence. ( Boolean )
		"""

		if not self.__elements:
			return False

		for item in foundations.walkers.dictionariesWalker(self.__elements):
			path, key, value = item
			if key == element:
				LOGGER.debug("> '{0}' attribute exists.".format(element))
				return True

		LOGGER.debug("> '{0}' element doesn't exists.".format(element))
		return False

	def filterValues(self, pattern, flags=0):
		"""
		| This method filters the :meth:`PlistFileParser.elements` class property elements using given pattern.
		| This method will return a list of matching elements values, if you want to get only one element value, use
			the :meth:`PlistFileParser.getValue` method instead.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.filterValues(r"String A")
			['My Value A']
			>>> plistFileParser.filterValues(r"String.*")
			['My Value C', 'My Value B', 'My Value A']

		:param pattern: Regex filtering pattern. ( String )
		:param flags: Regex flags. ( Integer )
		:return: Values. ( List )
		"""

		values = []
		if not self.__elements:
			return values

		for item in foundations.walkers.dictionariesWalker(self.__elements):
			path, element, value = item
			if re.search(pattern, element, flags):
				values.append(value)
		return values

	def getValue(self, element):
		"""
		| This method returns the given element value.
		| If multiple elements with the same name exists, only the first encountered will be returned.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.getValue("String A")
			'My Value A'

		:param element: Element to get the value. ( String )
		:return: Element value. ( Object )
		"""

		if not self.__elements:
			return

		values = self.filterValues(r"^{0}$".format(element))
		return foundations.common.getFirstItem(values)

def getAttributeCompound(attribute, value=None, splitter="|", bindingIdentifier="@"):
	"""
	This definition returns an attribute compound.
	
	Usage::
	
		>>> data = "@Link | Value | Boolean | Link Parameter"
		>>> attributeCompound = foundations.parsers.getAttributeCompound("Attribute Compound", data)
		>>> attributeCompound.name
		Attribute Compound
		>>> attributeCompound.value
		Value
		>>> attributeCompound.link
		@Link
		>>> attributeCompound.type
		Boolean
		>>> attributeCompound.alias
		Link Parameter
		
	:param attribute: Attribute. ( String )
	:param value: Attribute value. ( Object )
	:param splitter: Splitter. ( String )
	:param bindingIdentifier: Binding identifier. ( String )
	:return: Attribute compound. ( AttributeCompound )
	"""

	LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))

	if type(value) in (str, unicode):
		if splitter in value:
			valueTokens = value.split(splitter)
			if len(valueTokens) >= 3 and re.search(r"{0}\w*".format(bindingIdentifier), valueTokens[0]):
				return AttributeCompound(name=attribute,
										value=valueTokens[1].strip(),
										link=valueTokens[0].strip(),
										type=valueTokens[2].strip(),
										alias=len(valueTokens) == 4 and valueTokens[3].strip() or None)
		else:
			if re.search(r"{0}\w*".format(bindingIdentifier), value):
				return AttributeCompound(name=attribute, value=None, link=value, type=None, alias=None)

	return AttributeCompound(name=attribute, value=value, link=None, type=None, alias=None)
