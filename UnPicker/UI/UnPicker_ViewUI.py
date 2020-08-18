from PySide2 import QtWidgets, QtGui, QtCore
import UnPicker_ItemUI as ItemUI
import UnPicker.UnPicker_Utility as utility


class UnPicker_ViewUI(QtWidgets.QGraphicsView):

	"""
	creates a QGraphicsView widget
	
	accepts arguments:
		@viewColor[list] - view color background
		@imW[float] - image width
		@imH[float] - image height
	"""
	
	#tab delete signal
	removeTab = QtCore.Signal()
	
	def __init__(self, viewColor=[0.334, 0.334, 0.334], imW=10, imH=10):
		
		super(UnPicker_ViewUI, self).__init__()
		
		self.createContextMenu()
		
		#the object the cursor was over
		self.enterItem = None
		
		self.setMinimumSize(imW, imH)
		self.setMaximumSize(imW, imH)
		
		self.setSceneRect(QtCore.QRectF(QtCore.QPointF(0,0), QtCore.QSizeF(10000, 10000)))
		
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
		
		#defines when items get selected when we drun our cursor over
		#IntersectsItemShape - if we touch the shape of the item with a RubberBand
		self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)
		
		self.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
		
		self.setStyleSheet("border: no-focus;")
		color = QtGui.QColor()
		color.setRgbF(float(viewColor[0]), float(viewColor[1]), float(viewColor[2]))
		#self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(viewColor[0], viewColor[1], viewColor[2], 255), QtCore.Qt.SolidPattern))
		self.setBackgroundBrush(QtGui.QBrush(color, QtCore.Qt.SolidPattern))	
		
		#creating a timer for the correct rendering of the widget
		self.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.onTimer)
		self.timer.start(50)
	
	
	def createContextMenu(self):
	
		"""
		creates context menus
		"""
		
		#scene context menu-------------------------------------------------
		self.scenePopMenu = QtWidgets.QMenu(self)
		
		#open image background 
		self.scenePopMenuAdd = QtWidgets.QAction("Open Image Background", self)
		self.scenePopMenu.addAction(self.scenePopMenuAdd)
		self.scenePopMenuAdd.triggered.connect(self.openImBackgroung)
		
		#remove image background
		self.scenePopMenuRemoveIm = QtWidgets.QAction("Remove Image Background", self)
		self.scenePopMenu.addAction(self.scenePopMenuRemoveIm)
		self.scenePopMenuRemoveIm.triggered.connect(self.removeImBackgroung)
		
		#remove tab
		self.scenePopMenuRemoveTab = QtWidgets.QAction("Remove Tab", self)
		self.scenePopMenu.addAction(self.scenePopMenuRemoveTab)
		self.scenePopMenuRemoveTab.triggered.connect(self.deleteTab)

		#item context menu-------------------------------------------------
		self.itemPopMenu =  QtWidgets.QMenu(self)
		
		#duplicate item
		self.itemPopMenuDuplicate = QtWidgets.QAction("Duplicate Item", self)
		self.itemPopMenu.addAction(self.itemPopMenuDuplicate)
		self.itemPopMenuDuplicate.triggered.connect(self.duplicateItem)
		
		#remove item
		self.itemPopMenuRemove = QtWidgets.QAction("Remove Item", self)
		self.itemPopMenu.addAction(self.itemPopMenuRemove)
		self.itemPopMenuRemove.triggered.connect(self.removeItem)
		
		#settings menu
		self.setMouseTracking(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
	
	
	def openImBackgroung(self):
		
		"""
		context menu command handler, loads a new background image
		"""
		
		imagePath = utility.getImagePath()
		
		if not imagePath:
			return
		
		self.scene().addImageScene(imagePath)
		imW, imH = self.scene().getImageWidthHight()
		
		self.setMinimumSize(imW, imH)
		self.update()
	
	
	def removeImBackgroung(self):
		
		"""
		context menu command handler, removes the background image
		"""
		
		self.scene().removeImageBackgroung()
		self.setMinimumSize(10,10)
		self.update()
	
	
	def deleteTab(self):
		
		"""
		context menu command handler, removes a tab
		"""
		
		self.removeTab.emit()

	
	def removeItem(self):
	
		"""
		context menu command handler, remove select item
		"""
		
		self.enterItem = None
		self.scene().removeSelItem()
	
	
	def duplicateItem(self):
		
		"""
		context menu command handler, duplicate select item
		"""
		
		self.scene().duplicateSelItem()
	
	
	def onTimer(self):
	
		"""
		triggers on a timer, allows you to resize the widget
		"""
		
		#self.setMinimumSize(10,10)
		self.setMaximumSize(10000,10000)
	
	
	def getColor(self):
	
		"""
		returns color
		
		return arguments:
			@tabColor[str]
		"""
		
		color = self.backgroundBrush().color().getRgbF()[:-1]
		tabColor = "{};{};{}".format(color[0], color[1], color[2])

		return tabColor
	
	
	def mousePressEvent(self, event):
		
		"""
		triggered after pressing
		"""
		
		super(UnPicker_ViewUI, self).mousePressEvent(event)
		
		#check that the right mouse button was pressed
		if event.buttons() != QtCore.Qt.RightButton:
			return
		
		if not utility.UnPicker_EditMode:
			return
		
		item = self.items(event.pos())
		
		if item:
			item = item[0]
			
			#if this object ItemUI.UnPicker_TextUI
			if isinstance(item, ItemUI.UnPicker_TextUI):
				self.scene().clearSelectItem()
				self.scene().selectItem = item.parentItem()
				self.scene().selectItem.selected(True)
				self.itemPopMenu.exec_(self.mapToGlobal(event.pos()))
			
		#if other objects
		else:
			self.scenePopMenu.exec_(self.mapToGlobal(event.pos()))
		
		self.scene().update()
		
	
	def mouseMoveEvent(self, event):
	
		"""
		triggered when the mouse is moved, paints items on mouse hover
		"""
		
		super(UnPicker_ViewUI, self).mouseMoveEvent(event)
		
		item = self.items(event.pos())
		
		#if the cursor is over the object
		if item:
			item = item[0]
			
			#if this object ItemUI.UnPicker_TextUI
			if isinstance(item, ItemUI.UnPicker_TextUI):
				
				#if it's the same object, do nothing
				if self.enterItem == item:
					return
				
				#if another object was painted, first return it to its original color
				elif self.enterItem:
					self.enterItem.parentItem().leaveEv()
					item.parentItem().enterEv()
					self.enterItem = item
					
				else:
					item.parentItem().enterEv()
					self.enterItem = item
			
			#if the cursor is no longer over the object, return it to its original color
			elif self.enterItem:
				self.enterItem.parentItem().leaveEv()
				self.enterItem = None
		
		#if the cursor is no longer over the object, return it to its original color		
		elif self.enterItem:
			self.enterItem.parentItem().leaveEv()
			self.enterItem = None
	
		self.update()
	
	
	def wheelEvent(self, event):
		pass



#----------------------------END UnPicker_ViewUI		