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

__all__ = ["LOGGER", "RESOURCES_DIRECTORY", "DEFAULT_UI_FILE", "center_widget_on_screen", "QWidget_factory"]

LOGGER = foundations.verbose.install_logger()

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
DEFAULT_UI_FILE = os.path.join(RESOURCES_DIRECTORY, "QWidget.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def center_widget_on_screen(widget, screen=None):
	"""
	Centers given Widget on the screen.

	:param widget: Current Widget.
	:type widget: QWidget
	:param screen: Screen used for centering.
	:type screen: int
	:return: Definition success.
	:rtype: bool
	"""

	screen = screen and screen or QApplication.desktop().primaryScreen()
	desktop_width = QApplication.desktop().screenGeometry(screen).width()
	desktop_height = QApplication.desktop().screenGeometry(screen).height()
	widget.move(desktop_width / 2 - widget.sizeHint().width() / 2, desktop_height / 2 - widget.sizeHint().height() / 2)
	return True

def QWidget_factory(ui_file=None, *args, **kwargs):
	"""
	Defines a class factory creating `QWidget <http://doc.qt.nokia.com/qwidget.html>`_ classes
	using given ui file.

	:param ui_file: Ui file.
	:type ui_file: unicode
	:param \*args: Arguments.
	:type \*args: \*
	:param \*\*kwargs: Keywords arguments.
	:type \*\*kwargs: \*\*
	:return: QWidget class.
	:rtype: QWidget
	"""

	file = ui_file or DEFAULT_UI_FILE
	if not foundations.common.path_exists(file):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' ui file doesn't exists!".format(__name__, file))

	Form, Base = uic.loadUiType(file)

	class QWidget(Form, Base):
		"""
		Derives from :def:`QWidget_factory` class factory definition.
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

			self.__ui_file = file

			self.__geometry = None

			self.setupUi(self)

		#**************************************************************************************************************
		#***	Attributes properties.
		#**************************************************************************************************************
		@property
		def ui_file(self):
			"""
			Property for **self.__ui_file** attribute.

			:return: self.__ui_file.
			:rtype: unicode
			"""

			return self.__ui_file

		@ui_file.setter
		@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
		def ui_file(self, value):
			"""
			Setter for **self.__ui_file** attribute.

			:param value: Attribute value.
			:type value: unicode
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(
			self.__class__.__name__, "ui_file"))

		@ui_file.deleter
		@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
		def ui_file(self):
			"""
			Deleter for **self.__ui_file** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(
			self.__class__.__name__, "ui_file"))

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
				center_widget_on_screen(self)

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
