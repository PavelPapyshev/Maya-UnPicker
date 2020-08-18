import maya.cmds as mc
import UnPicker.UnPicker_NodeUtility as node
import UnPicker.UnPicker_Utility as utility
import UnPicker.UnPicker_MigratoryData as MigratoryData
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from UnPicker_AbstractButtonUI import UnPicker_AbstractButtonUI
from UnPicker_SelectColorUI import UnPicker_SelectColorUI
from UnPicker_TabWidgetUI import UnPicker_TabWidgetUI
from UnPicker_ItemOptionsWindowUI import UnPicker_ItemOptionsWindowUI


class UnPicker_MainWindowUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):
	
	"""
	creates a dialog window
	"""
	
	def __init__(self):
		
		super(UnPicker_MainWindowUI, self).__init__()
		
		self.setObjectName("MainWindowUnPickerUI")
		self.setWindowTitle("Universal Picker")
		
		self.dummyLayout = None
		self.tabsLayout = None
		
		#stores node names
		self.nodeDict = {}
		
		self.createUI()
		
		nodeList = node.findSaveNodes()
		
		if nodeList:
			self.autoloadNodeData(nodeList)
	
	
	def createUI(self):
		
		"""
		sets the window and its elements settings
		"""
		
		#main layout----------------------------------
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
		self.setLayout(self.mainLayout)
		
		#toolbar layout----------------------------------
		self.toolbarLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.toolbarLayout)
		
		#newPickerBtn----------------------------------
		self.newPickerBtn = QtWidgets.QPushButton()
		self.newPickerBtn.setMaximumWidth(32)
		self.newPickerBtn.setMaximumHeight(27)
		self.newPickerBtn.setEnabled(False)
		
		self.pixmap = QtGui.QPixmap(":/teAdd_Hover.svg")
		iconBtn = QtGui.QIcon(self.pixmap)
		self.newPickerBtn.setIcon(iconBtn)
		#self.newPickerBtn.setIconSize(QtCore.QSize(16,16))	
		self.newPickerBtn.clicked.connect(self.newDummy)
		self.toolbarLayout.addWidget(self.newPickerBtn)
		
		#character comboBox----------------------------------
		self.charCB = QtWidgets.QComboBox()
		#self.charCB.SizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
		self.charCB.activated.connect(self.editCharCB)
		self.toolbarLayout.addWidget(self.charCB)
		
		#editPickerBtn----------------------------------
		self.editPickerBtn = UnPicker_EditButtonUI(width=45, height=27, textLabel="Edit")
		self.editPickerBtn.clicked.connect(self.setEditMod)
		self.toolbarLayout.addWidget(self.editPickerBtn)
		
		#savePickerBtn----------------------------------
		self.savePickerBtn = QtWidgets.QPushButton("Save")
		self.savePickerBtn.setMaximumWidth(45)
		self.savePickerBtn.setMaximumHeight(27)
		self.savePickerBtn.setEnabled(False)
		self.savePickerBtn.clicked.connect(self.saveData)
		self.toolbarLayout.addWidget(self.savePickerBtn)
		
		#tabsLayout----------------------------------
		self.tabsLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.addLayout(self.tabsLayout)
	
	
	def autoloadNodeData(self, nodeList):
		
		"""
		loading data from nodes when running a script
		
		accepts arguments:
			@nodeList[list] - node names
		"""
		
		for nameNode in nodeList:		
			self.addCharCB(nameNode)
		
			#read data from the node
			dataTab = node.readNode(nameNode)	
			
			#create tabs
			self.creatTabOfLoadData(dataTab)
		
		self.editCharCB(len(nodeList)-1)
	
	
	def setEditMod(self, mod):
		
		"""
		switches mod
		
		accepts arguments:
			@mod[bool]
		"""
				
		utility.UnPicker_EditMode = mod
		
		#deselect items
		if not utility.UnPicker_EditMode:
			charCB_count = self.charCB.count()
			
			for charCB_index in range(charCB_count):
				nameNode = self.charCB.itemData(charCB_index)
				tabList = self.tabsLayout.itemAt(charCB_index).widget().getTabsWidet()
				
				for tab in tabList:
					tab.clearSelectItem()
	
		#enable/disable savePickerBtn
		if utility.UnPicker_EditMode:
			self.savePickerBtn.setEnabled(True)
			self.newPickerBtn.setEnabled(True)
			self.optWindow(show=True)
			
			#hide/show settings tab
			if self.charCB.count():
				tabsCount = self.tabsLayout.count()
				for i in range(tabsCount):
					self.tabsLayout.itemAt(i).widget().addSettingTab()
			
		else:
			self.savePickerBtn.setEnabled(False)
			self.newPickerBtn.setEnabled(False)
			self.optWindow(show=False)
			
			#hide/show settings tab
			if self.charCB.count():
				tabsCount = self.tabsLayout.count()
				for i in range(tabsCount):
					self.tabsLayout.itemAt(i).widget().removeSettingTab()
	
	
	def saveData(self, saveAll=True):
	
		"""
		collects data for saving to a node
		
		accepts arguments:
			@saveAll[bool] - full save or just a tab
		"""
		
		charCB_count = self.charCB.count()
		
		for charCB_index in range(charCB_count):
			
			nameNode = self.charCB.itemData(charCB_index)
			tabList = self.tabsLayout.itemAt(charCB_index).widget().getTabsWidet()
			index = 0
			
			#clearing attributes
			node.delAttr(nameNode)
			node.createAttrs(nameNode)
			
			#tabs
			for tab in tabList:
			
				tabName = tab.getTabName()
				tabColor = tab.getTabColor()
				tabImage = tab.getTabImage()
				dataItems = tab.getDataItems()

				node.addTabNameAttr(nameNode, index, tabName, tabColor, tabImage)
				
				if not saveAll:
					index += 1
					continue
				
				#items
				widgetType = dataItems.getWidgetType()
				widgetPos = dataItems.getWidgetPos()
				widgetWidthHeight = dataItems.getWidgetWidthHeight()
				widgetColor = dataItems.getWidgetColor()
				widgetLabel = dataItems.getWidgetLabel()
				widgetScript = dataItems.getWidgetScript()
				
				#save
				node.addAttr(nameNode, index, 
							widgetType, 
							widgetPos, 
							widgetWidthHeight, 
							widgetColor, 
							widgetLabel, 
							widgetScript)
				
				index += 1
		
		mc.inViewMessage(amg="<hl>UnPicker</hl> picker save, please save the scene", pos="botLeft", fade=True)
	
	
	def checkData(self, data):
		
		"""
		replaces None with ''
		
		accepts arguments:
			@data
		"""
		
		if not data:
			data = ""
		
		return data
	
	
	def editCharCB(self, index):
		
		"""
		triggered when choosing a character in the picker
		
		accepts arguments:
			@index[int] - index tab
		"""
		
		#nameSpace	
		nameNode = self.charCB.itemData(index)
		utility.UnPicker_NameSpace = self.getNameSpaceOfNodeDict(nameNode)
		
		if utility.UnPicker_NameSpace:
			utility.UnPicker_NameSpace = utility.UnPicker_NameSpace + ":"
		
		self.hideAllTabs()
		self.tabsLayout.itemAt(index).widget().setVisible(True)
		
	
	def hideAllTabs(self):
	
		"""
		hides all tab widgets
		"""
		
		tabsCount = self.tabsLayout.count()
		
		for i in range(tabsCount):
			self.tabsLayout.itemAt(i).widget().setVisible(False)
		
	
	def creatTabOfLoadData(self, dataTab=None):
	
		"""
		creates tabs with items
		
		accepts arguments:
			@dataTab[list]
		"""
		
		if not dataTab:
			return
		
		self.createTabsLayout(createTabs=False)
		
		for tab in dataTab:
			
			#color format
			color = tab[1].split(";")
			
			#create tab
			self.tabs.addNewTab(tabName=tab[0], viewColor=color, imagePath = tab[2])
			
			#add elements
			itemData = MigratoryData.UnPicker_MigratoryData()
			
			itemData.widgetType = tab[3]
			itemData.widgetPos = tab[4]
			itemData.widgetWidthHeight = tab[5]
			itemData.widgetColor = tab[6]
			itemData.widgetLabel = tab[7]
			itemData.widgetScript = tab[8]
			
			#self.tabs.createSceneItems(tab[0], tab[2], tab[3], tab[4], tab[5], tab[6], tab[7])
			self.tabs.createSceneItems(tab[0], itemData)
				
		if utility.UnPicker_EditMode:
			self.tabs.addSettingTab()
	
	
	def removeTabsLayout(self):
		
		"""
		removes the tab bar
		"""
		
		if self.tabsLayout:
		
			self.clearLayout(self.tabsLayout)
			self.tabsLayout.deleteLater()
			self.tabsLayout = None
	
	
	def removeDummyLayout(self):
	
		"""
		removes the new character bar
		"""
		
		if self.dummyLayout:
		
			self.clearLayout(self.dummyLayout)
			self.dummyLayout.deleteLater()			
			self.dummyLayout = None

		if self.charCB.count():
			
			index = self.charCB.currentIndex()
			self.editCharCB(index)
	
	
	def clearLayout(self, layout):
		
		"""
		clears layout contents
		
		accepts arguments:
			@layout[QLayout]
		"""
		
		if layout:
			while layout.count():
			
				child = layout.takeAt(0)
				
				if child.widget() is not None:
					child.widget().deleteLater()
					
				elif child.layout() is not None:
					self.clearLayout(child.layout())
	
	
	def manualCreateTabsLayout(self):
	
		"""
		creating the first tab manually
		"""
		
		charName = self.charNameLine.text()
		tabName = self.tabNameLine.text()
		imagePath = self.imageLine.text()
		backColor = self.colorBackroundSel.getColor()
		
		#you need to enter a name
		if not charName:
			mc.warning("Enter character name!")
			return
			
		#create a save node
		nameNode = node.createSaveNode(charName)
		
		#hide tab widgets
		self.removeDummyLayout()
		self.hideAllTabs()
		
		#adds a name to the list of nodes
		self.addCharCB(nameNode)
		
		self.viewColor = self.colorBackroundSel.getColor()
		
		self.createTabsLayout(tabName, True, imagePath)
		self.saveData(saveAll=False)
	
	
	def createTabsLayout(self, tabName="Main", createTabs=True, imagePath=None):
		
		"""
		create tab widget
		
		accepts arguments:
			@tabName[str]
			@createTabs[bool]
			@imagePath[str]
		"""
			
		#if we turn off the editing mode, then turn it on
		if (not self.editPickerBtn.edit) and (createTabs):
		
			self.editPickerBtn.switchEditMod(True)
			self.setEditMod(True)
		
		#tabs----------------------------------
		self.tabs = UnPicker_TabWidgetUI()
		self.tabs.selItem.connect(self.transmitSelItemSignal)
		
		if createTabs:
			self.tabs.addNewTab(tabName=tabName, viewColor=self.viewColor, imagePath=imagePath)
			self.tabs.addSettingTab()
			
		self.tabsLayout.addWidget(self.tabs)
	
	
	def newDummy(self):
		
		"""
		creates a new character bar
		"""
		
		#if there is a menu for a new character, then delete them		
		self.removeDummyLayout()
		
		#if there are tabs, then hide them
		self.hideAllTabs()
		
		#dummy layout----------------------------------
		self.dummyLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.addLayout(self.dummyLayout)
		
		#charNameLayout----------------------------------
		self.charNameLayout = QtWidgets.QHBoxLayout()
		self.charNameLayout.setContentsMargins(11,0,0,0)
		self.dummyLayout.addLayout(self.charNameLayout)
		
		#charNameLabel----------------------------------
		self.charNameLabel = QtWidgets.QLabel()
		self.charNameLabel.setText("Character Name:")
		self.charNameLayout.addWidget(self.charNameLabel)
		
		#charNameLine----------------------------------
		self.charNameLine = QtWidgets.QLineEdit()
		self.charNameLine.setText("Character")
		self.charNameLayout.addWidget(self.charNameLine)
		
		#tabNameLayout----------------------------------
		self.tabNameLayout = QtWidgets.QHBoxLayout()
		self.tabNameLayout.setContentsMargins(42,0,0,0)
		self.dummyLayout.addLayout(self.tabNameLayout)
		
		#tabNameLabel----------------------------------
		self.tabNameLabel = QtWidgets.QLabel()
		self.tabNameLabel.setText("Tab Name:")
		self.tabNameLayout.addWidget(self.tabNameLabel)
		
		#tabNameLine----------------------------------
		self.tabNameLine = QtWidgets.QLineEdit()
		self.tabNameLine.setText("Main")
		self.tabNameLayout.addWidget(self.tabNameLine)
		
		#imageLayout----------------------------------
		self.imageLayout = QtWidgets.QHBoxLayout()
		self.imageLayout.setContentsMargins(35,0,0,0)
		self.dummyLayout.addLayout(self.imageLayout)
		
		#imageLabel----------------------------------
		self.imageLabel = QtWidgets.QLabel()
		self.imageLabel.setText("Image Path:")
		self.imageLayout.addWidget(self.imageLabel)
		
		#imageLine----------------------------------
		self.imageLine = QtWidgets.QLineEdit()
		self.imageLayout.addWidget(self.imageLine)
		
		#imageBtn----------------------------------
		self.imageBtn = QtWidgets.QPushButton()
		self.imageBtn.setText("Open")
		self.imageBtn.setMaximumWidth(50)
		self.imageBtn.clicked.connect(self.getImagePath)
		self.imageLayout.addWidget(self.imageBtn)
		
		#colorBackroundLayout----------------------------------
		self.colorBackroundLayout = QtWidgets.QHBoxLayout()
		self.colorBackroundLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.dummyLayout.addLayout(self.colorBackroundLayout)
		
		#colorBackroundLabel----------------------------------
		self.colorBackroundLabel = QtWidgets.QLabel()
		self.colorBackroundLabel.setText("Background Color:")
		self.colorBackroundLayout.addWidget(self.colorBackroundLabel)

		#colorBackroundSel----------------------------------
		self.colorBackroundSel = UnPicker_SelectColorUI(width=60, height=20)
		self.colorBackroundLayout.addWidget(self.colorBackroundSel)
		
		#btnLayout----------------------------------
		self.btnLayout = QtWidgets.QHBoxLayout()
		self.dummyLayout.addLayout(self.btnLayout)
		
		#btnOK----------------------------------
		self.btnOK = QtWidgets.QPushButton()
		self.btnOK.setText("OK")
		self.btnOK.setMinimumWidth(50)
		self.btnOK.setMinimumHeight(30)
		self.btnOK.clicked.connect(self.manualCreateTabsLayout)
		self.btnLayout.addWidget(self.btnOK)
		
		#btnCancel----------------------------------
		self.btnCancel = QtWidgets.QPushButton()
		self.btnCancel.setText("Cancel")
		self.btnCancel.setMinimumWidth(50)
		self.btnCancel.setMinimumHeight(30)
		self.btnCancel.clicked.connect(self.removeDummyLayout)
		self.btnLayout.addWidget(self.btnCancel)
	
	
	def optWindow(self, show=True):
		
		"""
		show/hide settings window
		
		accepts arguments:
			@show[bool]
		"""
		
		if mc.workspaceControl("ItemOptionsWindowUnPickerUIWorkspaceControl", exists=1):
			mc.deleteUI("ItemOptionsWindowUnPickerUIWorkspaceControl", control = 1)
			mc.workspaceControlState("ItemOptionsWindowUnPickerUIWorkspaceControl", remove=1)
		
		if show:
			self.itemOptWin = UnPicker_ItemOptionsWindowUI()
			self.itemOptWin.show(dockable=1, area="right", allowedArea="right", floating=1)
			self.itemOptWin.setSelItem.connect(self.transmitSetSelItemSignal)
			
			mc.workspaceControl("ItemOptionsWindowUnPickerUIWorkspaceControl",
						label="Item Options",
						edit=1,
						dockToControl=["MainWindowUnPickerUIWorkspaceControl", "left"])
	
		
	def dockCloseEventTriggered(self):
		
		"""
		when closing the main window, remove the settings window. Works poorly
		"""
		
		try:
			if mc.workspaceControl("ItemOptionsWindowUnPickerUIWorkspaceControl", exists=1):
				mc.deleteUI("ItemOptionsWindowUnPickerUIWorkspaceControl", control = 1)
				mc.workspaceControlState("ItemOptionsWindowUnPickerUIWorkspaceControl", remove=1)
		except:
			pass
	
	
	def addCharCB(self, nameNode):
	
		"""
		adds a node to the list
		
		accepts arguments:
			@nameNode[str]
		"""
		
		#add a node to the dictionary
		self.addNodeDict(nameNode)
		
		
		#get the short name or NameSpace
		name = self.getNameSpaceOfNodeDict(nameNode)
		
		if not name:
			name = self.getNameOfNodeDict(nameNode)
		
		#add name to node list widget
		self.charCB.addItem(name, nameNode)
		
		#select the added name in the widget
		charCBIndex = self.charCB.count() - 1
		self.charCB.setCurrentIndex(charCBIndex)
	
	
	def addNodeDict(self, nameNode):
		
		"""
		populates the dictionary of node names
		
		accepts arguments:
			@nameNode[str] - full name
		"""
		
		#get NameSpace and short name
		nameSpace, name = utility.getNodeNameComposition(nameNode)
		self.nodeDict[nameNode] = [nameSpace, name]
	
	
	def getNameOfNodeDict(self, nameNode):
		
		"""
		return short name node
		
		accepts arguments:
			@nameNode[str] - full name
		
		return arguments:
			@[str] - short name
		"""
		
		return self.nodeDict.get(nameNode)[1]
	
	
	def getNameSpaceOfNodeDict(self, nameNode):
	
		"""
		return short NameSpace node
		
		accepts arguments:
			@nameNode[str] - full name
		
		return arguments:
			@[str] - NameSpace
		"""
		
		return self.nodeDict.get(nameNode)[0]
	
	
	def getImagePath(self):
	
		"""
		sets the path to the image
		"""
		
		imagePath = utility.getImagePath()		
		self.imageLine.setText(imagePath)

	
	def transmitSelItemSignal(self, data):
		
		"""
		transfers the data of the selected item to UnPicker_ItemOptionsWindowUI
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		if self.itemOptWin:
			self.itemOptWin.getSelItemData(data)
		
	
	def transmitSetSelItemSignal(self, data):
	
		"""
		transfers the data for the selected item to UnPicker_TabWidgetUI
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
	
		if not self.tabsLayout:
			return
		
		index = self.charCB.currentIndex()
		
		if self.tabsLayout.itemAt(index):
			self.tabsLayout.itemAt(index).widget().transmitSetSelItemSignal(data)

	
