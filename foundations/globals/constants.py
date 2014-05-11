#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package default constants through the :class:`Constants` class.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform

import foundations

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["Constants"]

class Constants():
	"""
	Defines **Foundations** package default constants.
	"""

	application_name = "Foundations"
	"""
	:param application_name: Package Application name.
	:type application_name: unicode
	"""
	major_version = "2"
	"""
	:param major_version: Package major version.
	:type major_version: unicode
	"""
	minor_version = "1"
	"""
	:param minor_version: Package minor version.
	:type minor_version: unicode
	"""
	change_version = "0"
	"""
	:param change_version: Package change version.
	:type change_version: unicode
	"""
	version = ".".join((major_version, minor_version, change_version))
	"""
	:param version: Package version.
	:type version: unicode
	"""

	logger = "Foundations_Logger"
	"""
	:param logger: Package logger name.
	:type logger: unicode
	"""
	verbosity_level = 3
	"""
	:param verbosity_level: Default logging verbosity level.
	:type verbosity_level: int
	"""
	verbosity_labels = ("Critical", "Error", "Warning", "Info", "Debug")
	"""
	:param verbosity_labels: Logging verbosity labels.
	:type verbosity_labels: tuple
	"""
	logging_default_formatter = "Default"
	"""
	:param logging_default_formatter: Default logging formatter name.
	:type logging_default_formatter: unicode
	"""
	logging_separators = "*" * 96
	"""
	:param logging_separators: Logging separators.
	:type logging_separators: unicode
	"""

	default_codec = "utf-8"
	"""
	:param default_codec: Default codec.
	:type default_codec: unicode
	"""
	codec_error = "ignore"
	"""
	:param codec_error: Default codec error behavior.
	:type codec_error: unicode
	"""

	application_directory = os.sep.join(("Foundations", ".".join((major_version, minor_version))))
	"""
	:param application_directory: Package Application directory.
	:type application_directory: unicode
	"""
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		provider_directory = "HDRLabs"
		"""
		:param provider_directory: Package provider directory.
		:type provider_directory: unicode
		"""
	elif platform.system() == "Linux":
		provider_directory = ".HDRLabs"
		"""
		:param provider_directory: Package provider directory.
		:type provider_directory: unicode
		"""

	null_object = "None"
	"""
	:param null_object: Default null object string.
	:type null_object: unicode
	"""
