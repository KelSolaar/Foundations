#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Foundations** package ui common utilities objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import os
from PyQt4 import uic
from PyQt4.QtGui import QApplication

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
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

__all__ = ["LOGGER", "RESOURCES_DIRECTORY", "DEFAULT_UI_FILE", "centerWidgetOnScreen", "QWidgetFactory"]

LOGGER = foundations.verbose.installLogger()

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
DEFAULT_UI_FILE = os.path.join(RESOURCES_DIRECTORY, "QWidget.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def centerWidgetOnScreen(widget, screen=None):
	"""
	Centers the given Widget on the screen.

	:param widget: Current Widget.
	:type widget: QWidget
	:param screen: Screen used for centering.
	:type screen: int
	:return: Definition success.
	:rtype: bool
	"""

	screen = screen and screen or QApplication.desktop().primaryScreen()
	desktopWidth = QApplication.desktop().screenGeometry(screen).width()
	desktopHeight = QApplication.desktop().screenGeometry(screen).height()
	widget.move(desktopWidth / 2 - widget.sizeHint().width() / 2, desktopHeight / 2 - widget.sizeHint().height() / 2)
	return True

def QWidgetFactory(uiFile=None, *args, **kwargs):
	"""
	Defines a class factory creating `QWidget <http://doc.qt.nokia.com/qwidget.html>`_ classes
	using given ui file.

	:param uiFile: Ui file.
	:type uiFile: unicode
	:param \*args: Arguments.
	:type \*args: \*
	:param \*\*kwargs: Keywords arguments.
	:type \*\*kwargs: \*\*
	:return: QWidget class.
	:rtype: QWidget
	"""

	file = uiFile or DEFAULT_UI_FILE
	if not foundations.common.pathExists(file):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' ui file doesn't exists!".format(__name__, file))

	Form, Base = uic.loadUiType(file)

	class QWidget(Form, Base):
		"""
		Derives from :def:`QWidgetFactory` class factory definition.
		"""

		def __init__(self, *args, **kwargs):
			"""
			Initializes the class.

			:param \*args: Arguments.
			:type \*args: \*
			:param \*\*kwargs: Keywords arguments.
			:type \*\*kwargs: \*\*
			"""

			LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

			super(QWidget, self).__init__(*args, **kwargs)

			self.__uiFile = file

			self.__geometry = None

			self.setupUi(self)

		#**************************************************************************************************************
		#***	Attributes properties.
		#**************************************************************************************************************
		@property
		def uiFile(self):
			"""
			Property for **self.__uiFile** attribute.

			:return: self.__uiFile.
			:rtype: unicode
			"""

			return self.__uiFile

		@uiFile.setter
		@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
		def uiFile(self, value):
			"""
			Setter for **self.__uiFile** attribute.

			:param value: Attribute value.
			:type value: unicode
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(
			self.__class__.__name__, "uiFile"))

		@uiFile.deleter
		@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
		def uiFile(self):
			"""
			Deleter for **self.__uiFile** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(
			self.__class__.__name__, "uiFile"))

		#******************************************************************************************************************
		#***	Class methods.
		#******************************************************************************************************************
		def show(self, setGeometry=True):
			"""
			Reimplements the :meth:`QWidget.show` method.

			:param setGeometry: Set geometry.
			:type setGeometry: bool
			"""

			if not setGeometry:
				super(QWidget, self).show()
				return

			wasHidden = not self.isVisible()

			if self.__geometry is None and wasHidden:
				centerWidgetOnScreen(self)

			super(QWidget, self).show()

			if self.__geometry is not None and wasHidden:
				self.restoreGeometry(self.__geometry)

		def closeEvent(self, event):
			"""
			Reimplements the :meth:`QWidget.closeEvent` method.

			:param event: QEvent.
			:type event: QEvent
			"""

			self.__geometry = self.saveGeometry()
			event.accept()

	return QWidget
