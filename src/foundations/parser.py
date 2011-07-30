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
	This is the AttributeCompound class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		@param kwargs: name, value, link, type, alias. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__dict__.update(kwargs)

class Parser(io.File):
	"""
	This class provides methods to parse sections file format files.
	"""

	@core.executionTrace
	def __init__(self, file=None, splitter="=", namespaceSplitter="|", commentLimiter=";", commentMarker="#", rawSectionContentIdentifier="_rawSectionContent"):
		"""
		This method initializes the class.

		@param file: Current file path. ( String )
		@param splitter: Splitter character. ( String )
		@param namespaceSplitter: Namespace splitter character. ( String )
		@param commentLimiter: Comment limiter character. ( String )
		@param rawSectionContentIdentifier: Raw section content identifier. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		io.File.__init__(self, file)

		# --- Setting class attributes. ---
		self.__splitter = None
		self.splitter = splitter
		self.__namespaceSplitter = None
		self.namespaceSplitter = namespaceSplitter
		self.__commentLimiter = None
		self.commentLimiter = commentLimiter
		self.__commentMarker = None
		self.commentMarker = commentMarker
		self.__rawSectionContentIdentifier = None
		self.rawSectionContentIdentifier = rawSectionContentIdentifier

		self.__sections = None
		self.__comments = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def splitter(self):
		"""
		This method is the property for the _splitter attribute.

		@return: self.__splitter. ( String )
		"""

		return self.__splitter

	@splitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def splitter(self, value):
		"""
		This method is the setter method for the _splitter attribute.

		@param value: Attribute value. ( String )
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
		This method is the deleter method for the _splitter attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("splitter"))

	@property
	def namespaceSplitter(self):
		"""
		This method is the property for the _namespaceSplitter attribute.

		@return: self.__namespaceSplitter. ( String )
		"""

		return self.__namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def namespaceSplitter(self, value):
		"""
		This method is the setter method for the _namespaceSplitter attribute.

		@param value: Attribute value. ( String )
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
		This method is the deleter method for the _namespaceSplitter attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("namespaceSplitter"))

	@property
	def commentLimiter(self):
		"""
		This method is the property for the _commentLimiter attribute.

		@return: self.__commentLimiter. ( String )
		"""

		return self.__commentLimiter

	@commentLimiter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def commentLimiter(self, value):
		"""
		This method is the setter method for the _commentLimiter attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("commentLimiter", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("commentLimiter", value)
		self.__commentLimiter = value

	@commentLimiter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commentLimiter(self):
		"""
		This method is the deleter method for the _commentLimiter attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("commentLimiter"))

	@property
	def commentMarker(self):
		"""
		This method is the property for the _commentMarker attribute.

		@return: self.__commentMarker. ( String )
		"""

		return self.__commentMarker

	@commentMarker.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def commentMarker(self, value):
		"""
		This method is the setter method for the _commentMarker attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("commentMarker", value)
			assert not re.search("\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format("commentMarker", value)
		self.__commentMarker = value

	@commentMarker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commentMarker(self):
		"""
		This method is the deleter method for the _commentMarker attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("commentMarker"))

	@property
	def rawSectionContentIdentifier(self):
		"""
		This method is the property for the _rawSectionContentIdentifier attribute.

		@return: self.__rawSectionContentIdentifier. ( String )
		"""

		return self.__rawSectionContentIdentifier

	@rawSectionContentIdentifier.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def rawSectionContentIdentifier(self, value):
		"""
		This method is the setter method for the _rawSectionContentIdentifier attribute.

		@param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("rawSectionContentIdentifier", value)
		self.__rawSectionContentIdentifier = value

	@rawSectionContentIdentifier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rawSectionContentIdentifier(self):
		"""
		This method is the deleter method for the _rawSectionContentIdentifier attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("rawSectionContentIdentifier"))

	@property
	def sections(self):
		"""
		This method is the property for the _sections attribute.

		@return: self.__sections. ( Dictionary )
		"""

		return self.__sections

	@sections.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def sections(self, value):
		"""
		This method is the setter method for the _sections attribute.

		@param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("sections", value)
		self.__sections = value

	@sections.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def sections(self):
		"""
		This method is the deleter method for the _sections attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("sections"))

	@property
	def comments(self):
		"""
		This method is the property for the _comments attribute.

		@return: self.__comments. ( Dictionary )
		"""

		return self.__comments

	@comments.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def comments(self, value):
		"""
		This method is the setter method for the _comments attribute.

		@param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("comments", value)
		self.__comments = value

	@comments.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def comments(self):
		"""
		This method is the deleter method for the _comments attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("comments"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileStructureError)
	def parse(self, orderedDictionary=True, rawSections=None, stripComments=True):
		"""
		This method process the file content to extract the sections as a dictionary.

		@param orderedDictionary: Parser data is stored in ordered dictionaries. ( Boolean )
		@param rawSections: Section is not parsed. ( Boolean )
		@param stripComments: Comments are stripped. ( Boolean )
		@return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Reading sections from: '{0}'.".format(self.file))
		if self.content:
			if re.search("^\[.*\]", self.content[0]):
				if not orderedDictionary:
					self.__sections = {}
					self.__comments = {}
				else:
					self.__sections = OrderedDict()
					self.__comments = OrderedDict()
				rawSections = rawSections or []
				commentId = 0
				for line in self.content:
					if re.search("^\[.*\]", line):
						section = re.search("(?<=^\[)(.*)(?=\])", line)
						section = section.group(0)
						if not orderedDictionary:
							attributes = {}
						else:
							attributes = OrderedDict()
						rawContent = []
					else:
						if section in rawSections:
							rawContent.append(line)
							attributes[section + self.__namespaceSplitter + self.__rawSectionContentIdentifier] = rawContent
						else:
							if re.search("^ *\n", line) or re.search("^ *\r\n", line):
								continue
							else:
								if line.startswith(self.__commentLimiter) and not stripComments:
									self.__comments[section + self.__namespaceSplitter + self.__commentMarker + str(commentId)] = {"id" : commentId, "content" : line.strip().strip(self.__commentLimiter)}
									commentId += 1
								elif self.__splitter in line:
									lineTokens = line.split(self.__splitter, 1)
									attributes[section + self.__namespaceSplitter + lineTokens[0].strip()] = lineTokens[1].strip().strip("\"")
						self.__sections[section] = attributes

				LOGGER.debug("> Sections: '{0}'.".format(self.__sections))
				LOGGER.debug("> '{0}' file parsing done!".format(self.file))
				return True

			else:
				raise foundations.exceptions.FileStructureError("'{0}' structure is invalid: No section found at first line!".format(self.file))

	@core.executionTrace
	def sectionsExists(self, section):
		"""
		This method checks if a section exists.

		@param section: Section to check existence. ( String )
		@return: Section existence. ( Boolean )
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

		@param attribute: Attribute to check existence. ( String )
		@param section: Section to search attribute into. ( String )
		@return: Attribute existence. ( Boolean )
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

		@param section: Section containing the searched attribute. ( String )
		@param useNamespace: Use namespace while getting attributes. ( Boolean )
		@param raise_: Raise if section doesn't exists. ( Boolean )
		@return: Attributes. ( Dictionary )
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

		@param attribute: Attribute name. ( String )
		@param section: Section containing the searched attribute. ( String )
		@param encode: Encode value to unicode. ( Boolean )
		@return: Attribute value. ( String )
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
	This definition gets an attribute compound.

	@param attribute: Attribute. ( String )
	@param value: Attribute value. ( Object )
	@param splitter: Splitter. ( String )
	@param bindingIdentifier: Binding identifier. ( String )
	@return: Attribute compound. ( AttributeObject )
	"""

	LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))

	if value:
		if splitter in value:
			valueTokens = value.split(splitter)
			if len(valueTokens) >= 3 and re.search("{0}[a-zA-Z0-9_]*".format(bindingIdentifier), valueTokens[0]):
				return AttributeCompound(name=attribute, value=valueTokens[1].strip(), link=valueTokens[0].strip(), type=valueTokens[2].strip(), alias=len(valueTokens) == 4 and valueTokens[3].strip() or None)
		else:
			if re.search("{0}[a-zA-Z0-9_]*".format(bindingIdentifier), value):
				return AttributeCompound(name=attribute, value=None, link=value, type=None, alias=None)

	return AttributeCompound(name=attribute, value=value, link=None, type=None, alias=None)

