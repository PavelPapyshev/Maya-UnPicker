from PySide2 import QtWidgets, QtGui, QtCore
from UnPicker_MimeUI import UnPicker_MimeUI
import maya.cmds as mc
import UnPicker.UnPicker_Utility as utility


class UnPicker_ItemUI(QtWidgets.QGraphicsItemGroup):
	
	"""
	creates a QGraphicsItemGroup widget
	
	accepts arguments:
		@color[list]
		@textLabel[str]
		@x1[float]
		@y1[float]
		@x2[float]
		@y2[float]
		@textScript[str]
	"""
	
	def __init__(self, color, textLabel="", x1=0, y1=0, x2=40, y2=20, textScript=""):
		
		super(UnPicker_ItemUI, self).__init__()
		
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
		#generate a script that is executed when clicked
		self.scriptTxt = textScript
		
		if not self.scriptTxt:
			self.createSelScript()
		
		#body---------------------------------
		self.body = UnPicker_ItemBodyUI(RGB=color, x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2)
		self.addToGroup(self.body)
		
		#text---------------------------------
		self.text = UnPicker_TextUI(name=textLabel, x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2)
		self.addToGroup(self.text)
		
		#ctrls---------------------------------
		self.ctrls = []
		self.ctrls.append(self.createCtrls("Ctrl_0", self.body.x1-5, self.body.y1-5))
		self.ctrls.append(self.createCtrls("Ctrl_1", (self.body.x2/2)-2.5, self.body.y1-5))
		self.ctrls.append(self.createCtrls("Ctrl_2", self.body.x2, self.body.y1-5))
		self.ctrls.append(self.createCtrls("Ctrl_3", self.body.x2, (self.body.y2/2)-2.5))
		self.ctrls.append(self.createCtrls("Ctrl_4", self.body.x2, self.body.y2))
		self.ctrls.append(self.createCtrls("Ctrl_5", (self.body.x2/2)-2.5, self.body.y2))
		self.ctrls.append(self.createCtrls("Ctrl_6", self.body.x1-5, self.body.y2))
		self.ctrls.append(self.createCtrls("Ctrl_7", self.body.x1-5, (self.body.y2/2)-2.5))	
	
	
	def setSize(self, x1, y1, x2, y2):
	
		"""
		resizes item
		
		accepts arguments:
			@x1[float]
			@y1[float]
			@x2[float]
			@y2[float]
		"""
		
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
		self.body.setSize(x1,y1,x2,y2)
		self.text.setSize(x1,y1,x2,y2)
		
	
	def createCtrls(self, name, posX=0, posY=0):
	
		"""
		create control
		
		accepts arguments:
			@name[str]
			@posX[float]
			@posY[float]
		
		return arguments:
			@ctrl[UnPicker_ItemCtrlUI]
		"""
		
		ctrl = UnPicker_ItemCtrlUI(RGB=[0,0,1], x1=0, y1=0, x2=5, y2=5, number=name)
		self.addToGroup(ctrl)
		ctrl.moveBy(posX, posY)
		ctrl.hide()
		
		return ctrl
	
	
	def showHideCtrls(self, value):
		
		"""
		show/hide controls
		
		accepts arguments:
			@value[bool]
		"""
		
		if value:
			
			#generate transmitted data
			data = UnPicker_MimeUI()
			data.color = self.body.RGB
			data.lable = self.text.name
			data.script = self.scriptTxt
			
			#transfer data
			self.scene().transmitSelItemSignal(data)
			
			for ctrl in self.ctrls:
				ctrl.show()
		
		else:
			for ctrl in self.ctrls:
				ctrl.hide()	
	
	
	def enterEv(self):
		
		"""
		triggered when the cursor is hovered over
		"""
		
		if not utility.UnPicker_EditMode:
			self.body.enterEv()
	
	
	def leaveEv(self):
		
		"""
		triggered when the cursor is removed
		"""
		
		if not utility.UnPicker_EditMode:
			self.body.leaveEv()
			
	
	def pressEv(self):
		
		"""
		triggered by left-clicking
		"""
		
		if not utility.UnPicker_EditMode:
			self.body.pressEv()
	
	
	def releaseEv(self):
		
		"""
		triggered after pressing
		"""
		
		if not utility.UnPicker_EditMode:
			self.body.releaseEv()
			self.enterScript()
			
	
	def selected(self, value):
		
		"""
		select/deselect item
		"""
		
		if utility.UnPicker_EditMode:
			self.body.selected(value)
			self.showHideCtrls(value)	
	
	
	def createSelScript(self):
		
		"""
		generate a script
		"""
		
		selObj = mc.ls(sl=1, l=1)
		
		if not selObj:
			return
		
		selObj = self.rename(selObj)
		
		importTxt = "import maya.cmds as mc\nimport UnPicker.UnPicker_Utility as utility\n\n"
		
		nameSpaceTxt = "nameSpace = utility.UnPicker_NameSpace\n"
		
		pressShiftTxt = "pressShift = utility.UnPicker_PressShift\n\n"
		
		selListTxt = "selectList = ["
		
		for obj in selObj:
			
			if selListTxt == "selectList = [":
				selListTxt = selListTxt + "'" + obj + "'"
			else:
				selListTxt = selListTxt + ", " + "'" + obj + "'"
			
		selListTxt = selListTxt + "]\n\n"	
			
		selTxt = "if pressShift:\n\tmc.select(selectList, add=1)\nelse:\n\tmc.select(selectList)"
		
		self.scriptTxt = importTxt + nameSpaceTxt + pressShiftTxt + selListTxt + selTxt
		
	
	def rename(self, selObj):
	
		"""
		adds NameSpace to objects
		
		accepts arguments:
			@selObj[list]
			
		return arguments:
			@newSelObj[list] - rename objects
		"""
		
		newSelObj = []
		
		for obj in selObj:
			name = obj.split("|")[1:]
			newNameObj = ""
			
			for i in name:
				newNameObj = newNameObj + "|'+nameSpace+'{}".format(i)
			
			newSelObj.append(newNameObj)
	
		return newSelObj
		
	
	def enterScript(self):
	
		"""
		enter script
		"""
		
		#if pressed Shift, objects will be added to the selection
		if QtGui.QGuiApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:
			utility.UnPicker_PressShift = True
		else:
			utility.UnPicker_PressShift = False
		
		if self.scriptTxt:
			exec(self.scriptTxt)
	
	
	def getSize(self):
	
		"""
		returns size
		
		returns arguments:
			@size[list]
		"""
		
		size = [self.body.x1, self.body.y1, self.body.x2, self.body.y2]
		return size
	
	
	def getColor(self):
		
		"""
		returns color
		
		returns arguments:
			@color[list]
		"""
		
		color = self.body.RGB
		return color
		
	
	def getLabel(self):
	
		"""
		returns label text
		
		returns arguments:
			@label[str]
		"""
		
		label = self.text.name
		return label
		
	
	def getScript(self):
		
		"""
		returns script text
		
		returns arguments:
			@[str]
		"""
		
		return self.scriptTxt
		
	
	def getPos(self):
	
		"""
		returns coordinates
		
		returns arguments:
			@[QPoint]
		"""
		
		return self.pos()
		
	
	def setScript(self, script):
	
		"""
		set script text
		
		accepts arguments:
			@script[str]
		"""
		
		self.scriptTxt = script

