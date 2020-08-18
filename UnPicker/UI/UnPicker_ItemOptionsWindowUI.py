from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from UnPicker_AbstractButtonUI import UnPicker_AbstractButtonUI
from UnPicker_MimeUI import UnPicker_MimeUI
from UnPicker_SelectColorUI import UnPicker_SelectColorUI
import UnPicker.UnPicker_Utility as utility



class UnPicker_ItemOptionsWindowUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):
	
	"""
	creates a button settings window
	"""
	
	#signal to transmit data to the selected item
	setSelItem = QtCore.Signal(UnPicker_MimeUI)
	
	def __init__(self):
		
		super(UnPicker_ItemOptionsWindowUI, self).__init__()
		
		self.setObjectName("ItemOptionsWindowUnPickerUI")
		self.itemsData = utility.loadItemsOptions()
		
		self.createUI()
	
	
	def createUI(self):
	
		"""
		create widget
		"""
		
		#mainLayout----------------------------------
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
		self.setLayout(self.mainLayout)
		
		#scrollGroupBox----------------------------------
		self.scrollGroupBox = QtWidgets.QGroupBox()
		self.scrollGroupBox.setTitle("Drag and Drop")
		self.scrollGroupBox.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
		self.scrollGroupBox.setMaximumHeight(110)
		self.mainLayout.addWidget(self.scrollGroupBox)
		
		#toolBarLayout----------------------------------
		self.toolBarLayout = QtWidgets.QHBoxLayout()
		self.toolBarLayout.setAlignment(QtCore.Qt.AlignTop)
		self.scrollGroupBox.setLayout(self.toolBarLayout)
		
		#scroll----------------------------------
		self.scroll = QtWidgets.QScrollArea()
		self.scroll.setWidgetResizable(True)
		self.scroll.setMaximumHeight(70)
		self.scroll.setFocusPolicy(QtCore.Qt.NoFocus)
		self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.toolBarLayout.addWidget(self.scroll)
		
		#scrollWidget----------------------------------
		self.scrollWidget = QtWidgets.QWidget()
		self.scrollWidget.setAutoFillBackground(1)
		color = 73
		pal = self.scrollWidget.palette()
		pal.setColor(self.scrollWidget.backgroundRole(), QtGui.QColor(color, color, color))
		self.scrollWidget.setPalette(pal)
		self.scroll.setWidget(self.scrollWidget)
		
		#scrollLayout----------------------------------
		self.scrollLayout = QtWidgets.QHBoxLayout()
		self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
		self.scrollLayout.setSpacing(3)
		self.scrollWidget.setLayout(self.scrollLayout)
				
		#scrollBtn----------------------------------
		self.scrollBtn = QtWidgets.QPushButton("+")
		self.scrollBtn.setFixedSize(20,40)
		self.scrollBtn.clicked.connect(self.addToolbarBtn)
		self.scrollLayout.addWidget(self.scrollBtn)
		
		#if there are presets create buttons from them otherwise default
		if self.itemsData:
			self.createItemsFile()
		
		else:
			self.createItemsDefault()
		
		#groupBox----------------------------------
		self.groupBox = QtWidgets.QGroupBox()
		self.groupBox.setTitle("Set Options")
		self.groupBox.setAlignment(QtCore.Qt.AlignHCenter)
		self.mainLayout.addWidget(self.groupBox)
		
		#groupLayout----------------------------------
		self.groupLayout = QtWidgets.QVBoxLayout()
		self.groupBox.setLayout(self.groupLayout)
		
		#groupLineLayout----------------------------------
		self.groupLineLayout = QtWidgets.QHBoxLayout()
		self.groupLayout.addLayout(self.groupLineLayout)
		
		#groupLabel----------------------------------
		self.groupLabel = QtWidgets.QLabel()
		self.groupLabel.setText("Label:")
		self.groupLineLayout.addWidget(self.groupLabel)
		
		#groupLineLabel----------------------------------
		self.groupLineLabel = QtWidgets.QLineEdit()
		self.groupLineLabel.setText("Text")
		self.groupLineLayout.addWidget(self.groupLineLabel)
		
		#groupColorLayout----------------------------------
		self.groupColorLayout = QtWidgets.QHBoxLayout()
		self.groupColorLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.groupLayout.addLayout(self.groupColorLayout)
		
		#groupColorLabel----------------------------------
		self.groupColorLabel = QtWidgets.QLabel()
		self.groupColorLabel.setText("Color:")
		self.groupColorLayout.addWidget(self.groupColorLabel)
		
		#groupColorSel----------------------------------
		self.groupColorSel = UnPicker_SelectColorUI(width=60, height=20)
		self.groupColorLayout.addWidget(self.groupColorSel)
		
		#groupScriptLabel----------------------------------
		self.groupScriptLabel = QtWidgets.QLabel()
		self.groupScriptLabel.setText("Python Script :")
		self.groupLayout.addWidget(self.groupScriptLabel)
		
		#groupScriptText----------------------------------
		self.groupScriptText = QtWidgets.QTextEdit()
		self.groupScriptText.setMinimumWidth(400)
		self.groupLayout.addWidget(self.groupScriptText)
		
		#btnApply----------------------------------
		self.btnApply = QtWidgets.QPushButton()
		self.btnApply.setText("Apply")
		self.btnApply.setMinimumHeight(30)
		self.btnApply.clicked.connect(self.setSelItemData)
		self.mainLayout.addWidget(self.btnApply)
	
	
	def createItemsFile(self):
		
		"""
		creates buttons from loaded presets
		"""
		
		for item in self.itemsData:
			
			btn = UnPicker_ToolBarBtnUI(width=40, 
									height=40, 
									RGB=item["color"], 
									textLabel=item["label"],
									textScript=item["script"])
			
			btn.delItem.connect(self.removeBtn)			
			self.scrollLayout.addWidget(btn)
	
	
	def createItemsDefault(self):
		
		"""
		creates buttons from default presets
		"""
		
		for i in range(7):
			
			color = None
			if i==0:
				color = [1,0,0]
			elif i==1:
				color = [0,1,0]
			elif i==2:
				color = [0,0,1]
			elif i==3:
				color = [1,1,0]
			elif i==4:
				color = [0,1,1]
			elif i==5:
				color = [1,1,1]
			elif i==6:
				color = [.334,.334,.334]
					
			btn = UnPicker_ToolBarBtnUI(width=40, height=40, RGB=color, textLabel="Text")
			btn.delItem.connect(self.removeBtn)
			self.scrollLayout.addWidget(btn)
	
	
	def removeBtn(self, obj):
		
		"""
		removes the button and saves the preset
		
		accepted arguments:
			@obj[str] - a string with a link to UnPicker_ToolBarBtnUI
		"""
		
		for i in range(self.scrollLayout.count()):
			item = self.scrollLayout.itemAt(i).widget()
			
			if obj == str(item):
				item.deleteLater()
				self.scrollLayout.removeWidget(item)
				break
		
		data = self.getItemsOptionsData()
		print len(data)
		utility.saveItemsOptions(data) 
		
		
	def getSelItemData(self, data):
	
		"""
		display the accepted properties of the selected item
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		self.groupColorSel.rgb = data.color
		self.groupColorSel.setColor()
		
		self.groupLineLabel.setText(data.lable)
		self.groupScriptText.setText(data.script)
	
	
	def setSelItemData(self):
	
		"""
		accepts properties to the selected item
		"""
		
		#generate transmitted data
		data = UnPicker_MimeUI()
		data.color = self.groupColorSel.getColor()
		data.lable = self.groupLineLabel.text()
		data.script = self.groupScriptText.toPlainText()
		
		#transfer data
		self.setSelItem.emit(data)
		
	
	def getItemsOptionsData(self):
		
		"""
		collects data on buttons
		
		return arguments
			@data[list]
		"""
		
		data = []
		
		for i in range(self.scrollLayout.count()):
			
			item = self.scrollLayout.itemAt(i).widget()
			
			if isinstance(item, QtWidgets.QPushButton):
				continue
			
			itemDict = {}
			itemDict["color"] = item.color
			itemDict["label"] = item.textLabel
			itemDict["script"] = item.script
			
			data.append(itemDict)
		
		return data
		
	
	def addToolbarBtn(self):
		
		"""
		add item to the tool bar
		"""
		
		btn = UnPicker_ToolBarBtnUI(width=40, 
									height=40, 
									RGB=self.groupColorSel.getColor(), 
									textLabel=self.groupLineLabel.text(),
									textScript=self.groupScriptText.toPlainText())
									
		self.scrollLayout.insertWidget(1, btn)
		
		data = self.getItemsOptionsData()
		utility.saveItemsOptions(data) 

	
#----------------------------END UnPicker_ItemOptionsWindowUI



class UnPicker_ToolBarBtnUI(UnPicker_AbstractButtonUI):
	
	"""
	creates buttons for tool bar
	
	accepts arguments:
		@objectName[string]
		@width[int]
		@height[int]
		@RGB[list]
		@textLabel[string]
	"""
	
	#signal emitted when a button is removed
	delItem = QtCore.Signal(str)
	
	def __init__(self, objectName="UnPicker_Button", width=None, height=None, RGB=None, textLabel="", textScript=""):
		
		super(UnPicker_ToolBarBtnUI, self).__init__(objectName, width, height, textLabel)
		
		self.color = None
		self.script = textScript
		
		#background color
		self.setAutoFillBackground(1)
		self.pal = self.palette()
		color = QtGui.QColor()
		color.setRgbF(RGB[0], RGB[1], RGB[2])
		self.pal.setColor(self.backgroundRole(), color)
		self.setPalette(self.pal)
		
		self.color = RGB
		self.enterRGB = utility.getEnterRGB(self.color)
		
		self.createContextMenu()
		
	
	def createContextMenu(self):
	
		"""
		creates context menus
		"""
		
		#context menu
		self.popMenu = QtWidgets.QMenu(self)
		
		#remove button
		self.popMeunRemoveBtn = QtWidgets.QAction("Remove", self)
		self.popMenu.addAction(self.popMeunRemoveBtn)
		self.popMeunRemoveBtn.triggered.connect(self.removeBtn)
		
		#settings menu
		self.setMouseTracking(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.onContextMenu)
		
	
	def onContextMenu(self, point):
		
		"""
		add context menu
		"""
		
		self.popMenu.exec_(self.mapToGlobal(point))
	
	
	def removeBtn(self):
	
		"""
		context menu command handler, emits a button delete signal
		"""
		
		obj = str(self)
		self.delItem.emit(obj)

	
	def enterEvent(self, event):
	
		"""
		triggered when the cursor is hovered over
		"""
		
		color = QtGui.QColor()
		color.setRgbF(self.enterRGB[0], self.enterRGB[1], self.enterRGB[2])
		self.pal.setColor(self.backgroundRole(), color)
		self.setPalette(self.pal)
	
	
	def leaveEvent(self, event):
		
		"""
		triggered when the cursor is removed
		"""
		
		color = QtGui.QColor()
		color.setRgbF(self.color[0], self.color[1], self.color[2])
		self.pal.setColor(self.backgroundRole(), color)
		self.setPalette(self.pal)
	
	
	def mousePressEvent(self, event):
	
		"""
		triggered by left-clicking
		"""
		
		if event.buttons() != QtCore.Qt.LeftButton:
			return
		
		data = UnPicker_MimeUI(color=self.color, lable=self.textLabel, script=self.script)
		
		self.pixmap = self.grab()
		painter = QtGui.QPainter(self.pixmap)
		painter.setCompositionMode(painter.CompositionMode_DestinationIn)
		painter.fillRect(self.pixmap.rect(), QtGui.QColor(80, 80, 80, 185))
		painter.end()
		
		drag = QtGui.QDrag(self)
		drag.setMimeData(data)
		drag.setPixmap(self.pixmap)
		drag.setHotSpot(event.pos())
		drag.exec_(QtCore.Qt.LinkAction | QtCore.Qt.MoveAction)
		
	
	def mouseReleaseEvent(self, event):
		pass

#----------------------------END UnPicker_ToolBarBtnUI