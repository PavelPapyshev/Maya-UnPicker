import maya.cmds as mc
import UnPicker.UnPicker_Utility as utility
import UnPicker_ItemUI as ItemUI
from PySide2 import QtWidgets, QtCore, QtGui
from UnPicker_SelectColorUI import UnPicker_SelectColorUI
from UnPicker_ViewUI import UnPicker_ViewUI
from UnPicker_SceneUI import UnPicker_SceneUI
from UnPicker_MimeUI import UnPicker_MimeUI


class UnPicker_TabWidgetUI(QtWidgets.QTabWidget):
	
	"""
	creates a tabs widget
	"""
	
	#signal for data transmission of the selected item
	selItem = QtCore.Signal(UnPicker_MimeUI)
	
	def __init__(self):
		
		super(UnPicker_TabWidgetUI, self).__init__()
		
		#list of available regular tabs
		self.tabsWidget = []
		
		#settings tab to create new tabs
		self.settingTab = None	
	
	
	def addNewTab(self, tabName="Main", insert=False, viewColor=[0.334, 0.334, 0.334], imagePath=None):
	
		"""
		adds a regular tab
		
		accepts arguments:
			@tabName[str]
			@insert[bool]
			@viewColor[list] - view color background
			@imagePath[str]
		"""
		
		newTab = UnPicker_TabUI(tabName, viewColor, imagePath)
		newTab.selItem.connect(self.transmitSelItemSignal)
		
		#insert a tab in a specific place or add to the end
		if insert:
			
			index = self.currentIndex()
			self.insertTab(index, newTab, tabName)
			self.setCurrentIndex(index)
		
		else:
			self.addTab(newTab, tabName)
		
		self.tabsWidget.append(newTab)
	
	
	def removeTab(self, tab):
		
		"""
		removes tab
		
		accepts arguments:
			@tab[UnPicker_TabUI] - link to the tab to be removed
		"""
		
		#you cannot delete the last tab
		if len(self.tabsWidget) < 2:
			mc.warning("Can't delete a single tab!")
			return
		
		if tab in self.tabsWidget:
			tab.deleteLater()
			self.tabsWidget.remove(tab)
			
	
	
	def addSettingTab(self):
		
		"""
		adds a settings tab
		"""
		
		self.settingTab = UnPicker_TabSettingUI()
		self.settingTab.insert.connect(self.addNewTab)
		self.addTab(self.settingTab, "+")
	
	
	def removeSettingTab(self):
	
		"""
		remove settings tab
		"""
		
		self.settingTab.insert.disconnect(self.addNewTab)
		self.settingTab.deleteLater()
		self.settingTab = None
		
	
	def getTabsWidet(self):
		
		"""
		returns a list of tab widgets
		
		return arguments:
			@[list]
		"""
		
		return self.tabsWidget
	
	
	def createSceneItems(self, tabName, itemData):
		
		"""
		create item widgets
		
		accepts arguments:
			@tabName[str]
			@itemData[UnPicker_MigratoryData]
		"""
		
		for widget in self.tabsWidget:
			
			nameWidget = widget.getTabName()
			
			if tabName == nameWidget:
				widget.createSceneItems(itemData)
				break
			
	
	def transmitSelItemSignal(self, data):
		
		"""
		transfers the data of the selected item to UnPicker_MainWindowUI
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		self.selItem.emit(data)
		
		
	def transmitSetSelItemSignal(self, data):
	
		"""
		transfers the data for the selected item to UnPicker_TabUI
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		index = self.currentIndex()
		
		try:
			self.tabsWidget[index].transmitSetSelItemSignal(data)
		
		except:
			return
	
	
#----------------------------END UnPicker_TabWidgetUI	


class UnPicker_TabSettingUI(QtWidgets.QWidget):
	
	"""
	creates a settings tab widget
	"""
	
	#signal when you click "OK" to add a new tab
	insert = QtCore.Signal(str, bool, list, str)
	
	def __init__(self):
		
		super(UnPicker_TabSettingUI, self).__init__()
		self.createUI()
	
	
	def createUI(self):
	
		"""
		create widget
		"""
		
		#mainLayout----------------------------------
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
		self.setLayout(self.mainLayout)
		
		#tabNameLayout----------------------------------
		self.tabNameLayout = QtWidgets.QHBoxLayout()
		self.tabNameLayout.setContentsMargins(42,0,0,0)
		self.mainLayout.addLayout(self.tabNameLayout)
		
		#tabNameLabel----------------------------------
		self.tabNameLabel = QtWidgets.QLabel()
		self.tabNameLabel.setText("Tab Name:")
		self.tabNameLayout.addWidget(self.tabNameLabel)
		
		#tabNameLine----------------------------------
		self.tabNameLine = QtWidgets.QLineEdit()
		self.tabNameLine.setText("Tab")
		self.tabNameLayout.addWidget(self.tabNameLine)
		
		#imageLayout----------------------------------
		self.imageLayout = QtWidgets.QHBoxLayout()
		self.imageLayout.setContentsMargins(35,0,0,0)
		self.mainLayout.addLayout(self.imageLayout)
		
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
		self.mainLayout.addLayout(self.colorBackroundLayout)
		
		#colorBackroundLabel----------------------------------
		self.colorBackroundLabel = QtWidgets.QLabel()
		self.colorBackroundLabel.setText("Background Color:")
		self.colorBackroundLayout.addWidget(self.colorBackroundLabel)

		#colorBackroundSel----------------------------------
		self.colorBackroundSel = UnPicker_SelectColorUI(width=60, height=20)
		self.colorBackroundLayout.addWidget(self.colorBackroundSel)
		
		#btnOK----------------------------------
		self.btnOK = QtWidgets.QPushButton()
		self.btnOK.setText("OK")
		self.btnOK.setMinimumWidth(50)
		self.btnOK.setMinimumHeight(30)
		self.btnOK.clicked.connect(self.insertTab)
		self.mainLayout.addWidget(self.btnOK)
		
		
	def insertTab(self):
		
		"""
		emits a tab add signal
		"""
		viewColor = self.colorBackroundSel.getColor()
		self.insert.emit(self.tabNameLine.text(), True, viewColor, self.imageLine.text())
	
	
	def getImagePath(self):
	
		"""
		sets the path to the image
		"""
		
		imagePath = utility.getImagePath()		
		self.imageLine.setText(imagePath)
	