#----------------------------END UnPicker_ItemUI	


class UnPicker_TextUI(QtWidgets.QGraphicsItem):
	
	def __init__(self, name, x1=0, y1=0, x2=40, y2=20):
	
		"""
		creates a rectangle widget for a group
	
		accepts arguments:
			@name[str] - text label
			@x1[float]
			@y1[float]
			@x2[float]
			@y2[float]
		"""
		
		super(UnPicker_TextUI, self).__init__()
		
		self.setAcceptHoverEvents(True)
		
		self.pen = QtGui.QPen((QtGui.QColor(0, 0, 0, 255)), 1, QtCore.Qt.SolidLine)
		self.name = name
		
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
			
	
	def paint(self, paint, QStyleOptionGraphicsItem, widget=None):
		
		"""
		drawing a rectangle
		"""
		
		paint.setPen(self.pen)
		
		font = paint.font()
		font.setPixelSize(12)
		font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
		font.setWeight(57)
		
		paint.setFont(font)
		#paint.drawText(QtCore.QRectF(0, 0, self.wigth, self.height),QtCore.Qt.AlignCenter,str(self.name))
		
		rect = QtCore.QRectF()
		
		topLeft = QtCore.QPointF(self.x1, self.y1)
		rect.setTopLeft(topLeft)
		
		topRight = QtCore.QPointF(self.x2, self.y1)
		rect.setTopRight(topRight)
		
		bottomLeft = QtCore.QPointF(self.x1, self.y2)
		rect.setBottomLeft(bottomLeft)
		
		bottomRight = QtCore.QPointF(self.x2, self.y2)
		rect.setBottomRight(bottomRight)
		
		paint.drawText(rect, QtCore.Qt.AlignCenter, str(self.name))
	
	
	def boundingRect(self):
	
		"""
		bounding a rectangle
		
		return arguments:
			@rect[QtCore.QRectF]
		"""
		
		rect = QtCore.QRectF()
		
		topLeft = QtCore.QPointF(self.x1, self.y1)
		rect.setTopLeft(topLeft)
		
		topRight = QtCore.QPointF(self.x2, self.y1)
		rect.setTopRight(topRight)
		
		bottomLeft = QtCore.QPointF(self.x1, self.y2)
		rect.setBottomLeft(bottomLeft)
		
		bottomRight = QtCore.QPointF(self.x2, self.y2)
		rect.setBottomRight(bottomRight)
			
		return rect
	
	
	def setSize(self, x1, y1, x2, y2):
		
		"""
		resizes item
		
		accepts arguments:
			@x1[float]
			@y1[float]
			@x2[float]
			@y2[float]
		"""
		
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
		self.boundingRect()