#----------------------------END UnPicker_MainWindowUI


class UnPicker_EditButtonUI(UnPicker_AbstractButtonUI):
	
	#signal when a button is pressed
	clicked = QtCore.Signal(bool)
	
	def __init__(self, objectName="UnPicker_Button", width=None, height=None, textLabel="Text"):
		
		#editMod
		self.edit = False
		
		super(UnPicker_EditButtonUI, self).__init__(objectName, width, height, textLabel)
	
	
	def enterEvent(self, event):
	
		"""
		triggered when the cursor is hovered over
		"""
		
		if self.edit:
			return
		
		super(UnPicker_EditButtonUI, self).enterEvent(event)
	
	
	def leaveEvent(self, event):
	
		"""
		triggered when the cursor is removed
		"""
		
		if self.edit:
			return
		
		super(UnPicker_EditButtonUI, self).leaveEvent(event)
	
	
	def switchEditMod(self, mod):
		
		"""
		switching mod editing
		
		accepts arguments:
			@mod[bool]
		"""
		
		if mod:
			self.edit = True
			self.pal.setColor(self.backgroundRole(), QtGui.QColor(255, 255, 0))
		
		else:
			self.edit = False
			color = 95
			self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		
		self.setPalette(self.pal)
	
	
	def mousePressEvent(self, event):
		
		"""
		triggered by left-clicking
		"""
		
		#check that the left mouse button was pressed
		if event.buttons() != QtCore.Qt.LeftButton:
			return
		
		if self.edit:
			self.switchEditMod(False)
				
		else:
			self.switchEditMod(True)
		
		self.clicked.emit(self.edit)
	
	
	def mouseReleaseEvent(self, event):
		pass


#----------------------------END UnPicker_EditButtonUI	
