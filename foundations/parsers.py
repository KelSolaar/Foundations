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

from __future__ import unicode_literals

import base64
import datetime
import re
import sys
from xml.etree import ElementTree

if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

import foundations.common
import foundations.data_structures
import foundations.exceptions
import foundations.io
import foundations.namespace
import foundations.strings
import foundations.verbose
import foundations.walkers

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "AttributeCompound", "SectionsFileParser", "PlistFileParser", "get_attribute_compound"]

LOGGER = foundations.verbose.install_logger()

class AttributeCompound(foundations.data_structures.Structure):
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

		foundations.data_structures.Structure.__init__(self, **kwargs)

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
				 namespace_splitter="|",
				 comment_limiters=(";", "#"),
				 comment_marker="#",
				 quotation_markers=("\"", "'", "`"),
				 raw_section_content_identifier="__raw__",
				 defaults_section="_defaults",
				 preserve_order=True):
		"""
		Initializes the class.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse(strip_comments=False)
			<foundations.parsers.SectionsFileParser object at 0x293892011>
			>>> sections_file_parser.sections.keys()
			[u'Section A', u'Section B']
			>>> sections_file_parser.comments
			OrderedDict([(u'Section A|#0', {u'content': u'Comment.', u'id': 0})])

		:param file: Current file path.
		:type file: unicode
		:param splitters: Splitter characters.
		:type splitters: tuple or list
		:param namespace_splitter: Namespace splitters character.
		:type namespace_splitter: unicode
		:param comment_limiters: Comment limiters characters.
		:type comment_limiters: tuple or list
		:param comment_marker: Character use to prefix extracted comments idientifiers.
		:type comment_marker: unicode
		:param quotation_markers: Quotation markers characters.
		:type quotation_markers: tuple or list
		:param raw_section_content_identifier: Raw section content identifier.
		:type raw_section_content_identifier: unicode
		:param defaults_section: Default section name.
		:type defaults_section: unicode
		:param preserve_order: Data order is preserved.
		:type preserve_order: bool
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.io.File.__init__(self, file)

		# --- Setting class attributes. ---
		self.__splitters = None
		self.splitters = splitters
		self.__namespace_splitter = None
		self.namespace_splitter = namespace_splitter
		self.__comment_limiters = None
		self.comment_limiters = comment_limiters
		self.__comment_marker = None
		self.comment_marker = comment_marker
		self.__quotation_markers = None
		self.quotation_markers = quotation_markers
		self.__raw_section_content_identifier = None
		self.raw_section_content_identifier = raw_section_content_identifier
		self.__defaults_section = None
		self.defaults_section = defaults_section
		self.__preserve_order = None
		self.preserve_order = preserve_order

		if not preserve_order:
			self.__sections = {}
			self.__comments = {}
		else:
			self.__sections = OrderedDict()
			self.__comments = OrderedDict()
		self.__parsing_errors = []

	@property
	def splitters(self):
		"""
		Property for **self.__splitters** attribute.

		:return: self.__splitters.
		:rtype: tuple or list
		"""

		return self.__splitters

	@splitters.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def splitters(self):
		"""
		Deleter for **self.__splitters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "splitters"))

	@property
	def namespace_splitter(self):
		"""
		Property for **self.__namespace_splitter** attribute.

		:return: self.__namespace_splitter.
		:rtype: unicode
		"""

		return self.__namespace_splitter

	@namespace_splitter.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def namespace_splitter(self, value):
		"""
		Setter for **self.__namespace_splitter** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"namespace_splitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespace_splitter",
																							  value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"namespace_splitter", value)
		self.__namespace_splitter = value

	@namespace_splitter.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def namespace_splitter(self):
		"""
		Deleter for **self.__namespace_splitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespace_splitter"))

	@property
	def comment_limiters(self):
		"""
		Property for **self.__comment_limiters** attribute.

		:return: self.__comment_limiters.
		:rtype: tuple or list
		"""

		return self.__comment_limiters

	@comment_limiters.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def comment_limiters(self, value):
		"""
		Setter for **self.__comment_limiters** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
				"comment_limiters", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"comment_limiters", element)
		self.__comment_limiters = value

	@comment_limiters.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def comment_limiters(self):
		"""
		Deleter for **self.__comment_limiters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "comment_limiters"))

	@property
	def comment_marker(self):
		"""
		Property for **self.__comment_marker** attribute.

		:return: self.__comment_marker.
		:rtype: unicode
		"""

		return self.__comment_marker

	@comment_marker.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def comment_marker(self, value):
		"""
		Setter for **self.__comment_marker** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"comment_marker", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"comment_marker", value)
		self.__comment_marker = value

	@comment_marker.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def comment_marker(self):
		"""
		Deleter for **self.__comment_marker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "comment_marker"))

	@property
	def quotation_markers(self):
		"""
		Property for **self.__quotation_markers** attribute.

		:return: self.__quotation_markers.
		:rtype: tuple or list
		"""

		return self.__quotation_markers

	@quotation_markers.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def quotation_markers(self, value):
		"""
		Setter for **self.__quotation_markers** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
				"quotation_markers", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"quotation_markers", element)
				assert len(element) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("quotation_markers",
																									element)
				assert not re.search(r"\w", element), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
					"quotation_markers", element)
		self.__quotation_markers = value

	@quotation_markers.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def quotation_markers(self):
		"""
		Deleter for **self.__quotation_markers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "quotation_markers"))

	@property
	def raw_section_content_identifier(self):
		"""
		Property for **self. __raw_section_content_identifier** attribute.

		:return: self.__raw_section_content_identifier.
		:rtype: unicode
		"""

		return self.__raw_section_content_identifier

	@raw_section_content_identifier.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def raw_section_content_identifier(self, value):
		"""
		Setter for **self. __raw_section_content_identifier** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"raw_section_content_identifier", value)
		self.__raw_section_content_identifier = value

	@raw_section_content_identifier.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def raw_section_content_identifier(self):
		"""
		Deleter for **self. __raw_section_content_identifier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "raw_section_content_identifier"))

	@property
	def defaults_section(self):
		"""
		Property for **self.__defaults_section** attribute.

		:return: self.__defaults_section.
		:rtype: unicode
		"""

		return self.__defaults_section

	@defaults_section.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def defaults_section(self, value):
		"""
		Setter for **self.__defaults_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"defaults_section", value)
		self.__defaults_section = value

	@defaults_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def defaults_section(self):
		"""
		Deleter for **self.__defaults_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaults_section"))

	@property
	def sections(self):
		"""
		Property for **self.__sections** attribute.

		:return: self.__sections.
		:rtype: OrderedDict or dict
		"""

		return self.__sections

	@sections.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def comments(self):
		"""
		Deleter for **self.__comments** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "comments"))

	@property
	def parsing_errors(self):
		"""
		Property for **self.__parsing_errors** attribute.

		:return: self.__parsing_errors.
		:rtype: list
		"""

		return self.__parsing_errors

	@parsing_errors.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def parsing_errors(self, value):
		"""
		Setter for **self.__parsing_errors** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("parsing_errors", value)
			for element in value:
				assert issubclass(element.__class__, foundations.exceptions.AbstractParsingError), \
					"'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
						"parsing_errors", element, foundations.exceptions.AbstractParsingError.__class__.__name__)
		self.__parsing_errors = value

	@parsing_errors.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def parsing_errors(self):
		"""
		Deleter for **self.__parsing_errors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parsing_errors"))

	@property
	def preserve_order(self):
		"""
		Property for **self.__preserve_order** attribute.

		:return: self.__preserve_order.
		:rtype: bool
		"""

		return self.__preserve_order

	@preserve_order.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def preserve_order(self, value):
		"""
		Setter method for **self.__preserve_order** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("preserve_order", value)
		self.__preserve_order = value

	@preserve_order.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def preserve_order(self):
		"""
		Deleter method for **self.__preserve_order** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preserve_order"))

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

		return self.section_exists(section)

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Sections count.
		:rtype: int
		"""

		return len(self.__sections)

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileStructureParsingError)
	def parse(self,
			  raw_sections=None,
			  namespaces=True,
			  strip_comments=True,
			  strip_whitespaces=True,
			  strip_quotation_markers=True,
			  raise_parsing_errors=True):
		"""
		Process the file content and extracts the sections / attributes
			as nested :class:`collections.OrderedDict` dictionaries or dictionaries.

		Usage::

			>>> content = ["; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse(strip_comments=False)
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sections_file_parser.sections.keys()
			[u'_defaults']
			>>> sections_file_parser.sections["_defaults"].values()
			[u'Value A', u'Value B']
			>>> sections_file_parser.parse(strip_comments=False, strip_quotation_markers=False)
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sections_file_parser.sections["_defaults"].values()
			[u'"Value A"', u'"Value B"']
			>>> sections_file_parser.comments
			OrderedDict([(u'_defaults|#0', {u'content': u'Comment.', u'id': 0})])
			>>> sections_file_parser.parse()
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sections_file_parser.sections["_defaults"]
			OrderedDict([(u'_defaults|Attribute 1', u'Value A'), (u'_defaults|Attribute 2', u'Value B')])
			>>> sections_file_parser.parse(namespaces=False)
			<foundations.parsers.SectionsFileParser object at 0x860323123>
			>>> sections_file_parser.sections["_defaults"]
			OrderedDict([(u'Attribute 1', u'Value A'), (u'Attribute 2', u'Value B')])

		:param raw_sections: Ignored raw sections.
		:type raw_sections: tuple or list
		:param namespaces: Attributes and comments are namespaced.
		:type namespaces: bool
		:param strip_comments: Comments are stripped.
		:type strip_comments: bool
		:param strip_whitespaces: Whitespaces are stripped.
		:type strip_whitespaces: bool
		:param strip_quotation_markers: Attributes values quotation markers are stripped.
		:type strip_quotation_markers: bool
		:param raise_parsing_errors: Raise parsing errors.
		:type raise_parsing_errors: bool
		:return: SectionFileParser instance.
		:rtype: SectionFileParser
		"""

		LOGGER.debug("> Reading sections from: '{0}'.".format(self.path))

		if not self.content:
			self.read()

		attributes = {} if not self.__preserve_order else OrderedDict()
		section = self.__defaults_section
		raw_sections = raw_sections or []

		commentId = 0
		for i, line in enumerate(self.content):
			# Comments matching.
			search = re.search(r"^\s*[{0}](?P<comment>.+)$".format("".join(self.__comment_limiters)), line)
			if search:
				if not strip_comments:
					comment = namespaces and foundations.namespace.set_namespace(section, "{0}{1}".format(
						self.__comment_marker, commentId), self.__namespace_splitter) or \
							  "{0}{1}".format(self.__comment_marker, commentId)
					self.__comments[comment] = {"id": commentId, "content": strip_whitespaces and \
																			search.group(
																				"comment").strip() or search.group(
						"comment")}
					commentId += 1
				continue

			# Sections matching.
			search = re.search(r"^\s*\[(?P<section>.+)\]\s*$", line)
			if search:
				section = strip_whitespaces and search.group("section").strip() or search.group("section")
				if not self.__preserve_order:
					attributes = {}
				else:
					attributes = OrderedDict()
				rawContent = []
				continue

			if section in raw_sections:
				rawContent.append(line)
				attributes[self.__raw_section_content_identifier] = rawContent
			else:
				# Empty line matching.
				search = re.search(r"^\s*$", line)
				if search:
					continue

				# Attributes matching.
				search = re.search(r"^(?P<attribute>.+?)[{0}](?P<value>.+)$".format("".join(self.__splitters)), line) \
					or re.search(r"^(?P<attribute>.+?)[{0}]\s*$".format("".join(self.__splitters)), line)
				if search:
					attribute = search.group("attribute").strip() if strip_whitespaces else search.group("attribute")
					attribute = foundations.namespace.set_namespace(section, attribute, self.__namespace_splitter) \
						if namespaces else attribute

					if len(search.groups()) == 2:
						value = search.group("value").strip() if strip_whitespaces else search.group("value")
						attributes[attribute] = value.strip("".join(self.__quotation_markers)) \
							if strip_quotation_markers else value
					else:
						attributes[attribute] = None
				else:
					self.__parsing_errors.append(foundations.exceptions.AttributeStructureParsingError(
						"Attribute structure is invalid: {0}".format(line), i + 1))

			self.__sections[section] = attributes

		LOGGER.debug("> Sections: '{0}'.".format(self.__sections))
		LOGGER.debug("> '{0}' file parsing done!".format(self.path))

		if self.__parsing_errors and raise_parsing_errors:
			raise foundations.exceptions.FileStructureParsingError(
				"{0} | '{1}' structure is invalid, parsing exceptions occured!".format(self.__class__.__name__,
																					   self.path))

		return self

	def section_exists(self, section):
		"""
		Checks if given section exists.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse()
			<foundations.parsers.SectionsFileParser object at 0x845683844>
			>>> sections_file_parser.section_exists("Section A")
			True
			>>> sections_file_parser.section_exists("Section C")
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

	def attribute_exists(self, attribute, section):
		"""
		Checks if given attribute exists.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse()
			<foundations.parsers.SectionsFileParser object at 0x234564563>
			>>> sections_file_parser.attribute_exists("Attribute 1", "Section A")
			True
			>>> sections_file_parser.attribute_exists("Attribute 2", "Section A")
			False

		:param attribute: Attribute to check existence.
		:type attribute: unicode
		:param section: Section to search attribute into.
		:type section: unicode
		:return: Attribute existence.
		:rtype: bool
		"""

		if foundations.namespace.remove_namespace(attribute, root_only=True) in self.get_attributes(section,
																								 strip_namespaces=True):
			LOGGER.debug("> '{0}' attribute exists in '{1}' section.".format(attribute, section))
			return True
		else:
			LOGGER.debug("> '{0}' attribute doesn't exists in '{1}' section.".format(attribute, section))
			return False

	def get_attributes(self, section, strip_namespaces=False):
		"""
		Returns given section attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse()
			<foundations.parsers.SectionsFileParser object at 0x125698322>
			>>> sections_file_parser.get_attributes("Section A")
			OrderedDict([(u'Section A|Attribute 1', u'Value A')])
			>>> sections_file_parser.preserve_order=False
			>>> sections_file_parser.get_attributes("Section A")
			{u'Section A|Attribute 1': u'Value A'}
			>>> sections_file_parser.preserve_order=True
			>>> sections_file_parser.get_attributes("Section A", strip_namespaces=True)
			OrderedDict([(u'Attribute 1', u'Value A')])

		:param section: Section containing the requested attributes.
		:type section: unicode
		:param strip_namespaces: Strip namespaces while retrieving attributes.
		:type strip_namespaces: bool
		:return: Attributes.
		:rtype: OrderedDict or dict
		"""

		LOGGER.debug("> Getting section '{0}' attributes.".format(section))

		attributes = OrderedDict() if self.__preserve_order else dict()
		if not self.section_exists(section):
			return attributes

		if strip_namespaces:
			for attribute, value in self.__sections[section].iteritems():
				attributes[foundations.namespace.remove_namespace(attribute, root_only=True)] = value
		else:
			attributes.update(self.__sections[section])
		LOGGER.debug("> Attributes: '{0}'.".format(attributes))
		return attributes

	def get_all_attributes(self):
		"""
		Returns all sections attributes.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse()
			<foundations.parsers.SectionsFileParser object at 0x845683844>
			>>> sections_file_parser.get_all_attributes()
			OrderedDict([(u'Section A|Attribute 1', u'Value A'), (u'Section B|Attribute 2', u'Value B')])
			>>> sections_file_parser.preserve_order=False
			>>> sections_file_parser.get_all_attributes()
			{u'Section B|Attribute 2': u'Value B', u'Section A|Attribute 1': u'Value A'}

		:return: All sections / files attributes.
		:rtype: OrderedDict or dict
		"""

		all_attributes = OrderedDict() if self.__preserve_order else dict()

		for attributes in self.__sections.itervalues():
			for attribute, value in attributes.iteritems():
				all_attributes[attribute] = value
		return all_attributes

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileStructureParsingError)
	def get_value(self, attribute, section, default=""):
		"""
		Returns requested attribute value.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse()
			<foundations.parsers.SectionsFileParser object at 0x679302423>
			>>> sections_file_parser.get_value("Attribute 1", "Section A")
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

		if not self.attribute_exists(attribute, section):
			return default

		if attribute in self.__sections[section]:
			value = self.__sections[section][attribute]
		elif foundations.namespace.set_namespace(section, attribute) in self.__sections[section]:
			value = self.__sections[section][foundations.namespace.set_namespace(section, attribute)]
		LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))
		return value

	def set_value(self, attribute, section, value):
		"""
		Sets requested attribute value.

		Usage::

			>>> content = ["[Section A]\\n", "; Comment.\\n", "Attribute 1 = \\"Value A\\"\\n", "\\n", \
"[Section B]\\n", "Attribute 2 = \\"Value B\\"\\n"]
			>>> sections_file_parser = SectionsFileParser()
			>>> sections_file_parser.content = content
			>>> sections_file_parser.parse()
			<foundations.parsers.SectionsFileParser object at 0x109304209>
			>>> sections_file_parser.set_value("Attribute 3", "Section C", "Value C")
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

		if not self.section_exists(section):
			LOGGER.debug("> Adding '{0}' section.".format(section))
			self.__sections[section] = OrderedDict() if self.__preserve_order else dict()

		self.__sections[section][attribute] = value

		return True

	def write(self,
			  namespaces=False,
			  splitter="=",
			  comment_limiter=(";"),
			  spaces_around_splitter=True,
			  space_after_comment_limiter=True):
		"""
		Writes defined file using :obj:`SectionsFileParser.sections` and
			:obj:`SectionsFileParser.comments` class properties content.

		Usage::

			>>> sections = {"Section A": {"Section A|Attribute 1": "Value A"}, \
"Section B": {"Section B|Attribute 2": "Value B"}}
			>>> sections_file_parser = SectionsFileParser("SectionsFile.rc")
			>>> sections_file_parser.sections = sections
			>>> sections_file_parser.write()
			True
			>>> sections_file_parser.read()
			u'[Section A]\\nAttribute 1 = Value A\\n\\n[Section B]\\nAttribute 2 = Value B\\n'

		:param namespaces: Attributes are namespaced.
		:type namespaces: bool
		:param splitter: Splitter character.
		:type splitter: unicode
		:param comment_limiter: Comment limiter character.
		:type comment_limiter: unicode
		:param spaces_around_splitter: Spaces around attributes and value splitters.
		:type spaces_around_splitter: bool
		:param space_after_comment_limiter: Space after comments limiter.
		:type space_after_comment_limiter: bool
		:return: Method success.
		:rtype: bool
		"""

		self.uncache()

		LOGGER.debug("> Setting '{0}' file content.".format(self.path))
		attribute_template = "{{0}} {0} {{1}}\n".format(splitter) if spaces_around_splitter else \
							"{{0}}{0}{{1}}\n".format(splitter)
		attribute_template = foundations.strings.replace(attribute_template, {"{{" : "{", "}}" : "}"})
		comment_template = space_after_comment_limiter and "{0} {{0}}\n".format(comment_limiter) or \
						  "{0}{{0}}\n".format(comment_limiter)
		if self.__defaults_section in self.__sections:
			LOGGER.debug("> Appending '{0}' default section.".format(self.__defaults_section))
			if self.__comments:
				for comment, value in self.__comments.iteritems():
					if self.__defaults_section in comment:
						value = value["content"] or ""
						LOGGER.debug("> Appending '{0}' comment with '{1}' value.".format(comment, value))
						self.content.append(comment_template.format(value))
			for attribute, value in self.__sections[self.__defaults_section].iteritems():
				attribute = namespaces and attribute or foundations.namespace.remove_namespace(attribute,
																							  self.__namespace_splitter,
																							  root_only=True)
				value = value or ""
				LOGGER.debug("> Appending '{0}' attribute with '{1}' value.".format(attribute, value))
				self.content.append(attribute_template.format(attribute, value))
			self.content.append("\n")

		for i, section in enumerate(self.__sections):
			LOGGER.debug("> Appending '{0}' section.".format(section))
			self.content.append("[{0}]\n".format(section))
			if self.__comments:
				for comment, value in self.__comments.iteritems():
					if section in comment:
						value = value["content"] or ""
						LOGGER.debug("> Appending '{0}' comment with '{1}' value.".format(comment, value))
						self.content.append(comment_template.format(value))
			for attribute, value in self.__sections[section].iteritems():
				if foundations.namespace.remove_namespace(attribute) == self.__raw_section_content_identifier:
					LOGGER.debug("> Appending '{0}' raw section content.".format(section))
					for line in value:
						self.content.append(line)
				else:
					LOGGER.debug("> Appending '{0}' section.".format(section))
					attribute = namespaces and attribute or foundations.namespace.remove_namespace(attribute,
																								  self.__namespace_splitter,
																								  root_only=True)
					value = value or ""
					LOGGER.debug("> Appending '{0}' attribute with '{1}' value.".format(attribute, value))
					self.content.append(attribute_template.format(attribute, value))
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

			>>> plist_file_parser = PlistFileParser("standard.plist")
			>>> plist_file_parser.parse()
			True
			>>> plist_file_parser.elements.keys()
			[u'Dictionary A', u'Number A', u'Array A', u'String A', u'Date A', u'Boolean A', u'Data A']
			>>> plist_file_parser.elements["Dictionary A"]
			{u'String C': u'My Value C', u'String B': u'My Value B'}

		:param file: Current file path.
		:type file: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.io.File.__init__(self, file)

		# --- Setting class attributes. ---
		self.__elements = None
		self.__parsing_errors = None

		self.__unserializers = {"array": lambda x: [value.text for value in x],
								"dict": lambda x: dict((x[i].text, x[i + 1].text) for i in range(0, len(x), 2)),
								"key": lambda x: foundations.strings.to_string(x.text) or "",
								"string": lambda x: foundations.strings.to_string(x.text) or "",
								"data": lambda x: base64.decodestring(x.text or ""),
								"date": lambda x: datetime.datetime(*map(int, re.findall("\d+", x.text))),
								"true": lambda x: True,
								"false": lambda x: False,
								"real": lambda x: float(x.text),
								"integer": lambda x: int(x.text)}

	@property
	def elements(self):
		"""
		Property for **self.__elements** attribute.

		:return: self.__elements.
		:rtype: OrderedDict or dict
		"""

		return self.__elements

	@elements.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def elements(self):
		"""
		Deleter for **self.__elements** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "elements"))

	@property
	def parsing_errors(self):
		"""
		Property for **self.__parsing_errors** attribute.

		:return: self.__parsing_errors.
		:rtype: list
		"""

		return self.__parsing_errors

	@parsing_errors.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def parsing_errors(self, value):
		"""
		Setter for **self.__parsing_errors** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("parsing_errors", value)
			for element in value:
				assert issubclass(element.__class__, foundations.exceptions.AbstractParsingError), \
					"'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
						"parsing_errors", element, foundations.exceptions.AbstractParsingError.__class__.__name__)
		self.__parsing_errors = value

	@parsing_errors.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def parsing_errors(self):
		"""
		Deleter for **self.__parsing_errors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parsing_errors"))

	@property
	def unserializers(self):
		"""
		Property for **self.__unserializers** attribute.

		:return: self.__unserializers.
		:rtype: dict
		"""

		return self.__unserializers

	@unserializers.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unserializers(self, value):
		"""
		Setter for **self.__unserializers** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "unserializers"))

	@unserializers.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unserializers(self):
		"""
		Deleter for **self.__unserializers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "unserializers"))

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileStructureParsingError)
	def parse(self, raise_parsing_errors=True):
		"""
		Process the file content.

		Usage::

			>>> plist_file_parser = PlistFileParser("standard.plist")
			>>> plist_file_parser.parse()
			True
			>>> plist_file_parser.elements.keys()
			[u'Dictionary A', u'Number A', u'Array A', u'String A', u'Date A', u'Boolean A', u'Data A']

		:param raise_parsing_errors: Raise parsing errors.
		:type raise_parsing_errors: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Reading elements from: '{0}'.".format(self.path))

		element_tree_parser = ElementTree.iterparse(self.path)

		self.__parsing_errors = []
		for action, element in element_tree_parser:
			unmarshal = self.__unserializers.get(element.tag)
			if unmarshal:
				data = unmarshal(element)
				element.clear()
				element.text = data
			elif element.tag != "plist":
				self.__parsing_errors.append(foundations.exceptions.FileStructureParsingError(
					"Unknown element: {0}".format(element.tag)))

		if self.__parsing_errors:
			if raise_parsing_errors:
				raise foundations.exceptions.FileStructureParsingError(
					"{0} | '{1}' structure is invalid, parsing exceptions occured!".format(self.__class__.__name__,
																						   self.path))
		else:
			self.__elements = foundations.common.get_first_item(element_tree_parser.root).text
			return True

	def element_exists(self, element):
		"""
		Checks if given element exists.

		Usage::

			>>> plist_file_parser = PlistFileParser("standard.plist")
			>>> plist_file_parser.parse()
			True
			>>> plist_file_parser.element_exists("String A")
			True
			>>> plist_file_parser.element_exists("String Nemo")
			False

		:param element: Element to check existence.
		:type element: unicode
		:return: Element existence.
		:rtype: bool
		"""

		if not self.__elements:
			return False

		for item in foundations.walkers.dictionaries_walker(self.__elements):
			path, key, value = item
			if key == element:
				LOGGER.debug("> '{0}' attribute exists.".format(element))
				return True

		LOGGER.debug("> '{0}' element doesn't exists.".format(element))
		return False

	def filter_values(self, pattern, flags=0):
		"""
		| Filters the :meth:`PlistFileParser.elements` class property elements using given pattern.
		| Will return a list of matching elements values, if you want to get only one element value, use
			the :meth:`PlistFileParser.get_value` method instead.

		Usage::

			>>> plist_file_parser = PlistFileParser("standard.plist")
			>>> plist_file_parser.parse()
			True
			>>> plist_file_parser.filter_values(r"String A")
			[u'My Value A']
			>>> plist_file_parser.filter_values(r"String.*")
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

		for item in foundations.walkers.dictionaries_walker(self.__elements):
			path, element, value = item
			if re.search(pattern, element, flags):
				values.append(value)
		return values

	def get_value(self, element):
		"""
		| Returns the given element value.
		| If multiple elements with the same name exists, only the first encountered will be returned.

		Usage::

			>>> plist_file_parser = PlistFileParser("standard.plist")
			>>> plist_file_parser.parse()
			True
			>>> plist_file_parser.get_value("String A")
			u'My Value A'

		:param element: Element to get the value.
		:type element: unicode
		:return: Element value.
		:rtype: object
		"""

		if not self.__elements:
			return

		values = self.filter_values(r"^{0}$".format(element))
		return foundations.common.get_first_item(values)

