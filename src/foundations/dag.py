#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**dag.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines various dag related class.

**Others:**
	Portions of the code from DAG by Simon Wittber: http://pypi.python.org/pypi/DAG/ and PyQt4 Model View Programming Tutorials by Yasin Uludag: http://www.yasinuludag.com/blog/?p=98
"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from collections import OrderedDict

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
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

__all__ = ["LOGGER", "Attribute", "AbstractNode", "AbstractCompositeNode"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Attribute(core.Structure):
	"""
	This class represents a storage object for the :class:`AbstractNode` class attributes.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: value, image. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class AbstractNode(core.Structure):
	"""
	| This class defines the base node class.
	| Although it can be instancied directly that class is meant to be subclassed.
	
	:note: This class doesn't provide compositing capabilities,class:`AbstractCompositeNode` class must be used for that purpose.
	"""

	__family = "Abstract"
	"""Node family. ( String )"""

	__instanceId = 1
	"""Node id: Defines the next node instance identity number. ( Integer )"""

	__nodesInstances = {}
	"""Node instances: Each node, once instanced is stored in this attribute. ( Dictionary )"""

	@core.executionTrace
	def __new__(self, *args, **kwargs):
		"""
		This method is the constructor of the class.
		
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		:return: Class instance. ( AbstractNode )
		"""

		instance = super(AbstractNode, self).__new__(self)
		instance.__identity = AbstractNode._AbstractNode__instanceId
		AbstractNode._AbstractNode__nodesInstances[instance.__identity] = instance
		AbstractNode._AbstractNode__instanceId += 1
		return instance

	@core.executionTrace
	def __init__(self, name=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))
		core.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__name = None
		self.__name = name or self.__getDefaultNodeName()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def family(self):
		"""
		This method is the property for **self.__family** attribute.

		:return: self.__family. ( String )
		"""

		return getattr(self, "_{0}__{1}".format(self.__class__.__name__, "family"))

	@family.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def family(self, value):
		"""
		This method is the setter method for **self.__family** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "family"))

	@family.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def family(self):
		"""
		This method is the deleter method for **self.__family** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "family"))

	@property
	def identity(self):
		"""
		This method is the property for **self.__identity** attribute.

		:return: self.__identity. ( String )
		"""

		return self.__identity

	@identity.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def identity(self, value):
		"""
		This method is the setter method for **self.__identity** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "identity"))

	@identity.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def identity(self):
		"""
		This method is the deleter method for **self.__identity** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "identity"))

	@property
	def nodesInstances(self):
		"""
		This method is the property for **self.__nodesInstances** attribute.

		:return: self.__nodesInstances. ( WeakValueDictionary )
		"""

		return self.__nodesInstances

	@nodesInstances.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def nodesInstances(self, value):
		"""
		This method is the setter method for **self.__nodesInstances** attribute.

		:param value: Attribute value. ( WeakValueDictionary )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "nodesInstances"))

	@nodesInstances.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def nodesInstances(self):
		"""
		This method is the deleter method for **self.__nodesInstances** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "nodesInstances"))

	@property
	def name(self):
		"""
		This method is the property for **self.__name** attribute.

		:return: self.__name. ( String )
		"""

		return self.__name

	@name.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self, value):
		"""
		This method is the setter method for **self.__name** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode, QVariant), "'{0}' attribute: '{1}' type is not 'str' or 'unicode' or 'QVariant'!".format("name", value)
		self.__name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		This method is the deleter method for **self.__name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "name"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __repr__(self):
		"""
		This method reimplements the :meth:`core.Structure.__repr__` method.
		
		:return: Object representation. ( String )
		"""

		return "<{0} object at {1}>".format(self.__class__.__name__, hex(id(self)))

	@core.executionTrace
	def __getDefaultNodeName(self):
		"""
		This method gets the default node name.
		
		:return: Node name. ( String )
		"""

		return "{0}{1}".format(self.family, self.__identity)

	@classmethod
	@core.executionTrace
	def getNodeByIdentity(self, identity):
		"""
		This method returns the node with provided identity.
	
		:param identity: Node identity. ( Integer )
		:return: Node. ( AbstractNode )
		"""

		if identity > len(self.__nodesInstances):
			return
		return self.__nodesInstances[identity]

	@core.executionTrace
	def listAttributes(self):
		"""
		This method returns the node attributes names.
	
		:return: Attributes names. ( List )
		"""

		return [attribute for attribute, value in self.items() if isinstance(value, Attribute)]

	@core.executionTrace
	def getAttributes(self):
		"""
		This method returns the node attributes.
	
		:return: Attributes. ( List )
		"""

		return [attribute for attribute in self.values() if isinstance(attribute, Attribute)]

	@core.executionTrace
	def attributeExists(self, name):
		"""
		This method returns if provided attribute exists in the node.
	
		:param name: Attribute name. ( String )
		:return: Attribute exists. ( Boolean )
		"""

		if name in self.keys():
			if isinstance(self[name], Attribute):
				return True
		return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.NodeAttributeTypeError)
	def addAttribute(self, name, value):
		"""
		This method adds provided attribute to the node.
	
		:param name: Attribute name. ( String )
		:param value: Attribute value. ( Attribute )
		:return: Method success. ( Boolean )
		"""

		if not isinstance(value, Attribute):
			raise foundations.exceptions.NodeAttributeTypeError("Node attribute value must be a '{0}' class instance!".format(Attribute.__class__.__name__))

		if self.attributeExists(name):
			raise foundations.exceptions.NodeAttributeExistsError("Node attribute '{0}' already exists!".format(name))

		self[name] = value
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.NodeAttributeExistsError)
	def removeAttribute(self, name):
		"""
		This method removes provided attribute from the node.
	
		:param name: Attribute name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not self.attributeExists(name):
			raise foundations.exceptions.NodeAttributeExistsError("Node attribute '{0}' doesn't exists!".format(name))

		del self[name]
		return True

class AbstractCompositeNode(AbstractNode):
	"""
	This class provides the base class object used by other nodes.
	"""

	__family = "AbstractComposite"

	@core.executionTrace
	def __init__(self, name=None, parent=None, children=None, **kwargs):
		"""
		This method initializes the class.

		:param parent: Node parent. ( AbstractCompositeNode / AbstractNode )
		:param name: Node name.  ( String )
		"""

#		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractNode.__init__(self, name, **kwargs)

		# --- Setting class attributes. ---
		self.__parent = None
		self.parent = parent
		self.__children = children or []

		parent and parent.addChild(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def parent(self):
		"""
		This method is the property for **self.__parent** attribute.

		:return: self.__parent. ( QObject )
		"""

		return self.__parent

	@parent.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parent(self, value):
		"""
		This method is the setter method for **self.__parent** attribute.

		:param value: Attribute value. ( QObject )
		"""

		if value:
			assert issubclass(value.__class__, AbstractNode), "'{0}' attribute: '{1}' is not a '{2}' subclass!".format("parent", value, AbstractNode.__class__.__name__)
		self.__parent = value

	@parent.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parent(self):
		"""
		This method is the deleter method for **self.__parent** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "name"))

	@property
	def children(self):
		"""
		This method is the property for **self.__children** attribute.

		:return: self.__children. ( QObject )
		"""

		return self.__children

	@children.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def children(self, value):
		"""
		This method is the setter method for **self.__children** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "children"))

	@children.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def children(self):
		"""
		This method is the deleter method for **self.__children** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "children"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def addChild(self, child):
		self.__children.append(child)

	@core.executionTrace
	def insertChild(self, index, child):
		if index < 0 or index > len(self.__children):
			return

		self.__children.insert(index, child)
		child.__parent = self
		return True

	@core.executionTrace
	def removeChild(self, index):
		if index < 0 or index > len(self.__children):
			return

		child = self.__children.pop(index)
		child.__parent = None
		return True

	@core.executionTrace
	def child(self, index):
		return self.__children[index]

	@core.executionTrace
	def childrenCount(self):
		return len(self.__children)

	@core.executionTrace
	def row(self):
		if self.__parent is not None:
			return self.__parent.children.index(self)

	@core.executionTrace
	def listNode(self, tabLevel= -1):
		output = ""
		tabLevel += 1
		for i in range(tabLevel):
			output += "\t"
		output += "|----'{}'\n".format(self.name)
		for child in self.__children:
			output += child.listNode(tabLevel)
		tabLevel -= 1
		return output

