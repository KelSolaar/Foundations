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
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
from foundations.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "RESOURCES_DIRECTORY", "DEFAULT_UI_FILE", "centerWidgetOnScreen", "QWidgetFactory"]

LOGGER = logging.getLogger(Constants.logger)

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
DEFAULT_UI_FILE = os.path.join(RESOURCES_DIRECTORY, "QWidget.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def centerWidgetOnScreen(widget, screen=None):
	"""
	This definition centers the given Widget on the screen.

	:param widget: Current Widget. ( QWidget )
	:param screen: Screen used for centering. ( Integer )
	:return: Definition success. ( Boolean )
	"""

	screen = screen and screen or QApplication.desktop().primaryScreen()
	desktopWidth = QApplication.desktop().screenGeometry(screen).width()
	desktopHeight = QApplication.desktop().screenGeometry(screen).height()
	widget.move(desktopWidth / 2 - widget.width() / 2, desktopHeight / 2 - widget.height() / 2)
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def QWidgetFactory(uiFile=None, *args, **kwargs):
	"""
	This definition is a class factory creating `QWidget <http://doc.qt.nokia.com/qwidget.html>`_ classes
	using given ui file.

	:param uiFile: Ui file. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: QWidget class. ( QWidget )
	"""

	file = uiFile or DEFAULT_UI_FILE
	if not foundations.common.pathExists(file):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' ui file doesn't exists!".format(
		inspect.getmodulename(__file__), file))

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
			:param \*\*kwargs: Keywords arguments. ( \*\* )
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
			This method is the property for **self.__uiFile** attribute.
	
			:return: self.__uiFile. ( String )
			"""

			return self.__uiFile

		@uiFile.setter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def uiFile(self, value):
			"""
			This method is the setter method for **self.__uiFile** attribute.
	
			:param value: Attribute value. ( String )
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(
			self.__class__.__name__, "uiFile"))

		@uiFile.deleter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def uiFile(self):
			"""
			This method is the deleter method for **self.__uiFile** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(
			self.__class__.__name__, "uiFile"))

		#******************************************************************************************************************
		#***	Class methods.
		#******************************************************************************************************************
		@core.executionTrace
		def show(self):
			"""
			This method reimplements the :meth:`QWidget.show` method.
			"""

			wasHidden = not self.isVisible()

			super(QWidget, self).show()

			if not wasHidden:
				return

			if self.__geometry is not None:
				self.restoreGeometry(self.__geometry)
			else:
				centerWidgetOnScreen(self)

		@core.executionTrace
		def closeEvent(self, event):
			"""
			This method reimplements the :meth:`QWidget.closeEvent` method.
	
			:param event: QEvent. ( QEvent )
			"""

			self.__geometry = self.saveGeometry()
			event.accept()

	return QWidget
