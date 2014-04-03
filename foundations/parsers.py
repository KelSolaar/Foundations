#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**parsers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`SectionsFileParser` class, :class:`PlistFileParser` class
	and others parsing related objects.

**Others:**
	Portions of the code from Fredrik Lundh: http://effbot.org/zone/element-iterparse.htm
"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a storage object for attributes compounds usually encountered in
	`sIBL_GUI <https://github.com/KelSolaar/sIBL_GUI>`_ Templates files.

	Some attributes compounds:

		- Name = @Name | Standard | String | Template Name
		- Background|BGfile = @BGfile
		- showCamerasDialog = @showCamerasDialog | 0 | Boolean | Cameras Selection Dialog

	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		Usage::

			AttributeCompound(name="showCamerasDialog",
							value="0",
							link="@showCamerasDialog",
							type="Boolean",
							alias="Cameras Selection Dialog")

		:param \*\*kwargs: name, value, link, type, alias.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class SectionsFileParser(foundations.io.File):
	"""
	Defines methods to parse sections file format files,
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
				 rawSectionContentIdentifier="__raw__",
				 defaultsSection="_defaults",
				 preserveOrder=True):
		"""
		Initializes the class.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse(stripComments=False)
			<foundations.parsers.SectionsFileParser object at 0x293892011>
			>>> sectionsFileParser.sections.keys()
			[u'Section A', u'Section B']
			>>> sectionsFileParser.comments
			OrderedDict([(u'Section A|#0', {u'content': u'Comment.', u'id': 0})])

		:param file: Current file path.
		:type file: unicode
		:param splitters: Splitter characters.
		:type splitters: tuple or list
		:param namespaceSplitter: Namespace splitters character.
		:type namespaceSplitter: unicode
		:param commentLimiters: Comment limiters characters.
		:type commentLimiters: tuple or list
		:param commentMarker: Character use to prefix extracted comments idientifiers.
		:type commentMarker: unicode
		:param quotationMarkers: Quotation markers characters.
		:type quotationMarkers: tuple or list
		:param rawSectionContentIdentifier: Raw section content identifier.
		:type rawSectionContentIdentifier: unicode
		:param defaultsSection: Default section name.
		:type defaultsSection: unicode
		:param preserveOrder: Data order is preserved.
		:type preserveOrder: bool
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
		self.__preserveOrder = None
		self.preserveOrder = preserveOrder

		if not preserveOrder:
			self.__sections = {}
			self.__comments = {}
		else:
			self.__sections = OrderedDict()
			self.__comments = OrderedDict()
		self.__parsingErrors = []

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def splitters(self):
		"""
		Property for **self.__splitters** attribute.

		:return: self.__splitters.
		:rtype: tuple or list
		"""

		return self.__splitters

	@splitters.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def splitters(self, value):
		"""
		Setter for **self.__splitters** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
				"splitters", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"splitters", element)
				assert len(element) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("splitter", element)
				assert not re.search(r"\w", element), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
					"splitter", element)
		self.__splitters = value

	@splitters.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def splitters(self):
		"""
		Deleter for **self.__splitters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "splitters"))

	@property
	def namespaceSplitter(self):
		"""
		Property for **self.__namespaceSplitter** attribute.

		:return: self.__namespaceSplitter.
		:rtype: unicode
		"""

		return self.__namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def namespaceSplitter(self, value):
		"""
		Setter for **self.__namespaceSplitter** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"namespaceSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespaceSplitter",
																							  value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"namespaceSplitter", value)
		self.__namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def namespaceSplitter(self):
		"""
		Deleter for **self.__namespaceSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespaceSplitter"))

	@property
	def commentLimiters(self):
		"""
		Property for **self.__commentLimiters** attribute.

		:return: self.__commentLimiters.
		:rtype: tuple or list
		"""

		return self.__commentLimiters

	@commentLimiters.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def commentLimiters(self, value):
		"""
		Setter for **self.__commentLimiters** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
				"commentLimiters", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"commentLimiters", element)
		self.__commentLimiters = value

	@commentLimiters.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def commentLimiters(self):
		"""
		Deleter for **self.__commentLimiters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commentLimiters"))

	@property
	def commentMarker(self):
		"""
		Property for **self.__commentMarker** attribute.

		:return: self.__commentMarker.
		:rtype: unicode
		"""

		return self.__commentMarker

	@commentMarker.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def commentMarker(self, value):
		"""
		Setter for **self.__commentMarker** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"commentMarker", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"commentMarker", value)
		self.__commentMarker = value

	@commentMarker.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def commentMarker(self):
		"""
		Deleter for **self.__commentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commentMarker"))

	@property
	def quotationMarkers(self):
		"""
		Property for **self.__quotationMarkers** attribute.

		:return: self.__quotationMarkers.
		:rtype: tuple or list
		"""

		return self.__quotationMarkers

	@quotationMarkers.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def quotationMarkers(self, value):
		"""
		Setter for **self.__quotationMarkers** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
				"quotationMarkers", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
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
		Deleter for **self.__quotationMarkers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "quotationMarkers"))

	@property
	def rawSectionContentIdentifier(self):
		"""
		Property for **self. __rawSectionContentIdentifier** attribute.

		:return: self.__rawSectionContentIdentifier.
		:rtype: unicode
		"""

		return self.__rawSectionContentIdentifier

	@rawSectionContentIdentifier.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def rawSectionContentIdentifier(self, value):
		"""
		Setter for **self. __rawSectionContentIdentifier** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"rawSectionContentIdentifier", value)
		self.__rawSectionContentIdentifier = value

	@rawSectionContentIdentifier.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def rawSectionContentIdentifier(self):
		"""
		Deleter for **self. __rawSectionContentIdentifier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rawSectionContentIdentifier"))

	@property
	def defaultsSection(self):
		"""
		Property for **self.__defaultsSection** attribute.

		:return: self.__defaultsSection.
		:rtype: unicode
		"""

		return self.__defaultsSection

	@defaultsSection.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def defaultsSection(self, value):
		"""
		Setter for **self.__defaultsSection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"defaultsSection", value)
		self.__defaultsSection = value

	@defaultsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultsSection(self):
		"""
		Deleter for **self.__defaultsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultsSection"))

	@property
	def sections(self):
		"""
		Property for **self.__sections** attribute.

		:return: self.__sections.
		:rtype: OrderedDict or dict
		"""

		return self.__sections

	@sections.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def sections(self, value):
		"""
		Setter for **self.__sections** attribute.

		:param value: Attribute value.
		:type value: OrderedDict or dict
		"""

		if value is not None:
			assert type(value) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
			'OrderedDict' or 'dict'!".format("sections", value)
			for key, element in value.iteritems():
				assert type(key) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"sections", key)
				assert type(element) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
				'OrderedDict' or 'dict'!".format("sections", key)
		self.__sections = value

	@sections.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def sections(self):
		"""
		Deleter for **self.__sections** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "sections"))

	@property
	def comments(self):
		"""
		Property for **self.__comments** attribute.

		:return: self.__comments.
		:rtype: OrderedDict or dict
		"""

		return self.__comments

	@comments.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def comments(self, value):
		"""
		Setter for **self.__comments** attribute.

		:param value: Attribute value.
		:type value: OrderedDict or dict
		"""

		if value is not None:
			assert type(value) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
			'OrderedDict' or 'dict'!".format("comments", value)
			for key, element in value.iteritems():
				assert type(key) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"comments", key)
				assert type(element) in (OrderedDict, dict), "'{0}' attribute: '{1}' type is not \
				'OrderedDict' or 'dict'!".format("comments", key)
		self.__comments = value

	@comments.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def comments(self):
		"""
		Deleter for **self.__comments** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "comments"))

	@property
	def parsingErrors(self):
		"""
		Property for **self.__parsingErrors** attribute.

		:return: self.__parsingErrors.
		:rtype: list
		"""

		return self.__parsingErrors

	@parsingErrors.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def parsingErrors(self, value):
		"""
		Setter for **self.__parsingErrors** attribute.

		:param value: Attribute value.
		:type value: list
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
		Deleter for **self.__parsingErrors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parsingErrors"))

	@property
	def preserveOrder(self):
		"""
		Property for **self.__preserveOrder** attribute.

		:return: self.__preserveOrder.
		:rtype: bool
		"""

		return self.__preserveOrder

	@preserveOrder.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def preserveOrder(self, value):
		"""
		Setter method for **self.__preserveOrder** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("preserveOrder", value)
		self.__preserveOrder = value

	@preserveOrder.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preserveOrder(self):
		"""
		Deleter method for **self.__preserveOrder** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preserveOrder"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __getitem__(self, section):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param section: Section name.
		:type section: unicode
		:return: Layout.
		:rtype: Layout
		"""

		return self.__sections.__getitem__(section)

	def __setitem__(self, section, value):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param section: Section name.
		:type section: unicode
		:param section: Value.
		:type section: dict
		:return: Layout.
		:rtype: Layout
		"""

		return self.__sections.__setitem__(section, value)

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Layouts iterator.
		:rtype: object
		"""

		return self.__sections.iteritems()

	def __contains__(self, section):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param section: Section name.
		:type section: unicode
		:return: Section existence.
		:rtype: bool
		"""

		return self.sectionExists(section)

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Sections count.
		:rtype: int
		"""

		return len(self.__sections)

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileStructureParsingError)
	def parse(self,
			  rawSections=None,
			  namespaces=True,
			  stripComments=True,
			  stripWhitespaces=True,
			  stripQuotationMarkers=True,
			  raiseParsingErrors=True):
		"""
		Process the file content and extracts the sections / attributes
			as nested :class:`collections.OrderedDict` dictionaries or dictionaries.

		Usage::

			>>> content = ["; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse(stripComments=False)
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sectionsFileParser.sections.keys()
			[u'_defaults']
			>>> sectionsFileParser.sections["_defaults"].values()
			[u'Value A', u'Value B']
			>>> sectionsFileParser.parse(stripComments=False, stripQuotationMarkers=False)
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sectionsFileParser.sections["_defaults"].values()
			[u'"Value A"', u'"Value B"']
			>>> sectionsFileParser.comments
			OrderedDict([(u'_defaults|#0', {u'content': u'Comment.', u'id': 0})])
			>>> sectionsFileParser.parse()
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sectionsFileParser.sections["_defaults"]
			OrderedDict([(u'_defaults|Attribute 1', u'Value A'), (u'_defaults|Attribute 2', u'Value B')])
			>>> sectionsFileParser.parse(namespaces=False)
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sectionsFileParser.sections["_defaults"]
			OrderedDict([(u'Attribute 1', u'Value A'), (u'Attribute 2', u'Value B')])

		:param rawSections: Ignored raw sections.
		:type rawSections: tuple or list
		:param namespaces: Attributes and comments are namespaced.
		:type namespaces: bool
		:param stripComments: Comments are stripped.
		:type stripComments: bool
		:param stripWhitespaces: Whitespaces are stripped.
		:type stripWhitespaces: bool
		:param stripQuotationMarkers: Attributes values quotation markers are stripped.
		:type stripQuotationMarkers: bool
		:param raiseParsingErrors: Raise parsing errors.
		:type raiseParsingErrors: bool
		:return: SectionFileParser instance.
		:rtype: SectionFileParser
		"""

		LOGGER.debug("> Reading sections from: '{0}'.".format(self.path))

		if not self.content:
			self.read()

		attributes = {} if not self.__preserveOrder else OrderedDict()
		section = self.__defaultsSection
		rawSections = rawSections or []

		commentId = 0
		for i, line in enumerate(self.content):
			# Comments matching.
			search = re.search(r"^\s*[{0}](?P<comment>.+)$".format("".join(self.__commentLimiters)), line)
			if search:
				if not stripComments:
					comment = namespaces and foundations.namespace.setNamespace(section, "{0}{1}".format(
						self.__commentMarker, commentId), self.__namespaceSplitter) or \
							  "{0}{1}".format(self.__commentMarker, commentId)
					self.__comments[comment] = {"id": commentId, "content": stripWhitespaces and \
																			search.group(
																				"comment").strip() or search.group(
						"comment")}
					commentId += 1
				continue

			# Sections matching.
			search = re.search(r"^\s*\[(?P<section>.+)\]\s*$", line)
			if search:
				section = stripWhitespaces and search.group("section").strip() or search.group("section")
				if not self.__preserveOrder:
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
				search = re.search(r"^(?P<attribute>.+?)[{0}](?P<value>.+)$".format("".join(self.__splitters)), line) \
					or re.search(r"^(?P<attribute>.+?)[{0}]\s*$".format("".join(self.__splitters)), line)
				if search:
					attribute = search.group("attribute").strip() if stripWhitespaces else search.group("attribute")
					attribute = foundations.namespace.setNamespace(section, attribute, self.__namespaceSplitter) \
						if namespaces else attribute

					if len(search.groups()) == 2:
						value = search.group("value").strip() if stripWhitespaces else search.group("value")
						attributes[attribute] = value.strip("".join(self.__quotationMarkers)) \
							if stripQuotationMarkers else value
					else:
						attributes[attribute] = None
				else:
					self.__parsingErrors.append(foundations.exceptions.AttributeStructureParsingError(
						"Attribute structure is invalid: {0}".format(line), i + 1))

			self.__sections[section] = attributes

		LOGGER.debug("> Sections: '{0}'.".format(self.__sections))
		LOGGER.debug("> '{0}' file parsing done!".format(self.path))

		if self.__parsingErrors and raiseParsingErrors:
			raise foundations.exceptions.FileStructureParsingError(
				"{0} | '{1}' structure is invalid, parsing exceptions occured!".format(self.__class__.__name__,
																					   self.path))

		return self

	def sectionExists(self, section):
		"""
		Checks if given section exists.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			<foundations.parsers.SectionsFileParser object at 0x845683844>
			>>> sectionsFileParser.sectionExists("Section A")
			True
			>>> sectionsFileParser.sectionExists("Section C")
			False

		:param section: Section to check existence.
		:type section: unicode
		:return: Section existence.
		:rtype: bool
		"""

		if section in self.__sections:
			LOGGER.debug("> '{0}' section exists in '{1}'.".format(section, self))
			return True
		else:
			LOGGER.debug("> '{0}' section doesn't exists in '{1}'.".format(section, self))
			return False

	def attributeExists(self, attribute, section):
		"""
		Checks if given attribute exists.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			<foundations.parsers.SectionsFileParser object at 0x234564563>
			>>> sectionsFileParser.attributeExists("Attribute 1", "Section A")
			True
			>>> sectionsFileParser.attributeExists("Attribute 2", "Section A")
			False

		:param attribute: Attribute to check existence.
		:type attribute: unicode
		:param section: Section to search attribute into.
		:type section: unicode
		:return: Attribute existence.
		:rtype: bool
		"""

		if foundations.namespace.removeNamespace(attribute, rootOnly=True) in self.getAttributes(section,
																								 stripNamespaces=True):
			LOGGER.debug("> '{0}' attribute exists in '{1}' section.".format(attribute, section))
			return True
		else:
			LOGGER.debug("> '{0}' attribute doesn't exists in '{1}' section.".format(attribute, section))
			return False

	def getAttributes(self, section, stripNamespaces=False):
		"""
		Returns given section attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			<foundations.parsers.SectionsFileParser object at 0x125698322>
			>>> sectionsFileParser.getAttributes("Section A")
			OrderedDict([(u'Section A|Attribute 1', u'Value A')])
			>>> sectionsFileParser.preserveOrder=False
			>>> sectionsFileParser.getAttributes("Section A")
			{u'Section A|Attribute 1': u'Value A'}
			>>> sectionsFileParser.preserveOrder=True
			>>> sectionsFileParser.getAttributes("Section A", stripNamespaces=True)
			OrderedDict([(u'Attribute 1', u'Value A')])

		:param section: Section containing the requested attributes.
		:type section: unicode
		:param stripNamespaces: Strip namespaces while retrieving attributes.
		:type stripNamespaces: bool
		:return: Attributes.
		:rtype: OrderedDict or dict
		"""

		LOGGER.debug("> Getting section '{0}' attributes.".format(section))

		attributes = OrderedDict() if self.__preserveOrder else dict()
		if not self.sectionExists(section):
			return attributes

		if stripNamespaces:
			for attribute, value in self.__sections[section].iteritems():
				attributes[foundations.namespace.removeNamespace(attribute, rootOnly=True)] = value
		else:
			attributes.update(self.__sections[section])
		LOGGER.debug("> Attributes: '{0}'.".format(attributes))
		return attributes

	def getAllAttributes(self):
		"""
		Returns all sections attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			<foundations.parsers.SectionsFileParser object at 0x845683844>
			>>> sectionsFileParser.getAllAttributes()
			OrderedDict([(u'Section A|Attribute 1', u'Value A'), (u'Section B|Attribute 2', u'Value B')])
			>>> sectionsFileParser.preserveOrder=False
			>>> sectionsFileParser.getAllAttributes()
			{u'Section B|Attribute 2': u'Value B', u'Section A|Attribute 1': u'Value A'}

		:return: All sections / files attributes.
		:rtype: OrderedDict or dict
		"""

		allAttributes = OrderedDict() if self.__preserveOrder else dict()

		for attributes in self.__sections.itervalues():
			for attribute, value in attributes.iteritems():
				allAttributes[attribute] = value
		return allAttributes

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileStructureParsingError)
	def getValue(self, attribute, section, default=""):
		"""
		Returns requested attribute value.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			<foundations.parsers.SectionsFileParser object at 0x679302423>
			>>> sectionsFileParser.getValue("Attribute 1", "Section A")
			u'Value A'

		:param attribute: Attribute name.
		:type attribute: unicode
		:param section: Section containing the searched attribute.
		:type section: unicode
		:param default: Default return value.
		:type default: object
		:return: Attribute value.
		:rtype: unicode
		"""

		if not self.attributeExists(attribute, section):
			return default

		if attribute in self.__sections[section]:
			value = self.__sections[section][attribute]
		elif foundations.namespace.setNamespace(section, attribute) in self.__sections[section]:
			value = self.__sections[section][foundations.namespace.setNamespace(section, attribute)]
		LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))
		return value

	def setValue(self, attribute, section, value):
		"""
		Sets requested attribute value.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sectionsFileParser = SectionsFileParser()
			>>> sectionsFileParser.content = content
			>>> sectionsFileParser.parse()
			<foundations.parsers.SectionsFileParser object at 0x109304209>
			>>> sectionsFileParser.setValue("Attribute 3", "Section C", "Value C")
			True

		:param attribute: Attribute name.
		:type attribute: unicode
		:param section: Section containing the searched attribute.
		:type section: unicode
		:param value: Attribute value.
		:type value: object
		:return: Definition success.
		:rtype: bool
		"""

		if not self.sectionExists(section):
			LOGGER.debug("> Adding '{0}' section.".format(section))
			self.__sections[section] = OrderedDict() if self.__preserveOrder else dict()

		self.__sections[section][attribute] = value

		return True

	def write(self,
			  namespaces=False,
			  splitter="=",
			  commentLimiter=(";"),
			  spacesAroundSplitter=True,
			  spaceAfterCommentLimiter=True):
		"""
		Writes defined file using :obj:`SectionsFileParser.sections` and
			:obj:`SectionsFileParser.comments` class properties content.

		Usage::

			>>> sections = {"Section A": {"Section A|Attribute 1": "Value A"}, \
"Section B": {"Section B|Attribute 2": "Value B"}}
			>>> sectionsFileParser = SectionsFileParser("SectionsFile.rc")
			>>> sectionsFileParser.sections = sections
			>>> sectionsFileParser.write()
			True
			>>> sectionsFileParser.read()
			u'[Section A]\\nAttribute 1 = Value A\\n\\n[Section B]\\nAttribute 2 = Value B\\n'

		:param namespaces: Attributes are namespaced.
		:type namespaces: bool
		:param splitter: Splitter character.
		:type splitter: unicode
		:param commentLimiter: Comment limiter character.
		:type commentLimiter: unicode
		:param spacesAroundSplitter: Spaces around attributes and value splitters.
		:type spacesAroundSplitter: bool
		:param spaceAfterCommentLimiter: Space after comments limiter.
		:type spaceAfterCommentLimiter: bool
		:return: Method success.
		:rtype: bool
		"""

		self.uncache()

		LOGGER.debug("> Setting '{0}' file content.".format(self.path))
		attributeTemplate = "{{0}} {0} {{1}}\n".format(splitter) if spacesAroundSplitter else \
							"{{0}}{0}{{1}}\n".format(splitter)
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
	Defines methods to parse plist files.
	"""

	def __init__(self, file=None):
		"""
		Initializes the class.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.elements.keys()
			[u'Dictionary A', u'Number A', u'Array A', u'String A', u'Date A', u'Boolean A', u'Data A']
			>>> plistFileParser.elements["Dictionary A"]
			{u'String C': u'My Value C', u'String B': u'My Value B'}

		:param file: Current file path.
		:type file: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.io.File.__init__(self, file)

		# --- Setting class attributes. ---
		self.__elements = None
		self.__parsingErrors = None

		self.__unserializers = {"array": lambda x: [value.text for value in x],
								"dict": lambda x: dict((x[i].text, x[i + 1].text) for i in range(0, len(x), 2)),
								"key": lambda x: foundations.strings.toString(x.text) or "",
								"string": lambda x: foundations.strings.toString(x.text) or "",
								"data": lambda x: base64.decodestring(x.text or ""),
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
		Property for **self.__elements** attribute.

		:return: self.__elements.
		:rtype: OrderedDict or dict
		"""

		return self.__elements

	@elements.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def elements(self, value):
		"""
		Setter for **self.__elements** attribute.

		:param value: Attribute value.
		:type value: OrderedDict or dict
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not  dict'!".format("elements", value)
		self.__elements = value

	@elements.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def elements(self):
		"""
		Deleter for **self.__elements** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "elements"))

	@property
	def parsingErrors(self):
		"""
		Property for **self.__parsingErrors** attribute.

		:return: self.__parsingErrors.
		:rtype: list
		"""

		return self.__parsingErrors

	@parsingErrors.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def parsingErrors(self, value):
		"""
		Setter for **self.__parsingErrors** attribute.

		:param value: Attribute value.
		:type value: list
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
		Deleter for **self.__parsingErrors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parsingErrors"))

	@property
	def unserializers(self):
		"""
		Property for **self.__unserializers** attribute.

		:return: self.__unserializers.
		:rtype: dict
		"""

		return self.__unserializers

	@unserializers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unserializers(self, value):
		"""
		Setter for **self.__unserializers** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "unserializers"))

	@unserializers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unserializers(self):
		"""
		Deleter for **self.__unserializers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unserializers"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.exceptions.handleExceptions(foundations.exceptions.FileStructureParsingError)
	def parse(self, raiseParsingErrors=True):
		"""
		Process the file content.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.elements.keys()
			[u'Dictionary A', u'Number A', u'Array A', u'String A', u'Date A', u'Boolean A', u'Data A']

		:param raiseParsingErrors: Raise parsing errors.
		:type raiseParsingErrors: bool
		:return: Method success.
		:rtype: bool
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
					"{0} | '{1}' structure is invalid, parsing exceptions occured!".format(self.__class__.__name__,
																						   self.path))
		else:
			self.__elements = foundations.common.getFirstItem(elementTreeParser.root).text
			return True

	def elementExists(self, element):
		"""
		Checks if given element exists.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.elementExists("String A")
			True
			>>> plistFileParser.elementExists("String Nemo")
			False

		:param element: Element to check existence.
		:type element: unicode
		:return: Element existence.
		:rtype: bool
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
		| Filters the :meth:`PlistFileParser.elements` class property elements using given pattern.
		| Will return a list of matching elements values, if you want to get only one element value, use
			the :meth:`PlistFileParser.getValue` method instead.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.filterValues(r"String A")
			[u'My Value A']
			>>> plistFileParser.filterValues(r"String.*")
			[u'My Value C', u'My Value B', u'My Value A']

		:param pattern: Regex filtering pattern.
		:type pattern: unicode
		:param flags: Regex flags.
		:type flags: int
		:return: Values.
		:rtype: list
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
		| Returns the given element value.
		| If multiple elements with the same name exists, only the first encountered will be returned.

		Usage::

			>>> plistFileParser = PlistFileParser("standard.plist")
			>>> plistFileParser.parse()
			True
			>>> plistFileParser.getValue("String A")
			u'My Value A'

		:param element: Element to get the value.
		:type element: unicode
		:return: Element value.
		:rtype: object
		"""

		if not self.__elements:
			return

		values = self.filterValues(r"^{0}$".format(element))
		return foundations.common.getFirstItem(values)

def getAttributeCompound(attribute, value=None, splitter="|", bindingIdentifier="@"):
	"""
	Returns an attribute compound.

	Usage::

		>>> data = "@Link | Value | Boolean | Link Parameter"
		>>> attributeCompound = foundations.parsers.getAttributeCompound("Attribute Compound", data)
		>>> attributeCompound.name
		u'Attribute Compound'
		>>> attributeCompound.value
		u'Value'
		>>> attributeCompound.link
		u'@Link'
		>>> attributeCompound.type
		u'Boolean'
		>>> attributeCompound.alias
		u'Link Parameter'

	:param attribute: Attribute.
	:type attribute: unicode
	:param value: Attribute value.
	:type value: object
	:param splitter: Splitter.
	:type splitter: unicode
	:param bindingIdentifier: Binding identifier.
	:type bindingIdentifier: unicode
	:return: Attribute compound.
	:rtype: AttributeCompound
	"""

	LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))

	if type(value) is unicode:
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
