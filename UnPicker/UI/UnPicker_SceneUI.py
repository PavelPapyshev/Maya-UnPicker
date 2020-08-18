from PySide2 import QtWidgets, QtGui, QtCore
from UnPicker_ImageBackgroundUI import UnPicker_ImageBackgroundUI
from UnPicker_MimeUI import UnPicker_MimeUI
import maya.cmds as mc
import UnPicker_ItemUI as ItemUI
import UnPicker.UnPicker_MigratoryData as MigratoryData
import UnPicker.UnPicker_Utility as utility


class UnPicker_SceneUI(QtWidgets.QGraphicsScene):
	
	"""
	creates a QGraphicsScene widget
	"""
	
	#signal for data transmission of the selected item
	selItem = QtCore.Signal(UnPicker_MimeUI)
	
	def __init__(self):
		
		super(UnPicker_SceneUI, self).__init__()
		
		self.imageBackground = None
		self.selectItem = None
		self.itemOffset = [] #new position offset 
		
	
	def transmitSelItemSignal(self, data):
		
		"""
		transfers the data of the selected item to UnPicker_TabUI
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		self.selItem.emit(data)
		
		
	def setSelItemData(self, data):
	
		"""
		sets properties on the selected item
		
		accepts arguments:
			@data[UnPicker_MimeUI] - transmitted data
		"""
		
		if isinstance(self.selectItem, ItemUI.UnPicker_ItemCtrlUI):
			selItem = self.selectItem.parentItem()
		
		elif isinstance(self.selectItem, ItemUI.UnPicker_ItemUI):
			selItem = self.selectItem
		
		else:
			return
		
		selItem.body.setColors(data.color)
		selItem.text.name = data.lable
		selItem.setScript(data.script)
		
		self.update()
	
	
	def clearSelectItem(self):
	
		"""
		unselects an item
		"""
	
		self.selectItem = None
		
		for i in self.items():
			
			if type(i) == ItemUI.UnPicker_ItemUI:
				i.selected(False)
		
		self.update()
	
	
	def mousePressEvent(self, event):
		
		"""
		triggered after pressing
		"""
		
		#check that the left mouse button was pressed
		if event.buttons() != QtCore.Qt.LeftButton:
			return
		
		item = self.itemAt(event.scenePos(), QtGui.QTransform())	
		self.clearSelectItem()
		
		if isinstance(item, ItemUI.UnPicker_TextUI):
			
			#new select item
			self.selectItem = item.parentItem()
			self.selectItem.selected(True)
			self.selectItem.pressEv()
			
			#calculation itemOffset
			x = event.scenePos().x() - self.selectItem.pos().x()
			y = event.scenePos().y() - self.selectItem.pos().y()
			
			self.itemOffset.append(x)
			self.itemOffset.append(y)
			
			self.update()
		
		#ctrl
		elif isinstance(item, ItemUI.UnPicker_ItemCtrlUI):
			
			self.setCursor(item.getName())
			
			#new select item
			self.selectItem = item
			self.selectItem.parentItem().selected(True)
			
			#calculation itemOffset
			x = event.scenePos().x() - self.selectItem.pos().x()
			y = event.scenePos().y() - self.selectItem.pos().y()
			
			self.itemOffset.append(x)
			self.itemOffset.append(y)
			
			self.update()
		
		else:
			self.selectItem = None
			self.update()
	
	
	def mouseReleaseEvent(self, event):
	
		"""
		triggered after release
		"""		
		
		self.itemOffset = []
		self.views()[0].setCursor(QtCore.Qt.ArrowCursor)
		
		if not self.selectItem:
			self.clearSelectItem()
			return	
		
		item = self.itemAt(event.scenePos(), QtGui.QTransform())

		if isinstance(item, ItemUI.UnPicker_TextUI):
			
			#release event item
			if self.selectItem == item.parentItem():
				
				if not utility.UnPicker_EditMode:
					self.selectItem = item.parentItem()
					self.selectItem.releaseEv()
					self.clearSelectItem()
					self.update()
			
			else:
				self.clearSelectItem()
		
		#ctrl
		elif isinstance(item, ItemUI.UnPicker_ItemCtrlUI):
			pass
		
		else:
			if self.selectItem != ItemUI.UnPicker_ItemCtrlUI:
				return
			
			self.clearSelectItem()

		
	def mouseMoveEvent(self, event):
	
		"""
		triggered when the mouse is moved
		"""
		
		if not utility.UnPicker_EditMode:
			return
			
		#check that the left mouse button was pressed
		if event.buttons() != QtCore.Qt.LeftButton:
			return
		
		#move item
		if isinstance(self.selectItem, ItemUI.UnPicker_ItemUI):
			
			try:
				self.selectItem.setPos(event.scenePos().x() - self.itemOffset[0], event.scenePos().y() - self.itemOffset[1])
			except:
				pass
			
			self.update()
		
		#ctrl
		elif isinstance(self.selectItem, ItemUI.UnPicker_ItemCtrlUI):
			
			itemGrp = self.selectItem.parentItem()
			ctrlName = self.selectItem.getName()
			self.calculationPosCtrls(ctrlName, itemGrp, event)
			
			self.update()
		
	
	def dragMoveEvent(self, event):
		
		"""
		drag and drop buttons
		"""
		
		event.acceptProposedAction()
	
	
	def dropEvent(self, event):
		
		"""
		button creation
		"""
		
		data = event.mimeData()
		
		dropX = event.scenePos().x() - 20
		dropY = event.scenePos().y() - 10
		
		
		gItem = ItemUI.UnPicker_ItemUI(color=data.color, 
										textLabel=data.lable, 
										x1=0, 
										y1=0, 
										x2=40, 
										y2=20, 
										textScript=data.script)
										
		self.addItem(gItem)
		gItem.setPos(dropX, dropY)
		
		#select item
		self.clearSelectItem()
		
		self.selectItem = gItem
		self.selectItem.selected(True)
		
		self.update()
	

	def calculationPosCtrls(self, ctrlName, itemGrp, event):
	
		"""
		calculates the position of controls
		
		accepts arguments:
			@ctrlName[str]
			@itemGrp[UnPicker_ItemUI] - groups in which controls are located
			@event - to retrieve the coordinates of the cursor
		"""
		
		#-------------------------------ctrl_0	
		if ctrlName == "Ctrl_0":
		
			#move ctrl_0
			ctrl = itemGrp.ctrls[0]
			x = event.scenePos().x()
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_1
			ctrl = itemGrp.ctrls[1]
			x = (itemGrp.ctrls[0].scenePos().x() + itemGrp.ctrls[2].scenePos().x())/2
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_2
			ctrl = itemGrp.ctrls[2]
			x = itemGrp.ctrls[2].scenePos().x()
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_3
			ctrl = itemGrp.ctrls[3]
			x = itemGrp.ctrls[3].scenePos().x()
			y = (itemGrp.ctrls[2].scenePos().y() + itemGrp.ctrls[4].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_5
			ctrl = itemGrp.ctrls[5]
			x = (itemGrp.ctrls[4].scenePos().x() + itemGrp.ctrls[6].scenePos().x())/2
			y = itemGrp.ctrls[5].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_6
			ctrl = itemGrp.ctrls[6]
			x = event.scenePos().x()
			y = itemGrp.ctrls[6].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_7
			ctrl = itemGrp.ctrls[7]
			x = itemGrp.ctrls[0].scenePos().x()
			y = (itemGrp.ctrls[0].scenePos().y() + itemGrp.ctrls[6].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
		
		#-------------------------------ctrl_1	
		elif ctrlName == "Ctrl_1":
			
			#move ctrl_1
			ctrl = itemGrp.ctrls[1]
			x = itemGrp.ctrls[1].scenePos().x()
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_0
			ctrl = itemGrp.ctrls[0]
			x = itemGrp.ctrls[0].scenePos().x()
			y = itemGrp.ctrls[1].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_2
			ctrl = itemGrp.ctrls[2]
			x = itemGrp.ctrls[2].scenePos().x()
			y = itemGrp.ctrls[1].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_3
			ctrl = itemGrp.ctrls[3]
			x = itemGrp.ctrls[3].scenePos().x()
			y = (itemGrp.ctrls[2].scenePos().y() + itemGrp.ctrls[4].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_7
			ctrl = itemGrp.ctrls[7]
			x = itemGrp.ctrls[7].scenePos().x()
			y = (itemGrp.ctrls[0].scenePos().y() + itemGrp.ctrls[6].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
		#-------------------------------ctrl_2	
		elif ctrlName == "Ctrl_2":
			
			#move ctrl_2
			ctrl = itemGrp.ctrls[2]
			x = event.scenePos().x()
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_0
			ctrl = itemGrp.ctrls[0]
			x = itemGrp.ctrls[0].scenePos().x()
			y = itemGrp.ctrls[1].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_1
			ctrl = itemGrp.ctrls[1]
			x = (itemGrp.ctrls[0].scenePos().x() + itemGrp.ctrls[2].scenePos().x())/2
			y = itemGrp.ctrls[2].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_3
			ctrl = itemGrp.ctrls[3]
			x = itemGrp.ctrls[2].scenePos().x()
			y = (itemGrp.ctrls[2].scenePos().y() + itemGrp.ctrls[4].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_4
			ctrl = itemGrp.ctrls[4]
			x = itemGrp.ctrls[2].scenePos().x()
			y = itemGrp.ctrls[4].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_5
			ctrl = itemGrp.ctrls[5]
			x = (itemGrp.ctrls[4].scenePos().x() + itemGrp.ctrls[6].scenePos().x())/2
			y = itemGrp.ctrls[5].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_7
			ctrl = itemGrp.ctrls[7]
			x = itemGrp.ctrls[7].scenePos().x()
			y = (itemGrp.ctrls[0].scenePos().y() + itemGrp.ctrls[6].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
		
		#-------------------------------ctrl_3	
		elif ctrlName == "Ctrl_3":
			
			#move ctrl_3
			ctrl = itemGrp.ctrls[3]
			x = event.scenePos().x()
			y = itemGrp.ctrls[3].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_1
			ctrl = itemGrp.ctrls[1]
			x = (itemGrp.ctrls[0].scenePos().x() + itemGrp.ctrls[2].scenePos().x())/2
			y = itemGrp.ctrls[1].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_2
			ctrl = itemGrp.ctrls[2]
			x = itemGrp.ctrls[3].scenePos().x()
			y = itemGrp.ctrls[2].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_4
			ctrl = itemGrp.ctrls[4]
			x = itemGrp.ctrls[3].scenePos().x()
			y = itemGrp.ctrls[4].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_5
			ctrl = itemGrp.ctrls[5]
			x = (itemGrp.ctrls[4].scenePos().x() + itemGrp.ctrls[6].scenePos().x())/2
			y = itemGrp.ctrls[5].scenePos().y()
			self.moveCtrl(ctrl, x, y)
		
		#-------------------------------ctrl_4
		elif ctrlName == "Ctrl_4":
			
			#move ctrl_4
			ctrl = itemGrp.ctrls[4]
			x = event.scenePos().x()
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_1
			ctrl = itemGrp.ctrls[1]
			x = (itemGrp.ctrls[0].scenePos().x() + itemGrp.ctrls[2].scenePos().x())/2
			y = itemGrp.ctrls[1].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_2
			ctrl = itemGrp.ctrls[2]
			x = itemGrp.ctrls[4].scenePos().x()
			y = itemGrp.ctrls[2].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_3
			ctrl = itemGrp.ctrls[3]
			x = itemGrp.ctrls[4].scenePos().x()
			y = (itemGrp.ctrls[2].scenePos().y() + itemGrp.ctrls[4].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_5
			ctrl = itemGrp.ctrls[5]
			x = (itemGrp.ctrls[4].scenePos().x() + itemGrp.ctrls[6].scenePos().x())/2
			y = itemGrp.ctrls[4].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_6
			ctrl = itemGrp.ctrls[6]
			x = itemGrp.ctrls[6].scenePos().x()
			y = itemGrp.ctrls[4].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_7
			ctrl = itemGrp.ctrls[7]
			x = itemGrp.ctrls[7].scenePos().x()
			y = (itemGrp.ctrls[6].scenePos().y() + itemGrp.ctrls[0].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
		#-------------------------------ctrl_5
		elif ctrlName == "Ctrl_5":
			
			#move ctrl_5
			ctrl = itemGrp.ctrls[5]
			x = itemGrp.ctrls[5].scenePos().x()
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_3
			ctrl = itemGrp.ctrls[3]
			x = itemGrp.ctrls[3].scenePos().x()
			y = (itemGrp.ctrls[2].scenePos().y() + itemGrp.ctrls[4].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_4
			ctrl = itemGrp.ctrls[4]
			x = itemGrp.ctrls[4].scenePos().x()
			y = itemGrp.ctrls[5].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_6
			ctrl = itemGrp.ctrls[6]
			x = itemGrp.ctrls[6].scenePos().x()
			y = itemGrp.ctrls[5].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_7
			ctrl = itemGrp.ctrls[7]
			x = itemGrp.ctrls[7].scenePos().x()
			y = (itemGrp.ctrls[6].scenePos().y() + itemGrp.ctrls[0].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
		#-------------------------------ctrl_6
		elif ctrlName == "Ctrl_6":
			
			#move ctrl_6
			ctrl = itemGrp.ctrls[6]
			x = event.scenePos().x()
			y = event.scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_0
			ctrl = itemGrp.ctrls[0]
			x = itemGrp.ctrls[6].scenePos().x()
			y = itemGrp.ctrls[0].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_1
			ctrl = itemGrp.ctrls[1]
			x = (itemGrp.ctrls[0].scenePos().x() + itemGrp.ctrls[2].scenePos().x())/2
			y = itemGrp.ctrls[1].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_3
			ctrl = itemGrp.ctrls[3]
			x = itemGrp.ctrls[3].scenePos().x()
			y = (itemGrp.ctrls[2].scenePos().y() + itemGrp.ctrls[4].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_4
			ctrl = itemGrp.ctrls[4]
			x = itemGrp.ctrls[4].scenePos().x()
			y = itemGrp.ctrls[6].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_5
			ctrl = itemGrp.ctrls[5]
			x = (itemGrp.ctrls[4].scenePos().x() + itemGrp.ctrls[6].scenePos().x())/2
			y = itemGrp.ctrls[6].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_7
			ctrl = itemGrp.ctrls[7]
			x = itemGrp.ctrls[6].scenePos().x()
			y = (itemGrp.ctrls[6].scenePos().y() + itemGrp.ctrls[0].scenePos().y())/2
			self.moveCtrl(ctrl, x, y)
		
		#-------------------------------ctrl_7
		elif ctrlName == "Ctrl_7":
			
			#move ctrl_7
			ctrl = itemGrp.ctrls[7]
			x = event.scenePos().x()
			y = itemGrp.ctrls[7].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_0
			ctrl = itemGrp.ctrls[0]
			x = itemGrp.ctrls[7].scenePos().x()
			y = itemGrp.ctrls[0].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_1
			ctrl = itemGrp.ctrls[1]
			x = (itemGrp.ctrls[0].scenePos().x() + itemGrp.ctrls[2].scenePos().x())/2
			y = itemGrp.ctrls[1].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_5
			ctrl = itemGrp.ctrls[5]
			x = (itemGrp.ctrls[4].scenePos().x() + itemGrp.ctrls[6].scenePos().x())/2
			y = itemGrp.ctrls[5].scenePos().y()
			self.moveCtrl(ctrl, x, y)
			
			#move ctrl_6
			ctrl = itemGrp.ctrls[6]
			x = itemGrp.ctrls[7].scenePos().x()
			y = itemGrp.ctrls[6].scenePos().y()
			self.moveCtrl(ctrl, x, y)
		
		
		#item size
		x1 = itemGrp.ctrls[0].pos().x()+5
		y1 = itemGrp.ctrls[0].pos().y()+5
		x2 = itemGrp.ctrls[4].pos().x()
		y2 = itemGrp.ctrls[4].pos().y()
		
		itemGrp.setSize(x1,y1,x2,y2)
		self.update()
	
	
	def moveCtrl(self, ctrl, x, y):
		
		"""
		moves control
		
		accepts arguments:
			@ctrl[UnPicker_ItemCtrlUI]
			@x[float] - position X
			@y[float] - position Y
		"""
		
		point = QtCore.QPointF(x,y)
		itemPos = ctrl.parentItem().mapFromScene(point)
		ctrl.setPos(itemPos)
	
	
	def setCursor(self, ctrlName):
		
		"""
		changes cursor when clicking on control
		
		accepts arguments:
			@ctrlName[str]
		"""
		
		if ctrlName == "Ctrl_0":
				self.views()[0].setCursor(QtCore.Qt.SizeFDiagCursor)
			
		elif ctrlName == "Ctrl_1":
			self.views()[0].setCursor(QtCore.Qt.SizeVerCursor)
		
		elif ctrlName == "Ctrl_2":
			self.views()[0].setCursor(QtCore.Qt.SizeBDiagCursor)
		
		elif ctrlName == "Ctrl_3":
			self.views()[0].setCursor(QtCore.Qt.SizeHorCursor)
		
		elif ctrlName == "Ctrl_4":
			self.views()[0].setCursor(QtCore.Qt.SizeFDiagCursor)
			
		elif ctrlName == "Ctrl_5":
			self.views()[0].setCursor(QtCore.Qt.SizeVerCursor)
			
		elif ctrlName == "Ctrl_6":
			self.views()[0].setCursor(QtCore.Qt.SizeBDiagCursor)
		
		elif ctrlName == "Ctrl_7":
			self.views()[0].setCursor(QtCore.Qt.SizeHorCursor)
			
		self.update()
	
	
	def getAllItems(self):
	
		"""
		collects items data
		
		return arguments:
			@itemData[UnPicker_MigratoryData]
		"""
		
		itemData = MigratoryData.UnPicker_MigratoryData()
		
		for i in self.items():
			
			if type(i) == ItemUI.UnPicker_ItemUI:
				
				#widgetType
				#data.append(None)
				itemData.addWidgetType("")
				
				#widgetPos
				pos = i.getPos()
				#data.append("{};{}".format(pos.x(), pos.y()))
				itemData.addWidgetPos("{};{}".format(pos.x(), pos.y()))
				
				#widgetWidthHeight
				size = i.getSize()
				#data.append("{};{};{};{}".format(size[0],size[1],size[2],size[3]))
				itemData.addWidgetWidthHeight("{};{};{};{}".format(size[0],size[1],size[2],size[3]))
				
				#widgetColor
				color = i.getColor()
				#data.append("{};{};{}".format(color[0], color[1], color[2]))
				itemData.addWidgetColor("{};{};{}".format(color[0], color[1], color[2]))
				
				#widgetLabel
				lable = i.getLabel()
				#data.append(None)
				itemData.addWidgetLabel(lable)
				
				#widgetScript
				script = i.getScript()
				#data.append(script)
				itemData.addWidgetScript(script)
			
				#itemData.append(data)
			
		return itemData
	
	
	def createSceneItems(self, itemData):
		
		"""
		creates items
		
		accepts arguments:
			@itemData[UnPicker_MigratoryData]
		"""
		
		#extract data
		widgetType = itemData.getWidgetType()
		widgetPos = itemData.getWidgetPos()
		widgetWidthHeight = itemData.getWidgetWidthHeight()
		widgetColor = itemData.getWidgetColor()
		widgetLabel = itemData.getWidgetLabel()
		widgetScript = itemData.getWidgetScript()
		
		if not widgetColor:
			return
		
		for i in range(len(widgetColor)):
			
			RGB = widgetColor[i].split(";")
			size = widgetWidthHeight[i].split(";")
			pos = widgetPos[i].split(";")
			
			gItem = ItemUI.UnPicker_ItemUI(color=[float(RGB[0]), float(RGB[1]), float(RGB[2])], 
											textLabel=widgetLabel[i],
											x1=float(size[0]), y1=float(size[1]), x2=float(size[2]), y2=float(size[3]),
											textScript=widgetScript[i])
			#gItem.setScript(widgetScript[i])
			self.addItem(gItem)
			gItem.setPos(float(pos[0]), float(pos[1]))
			
			
			
	def addImageScene(self, imagePath):
	
		"""
		adds a background image
		
		accepts arguments:
			@imagePath[str]
		"""
		
		if not self.imageBackground:
			self.imageBackground = UnPicker_ImageBackgroundUI(imagePath)
			self.addItem(self.imageBackground)
		
		else:
			self.imageBackground.setImagePath(imagePath)
		
	
	def getImageWidthHight(self):
	
		"""
		returns the dimensions of the image
		
		return arguments:
			@width[float]
			@hight[float]
		"""
		
		width, hight = self.imageBackground.getImageWidthHight()
		
		return width, hight
		
	
	def getImagePath(self):
	
		"""
		returns the path to the image
		
		return arguments:
			@tabImage[str]
		"""
		
		if self.imageBackground:
			tabImage = self.imageBackground.getImagePath()
		
		else:
			tabImage = ""
		
		return tabImage
		
	
	def removeImageBackgroung(self):
	
		"""
		remove the background image
		"""
		
		if self.imageBackground:
			self.removeItem(self.imageBackground)
			self.imageBackground = None
			
			
	def removeSelItem(self):
		
		"""
		remove select item
		"""
		
		if isinstance(self.selectItem, ItemUI.UnPicker_ItemUI):
			item = self.selectItem
		
		elif (isinstance(self.selectItem, ItemUI.UnPicker_TextUI)) or (isinstance(self.selectItem, ItemUI.UnPicker_ItemCtrlUI)):
			item = self.selectItem.parentItem()
		
		else:
			return()
		
		self.removeItem(item)
		self.destroyItemGroup(item)
		self.clearSelectItem()
		self.update()
	
	
	def duplicateSelItem(self):
		
		"""
		duplicate select item
		"""
		
		if isinstance(self.selectItem, ItemUI.UnPicker_ItemUI):
			item = self.selectItem
		
		elif (isinstance(self.selectItem, ItemUI.UnPicker_TextUI)) or (isinstance(self.selectItem, ItemUI.UnPicker_ItemCtrlUI)):
			item = self.selectItem.parentItem()
		
		else:
			return()
		
		#get data
		pos = item.getPos()
		size = item.getSize()
		RGB = item.getColor()
		lable = item.getLabel()
		
		if mc.ls(sl=1, l=1):
			script = ""
		else:
			script = item.getScript()
		
		#create item
		gItem = ItemUI.UnPicker_ItemUI(color=[float(RGB[0]), float(RGB[1]), float(RGB[2])], 
										textLabel=lable,
										x1=float(size[0]), y1=float(size[1]), x2=float(size[2]), y2=float(size[3]),
										textScript=script)
		
		#set data
		#gItem.setScript(script)
		self.addItem(gItem)
		gItem.setPos(float(pos.x()), float(pos.y()))
		
		#select item
		self.clearSelectItem()
		self.selectItem = gItem
		self.selectItem.selected(True)
		

#----------------------------END UnPicker_SceneUI