if __name__ == "__main__":
	class DefaultNode(AbstractCompositeNode):
		__family = "Default"

		@core.executionTrace
		def __init__(self, name=None, parent=None, **kwargs):
			AbstractCompositeNode.__init__(self, name, parent, **kwargs)

	class TemplateNode(AbstractCompositeNode):
		__family = "Template"

		@core.executionTrace
		def __init__(self, name=None, parent=None, **kwargs):
			AbstractCompositeNode.__init__(self, name, parent, **kwargs)

	class SoftwareNode(AbstractCompositeNode):
		__family = "Software"

		@core.executionTrace
		def __init__(self, name=None, parent=None, **kwargs):
			AbstractCompositeNode.__init__(self, name, parent, **kwargs)

	class CollectionNode(AbstractCompositeNode):
		__family = "Collection"

		@core.executionTrace
		def __init__(self, name=None, parent=None, **kwargs):
			AbstractCompositeNode.__init__(self, name, parent, **kwargs)

	rootNode = AbstractCompositeNode(name="InvisibleRootNode", toto=Attribute())
	factoryCollection = CollectionNode(name="Factory", parent=rootNode)
	mayaSoftware = SoftwareNode(name="Maya", parent=factoryCollection)
	mayaMRStandard = TemplateNode(parent=mayaSoftware, release="1.0.1", software="Maya")
	mayaVRayStandard = TemplateNode(name="Maya VRay Standard", parent=mayaSoftware, release="1.8.1", software="Maya")
	softimageSoftware = SoftwareNode(name="Softimage", parent=factoryCollection)
	softimageMRStandard = TemplateNode(name="Softimage MR Standard", parent=softimageSoftware, release="1.2.0", software="Softimage")
	softimageVRayStandard = TemplateNode(name="Softimage VRay Standard", parent=softimageSoftware, release="1.5.0")

	print rootNode.listAttributes()
