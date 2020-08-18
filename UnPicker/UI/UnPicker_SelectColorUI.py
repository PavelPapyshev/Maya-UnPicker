import maya.cmds as mc
from PySide2 import QtWidgets, QtCore, QtGui


class UnPicker_SelectColorUI(QtWidgets.QWidget):
	
	"""
	creates a color picker widget
	
	accepts arguments:
		@objectName[string]
		@width[int]
		@height[int]
	"""
	
	def __init__(self, objectName="UnPicker_SelectBackgroundColor", width=None, height=None):
		
		super(UnPicker_SelectColorUI, self).__init__()
		
		self.setObjectName(objectName)
		
		self.width = width
		self.height = height
		self.rgb = [0.334, 0.334, 0.334]
		
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
		self.pal = self.palette()	
		self.setColor()
		
	
	def setColor(self):
		
		"""
		sets the color of the widget
		"""
		
		color = QtGui.QColor()
		color.setRgbF(self.rgb[0], self.rgb[1], self.rgb[2])
		self.pal.setColor(self.backgroundRole(), color)
		self.setPalette(self.pal)
	
	
	def mouseReleaseEvent(self, event):
	
		"""
		triggered by clicking
		"""
		
		#create maya color editor
		self.colorMenu = mc.colorEditor(rgb = (self.rgb[0], self.rgb[1], self.rgb[2]))
		
		#get value maya color editor
		if mc.colorEditor(query=1, result=1):
			
			self.rgb = mc.colorEditor(query=1, rgb=1)
			self.check()
			self.setColor()
		
		super(UnPicker_SelectColorUI, self).mouseReleaseEvent(event)
	
	
	def getColor(self):	
		
		"""
		returns the selected color
		
		return arguments:
			@rgb[list]
		"""

		return self.rgb
		
	
	def check(self):
	
		"""
		checks the color for compliance
		"""
		
		#color conversion to DisplaySpace
		self.rgb = mc.colorManagementConvert(toDisplaySpace=[self.rgb[0], self.rgb[1], self.rgb[2]])
		
		#the value cannot be greater than 1.0
		for i in range(len(self.rgb)):
			
			if self.rgb[i] > 1.0:
				self.rgb[i] = 1.0
		
#----------------------------END UnPicker_SelectColorUI