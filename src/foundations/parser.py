#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**parser.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Parser Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import re
from collections import OrderedDict

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.namespace as namespace
from foundations.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class AttributeCompound(core.Structure):
	"""
	This class represents a storage object for attributes compounds usually encountered in `sIBL_GUI <https://github.com/KelSolaar/sIBL_GUI>`_ Templates files.

	Some attributes compounds:

		- Name = @Name | Standard | String | Template Name
		- Background|BGfile = @BGfile
		- showCamerasDialog = @showCamerasDialog | 0 | Boolean | Cameras Selection Dialog

	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		Usage::

			AttributeCompound(name="showCamerasDialog", value="0", link="@showCamerasDialog", type="Boolean", alias="Cameras Selection Dialog")

		:param kwargs: name, value, link, type, alias. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__dict__.update(kwargs)

class Parser(io.File):
	"""
	This class provides methods to parse sections file format files, an alternative configuration file parser is available directly with Python: :class:`ConfigParser.ConfigParser`.

	The parser provided by this class has some major differences with Python :class:`ConfigParser.ConfigParser`:

		- Sections and attributes are stored in their appearance order by default. ( Using Python :class:`collections.OrderedDict` )
		- A default section ( **_default** ) will store orphans attributes ( Attributes appearing before any declared section ).
		- File comments are stored inside the :obj:`foundations.parser.Parser.comments` class property. 
		- Sections, attributes and values are whitespaces stripped by default but can also be stored with their leading and trailing whitespaces. 
		- Values are quotations markers stripped by default but can also be stored with their leading and trailing quotations markers. 
		- Attributes are namespaced by default allowing sections merge without keys collisions. 

	"""

	@core.executionTrace
	def __init__(self, file=None, splitters=("=", ":"), namespaceSplitter="|", commentLimiters=(";", "#"), commentMarker="#", quotationMarkers=("\"", "'", "`"), rawSectionContentIdentifier="_rawSectionContent", defaultsSection="_defaults"):
		"""
		This method initializes the class.
		
		Usage::
		
			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", "[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> parser = Parser()
			>>> parser.content = content
			>>> parser.parse(stripComments=False)
			True
			>>> print parser.sections.keys()
			['Section A', 'Section B']
			>>> print parser.comments 
			OrderedDict([('Section A|#0', {'content': 'Comment.', 'id': 0})])

		:param file: Current file path. ( String )
		:param splitters: Splitter character. ( String )
		:param namespaceSplitter: Namespace splitters character. ( String )
		:param commentLimiters: Comment limiters character. ( List / Tuple )
		:param commentMarker: Character use to prefix extracted comments idientifiers. ( String )
		:param quotationMarkers: Quotation markers characters. ( List / Tuple )
		:param rawSectionContentIdentifier: Raw section content identifier. ( String )
		:param defaultsSection: Default section name. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		io.File.__init__(self, file)

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

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def splitters(self):
		"""
		This method is the property for **self.__splitters** attribute.

		:return: self.__splitters. ( List / Tuple )
		"""

		return self.__splitters

	@splitters.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def splitters(self, value):
		"""
		This method is the setter method for **self.__splitters** attribute.

		:param value: Attribute value. ( List / Tuple )
		"""

		if value:
			assert type(value) in (list, tuple), "'{0}' attribute: '{1}' type is not 'list' or 'tuple'!".format("splitters", value)
			for element in value:
				assert len(element) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("splitter", element)
				assert not re.search("\w", element), "'{0}' attribute: '{1}' is an alphanumeric character!".format("splitter", element)
		self.__splitters = value

	@splitters.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def splitters(self):
		"""
		This method is the deleter method for **self.__splitters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("splitters"))

	@property
	def namespaceSplitter(self):
		"""
		This method is the property for **self.__namespaceSplitter** attribute.

		:return: self.__namespaceSplitter. ( String )
		"""

		return self.__namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def namespaceSplitter(self, value):
		"""
		This method is the setter method for **self.__namespaceSplitter** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("namespaceSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespaceSplitter", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("namespaceSplitter", value)
		self.__namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def namespaceSplitter(self):
		"""
		This method is the deleter method for **self.__namespaceSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("namespaceSplitter"))

	@property
	def commentLimiters(self):
		"""
		This method is the property for **self.__commentLimiters** attribute.

		:return: self.__commentLimiters. ( List / Tuple )
		"""

		return self.__commentLimiters

	@commentLimiters.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def commentLimiters(self, value):
		"""
		This method is the setter method for **self.__commentLimiters** attribute.

		:param value: Attribute value. ( List / Tuple )
		"""

		if value:
			assert type(value) in (list, tuple), "'{0}' attribute: '{1}' type is not 'list' or 'tuple'!".format("commentLimiters", value)
		self.__commentLimiters = value

	@commentLimiters.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commentLimiters(self):
		"""
		This method is the deleter method for **self.__commentLimiters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("commentLimiters"))

	@property
	def commentMarker(self):
		"""
		This method is the property for **self.__commentMarker** attribute.

		:return: self.__commentMarker. ( String )
		"""

		return self.__commentMarker

	@commentMarker.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def commentMarker(self, value):
		"""
		This method is the setter method for **self.__commentMarker** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("commentMarker", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("commentMarker", value)
		self.__commentMarker = value

	@commentMarker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commentMarker(self):
		"""
		This method is the deleter method for **self.__commentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("commentMarker"))

	@property
	def quotationMarkers(self):
		"""
		This method is the property for **self.__quotationMarkers** attribute.

		:return: self.__quotationMarkers. ( List / Tuple )
		"""

		return self.__quotationMarkers

	@quotationMarkers.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def quotationMarkers(self, value):
		"""
		This method is the setter method for **self.__quotationMarkers** attribute.

		:param value: Attribute value. ( List / Tuple )
		"""

		if value:
			assert type(value) in (list, tuple), "'{0}' attribute: '{1}' type is not 'list' or 'tuple'!".format("quotationMarkers", value)
			for element in value:
				assert len(element) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("splitter", element)
				assert not re.search("\w", element), "'{0}' attribute: '{1}' is an alphanumeric character!".format("splitter", element)
		self.__quotationMarkers = value

	@quotationMarkers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def quotationMarkers(self):
		"""
		This method is the deleter method for **self.__quotationMarkers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("quotationMarkers"))

	@property
	def rawSectionContentIdentifier(self):
		"""
		This method is the property for **self.__rawSectionContentIdentifier** attribute.

		:return: self.__rawSectionContentIdentifier. ( String )
		"""

		return self.__rawSectionContentIdentifier

	@rawSectionContentIdentifier.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def rawSectionContentIdentifier(self, value):
		"""
		This method is the setter method for **self.__rawSectionContentIdentifier** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("rawSectionContentIdentifier", value)
		self.__rawSectionContentIdentifier = value

	@rawSectionContentIdentifier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rawSectionContentIdentifier(self):
		"""
		This method is the deleter method for **self.__rawSectionContentIdentifier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("rawSectionContentIdentifier"))
	@property
	def defaultsSection(self):
		"""
		This method is the property for **self.__defaultsSection** attribute.

		:return: self.__defaultsSection. ( String )
		"""

		return self.__defaultsSection

	@defaultsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultsSection(self, value):
		"""
		This method is the setter method for **self.__defaultsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("defaultsSection", value)
		self.__defaultsSection = value

	@defaultsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultsSection(self):
		"""
		This method is the deleter method for **self.__defaultsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultsSection"))

	@property
	def sections(self):
		"""
		This method is the property for **self.__sections** attribute.

		:return: self.__sections. ( Dictionary )
		"""

		return self.__sections

	@sections.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def sections(self, value):
		"""
		This method is the setter method for **self.__sections** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("sections", value)
		self.__sections = value

	@sections.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def sections(self):
		"""
		This method is the deleter method for **self.__sections** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("sections"))

	@property
	def comments(self):
		"""
		This method is the property for **self.__comments** attribute.

		:return: self.__comments. ( Dictionary )
		"""

		return self.__comments

	@comments.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def comments(self, value):
		"""
		This method is the setter method for **self.__comments** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("comments", value)
		self.__comments = value

	@comments.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def comments(self):
		"""
		This method is the deleter method for **self.__comments** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("comments"))

	@property
	def parsingErrors(self):
		"""
		This method is the property for **self.__parsingErrors** attribute.

		:return: self.__parsingErrors. ( List )
		"""

		return self.__parsingErrors

	@parsingErrors.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def parsingErrors(self, value):
		"""
		This method is the setter method for **self.__parsingErrors** attribute.

		:param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("parsingErrors", value)
		self.__parsingErrors = value

	@parsingErrors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parsingErrors(self):
		"""
		This method is the deleter method for **self.__parsingErrors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("parsingErrors"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileStructureParsingError)
	def parse(self, orderedDictionary=True, rawSections=None, namespaces=True, stripComments=True, stripWhitespaces=True, stripQuotationMarkers=True, raiseParsingErrors=True):
		"""
		This method process the file content and extract the sections / attributes as nested :class:`collections.OrderedDict` dictionaries or dictionaries.

		Usage::

			>>> content = ["; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> parser = Parser()
			>>> parser.content = content
			>>> parser.parse(stripComments=False)
			True
			>>> print parser.sections.keys()
			['_defaults']
			>>> print parser.sections["_defaults"].values()
			['Value A', 'Value B']
			>>> parser.parse(stripQuotationMarkers=False)
			True
			>>> print parser.sections["_defaults"].values()
			['"Value A"', '"Value B"']
			>>> print parser.comments 
			OrderedDict([('_defaults|#0', {'content': 'Comment.', 'id': 0})])
			>>> parser.parse()
			True
			>>> print parser.sections["_defaults"]
			OrderedDict([('_defaults|Attribute 1', 'Value A'), ('_defaults|Attribute 2', 'Value B')])
			>>> parser.parse(namespaces=False)
			OrderedDict([('Attribute 1', 'Value A'), ('Attribute 2', 'Value B')])

		:param orderedDictionary: Parser data is stored in :class:`collections.OrderedDict` dictionaries. ( Boolean )
		:param rawSections: Ignored raw sections. ( List / Tuple )
		:param namespaces: Attributes and comments are namespaced. ( Boolean )
		:param stripComments: Comments are stripped. ( Boolean )
		:param stripWhitespaces: Whitespaces are stripped. ( Boolean )
		:param stripQuotationMarkers: Attributes values quotation markers are stripped. ( Boolean )
		:param raiseParsingErrors: Raise parsing errors. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Reading sections from: '{0}'.".format(self.file))

		if not self.content:
			return

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
					comment = namespaces and foundations.namespace.setNamespace(section, "{0}{1}".format(self.__commentMarker, str(commentId)), self.__namespaceSplitter) or "{0}{1}".format(self.__commentMarker, str(commentId))
					self.__comments[comment] = {"id" : commentId, "content" : stripWhitespaces and search.group("comment").strip() or search.group("comment")}
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
				attribute = namespaces and foundations.namespace.setNamespace(section, self.__rawSectionContentIdentifier, self.__namespaceSplitter) or self.__rawSectionContentIdentifier
				attributes[attribute] = rawContent
			else:
				# Empty line matching.
				search = re.search(r"^\s*$", line)
				if search:
					continue

				# Attributes matching.
				search = re.search(r"^(?P<attribute>.+?)[{0}](?P<value>.+)$".format("".join(self.__splitters)), line)
				if search:
					attribute = stripWhitespaces and search.group("attribute").strip() or search.group("attribute")
					attribute = namespaces and foundations.namespace.setNamespace(section, attribute, self.__namespaceSplitter) or attribute
					value = stripWhitespaces and search.group("value").strip() or search.group("value")
					attributes[attribute] = stripQuotationMarkers and value.strip("".join(self.__quotationMarkers)) or value
				else:
					self.__parsingErrors.append(foundations.exceptions.AttributeStructureParsingError("Attribute structure is invalid: {0}".format(line), i + 1))

			self.__sections[section] = attributes

		LOGGER.debug("> Sections: '{0}'.".format(self.__sections))
		LOGGER.debug("> '{0}' file parsing done!".format(self.file))

		if self.__parsingErrors and raiseParsingErrors:
			raise foundations.exceptions.FileStructureParsingError("'{0}' structure is invalid, parsing exceptions occured!".format(self.file))

		return True

	@core.executionTrace
	def sectionExists(self, section):
		"""
		This method checks if provided section exists.
		
		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", "[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> parser = Parser()
			>>> parser.content = content
			>>> parser.parse()
			True
			>>> print parser.sectionExists("Section A")
			True
			>>> print parser.sectionExists("Section C")
			False

		:param section: Section to check existence. ( String )
		:return: Section existence. ( Boolean )
		"""

		if not self.__sections:
			return

		if section in self.__sections.keys():
			LOGGER.debug("> '{0}' section exists in '{1}'.".format(section, self))
			return True
		else:
			LOGGER.debug("> '{0}' section doesn't exists in '{1}'.".format(section, self))
			return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, KeyError)
	def attributeExists(self, attribute, section):
		"""
		This method checks if provided attribute exists.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", "[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> parser = Parser()
			>>> parser.content = content
			>>> parser.parse()
			True
			>>> print parser.attributeExists("Attribute 1", "Section A")
			True
			>>> print parser.attributeExists("Attribute 2", "Section A")
			False

		:param attribute: Attribute to check existence. ( String )
		:param section: Section to search attribute into. ( String )
		:return: Attribute existence. ( Boolean )
		"""

		if not self.__sections:
			return

		if namespace.removeNamespace(attribute, rootOnly=True) in self.getAttributes(section, orderedDictionary=True, stripNamespaces=True):
			LOGGER.debug("> '{0}' attribute exists in '{1}' section.".format(attribute, section))
			return True
		else:
			LOGGER.debug("> '{0}' attribute doesn't exists in '{1}' section.".format(attribute, section))
			return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, KeyError)
	def getAttributes(self, section, orderedDictionary=True, stripNamespaces=False, raiseExceptions=True):
		"""
		This method returns provided section attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", "[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> parser = Parser()
			>>> parser.content = content
			>>> parser.parse()
			True
			>>> print parser.getAttributes("Section A")
			OrderedDict([('Section A|Attribute 1', 'Value A')])
			>>> print parser.getAttributes("Section A", orderedDictionary=False)
			{'Section A|Attribute 1': 'Value A'}
			>>> print parser.getAttributes("Section A", stripNamespaces=True)
			OrderedDict([('Attribute 1', 'Value A')])

		:param section: Section containing the requested attributes. ( String )
		:param orderedDictionary: Use an :class:`collections.OrderedDict` dictionary to store the attributes. ( String )
		:param stripNamespaces: Strip namespaces while retrieving attributes. ( Boolean )
		:param raiseExceptions: Raise if section doesn't exists. ( Boolean )
		:return: Attributes. ( OrderedDict / Dictionary )
		"""

		LOGGER.debug("> Getting section '{0}' attributes.".format(section))
		if self.sectionExists(section):
			dictionary = orderedDictionary and OrderedDict or dict
			attributes = dictionary()
			if stripNamespaces:
				for attribute, value in self.__sections[section].items():
					attributes[namespace.removeNamespace(attribute, rootOnly=True)] = value
			else:
				attributes.update(self.__sections[section])
			LOGGER.debug("> Attributes: '{0}'.".format(attributes))
			return attributes
		else:
			if raiseExceptions:
				raise KeyError("'{0}' section doesn't exists in '{1}' sections!".format(section, self.file))
			else:
				LOGGER.warning("!> {0} | '{1}' section doesn't exists in '{2}' sections!".format(self.__class__.__name__, section, self.file))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getAllAttributes(self, orderedDictionary=True):
		"""
		This method returns all sections attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", "[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> parser = Parser()
			>>> parser.content = content
			>>> parser.parse()
			True
			>>> print parser.getAllAttributes()
			OrderedDict([('Section A|Attribute 1', 'Value A'), ('Section B|Attribute 2', 'Value B')])
			>>> print parser.getAllAttributes(orderedDictionary=False)
			{'Section B|Attribute 2': 'Value B', 'Section A|Attribute 1': 'Value A'}

		:param orderedDictionary: Use an :class:`collections.OrderedDict` dictionary to store the attributes. ( String )
		:return: All sections / files attributes. ( OrderedDict / Dictionary )
		"""

		if not self.__sections:
			return

		dictionary = orderedDictionary and OrderedDict or dict
		allAttributes = dictionary()
		for attributes in self.__sections.values():
			for attribute, value in attributes.items():
				allAttributes[attribute] = value
		return allAttributes

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, KeyError)
	def getValue(self, attribute, section, encode=False):
		"""
		This method returns requested attribute value.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", "[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> parser = Parser()
			>>> parser.content = content
			>>> parser.parse()
			True
			>>> print parser.getValue("Attribute 1", "Section A")
			Value A

		:param attribute: Attribute name. ( String )
		:param section: Section containing the searched attribute. ( String )
		:param encode: Encode value to unicode. ( Boolean )
		:return: Attribute value. ( String )
		"""

		if not self.__sections:
			return

		if self.attributeExists(attribute, section):
			if attribute in self.__sections[section].keys():
				value = self.__sections[section][attribute]
			elif namespace.setNamespace(section, attribute) in self.__sections[section].keys():
				value = self.__sections[section][namespace.setNamespace(section, attribute)]
			LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))
			value = encode and unicode(value, Constants.encodingFormat, Constants.encodingError) or value
			return value

@core.executionTrace
def getAttributeCompound(attribute, value=None, splitter="|", bindingIdentifier="@"):
	"""
	This definition returns an attribute compound.
	
	Usage::
	
		>>> datas = "@Link | Value | Boolean | Link Parameter"
		>>> attributeCompound = foundations.parser.getAttributeCompound("Attribute Compound", datas)
		>>> print attributeCompound.name
		Attribute Compound
		>>> print attributeCompound.value
		Value
		>>> print attributeCompound.link
		@Link
		>>> print attributeCompound.type
		Boolean
		>>> print attributeCompound.alias
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
			if len(valueTokens) >= 3 and re.search("{0}[a-zA-Z0-9_]*".format(bindingIdentifier), valueTokens[0]):
				return AttributeCompound(name=attribute, value=valueTokens[1].strip(), link=valueTokens[0].strip(), type=valueTokens[2].strip(), alias=len(valueTokens) == 4 and valueTokens[3].strip() or None)
		else:
			if re.search("{0}[a-zA-Z0-9_]*".format(bindingIdentifier), value):
				return AttributeCompound(name=attribute, value=None, link=value, type=None, alias=None)

	return AttributeCompound(name=attribute, value=value, link=None, type=None, alias=None)