#	print rootNode.identity
#	print softimageVRayStandard.identity
#	print AbstractNode.getNodeByIdentity(1)
#	print softimageVRayStandard.keys()

	userCollection = CollectionNode(name="User", parent=rootNode)
	maxSoftware = TemplateNode(name="3dsMax", parent=userCollection)
	maxMRStandard = TemplateNode(name="3dsMax MR Standard", parent=maxSoftware)

	from PyQt4.QtGui import *
	from PyQt4.QtCore import *
	import sys

	application = QApplication(sys.argv)
	class GraphModel(QAbstractItemModel):

		@core.executionTrace
		def __init__(self, parent=None, root=None, headers=None):
			QAbstractItemModel.__init__(self)
			self.__rootNode = root
			self.__headers = headers

		#***********************************************************************************************
		#***	Attributes properties.
		#***********************************************************************************************
		@property
		def headers(self):
			"""
			This method is the property for **self.__headers** attribute.
	
			:return: self.__headers. ( QObject )
			"""

			return self.__headers

		@headers.setter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def headers(self, value):
			"""
			This method is the setter method for **self.__headers** attribute.
	
			:param value: Attribute value. ( QObject )
			"""

			if value:
				assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format("headers", value)
			self.__headers = value

		@headers.deleter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def headers(self):
			"""
			This method is the deleter method for **self.__headers** attribute.
			"""

		#***********************************************************************************************
		#***	Class methods.
		#***********************************************************************************************
		@core.executionTrace
		def rowCount(self, parent):
			if not parent.isValid():
				parentNode = self.__rootNode
			else:
				parentNode = parent.internalPointer()
			return parentNode.childrenCount()

		@core.executionTrace
		def columnCount(self, parent):
			return len(self.__headers)

		@core.executionTrace
		def data(self, index, role):
			if not index.isValid():
				return

			node = index.internalPointer()
			if role == Qt.DisplayRole or role == Qt.EditRole:
				if index.column() == 0:
					return node.name
				else:
					if index.column() < len(self.__headers):
						return node.get(self.__headers[self.__headers.keys()[index.column()]], None)

			if role == Qt.DecorationRole:
				if index.column() == 0:
					family = node.family

					if family == "":
						return QIcon(QPixmap(""))

		@core.executionTrace
		def setData(self, index, value, role=Qt.EditRole):
			if index.isValid():
				if role == Qt.EditRole:
					node = index.internalPointer()
					node.name = value
					self.dataChanged.emit(index, index)
					return True

		@core.executionTrace
		def headerData(self, section, orientation, role):
			if role == Qt.DisplayRole:
				if orientation == Qt.Horizontal:
					if section < len(self.__headers):
						return self.__headers.keys()[section]

		@core.executionTrace
		def flags(self, index):
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

		@core.executionTrace
		def parent(self, index):
			node = self.getNode(index)
			parentNode = node.parent
			if parentNode == self.__rootNode:
				return QModelIndex()
			return self.createIndex(parentNode.row(), 0, parentNode)

		@core.executionTrace
		def index(self, row, column, parent):
			parentNode = self.getNode(parent)
			childItem = parentNode.child(row)
			if childItem:
				return self.createIndex(row, column, childItem)
			else:
				return QModelIndex()

		@core.executionTrace
		def getNode(self, index):
			if index.isValid():
				node = index.internalPointer()
				if node:
					return node
			return self.__rootNode

		@core.executionTrace
		def insertRows(self, position, rows, parent=QModelIndex()):
			parentNode = self.getNode(parent)
			self.beginInsertRows(parent, position, position + rows - 1)
			for row in range(rows):
				childNode = DefaultNode()
				success = parentNode.insertChild(position, childNode)
			self.endInsertRows()
			return success

		@core.executionTrace
		def removeRows(self, position, rows, parent=QModelIndex()):
			parentNode = self.getNode(parent)
			self.beginRemoveRows(parent, position, position + rows - 1)
			success = True
			for row in range(rows):
				success *= parentNode.removeChild(position)
			self.endRemoveRows()
			return success
	model = GraphModel(root=rootNode, headers=OrderedDict([("Templates", "templates"), ("Version", "release"), ("Package", "software")]))

#	print rootNode.listNode()

	listView = QListView()
	listView.setModel(model)

	comboBox = QComboBox()
	comboBox.setModel(model)

	tableView = QTableView()
	tableView.setModel(model)

	treeView = QTreeView()
	treeView.setModel(model)
	treeView.expandAll()
	for column in range(len(treeView.model().headers)):
		treeView.resizeColumnToContents(column)
	treeView.resize(640, 480)

	listView.show()
	comboBox.show()
	tableView.show()
	treeView.show()

	sys.exit(application.exec_())

