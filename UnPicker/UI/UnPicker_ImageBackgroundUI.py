from PySide2 import QtWidgets, QtGui, QtCore
import os


class UnPicker_ImageBackgroundUI(QtWidgets.QGraphicsPixmapItem):
	
	"""
	draws the background image
	
	accepts arguments:
		@imagePath[str]
	"""
	
	def __init__(self, imagePath=None):
		
		super(UnPicker_ImageBackgroundUI, self).__init__()
		
		self.imagePath = imagePath
		self.pixmap = QtGui.QPixmap(self.imagePath)
		#self.pixmap = self.pixmap.scaled()
		
		self.setFlags(QtWidgets.QGraphicsItem.ItemStacksBehindParent)
	
	
	def paint(self, paint, QStyleOptionGraphicsItem, widget=None):
		
		"""
		drawing image
		"""
		
		paint.drawPixmap(QtCore.QPointF(0,0), self.pixmap)
		
		
	def setImagePath(self, imagePath=None):
	
		"""
		sets the path to the image
		
		accepts arguments:
			@imagePath[str]
		"""
		
		self.imagePath = imagePath
		self.pixmap = QtGui.QPixmap(self.imagePath)

	
	def getImageWidthHight(self):
	
		"""
		returns the dimensions of the image
		
		return arguments:
			@width[float]
			@hight[float]
		"""
		
		width = self.pixmap.width()
		hight = self.pixmap.height()
		
		return width, hight
	
	
	def getImagePath(self):
		
		"""
		returns the path to the image
		
		return arguments:
			@[str]
		"""
		
		return self.imagePath