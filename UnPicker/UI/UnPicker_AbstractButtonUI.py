from PySide2 import QtWidgets, QtCore, QtGui


class UnPicker_AbstractButtonUI(QtWidgets.QWidget):
	
	"""
	creates a button widget
	
	accepts arguments:
		@objectName[string]
		@width[int]
		@height[int]
		@textLabel[string]
	"""
	
	#signal when a button is pressed
	clicked = QtCore.Signal()
	
	def __init__(self, objectName="UnPicker_Button", width=None, height=None, textLabel="Text"):
		
		super(UnPicker_AbstractButtonUI, self).__init__()
		
		self.setObjectName(objectName)
		
		self.width = width
		self.height = height
		self.textLabel = textLabel
		
		self.createUI()
	
	
	def createUI(self):
		
		"""
		create widget
		"""
		
		#size
		if self.width:
			self.setFixedWidth(self.width)
		
		if self.height:
			self.setFixedHeight(self.height)
		
		#background color
		self.setAutoFillBackground(1)
		color = 85
		self.pal = self.palette()
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		#main Layout
		self.mainLayout = QtWidgets.QHBoxLayout()
		self.setLayout(self.mainLayout)
		
		#label
		self.label = QtWidgets.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setText(self.textLabel)
		self.mainLayout.addWidget(self.label)
		
	
	def enterEvent(self, event):
		
		"""
		triggered when the cursor is hovered over
		"""
		
		color = 95
		
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		super(UnPicker_AbstractButtonUI, self).enterEvent(event)
	
	
	def leaveEvent(self, event):
	
		"""
		triggered when the cursor is removed
		"""
		
		color = 85
		
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		super(UnPicker_AbstractButtonUI, self).leaveEvent(event)
	
	
	def mousePressEvent(self, event):
		
		"""
		triggered by left-clicking
		"""
		
		#check that the left mouse button was pressed
		if event.buttons() != QtCore.Qt.LeftButton:
			return
		
		color = 0
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		super(UnPicker_AbstractButtonUI, self).mousePressEvent(event)
	
	
	def mouseReleaseEvent(self, event):
	
		"""
		triggered after pressing
		"""
		
		color = 95
		
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		self.clicked.emit()
		
		super(UnPicker_AbstractButtonUI, self).mouseReleaseEvent(event)
		
#----------------------------END UnPicker_AbstractButtonUI