#----------------------------END UnPicker_TabSettingUI		


class UnPicker_TabUI(QtWidgets.QWidget):
	
	"""
	creates a settings tab widget
	
	accepts arguments:
		@name[str] - tab name
		@viewColor[list] - view color background
		@imagePath[str]
	"""
	
	#signal for data transmission of the selected item
	selItem = QtCore.Signal(UnPicker_MimeUI)
	
	
	def __init__(self, name, viewColor=[0.334, 0.334, 0.334], imagePath=None):
		
		super(UnPicker_TabUI, self).__init__()
		
		self.name = name
		self.viewColor = viewColor
		self.imagePath = imagePath
		
		if self.imagePath:
			self.imagePath = utility.imageSearch(self.imagePath)
	
		self.createUI()
	
	
	def createUI(self):
	
		"""
		create widget
		"""
		
		#mainLayout----------------------------------
		self.mainLayout = QtWidgets.QVBoxLayout()
		#self.mainLayout.setAlignment(QtCore.Qt.AlignRight)
		self.setLayout(self.mainLayout)
		
		#scene----------------------------------
		self.scene = UnPicker_SceneUI()
		self.scene.selItem.connect(self.transmitSelItemSignal)
		
		#if there is a picture, then load it
		if self.imagePath:
			self.scene.addImageScene(self.imagePath)
			imW, imH = self.scene.getImageWidthHight()
		
		else:
			imW = 10 
			imH = 10
		
		#viewport----------------------------------
		self.viewport = UnPicker_ViewUI(viewColor=self.viewColor, imW=imW, imH=imH)
		self.viewport.setDragMode(QtWidgets.QGraphicsView.NoDrag)
		self.viewport.setScene(self.scene)
		self.viewport.removeTab.connect(self.delteTab)
		self.mainLayout.addWidget(self.viewport)
				
		#set sliders to start
		self.viewport.verticalScrollBar().setSliderPosition(1)
		self.viewport.horizontalScrollBar().setSliderPosition(1)	
	
	
	def transmitSelItemSignal(self, data):
		
		"""
		transfers the data of the selected item to UnPicker_TabWidgetUI
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		self.selItem.emit(data)
	
	
	def transmitSetSelItemSignal(self, data):
	
		"""
		transfers the data for the selected item to UnPicker_SceneUI
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		self.scene.setSelItemData(data)
	
	
	def delteTab(self):
	
		"""
		call tab deletion
		"""
		
		self.parent().parent().removeTab(self)
	
	
	def getTabName(self):
		
		"""
		returns name of the tab
			
		return arguments:
			@[str]
		"""
		
		return self.name
	
	
	def getTabColor(self):
	
		"""
		returns the background color of the tab
		
		return arguments:
			@tabColor[str]
		"""
		
		tabColor = self.viewport.getColor()
		return tabColor
	
	
	def getTabImage(self):
		
		"""
		returns the background color of the tab
		
		return arguments:
			@tabImage[str]
		"""
		
		tabImage = self.scene.getImagePath()
		return tabImage
	
	
	def getDataItems(self):
	
		"""
		returns list items
			
		return arguments:
			@[list]
		"""
		
		return self.scene.getAllItems()
		
	
	def createSceneItems(self, itemData):
		
		"""
		relaying creates items
		
		accepts arguments:
			@itemData[UnPicker_MigratoryData]
		"""
		
		self.scene.createSceneItems(itemData)
		
	
	def clearSelectItem(self):
	
		"""
		deselect items after turning off EditMod
		"""
		
		if isinstance(self.scene.selectItem, ItemUI.UnPicker_ItemUI):
			self.scene.selectItem.body.selected(False)
			self.scene.selectItem.showHideCtrls(False)
		
		elif isinstance(self.scene.selectItem, ItemUI.UnPicker_ItemCtrlUI):
			self.scene.selectItem.parentItem().body.selected(False)
			self.scene.selectItem.parentItem().showHideCtrls(False)
		
		
		
#----------------------------END UnPicker_TabUI	