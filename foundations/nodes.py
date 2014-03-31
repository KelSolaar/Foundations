#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines various nodes and dag related classes.

**Others:**
	Portions of the code from DAG by Simon Wittber: http://pypi.python.org/pypi/DAG/ and
	PyQt4 Model View Programming Tutorials by Yasin Uludag: http://www.yasinuludag.com/blog/?p=98
"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re
import weakref

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.exceptions
import foundations.verbose
import foundations.walkers

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Attribute", "AbstractNode", "AbstractCompositeNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Attribute(foundations.dataStructures.Structure):
	"""
	Defines a storage object for the :class:`AbstractNode` class attributes.
	"""

	def __init__(self, name=None, value=None, **kwargs):
		"""
		Initializes the class.

		Usage::

			>>> attribute = Attribute(name="My Attribute", value="My Value")
			>>> attribute.name
			u'My Attribute'
			>>> attribute["name"]
			u'My Attribute'
			>>> attribute.value
			u'My Value'
			>>> attribute["value"]
			u'My Value'

		:param name: Attribute name.
		:type name: unicode
		:param value: Attribute value.
		:type value: object
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__name = None
		self.name = name
		self.__value = None
		self.value = value

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def name(self):
		"""
		Property for **self.__name** attribute.

		:return: Value.
		:rtype: unicode
		"""

		return self.__name

	@name.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def name(self, value):
		"""
		Setter for **self.__name** attribute.

		:param name: Attribute name.
		:type name: unicode
		"""

		self.__name = value

	@name.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		Deleter for **name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "name"))

	@property
	def value(self):
		"""
		Property for **self.__value** attribute.

		:return: Value.
		:rtype: object
		"""

		return self.__value

	@value.setter
	def value(self, value):
		"""
		Setter for **self.__value** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		self.__value = value

	@value.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def value(self):
		"""
		Deleter for **value** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "value"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __hash__(self):
		"""
		Reimplements the :meth:`foundations.dataStructures.Structure.__hash__` method.
		
		:return: Object hash.
		:rtype: int
		
		:note: :class:`foundations.dataStructures.Structure` inherits from **dict** and
		should not be made hashable because of its mutability, however considering the fact the id
		is used as the hash value, making the object hashable should be fairly safe. 
		"""

		return hash(id(self))

 	def __repr__(self):
 		"""
 		Reimplements the :meth:`foundations.dataStructures.Structure.__repr__` method.

 		:return: Object representation.
 		:rtype: unicode
 		"""

 		return "<{0} object at {1}>".format(self.__class__.__name__, hex(id(self)))

class AbstractNode(foundations.dataStructures.Structure):
	"""
	| Defines the base Node class.
	| Although it can be instancied directly that class is meant to be subclassed.
	
	:note: Doesn't provide compositing capabilities, :class:`AbstractCompositeNode` class must be used for that purpose.
	"""

	__family = "Abstract"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	__instanceId = 1
	"""
	:param __instanceId: Node id.
	:type __instanceId: int
	"""

	__nodesInstances = weakref.WeakValueDictionary()
	"""
	:param __nodesInstances: Nodes instances.
	:type __nodesInstances: dict
	"""

	def __new__(cls, *args, **kwargs):
		"""
		Constructor of the class.
		
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Class instance.
		:rtype: AbstractNode
		"""

		instance = super(AbstractNode, cls).__new__(cls)

		instance._AbstractNode__identity = AbstractNode._AbstractNode__instanceId

		AbstractNode._AbstractNode__nodesInstances[instance.__identity] = instance
		AbstractNode._AbstractNode__instanceId += 1
		return instance

	def __init__(self, name=None, **kwargs):
		"""
		Initializes the class.

		Usage::

			>>> nodeA = AbstractNode("MyNodeA")
			>>> nodeA.identity
			1
			>>> nodeB = AbstractNode()
			>>> nodeB.name
			u'Abstract2'
			>>> nodeB.identity
			2

		:param name: Node name.
		:type name: unicode
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

		# --- Setting class attributes. ---
		self.__name = None
		self.name = name or self.__getDefaultNodeName()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def family(self):
		"""
		Property for **self.__family** attribute.

		:return: self.__family.
		:rtype: unicode
		"""

		return getattr(self, "_{0}__{1}".format(self.__class__.__name__, "family"))

	@family.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def family(self, value):
		"""
		Setter for **self.__family** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "family"))

	@family.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def family(self):
		"""
		Deleter for **self.__family** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "family"))

	@property
	def nodesInstances(self):
		"""
		Property for **self.__nodesInstances** attribute.

		:return: self.__nodesInstances.
		:rtype: WeakValueDictionary
		"""

		return self.__nodesInstances

	@nodesInstances.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def nodesInstances(self, value):
		"""
		Setter for **self.__nodesInstances** attribute.

		:param value: Attribute value.
		:type value: WeakValueDictionary
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "nodesInstances"))

	@nodesInstances.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def nodesInstances(self):
		"""
		Deleter for **self.__nodesInstances** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "nodesInstances"))

	@property
	def identity(self):
		"""
		Property for **self.__identity** attribute.

		:return: self.__identity.
		:rtype: unicode
		"""

		return self.__identity

	@identity.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def identity(self, value):
		"""
		Setter for **self.__identity** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "identity"))

	@identity.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def identity(self):
		"""
		Deleter for **self.__identity** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "identity"))

	@property
	def name(self):
		"""
		Property for **self.__name** attribute.

		:return: self.__name.
		:rtype: unicode
		"""

		return self.__name

	@name.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def name(self, value):
		"""
		Setter for **self.__name** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("name", value)
		self.__name = value

	@name.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		Deleter for **self.__name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "name"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __repr__(self):
		"""
		Reimplements the :meth:`foundations.dataStructures.Structure.__repr__` method.
		
		:return: Object representation.
		:rtype: unicode
		"""

		return "<{0} object at {1}>".format(self.__class__.__name__, hex(id(self)))

	def __hash__(self):
		"""
		Reimplements the :meth:`foundations.dataStructures.Structure.__hash__` method.
		
		:return: Object hash.
		:rtype: int
		
		:note: :class:`foundations.dataStructures.Structure` inherits from **dict** and
		should not be made hashable because of its mutability, however considering the fact the id
		is used as the hash value, making the object hashable should be fairly safe. 
		"""

		return hash(id(self))

	def __getDefaultNodeName(self):
		"""
		Gets the default Node name.
		
		:return: Node name.
		:rtype: unicode
		"""

		return "{0}{1}".format(self.family, self.__identity)

	@classmethod
	def getNodeByIdentity(cls, identity):
		"""
		Returns the Node with given identity.
	
		Usage::

			>>> nodeA = AbstractNode("MyNodeA")
			>>> AbstractNode.getNodeByIdentity(1)
			<AbstractNode object at 0x101043a80>

		:param identity: Node identity.
		:type identity: int
		:return: Node.
		:rtype: AbstractNode

		:note: Nodes identities are starting from '1' to nodes instances count.
		"""

		return cls.__nodesInstances.get(identity, None)

	def listAttributes(self):
		"""
		Returns the Node attributes names.

		Usage::

			>>>	nodeA = AbstractNode("MyNodeA", attributeA=Attribute(), attributeB=Attribute())
			>>> nodeA.listAttributes()
			['attributeB', 'attributeA']
			
		:return: Attributes names.
		:rtype: list
		"""

		return [attribute for attribute, value in self.iteritems() if issubclass(value.__class__, Attribute)]

	def getAttributes(self):
		"""
		Returns the Node attributes.

		Usage::

			>>>	nodeA = AbstractNode("MyNodeA", attributeA=Attribute(value="A"), attributeB=Attribute(value="B"))
			>>> nodeA.getAttributes()
			[<Attribute object at 0x7fa471d3b5e0>, <Attribute object at 0x101e6c4a0>]

		:return: Attributes.
		:rtype: list
		"""

		return [attribute for attribute in self.itervalues() if issubclass(attribute.__class__, Attribute)]

	def attributeExists(self, name):
		"""
		Returns if given attribute exists in the node.

		Usage::

			>>>	nodeA = AbstractNode("MyNodeA", attributeA=Attribute(), attributeB=Attribute())
			>>> nodeA.attributeExists("attributeA")
			True
			>>> nodeA.attributeExists("attributeC")
			False

		:param name: Attribute name.
		:type name: unicode
		:return: Attribute exists.
		:rtype: bool
		"""

		if name in self:
			if issubclass(self[name].__class__, Attribute):
				return True
		return False

	@foundations.exceptions.handleExceptions(foundations.exceptions.NodeAttributeTypeError)
	def addAttribute(self, name, value):
		"""
		Adds given attribute to the node.

		Usage::

			>>>	nodeA = AbstractNode()
			>>> nodeA.addAttribute("attributeA", Attribute())
			True
			>>> nodeA.listAttributes()
			[u'attributeA']
	
		:param name: Attribute name.
		:type name: unicode
		:param value: Attribute value.
		:type value: Attribute
		:return: Method success.
		:rtype: bool
		"""

		if not issubclass(value.__class__, Attribute):
			raise foundations.exceptions.NodeAttributeTypeError(
			"Node attribute value must be a '{0}' class instance!".format(Attribute.__class__.__name__))

		if self.attributeExists(name):
			raise foundations.exceptions.NodeAttributeExistsError("Node attribute '{0}' already exists!".format(name))

		self[name] = value
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.NodeAttributeExistsError)
	def removeAttribute(self, name):
		"""
		Removes given attribute from the node.

		Usage::

			>>>	nodeA = AbstractNode("MyNodeA", attributeA=Attribute(), attributeB=Attribute())
			>>> nodeA.removeAttribute("attributeA")
			True
			>>> nodeA.listAttributes()
			['attributeB']

		:param name: Attribute name.
		:type name: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not self.attributeExists(name):
			raise foundations.exceptions.NodeAttributeExistsError("Node attribute '{0}' doesn't exists!".format(name))

		del self[name]
		return True