#----------------------------END UnPicker_TextUI			
		

		
class UnPicker_ItemRectUI(QtWidgets.QGraphicsItem):
	
	"""
	creates a rectangle widget for a group
	
	accepts arguments:
		@RGB[list]
		@x1[float]
		@y1[float]
		@x2[float]
		@y2[float]
	"""
	
	def __init__(self, RGB, x1=0, y1=0, x2=40, y2=20):
		
		super(UnPicker_ItemRectUI, self).__init__()	
		
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
		self.RGB = RGB
		
		color = QtGui.QColor()
		color.setRgbF(self.RGB[0], self.RGB[1], self.RGB[2])
		self.pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
		self.brush = QtGui.QBrush(color, QtCore.Qt.BrushStyle.SolidPattern)
	
	
	def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
	
		"""
		drawing a rectangle
		"""
		
		painter.setRenderHints(QtGui.QPainter.Antialiasing)
		
		painter.setPen(self.pen)
		painter.setBrush(self.brush)
		
		rect = QtCore.QRectF()
		
		topLeft = QtCore.QPointF(self.x1, self.y1)
		rect.setTopLeft(topLeft)
		
		topRight = QtCore.QPointF(self.x2, self.y1)
		rect.setTopRight(topRight)
		
		bottomLeft = QtCore.QPointF(self.x1, self.y2)
		rect.setBottomLeft(bottomLeft)
		
		bottomRight = QtCore.QPointF(self.x2, self.y2)
		rect.setBottomRight(bottomRight)
		
		painter.drawRect(rect)
	
	
	def boundingRect(self):
		
		"""
		bounding a rectangle
		
		return arguments:
			@rect[QtCore.QRectF]
		"""
		
		rect = QtCore.QRectF()
		
		topLeft = QtCore.QPointF(self.x1, self.y1)
		rect.setTopLeft(topLeft)
		
		topRight = QtCore.QPointF(self.x2, self.y1)
		rect.setTopRight(topRight)
		
		bottomLeft = QtCore.QPointF(self.x1, self.y2)
		rect.setBottomLeft(bottomLeft)
		
		bottomRight = QtCore.QPointF(self.x2, self.y2)
		rect.setBottomRight(bottomRight)
		
		return rect
	