def get_attribute_compound(attribute, value=None, splitter="|", binding_identifier="@"):
	"""
	Returns an attribute compound.

	Usage::

		>>> data = "@Link | Value | Boolean | Link Parameter"
		>>> attribute_compound = foundations.parsers.get_attribute_compound("Attribute Compound", data)
		>>> attribute_compound.name
		u'Attribute Compound'
		>>> attribute_compound.value
		u'Value'
		>>> attribute_compound.link
		u'@Link'
		>>> attribute_compound.type
		u'Boolean'
		>>> attribute_compound.alias
		u'Link Parameter'

	:param attribute: Attribute.
	:type attribute: unicode
	:param value: Attribute value.
	:type value: object
	:param splitter: Splitter.
	:type splitter: unicode
	:param binding_identifier: Binding identifier.
	:type binding_identifier: unicode
	:return: Attribute compound.
	:rtype: AttributeCompound
	"""

	LOGGER.debug("> Attribute: '{0}', value: '{1}'.".format(attribute, value))

	if type(value) is unicode:
		if splitter in value:
			value_tokens = value.split(splitter)
			if len(value_tokens) >= 3 and re.search(r"{0}\w*".format(binding_identifier), value_tokens[0]):
				return AttributeCompound(name=attribute,
										 value=value_tokens[1].strip(),
										 link=value_tokens[0].strip(),
										 type=value_tokens[2].strip(),
										 alias=len(value_tokens) == 4 and value_tokens[3].strip() or None)
		else:
			if re.search(r"{0}\w*".format(binding_identifier), value):
				return AttributeCompound(name=attribute, value=None, link=value, type=None, alias=None)

	return AttributeCompound(name=attribute, value=value, link=None, type=None, alias=None)