class AbstractCompositeNode(AbstractNode):
	"""
	| Defines the base composite Node class.
	| It provides compositing capabilities allowing the assembly of graphs and various trees structures.
	"""

	__family = "AbstractComposite"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self, name=None, parent=None, children=None, **kwargs):
		"""
		Initializes the class.

		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: AbstractNode or AbstractCompositeNode
		:param children: Children.
		:type children: list
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		
		:note: :data:`pickle.HIGHEST_PROTOCOL` must be used to pickle :class:`foundations.nodes.AbstractCompositeNode` class.
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractNode.__init__(self, name, **kwargs)

		# --- Setting class attributes. ---
		self.__parent = None
		self.parent = parent
		self.__children = None
		self.children = children or []

		parent and parent.addChild(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def parent(self):
		"""
		Property for **self.__parent** attribute.

		:return: self.__parent.
		:rtype: AbstractNode or AbstractCompositeNode
		"""

		return self.__parent

	@parent.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def parent(self, value):
		"""
		Setter for **self.__parent** attribute.

		:param value: Attribute value.
		:type value: AbstractNode or AbstractCompositeNode
		"""

		if value is not None:
			assert issubclass(value.__class__, AbstractNode), "'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
			"parent", value, AbstractNode.__class__.__name__)
		self.__parent = value

	@parent.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def parent(self):
		"""
		Deleter for **self.__parent** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "name"))

	@property
	def children(self):
		"""
		Property for **self.__children** attribute.

		:return: self.__children.
		:rtype: list
		"""

		return self.__children

	@children.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def children(self, value):
		"""
		Setter for **self.__children** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("children", value)
			for element in value:
				assert issubclass(element.__class__, AbstractNode), "'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
				"children", element, AbstractNode.__class__.__name__)
		self.__children = value

	@children.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def children(self):
		"""
		Deleter for **self.__children** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "children"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __eq__(self, object):
		"""
		Reimplements the :meth:`AbstractNode.__eq__` method.
		
		:param object: Comparing object.
		:type object: object
		:return: Equality.
		:rtype: bool
		"""

		if self is object:
			return True
		elif isinstance(object, AbstractCompositeNode):
			for childA, childB in zip(self.__children, object.children):
				return childA.identity == childB.identity
		else:
			return False

	def child(self, index):
		"""
		Returns the child associated with given index.

		Usage::

			>>> nodeB = AbstractCompositeNode("MyNodeB")
			>>> nodeC = AbstractCompositeNode("MyNodeC")
			>>> nodeA = AbstractCompositeNode("MyNodeA", children=[nodeB, nodeC])
			>>> nodeA.child(0)
			<AbstractCompositeNode object at 0x10107b6f0>
			>>> nodeA.child(0).name
			u'MyNodeB'

		:param index: Child index.
		:type index: int
		:return: Child node.
		:rtype: AbstractNode or AbstractCompositeNode or Object
		"""

		if not self.__children:
			return

		if index >= 0 and index < len(self.__children):
			return self.__children[index]

	def indexOf(self, child):
		"""
		Returns the given child index.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
			>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
			>>> nodeA.indexOf(nodeB)
			0
			>>> nodeA.indexOf(nodeC)
			1
	
		:param child: Child node.
		:type child: AbstractNode or AbstractCompositeNode or Object
		:return: Child index.
		:rtype: int
		"""

		for i, item in enumerate(self.__children):
			if child is item:
				return i

	def row(self):
		"""
		Returns the Node row.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
			>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
			>>> nodeB.row()
			0
			>>> nodeC.row()
			1	

		:return: Node row.
		:rtype: int
		"""

		if self.__parent:
			return self.__parent.indexOf(self)

	def addChild(self, child):
		"""
		Adds given child to the node.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB")
			>>> nodeA.addChild(nodeB)
			True
			>>> nodeA.children
			[<AbstractCompositeNode object at 0x10107afe0>]

		:param child: Child node.
		:type child: AbstractNode or AbstractCompositeNode or Object
		:return: Method success.
		:rtype: bool
		"""

		self.__children.append(child)
		child.parent = self
		return True

	def removeChild(self, index):
		"""
		Removes child at given index from the Node children.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
			>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
			>>> nodeA.removeChild(1)
			True
			>>> [child.name for child in nodeA.children]
			[u'MyNodeB']

		:param index: Node index.
		:type index: int
		:return: Removed child.
		:rtype: AbstractNode or AbstractCompositeNode or Object
		"""

		if index < 0 or index > len(self.__children):
			return

		child = self.__children.pop(index)
		child.parent = None
		return child

	def insertChild(self, child, index):
		"""
		Inserts given child at given index.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
			>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
			>>> nodeD = AbstractCompositeNode("MyNodeD")
			>>> nodeA.insertChild(nodeD, 1)
			True
			>>> [child.name for child in nodeA.children]
			[u'MyNodeB', u'MyNodeD', u'MyNodeC']

		:param child: Child node.
		:type child: AbstractNode or AbstractCompositeNode or Object
		:param index: Insertion index.
		:type index: int
		:return: Method success.
		:rtype: bool
		"""

		if index < 0 or index > len(self.__children):
			return False

		self.__children.insert(index, child)
		child.parent = self
		return child

	def hasChildren(self):
		"""
		Returns if the Node has children.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeA.hasChildren()
			False

		:return: Children count.
		:rtype: int
		"""

		return True if self.childrenCount() > 0 else False

	def childrenCount(self):
		"""
		Returns the children count.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
			>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
			>>> nodeA.childrenCount()
			2

		:return: Children count.
		:rtype: int
		"""

		return len(self.__children)

	def sortChildren(self, attribute=None, reverseOrder=False):
		"""
		Sorts the children using either the given attribute or the Node name.

		:param attribute: Attribute name used for sorting.
		:type attribute: unicode
		:param reverseOrder: Sort in reverse order.
		:type reverseOrder: bool
		:return: Method success.
		:rtype: bool
		"""

		sortedChildren = []
		if attribute:
			sortableChildren = []
			unsortableChildren = []
			for child in self.__children:
				if child.attributeExists(attribute):
					sortableChildren.append(child)
				else:
					unsortableChildren.append(child)
			sortedChildren = sorted(sortableChildren, key=lambda x: getattr(x, attribute).value, reverse=reverseOrder or False)
			sortedChildren.extend(unsortableChildren)
		else:
			sortedChildren = sorted(self.children, key=lambda x: (x.name), reverse=reverseOrder or False)

		self.__children = sortedChildren

		for child in self.__children:
			child.sortChildren(attribute, reverseOrder)

		return True

	def findChildren(self, pattern=r".*", flags=0, candidates=None):
		"""
		Finds the children matching the given patten.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
			>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
			>>> nodeA.findChildren("c", re.IGNORECASE)
			[<AbstractCompositeNode object at 0x101078040>]

		:param pattern: Matching pattern.
		:type pattern: unicode
		:param flags: Matching regex flags.
		:type flags: int
		:param candidates: Matching candidates.
		:type candidates: list
		:return: Matching children.
		:rtype: list
		"""

		if candidates is None:
			candidates = []

		for child in self.__children:
			if re.search(pattern, child.name, flags):
				child not in candidates and candidates.append(child)
			child.findChildren(pattern, flags, candidates)
		return candidates

	def findFamily(self, pattern=r".*", flags=0, node=None):
		"""
		Returns the Nodes from given family.
		
		:param pattern: Matching pattern.
		:type pattern: unicode
		:param flags: Matching regex flags.
		:type flags: int
		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or Object
		:return: Family nodes.
		:rtype: list
		"""

		return [node for node in foundations.walkers.nodesWalker(node or self) if re.search(pattern, node.family, flags)]

	def listNode(self, tabLevel= -1):
		"""
		Lists the current Node and its children.

		Usage::

			>>> nodeA = AbstractCompositeNode("MyNodeA")
			>>> nodeB = AbstractCompositeNode("MyNodeB", nodeA)
			>>> nodeC = AbstractCompositeNode("MyNodeC", nodeA)
			>>> print nodeA.listNode()
			|----'MyNodeA'
					|----'MyNodeB'
					|----'MyNodeC'

		:param tabLevel: Tab level.
		:type tabLevel: int
		:return: Node listing.
		:rtype: unicode
		"""

		output = ""
		tabLevel += 1
		for i in range(tabLevel):
			output += "\t"
		output += "|----'{0}'\n".format(self.name)
		for child in self.__children:
			output += child.listNode(tabLevel)
		tabLevel -= 1
		return output
