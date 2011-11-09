#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Foundations** package ui common utilities objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import logging
import os
from PyQt4 import uic
from PyQt4.QtGui import QWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "RESOURCES_DIRECTORY", "DEFAULT_UI_FILE", "QWidgetFactory"]

LOGGER = logging.getLogger(Constants.logger)

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
DEFAULT_UI_FILE = os.path.join(RESOURCES_DIRECTORY, "QWidget.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def QWidgetFactory(uiFile=None, *args, **kwargs):
	"""
	This definition is a class factory creating `QWidget <http://doc.qt.nokia.com/4.7/qwidget.html>`_ classes using given ui file.

	:param uiFile: Ui file. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \* )
	:return: QWidget class. ( QWidget )
	"""

	file = uiFile or DEFAULT_UI_FILE
	if not os.path.exists(file):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' ui file doesn't exists!".format(inspect.getmodulename(__file__), file))

	Form, Base = uic.loadUiType(file)

	class QWidget(Form, Base):
		"""
		This class is built by the :def:`QWidgetFactory` definition.
		"""

		@core.executionTrace
		def __init__(self, *args, **kwargs):
			"""
			This method initializes the class.
	
			:param \*args: Arguments. ( \* )
			:param \*\*kwargs: Keywords arguments. ( \* )
			"""

			LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

			super(QWidget, self).__init__(*args, **kwargs)

			self.__uiFile = file

			self.setupUi(self)

		#**************************************************************************************************************
		#***	Attributes properties.
		#**************************************************************************************************************
		@property
		def uiFile(self):
			"""
			This method is the property for **self.__uiFile** attribute.
	
			:return: self.__uiFile. ( String )
			"""

			return self.__uiFile

		@uiFile.setter
		@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
		def uiFile(self, value):
			"""
			This method is the setter method for **self.__uiFile** attribute.
	
			:param value: Attribute value. ( String )
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiFile"))

		@uiFile.deleter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def uiFile(self):
			"""
			This method is the deleter method for **self.__uiFile** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiFile"))

	return QWidget
