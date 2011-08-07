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
	This class represents a storage object for attributes compounds usually encountered in `sIBL_GUI <https://github.com/KelSolaar/sIBL_GUI>`_  Templates files.
	
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
	This class provides methods to parse sections file format files and more, an alternative fully compliant basic configuration file parser is available directly with Python: `ConfigParser <http://docs.python.org/library/configparser.html>`_.
	"""

	@core.executionTrace
	def __init__(self, file=None, splitter="=", namespaceSplitter="|", commentLimiters=(";", "#"), commentMarker="#", stringsMarkers=("\"", "'"), rawSectionContentIdentifier="_rawSectionContent", defaultsSection="_defaults"):
		"""
		This method initializes the class.

		:param file: Current file path. ( String )
		:param splitter: Splitter character. ( String )
		:param namespaceSplitter: Namespace splitter character. ( String )
		:param commentLimiters: Comment limiters character. ( List / Tuple )
		:param commentMarker: Character use to prefix extracted comments idientifiers. ( String )
		:param stringsMarkers: Strings markers characters. ( List / Tuple )
		:param rawSectionContentIdentifier: Raw section content identifier. ( String )
		:param defaultsSection: Default section name. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		io.File.__init__(self, file)

		# --- Setting class attributes. ---
		self.__splitter = None
		self.splitter = splitter
		self.__namespaceSplitter = None
		self.namespaceSplitter = namespaceSplitter
		self.__commentLimiters = None
		self.commentLimiters = commentLimiters
		self.__commentMarker = None
		self.commentMarker = commentMarker
		self.__stringsMarkers = None
		self.stringsMarkers = stringsMarkers
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
	def splitter(self):
		"""
		This method is the property for **self.__splitter** attribute.

		:return: self.__splitter. ( String )
		"""

		return self.__splitter

	@splitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def splitter(self, value):
		"""
		This method is the setter method for **self.__splitter** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("splitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("splitter", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("splitter", value)
		self.__splitter = value

	@splitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def splitter(self):
		"""
		This method is the deleter method for **self.__splitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("splitter"))

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
	def stringsMarkers(self):
		"""
		This method is the property for **self.__stringsMarkers** attribute.

		:return: self.__stringsMarkers. ( List / Tuple )
		"""

		return self.__stringsMarkers

	@stringsMarkers.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def stringsMarkers(self, value):
		"""
		This method is the setter method for **self.__stringsMarkers** attribute.

		:param value: Attribute value. ( List / Tuple )
		"""

		if value:
			assert type(value) in (list, tuple), "'{0}' attribute: '{1}' type is not 'list' or 'tuple'!".format("stringsMarkers", value)
		self.__stringsMarkers = value

	@stringsMarkers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def stringsMarkers(self):
		"""
		This method is the deleter method for **self.__stringsMarkers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("stringsMarkers"))

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
	def parse(self, orderedDictionary=True, rawSections=None, stripComments=True, stripWhitespaces=True, stripValues=True, raiseParsingErrors=True):
		"""
		This method process the file content to extract the sections as a dictionary.

		:param orderedDictionary: Parser data is stored in ordered dictionaries. ( Boolean )
		:param rawSections: Ignored raw sections. ( List / Tuple )
		:param stripComments: Comments are stripped. ( Boolean )
		:param stripWhitespaces: Whitespaces are stripped. ( Boolean )
		:param stripValues: Values are stripped using **self.__stringsMarkers** attribute value. ( Boolean )
		:param raiseParsingErrors: Raise parsing errors. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Reading sections from: '{0}'.".format(self.file))
		if self.content:
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
						self.__comments[foundations.namespace.setNamespace(section, "{0}{1}".format(self.__commentMarker, str(commentId)), self.__namespaceSplitter)] = {"id" : commentId, "content" : stripWhitespaces and search.group("comment").strip() or search.group("comment")}
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
					attributes[foundations.namespace.setNamespace(section, self.__rawSectionContentIdentifier, self.__namespaceSplitter)] = rawContent
				else:
					# Empty line matching.
					search = re.search(r"^\s*$", line)
					if search:
						continue

					# Attributes matching.
					search = re.search(r"^(?P<attribute>.+?){0}(?P<value>.+)$".format(self.__splitter), line)
					if search:
						attribute = stripWhitespaces and search.group("attribute").strip() or search.group("attribute")
						value = stripWhitespaces and search.group("value").strip() or search.group("value")
						attributes[foundations.namespace.setNamespace(section, attribute, self.__namespaceSplitter)] = stripValues and value.strip("".join(self.__stringsMarkers)) or value
					else:
						self.__parsingErrors.append(foundations.exceptions.AttributeStructureParsingError("Attribute structure is invalid: {0}".format(line), i + 1))

				self.__sections[section] = attributes

			LOGGER.debug("> Sections: '{0}'.".format(self.__sections))
			LOGGER.debug("> '{0}' file parsing done!".format(self.file))

			if self.__parsingErrors and raiseParsingErrors:
				raise foundations.exceptions.FileStructureParsingError("'{0}' structure is invalid, parsing exceptions occured!".format(self.file))

			return True

	@core.executionTrace
	def sectionsExists(self, section):
		"""
		This method checks if a section exists.

		:param section: Section to check existence. ( String )
		:return: Section existence. ( Boolean )
		"""

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
		This method checks if an attribute exists.

		:param attribute: Attribute to check existence. ( String )
		:param section: Section to search attribute into. ( String )
		:return: Attribute existence. ( Boolean )
		"""

		if namespace.removeNamespace(attribute) in self.getAttributes(section, True, False):
			LOGGER.debug("> '{0}' attribute exists in '{1}' section.".format(attribute, section))
			return True
		else:
			LOGGER.debug("> '{0}' attribute doesn't exists in '{1}' section.".format(attribute, section))
			return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, KeyError)
	def getAttributes(self, section, orderedDictionary=True, useNamespace=True, raise_=True):
		"""
		This method returns the section / files attributes.

		:param section: Section containing the searched attribute. ( String )
		:param useNamespace: Use namespace while getting attributes. ( Boolean )
		:param raise_: Raise if section doesn't exists. ( Boolean )
		:return: Attributes. ( Dictionary )
		"""

		LOGGER.debug("> Getting section '{0}' attributes.".format(section))

		if self.sectionsExists(section):
			dictionary = orderedDictionary and OrderedDict or dict
			attributes = useNamespace and self.__sections[section] or dictionary(((namespace.removeNamespace(attribute), self.__sections[section][attribute]) for attribute in self.__sections[section].keys()))
			LOGGER.debug("> Attributes: '{0}'.".format(attributes))
			return attributes
		else:
			if raise_:
				raise KeyError("'{0}' section doesn't exists in '{1}' sections!".format(section, self.file))
			else:
				LOGGER.warning("!> {0} | '{1}' section doesn't exists in '{2}' sections!".format(self.__class__.__name__, section, self.file))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, KeyError)
	def getValue(self, attribute, section, encode=False):
		"""
		This method returns the requested attribute value abstracting the namespace.

		:param attribute: Attribute name. ( String )
		:param section: Section containing the searched attribute. ( String )
		:param encode: Encode value to unicode. ( Boolean )
		:return: Attribute value. ( String )
		"""

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