#----------------------------END UnPicker_ItemRectUI	


class UnPicker_ItemBodyUI(UnPicker_ItemRectUI):
	
	"""
	creates a rectangle widget body for a group
	
	accepts arguments:
		@RGB[list]
		@x1[float]
		@y1[float]
		@x2[float]
		@y2[float]
	"""
	
	
	def __init__(self, RGB, x1=0, y1=0, x2=40, y2=20):
		
		super(UnPicker_ItemBodyUI, self).__init__(RGB, x1, y1, x2, y2)
		
		self.setColors(self.RGB)
	
	
	def setColors(self, color):
		
		"""
		sets the color of the button
		
		accepts arguments:
			@color[list]
		"""
		
		self.RGB = color
		
		#color when the cursor is over an object
		self.enterRGB = utility.getEnterRGB(self.RGB)
		
		#color in which to paint the object
		self.currentRGB = self.RGB
		
		self.leaveEv()
	
	
	def enterEv(self):
		
		"""
		triggered when the cursor is hovered over
		"""
		
		self.currentRGB = self.enterRGB
		color = QtGui.QColor()
		color.setRgbF(self.enterRGB[0], self.enterRGB[1], self.enterRGB[2])
		self.pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
		self.brush = QtGui.QBrush(color, QtCore.Qt.BrushStyle.SolidPattern)

	
	def leaveEv(self):
		
		"""
		triggered when the cursor is removed
		"""
		
		self.currentRGB = self.RGB
		color = QtGui.QColor()
		color.setRgbF(self.currentRGB[0], self.currentRGB[1], self.currentRGB[2])
		self.pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
		self.brush = QtGui.QBrush(color, QtCore.Qt.BrushStyle.SolidPattern)
	
	
	def pressEv(self):
		
		"""
		triggered by left-clicking
		"""
		
		color = QtGui.QColor()
		color.setRgbF(0, 0, 0)
		self.pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
		self.brush = QtGui.QBrush(color, QtCore.Qt.BrushStyle.SolidPattern)
	
	
	def releaseEv(self):
		
		"""
		triggered after pressing
		"""
		
		color = QtGui.QColor()
		color.setRgbF(self.currentRGB[0], self.currentRGB[1], self.currentRGB[2])
		self.pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
		self.brush = QtGui.QBrush(color, QtCore.Qt.BrushStyle.SolidPattern)

	
	def setSize(self, x1, y1, x2, y2):
		
		"""
		resizes item
		
		accepts arguments:
			@x1[float]
			@y1[float]
			@x2[float]
			@y2[float]
		"""
		
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
	
	
	def selected(self, value):
		
		"""
		highlight frame on selection
		
		accepts arguments:
			@value[bool] - select/unselect
		"""
		
		if value:
			color = QtGui.QColor()
			color.setRgbF(0, 0, 1)
			self.pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
		
		else:
			color = QtGui.QColor()
			color.setRgbF(self.RGB[0], self.RGB[1], self.RGB[2])
			self.pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
		
	
	def getEnterRGB(self):
		
		"""
		returns color when the cursor is over an object
		
		return arguments:
			@rgb[list]
		"""
		
		rgb = []
		
		for color in self.RGB:
			newColor = color + .35
			
			if newColor > 1:
				newColor = color - .35
			
			rgb.append(newColor)
		
		return rgb

#----------------------------END UnPicker_ItemBodyUI	


class UnPicker_ItemCtrlUI(UnPicker_ItemRectUI):

	"""
	creates a rectangle widget control for a group
	
	accepts arguments:
		@RGB[list]
		@x1[float]
		@y1[float]
		@x2[float]
		@y2[float]
		@nuber[str] - name control
	"""
	
	def __init__(self, RGB, x1=0, y1=0, x2=40, y2=20, number="ctrl_0"):
	
		super(UnPicker_ItemCtrlUI, self).__init__(RGB, x1, y1, x2, y2)
		self.number = number

	
	def getName(self):
		
		"""
		return name control
		
		return arguments:
			@[str]
		"""
		
		return self.number
	
#----------------------------END UnPicker_ItemCtrlUI	