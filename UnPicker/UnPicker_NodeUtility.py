import maya.cmds as mc


def findSaveNodes():

	"""
	looking for picker nodes
	
	returns arguments:
		@nodeList[list] - names of found nodes
	"""
	
	nodeList = []
	nodes = mc.ls(type="geometryVarGroup", l=1)
	
	for nameNode in nodes:
		
		if "UnPicker" in nameNode:	
			nodeList.append(nameNode)
	
	return nodeList


def createSaveNode(nameNode):

	"""
	creates a node to store the picker data
	
	accepts arguments:
		@nameNode[str]
	
	returns arguments:
		@node[str] - link to the created node
	"""
	
	nameNode = "UnPicker_{}".format(nameNode)
	node = mc.createNode("geometryVarGroup", n=nameNode, ss=1)
	
	createAttrs(node)
	
	return node

	
def createAttrs(node):

	"""
	adds node attrbutes
	
	accepts arguments:
		@node[str] - link to the created node
	"""
	
	#check for node existence
	if not mc.objExists(node):
		mc.warning("'{}' not found!".format(node))
		return False
	
	#group attr
	mc.addAttr(node, longName="UnPicker", numberOfChildren=1, at="compound")
	
	#multi attr
	mc.addAttr(node, longName="Tab", numberOfChildren=9, at="compound", parent="UnPicker", m=1, im=1)
	
	#children attrs
	mc.addAttr(node, longName="TabName", dt="string", parent="Tab")
	mc.addAttr(node, longName="TabColor", dt="string", parent="Tab")
	mc.addAttr(node, longName="TabImage", dt="string", parent="Tab")
	mc.addAttr(node, longName="WidgetType", dt="stringArray", parent="Tab")
	mc.addAttr(node, longName="WidgetPos", dt="stringArray", parent="Tab")
	mc.addAttr(node, longName="WidgetWidthHeight", dt="stringArray", parent="Tab")
	mc.addAttr(node, longName="WidgetColor", dt="stringArray", parent="Tab")
	mc.addAttr(node, longName="WidgetLabel", dt="stringArray", parent="Tab")
	mc.addAttr(node, longName="WidgetScript", dt="stringArray", parent="Tab")

	
def addAttr(node, index, widgetType, widgetPos, widgetWidthHeight, widgetColor, widgetLabel, widgetScript):

	"""
	writes data to the node
	
	accepts arguments:
		@node[str] - link to the created node
		@index[int] - tab number
		@widgetType[list]
		@widgetPos[list]
		@widgetWidthHeight[list]
		@widgetColor[list]
		@widgetLabel[list]
		@widgetScript[list]
	"""
	
	#check for node existence
	if not mc.objExists(node):
		mc.warning("'{}' not found!".format(node))
		return
	
	mc.setAttr("{}.Tab[{}].WidgetType".format(node, index), type="stringArray", *([len(widgetType)] + widgetType))
	mc.setAttr("{}.Tab[{}].WidgetPos".format(node, index), type="stringArray", *([len(widgetPos)] + widgetPos))
	mc.setAttr("{}.Tab[{}].WidgetWidthHeight".format(node, index), type="stringArray", *([len(widgetWidthHeight)] + widgetWidthHeight))
	mc.setAttr("{}.Tab[{}].WidgetColor".format(node, index), type="stringArray", *([len(widgetColor)] + widgetColor))
	mc.setAttr("{}.Tab[{}].WidgetLabel".format(node, index), type="stringArray", *([len(widgetLabel)] + widgetLabel))
	mc.setAttr("{}.Tab[{}].WidgetScript".format(node, index), type="stringArray", *([len(widgetScript)] + widgetScript))


def addTabNameAttr(node, index, tabName, tabColor, tabImage):

	"""
	writes tabName and tabColor to the node
	
	accepts arguments:
		@node[str] - link to the created node
		@index[int] - tab number
		@tabName[str]
		@tabColor[str]
		@tabImage[str]
	"""
	
	#check for node existence
	if not mc.objExists(node):
		mc.warning("'{}' not found!".format(node))
		return
	
	mc.setAttr("{}.Tab[{}].TabName".format(node, index), tabName, type="string")
	mc.setAttr("{}.Tab[{}].TabColor".format(node, index), tabColor, type="string")
	mc.setAttr("{}.Tab[{}].TabImage".format(node, index), tabImage, type="string")
	

def delAttr(node):

	"""
	removes attributes from a node
	
	accepts arguments:
		@node[str] - link to the created node
	"""
	
	#check for node existence
	if not mc.objExists(node):
		mc.warning("'{}' not found!".format(node))
		return False
	
	mc.deleteAttr(node, at="UnPicker")

	
def readNode(node):

	"""
	reads data from a node
	
	accepts arguments:
		@node[str] - link to the created node
		
	returns arguments:
		@dataTab[list] - data from the node
	"""
	
	#check for node existence
	if not mc.objExists(node):
		mc.warning("'{}' not found!".format(node))
		return
	
	#get multi attribute
	attr = mc.getAttr("{}.Tab".format(node), mi=1)
	
	#if it is empty, finish
	if not attr:
		return
	
	dataTab = []
	
	for index in range(len(attr)):
		
		data = []
		
		tabName = mc.getAttr("{}.Tab[{}].TabName".format(node, index))
		data.append(tabName)
		
		tabColor = mc.getAttr("{}.Tab[{}].TabColor".format(node, index))
		data.append(tabColor)
		
		tabImage = mc.getAttr("{}.Tab[{}].TabImage".format(node, index))
		data.append(tabImage)
		
		widgetType = mc.getAttr("{}.Tab[{}].WidgetType".format(node, index))
		data.append(widgetType)
		
		widgetPos = mc.getAttr("{}.Tab[{}].WidgetPos".format(node, index))
		data.append(widgetPos)
		
		widgetWidthHeight = mc.getAttr("{}.Tab[{}].WidgetWidthHeight".format(node, index))
		data.append(widgetWidthHeight)
		
		widgetColor = mc.getAttr("{}.Tab[{}].WidgetColor".format(node, index))
		data.append(widgetColor)
		
		widgetLabel = mc.getAttr("{}.Tab[{}].WidgetLabel".format(node, index))
		data.append(widgetLabel)
		
		widgetScript = mc.getAttr("{}.Tab[{}].WidgetScript".format(node, index))
		data.append(widgetScript)
		
		dataTab.append(data)
	
	return dataTab
		