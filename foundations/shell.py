#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**shell.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines various shell manipulation objects.

**Others:**
	*ANSI* escape codes for colors from: https://wiki.archlinux.org/index.php/Color_Bash_Prompt

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.exceptions
import inspect
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "BACKGROUND_ANSI_ESCAPE_CODES", "FOREGROUND_ANSI_ESCAPE_CODES", "AnsiEscapeCodes", "colorize"]

LOGGER = foundations.verbose.installLogger()

BACKGROUND_ANSI_ESCAPE_CODES = (("bBlack", "40m"),
								("bRed", "41m"),
								("bGreen", "42m"),
								("bYellow", "43m"),
								("bBlue", "44m"),
								("bPurple", "45m"),
								("bCyan", "46m"),
								("bWhite", "47m"),
								("bHighBlack", "100m"),
								("bHighRed", "101m"),
								("bHighGreen", "102m"),
								("bHighYellow", "103m"),
								("bHighBlue", "104m"),
								("bHighPurple", "105m"),
								("bHighCyan", "106m"),
								("bHighWhite", "107m"))

FOREGROUND_ANSI_ESCAPE_CODES = (("black", "30m"),
								("red", "31m"),
								("green", "32m"),
								("yellow", "33m"),
								("blue", "34m"),
								("purple", "35m"),
								("cyan", "36m"),
								("white", "37m"),
								("boldBlack", "1;30m"),
								("boldRed", "1;31m"),
								("boldGreen", "1;32m"),
								("boldYellow", "1;33m"),
								("boldBlue", "1;34m"),
								("boldPurple", "1;35m"),
								("boldCyan", "1;36m"),
								("boldWhite", "1;37m"),
								("underlineBlack", "4;30m"),
								("underlineRed", "4;31m"),
								("underlineGreen", "4;32m"),
								("underlineYellow", "4;33m"),
								("underlineBlue", "4;34m"),
								("underlinePurple", "4;35m"),
								("underlineCyan", "4;36m"),
								("underlineWhite", "4;37m"),
								("highBlack", "0;90m"),
								("highRed", "0;91m"),
								("highGreen", "0;92m"),
								("highYellow", "0;93m"),
								("highBlue", "0;94m"),
								("highPurple", "0;95m"),
								("highCyan", "0;96m"),
								("highWhite", "0;97m"),
								("highBoldBlack", "1;90m"),
								("highBoldRed", "1;91m"),
								("highBoldGreen", "1;92m"),
								("highBoldYellow", "1;93m"),
								("highBoldBlue", "1;94m"),
								("highBoldPurple", "1;95m"),
								("highBoldCyan", "1;96m"),
								("highBoldWhite", "1;97m"))

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
AnsiEscapeCodes = foundations.dataStructures.OrderedStructure()

def _setAnsiEscapeCodes():
	"""
	Injects *ANSI* escape codes into :class:`AnsiEscapeCodes` class.
	"""

	AnsiEscapeCodes["reset"] = "\033[0m"

	for foregroundCodeName, foregroundCode in FOREGROUND_ANSI_ESCAPE_CODES:
		AnsiEscapeCodes[foregroundCodeName] = "\033[{0}".format(foregroundCode)

	for backgroundCodeName, backgroundCode in BACKGROUND_ANSI_ESCAPE_CODES:
		AnsiEscapeCodes[backgroundCodeName] = "\033[{0}".format(backgroundCode)

	for backgroundCodeName, backgroundCode in BACKGROUND_ANSI_ESCAPE_CODES:
		for foregroundCodeName, foregroundCode in FOREGROUND_ANSI_ESCAPE_CODES:
			AnsiEscapeCodes["{0}{1}".format(foregroundCodeName,
											"{0}{1}".format(backgroundCodeName[0].upper(),
															backgroundCodeName[1:]))] = "\033[{0}\033[{1}".format(
				foregroundCode, backgroundCode)

_setAnsiEscapeCodes()

def colorize(text, color):
	"""
	Colorizes given text using given color.

	:param text: Text to colorize.
	:type text: unicode
	:param color: *ANSI* escape code name.
	:type color: unicode
	:return: Colorized text.
	:rtype: unicode
	"""

	escapeCode = getattr(AnsiEscapeCodes, color, None)
	if escapeCode is None:
		raise foundations.exceptions.AnsiEscapeCodeExistsError(
			"'{0}' | '{1}' 'ANSI' escape code name doesn't exists!".format(
				inspect.getmodulename(__file__), color))

	return "{0}{1}{2}".format(escapeCode, text, AnsiEscapeCodes.reset)